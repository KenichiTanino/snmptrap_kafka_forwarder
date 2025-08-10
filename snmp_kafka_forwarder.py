import json
import logging
import signal
import asyncio
import traceback
from datetime import datetime
from pathlib import Path

from kafka import KafkaProducer
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.smi import builder, compiler
from pysnmp.smi import view, error


# --- ロギング設定 ---
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
            bootstrap_servers=kafka_config.get(
                'bootstrap_servers', 'localhost:9092').split(','),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            security_protocol=kafka_config.get(
                'security_protocol', 'PLAINTEXT')
        )
        logging.info(
            f"Kafkaプロデューサーを初期化しました: {kafka_config.get('bootstrap_servers')}")
        return producer
    except Exception as e:
        logging.error(f"Kafkaプロデューサーの初期化に失敗しました: {e}")
        return None


def create_trap_callback(producer, kafka_topic, mib_source=None):
    """SNMPトラップ受信時のコールバック関数"""
    def trap_callback(snmpEngine, stateReference, _contextEngineId, contextName,
                      varBinds, _cbCtx):
        # 必要に応じてmib_sourceを利用可能
        # 例: logging.debug(f"mib_source: {mib_source}")
        _transportDomain, transportAddress = snmpEngine.message_dispatcher.get_transport_info(
            stateReference)
        source_ip, source_port = transportAddress
        community_name = contextName.prettyPrint()

        logging.info(
            f"トラップを受信しました from {source_ip}:{source_port} (Community: {community_name})")

        trap_data = {
            "source_ip": source_ip,
            "source_port": source_port,
            "community": community_name,
            "protocol_version": "v1/v2c",
            "timestamp": datetime.now().isoformat() + 'Z',
            "variables": []
        }

        for oid, val in varBinds:
            breakpoint()
            try:
                trap_data["variables"].append({
                    "oid": str(oid),
                    "oid_full": oid.prettyPrint(),
                    "value": val.prettyPrint(),
                    "value_type": val.__class__.__name__
                })
            except Exception as e:
                logging.warning(f"VarBindの解析中にエラーが発生しました: {e}")

        logging.debug(f"トラップデータ: {trap_data}")

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

    # MIB設定: コンパイル済みMIBを読み込む
    mibBuilder = snmpEngine.get_mib_builder()
    mibView = view.MibViewController(mibBuilder)
    mib_source_path = (Path(__file__).resolve().parent /
                       'tools' / 'compiled_mibs')
    mib_source = None
    if mib_source_path.is_dir():
        logging.info(f"コンパイル済みMIBディレクトリを読み込みます: {mib_source_path}")
        mib_source = builder.DirMibSource(str(mib_source_path))
        mibBuilder.add_mib_sources(mib_source)
        try:
            mibBuilder.load_modules(
                'SNMPv2-SMI',
                'SNMPv2-TC',
                'SNMPv2-CONF',
                'INET-ADDRESS-MIB',
                'HCNUM-TC',
                'ARBOR-SMI',
                'PEAKFLOW-SP-MIB',
                'PEAKFLOW-DOS-MIB'
            )
            logging.info("カスタムMIBモジュールを正常にロードしました。")
        except Exception as e:
            logging.error(f"カスタムMIBモジュールのロード中にエラーが発生しました: {e}")
    else:
        logging.warning(
            f"コンパイル済みMIBディレクトリが見つかりません: {mib_source_path}。OIDの名前解決は行われません。")

    config.add_transport(
        snmpEngine,
        udp.DOMAIN_NAME,
        udp.UdpTransport().open_server_mode((host, port))
    )

    for i, community in enumerate(communities):
        config.add_v1_system(snmpEngine, f'my-area-{i}', community)

    logging.info(
        f"SNMPトラップの待受を開始します: {host}:{port}, Communities: {communities}")
    return snmpEngine, mib_source


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

                # producer, snmpEngine, trap_callback_handlerの初期化部分
                producer = initialize_kafka_producer(kafka_config)
                if not producer:
                    await asyncio.sleep(10)
                    continue

                # setup_snmp_engineの返り値を2つ受け取る
                snmpEngine, mib_source = await setup_snmp_engine(snmp_config, None)
                # mib_source = None
                # snmpEngine = await setup_snmp_engine(snmp_config, None)

                trap_callback_handler = create_trap_callback(
                    producer,
                    kafka_config.get('topic', 'snmp-traps'),
                    mib_source
                )

                # コールバック登録
                ntfrcv.NotificationReceiver(snmpEngine, trap_callback_handler)
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
