import unittest
import json
import logging
import asyncio
from unittest.mock import patch, MagicMock, mock_open, AsyncMock

# テスト対象のモジュールをインポート
import snmp_kafka_forwarder

class TestSnmpKafkaForwarder(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @patch("builtins.open", new_callable=mock_open, read_data='{"snmp": {}, "kafka": {}}')
    def test_load_config_success(self, mock_file):
        """設定ファイルの読み込みが成功するケース"""
        config = snmp_kafka_forwarder.load_config('dummy_path.json')
        self.assertIsNotNone(config)
        self.assertIn('snmp', config)
        self.assertIn('kafka', config)
        mock_file.assert_called_with('dummy_path.json')

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_config_not_found(self, mock_file):
        """設定ファイルが見つからないケース"""
        config = snmp_kafka_forwarder.load_config()
        self.assertIsNone(config)

    @patch("builtins.open", new_callable=mock_open, read_data='this is not json')
    def test_load_config_invalid_json(self, mock_file):
        """設定ファイルが不正なJSONであるケース"""
        config = snmp_kafka_forwarder.load_config()
        self.assertIsNone(config)

    @patch('snmp_kafka_forwarder.KafkaProducer')
    def test_initialize_kafka_producer_success(self, MockKafkaProducer):
        """Kafkaプロデューサーの初期化が成功するケース"""
        mock_instance = MockKafkaProducer.return_value
        kafka_config = {'bootstrap_servers': 'localhost:9092'}
        producer = snmp_kafka_forwarder.initialize_kafka_producer(kafka_config)
        self.assertIsNotNone(producer)
        self.assertEqual(producer, mock_instance)
        MockKafkaProducer.assert_called_once()

    @patch('snmp_kafka_forwarder.KafkaProducer', side_effect=Exception("Kafka connection failed"))
    def test_initialize_kafka_producer_failure(self, MockKafkaProducer):
        """Kafkaプロデューサーの初期化が失敗するケース"""
        producer = snmp_kafka_forwarder.initialize_kafka_producer({})
        self.assertIsNone(producer)

    def test_create_trap_callback(self):
        """トラップコールバックが正しくKafkaにメッセージを送信しようとするか"""
        mock_producer = MagicMock()
        kafka_topic = "test-topic"

        callback = snmp_kafka_forwarder.create_trap_callback(mock_producer, kafka_topic)

        mock_snmp_engine = MagicMock()
        mock_snmp_engine.msgAndPduDsp.getTransportInfo.return_value = (None, ('127.0.0.1', 12345))
        
        mock_context_name = MagicMock()
        mock_context_name.prettyPrint.return_value = 'public'

        mock_oid = MagicMock()
        mock_oid.prettyPrint.return_value = '1.3.6.1.2.1.1.1.0'
        mock_val = MagicMock()
        mock_val.prettyPrint.return_value = 'Test String'
        type(mock_val).__name__ = 'OctetString'

        var_binds = [(mock_oid, mock_val)]

        callback(mock_snmp_engine, None, None, mock_context_name, var_binds, None)

        mock_producer.send.assert_called_once()
        sent_topic = mock_producer.send.call_args[0][0]
        sent_message = mock_producer.send.call_args[0][1]

        self.assertEqual(sent_topic, kafka_topic)
        self.assertEqual(sent_message['community'], 'public')

    @patch('snmp_kafka_forwarder.engine')
    @patch('snmp_kafka_forwarder.config')
    @patch('snmp_kafka_forwarder.ntfrcv')
    @patch('snmp_kafka_forwarder.udp.UdpTransport')
    async def test_setup_snmp_engine(self, MockUdpTransport, mock_ntfrcv, mock_config, mock_engine):
        """SNMP Engineのセットアップが正しく行われるか (async)"""
        mock_transport_instance = MockUdpTransport.return_value
        mock_transport_instance.openServerMode = AsyncMock()

        snmp_config = {
            'host': '0.0.0.0',
            'port': 162,
            'communities': ['public', 'private']
        }
        mock_callback = MagicMock()

        snmp_engine_instance = await snmp_kafka_forwarder.setup_snmp_engine(snmp_config, mock_callback)

        self.assertIsNotNone(snmp_engine_instance)
        mock_config.addTransport.assert_called_once()
        self.assertEqual(mock_config.addV1System.call_count, 2)
        mock_ntfrcv.NotificationReceiver.assert_called_with(unittest.mock.ANY, mock_callback)

    @patch("builtins.open", new_callable=mock_open)
    @patch("snmp_kafka_forwarder.traceback.print_exc")
    def test_log_crash_report(self, mock_print_exc, mock_file):
        """クラッシュレポートがファイルに書き込まれるか"""
        try:
            raise ValueError("Test crash")
        except ValueError as e:
            snmp_kafka_forwarder.log_crash_report(e)
        
        mock_file.assert_called_once()
        self.assertIn('/var/tmp/snmp_forwarder_crash_', mock_file.call_args[0][0])
        mock_print_exc.assert_called_once()

if __name__ == '__main__':
    unittest.main()
