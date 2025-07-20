# SNMP Trap to Kafka Forwarder Design

## 1. 目的

受信したSNMPトラップメッセージを解析し、指定されたKafkaトピックにJSON形式で転送するPythonアプリケーションを開発する。

## 2. 機能要件

-   指定されたIPアドレスとポートでSNMPトラップ（v1, v2c, v3）を受信する。
-   受信したトラップデータを人間が判読可能な形式（JSON）にパースする。
-   パースしたデータを指定されたKafkaブローカーのトピックに送信する。
-   設定は外部の設定ファイル（`config.json`）から読み込む。
-   アプリケーションの動作状況を標準出力にロギングする。

## 3. 技術スタック

-   **プログラミング言語:** Python 3
-   **主要ライブラリ:**
    -   `pysnmp`: SNMPトラップの受信と解析
    -   `kafka-python`: Kafkaへのデータ送信

## 4. 設定ファイル (`config.json`)

アプリケーションの動作は以下のJSON形式の設定ファイルで管理する。

```json
{
  "snmp": {
    "host": "0.0.0.0",
    "port": 162,
    "community": "public"
  },
  "kafka": {
    "bootstrap_servers": "localhost:9092",
    "topic": "snmp-traps",
    "security_protocol": "PLAINTEXT"
  }
}
```

-   **snmp.host**: トラップを受信するリスニングIPアドレス。
-   **snmp.port**: トラップを受信するリスニングポート。
-   **snmp.community**: SNMPv1/v2cのコミュニティ名。
-   **kafka.bootstrap_servers**: 接続先のKafkaブローカーのリスト。
-   **kafka.topic**: メッセージを送信するKafkaトピック名。
-   **kafka.security_protocol**: Kafkaとの接続に使用するセキュリティプロトコル（例: `PLAINTEXT`, `SSL`）。

## 5. データフォーマット

Kafkaに送信されるメッセージは、以下の情報を含むJSON形式とする。

```json
{
  "source_ip": "192.168.1.1",
  "source_port": 49152,
  "community": "public",
  "protocol_version": "v2c",
  "timestamp": "2025-07-20T10:30:00Z",
  "variables": [
    {
      "oid": "1.3.6.1.6.3.1.1.4.1.0",
      "oid_full": "SNMPv2-MIB::snmpTrapOID.0",
      "value": "1.3.6.1.4.1.8072.2.3.0.1",
      "value_type": "OBJECT IDENTIFIER"
    },
    {
      "oid": "1.3.6.1.2.1.1.3.0",
      "oid_full": "DISMAN-EVENT-MIB::sysUpTimeInstance",
      "value": "12345",
      "value_type": "TimeTicks"
    },
    {
      "oid": "1.3.6.1.4.1.8072.2.3.2.1",
      "oid_full": "NET-SNMP-EXAMPLES-MIB::netSnmpExampleString",
      "value": "Hello, World!",
      "value_type": "OCTET STRING"
    }
  ]
}
```

## 6. プログラムの構造

1.  **初期化**:
    -   `config.json`を読み込み、設定をグローバル変数または設定クラスに格納する。
    -   Kafkaプロデューサーを初期化し、接続を確立する。
2.  **SNMPトラップ受信機**:
    -   `pysnmp`の`SnmpEngine`を初期化する。
    -   設定ファイルの情報に基づき、リスニングエンドポイントとコミュニティを設定する。
    -   トラップを受信した際に呼び出されるコールバック関数を登録する。
3.  **コールバック関数 (`trap_callback`)**:
    -   受信したトラップデータ（PDU）と送信元アドレスを受け取る。
    -   PDUからOIDとVarBinds（変数束縛）を抽出する。
    -   抽出したデータを上記のJSONフォーマットに従って整形する。
    -   整形したJSONメッセージをKafkaプロデューサー経由で送信する。
    -   処理の成功または失敗をロギングする。
4.  **メイン処理**:
    -   初期化処理を呼び出す。
    -   SNMPトラップ受信機を起動し、無限ループで待機させる。
    -   `KeyboardInterrupt`（Ctrl+C）を捕捉し、安全にシャットダウン処理を行う。

## 7. 実行方法

1.  必要なライブラリをインストールする。
    ```bash
    pip install pysnmp kafka-python
    ```
2.  `config.json`を作成・編集する。
3.  以下のコマンドでアプリケーションを起動する。
    ```bash
    python snmp_kafka_forwarder.py
    ```
