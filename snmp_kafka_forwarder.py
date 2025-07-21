import json
import logging
import signal
import asyncio
import traceback
from datetime import datetime

from kafka import KafkaProducer
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.proto.api import v2c

# --- ロギング設定 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- グローバルイベント ---
SHUTDOWN_EVENT = asyncio.Event()
RELOAD_EVENT = asyncio.Event()

def signal_handler(signum):
    """シグナルを処理してイベントをセットする"""
    if signum == signal.SIGHUP:
        logging.info("SIGHUPシグナルを受信しました。リロードをスケジュールします。")
        RELOAD_EVENT.set()
    elif signum in [signal.SIGINT, signal.SIGTERM]:
        logging.info(f"{signal.Signals(signum).name}シグナルを受信しました。シャットダウンします。")
        SHUTDOWN_EVENT.set()

def load_config(config_path='config.json'):
    """設定ファイルを読み込む"""
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"設定ファイル '{config_path}' が見つかりません。")
        return None
    except json.JSONDecodeError:
        logging.error(f"設定ファイル '{config_path}' の形式が正しくありません。")
        return None

def initialize_kafka_producer(kafka_config):
    """Kafkaプロデューサーを初期化する"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=kafka_config.get('bootstrap_servers', 'localhost:9092').split(','),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            security_protocol=kafka_config.get('security_protocol', 'PLAINTEXT')
        )
        logging.info(f"Kafkaプロデューサーを初期化しました: {kafka_config.get('bootstrap_servers')}")
        return producer
    except Exception as e:
        logging.error(f"Kafkaプロデューサーの初期化に失敗しました: {e}")
        return None

def create_trap_callback(producer, kafka_topic):
    """SNMPトラップ受信時のコールバック関数を作成する"""
    def trap_callback(snmpEngine, stateReference, _contextEngineId, contextName,
                      varBinds, _cbCtx):
        _transportDomain, transportAddress = snmpEngine.msgAndPduDsp.get_transport_info(stateReference)
        source_ip, source_port = transportAddress
        community_name = contextName.prettyPrint()

        logging.info(f"トラップを受信しました from {source_ip}:{source_port} (Community: {community_name})")

        trap_data = {
            "source_ip": source_ip,
            "source_port": source_port,
            "community": community_name,
            "protocol_version": "v1/v2c",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "variables": []
        }

        for oid, val in varBinds:
            try:
                trap_data["variables"].append({
                    "oid": str(oid),
                    "oid_full": oid.prettyPrint(),
                    "value": val.prettyPrint(),
                    "value_type": val.__class__.__name__
                })
            except Exception as e:
                logging.warning(f"VarBindの解析中にエラーが発生しました: {e}")

        try:
            future = producer.send(kafka_topic, trap_data)
            future.get(timeout=10)
        except Exception as e:
            logging.error(f"Kafkaへのメッセージ送信に失敗しました: {e}")

    return trap_callback

async def setup_snmp_engine(snmp_config, callback):
    """SNMP Engineをセットアップする"""
    host = snmp_config.get('host', '0.0.0.0')
    port = snmp_config.get('port', 162)
    communities = snmp_config.get('communities', ['public'])

    snmpEngine = engine.SnmpEngine()

    # MIBs are expected to be in pysnmp_mibs directory
    # mibBuilder = snmpEngine.get  ('mibBuilder')
    # mibBuilder.add_mib_sources(builder.DirMibSource(str(Path(__file__).resolve().parent / "compiled_mibs")))

    config.add_transport(
        snmpEngine,
        udp.DOMAIN_NAME,
        udp.UdpTransport().open_server_mode((host, port))
    )

    for i, community in enumerate(communities):
        config.add_v1_system(snmpEngine, f'my-area-{i}', community)

    ntfrcv.NotificationReceiver(snmpEngine, callback)
    logging.info(f"SNMPトラップの待受を開始します: {host}:{port}, Communities: {communities}")
    return snmpEngine

def log_crash_report(e):
    """クラッシュレポートを/var/tmpに書き出す"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"/var/tmp/snmp_forwarder_crash_{timestamp}.log"
    
    logging.critical(f"予期せぬエラーによりクラッシュしました。詳細は {log_file} を確認してください。")

    try:
        with open(log_file, 'w') as f:
            f.write(f"Crash Time: {datetime.now()}\n")
            f.write(f"Error: {e}\n\n")
            f.write("--- Stack Trace ---\n")
            traceback.print_exc(file=f)
    except IOError as io_err:
        logging.error(f"クラッシュレポートの書き込みに失敗しました: {io_err}")

async def main():
    """メイン処理"""
    loop = asyncio.get_running_loop()
    for sig in [signal.SIGHUP, signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, signal_handler, sig)

    producer = None
    snmpEngine = None

    try:
        while not SHUTDOWN_EVENT.is_set():
            if producer is None or RELOAD_EVENT.is_set():
                if RELOAD_EVENT.is_set():
                    logging.info("設定のリロードを開始します...")
                    if snmpEngine:
                        snmpEngine.transport_dispatcher.close_dispatcher()
                    if producer:
                        producer.close()
                    RELOAD_EVENT.clear()

                config_data = load_config()
                if not config_data:
                    await asyncio.sleep(10)
                    continue

                snmp_config = config_data.get('snmp', {})
                kafka_config = config_data.get('kafka', {})

                producer = initialize_kafka_producer(kafka_config)
                if not producer:
                    await asyncio.sleep(10)
                    continue

                trap_callback_handler = create_trap_callback(
                    producer,
                    kafka_config.get('topic', 'snmp-traps')
                )

                snmpEngine = await setup_snmp_engine(snmp_config, trap_callback_handler)
                snmpEngine.transport_dispatcher.job_started(1)

            await asyncio.sleep(1)

    except asyncio.CancelledError:
        logging.info("メインタスクがキャンセルされました。")
    except Exception as e:
        log_crash_report(e)
    finally:
        logging.info("シャットダウン処理を開始します。")
        if snmpEngine:
            snmpEngine.transport_dispatcher.close_dispatcher()
        if producer:
            producer.close()
        logging.info("アプリケーションを終了しました。")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("プログラムが割り込みにより終了しました。")
