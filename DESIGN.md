# SNMP Trap to Kafka Forwarder Design

## 1. 概要

このアプリケーションは、SNMP トラップを受信し、その内容を JSON 形式に変換して Apache Kafka の指定されたトピックに転送する非同期フォワーダーです。

`pysnmp`ライブラリを利用して SNMP トラップを受信・解析し、`kafka-python`ライブラリを使用して Kafka へメッセージを送信します。設定ファイルによる柔軟な設定変更や、シグナルによるリロード・シャットダウンに対応しています。

### 1.1. アーキテクチャ概要図

```
+----------------+      +--------------------------+      +----------------+      +-------------------+
|                |      |                          |      |                |      |                   |
|  SNMP-enabled  |----->|  snmp_kafka_forwarder.py |----->|      Kafka     |----->|  Kafka Consumer   |
|    Devices     | SNMP |       (UDP Listener)     | JSON |(Message Broker)| JSON |                   |
|                | Trap |                          |      |                |      |                   |
+----------------+      +--------------------------+      +----------------+      +-------------------+
                          |
                          | 1. Listen for SNMP traps on UDP port.
                          | 2. Parse trap using pre-compiled MIBs.
                          | 3. Convert to JSON.
                          | 4. Send to Kafka topic.
```

## 2. 主な機能

- **SNMP トラップ受信**: 指定した IP アドレスとポートで SNMP v1/v2c トラップを待ち受けます。
- **MIB による OID の名前解決**: `tools/compiled_mibs`ディレクトリにあるコンパイル済みの MIB ファイルを使用して、受信したトラップの OID（Object Identifier）を人間が読みやすいシンボル名（例: `SNMPv2-MIB::sysUpTime.0`）に解決します。
- **JSON への変換**: 受信したトラップの情報を、送信元 IP、コミュニティ名、タイムスタンプ、変数束縛（VarBinds）などを含む構造化された JSON 形式に変換します。
- **Kafka への転送**: 変換した JSON データを指定された Kafka ブローカーのトピックへ非同期で送信します。
- **設定の外部化**: `config.json`ファイルにより、リッスンするインターフェース、ポート、コミュニティ、Kafka の接続情報などを容易に変更できます。
- **動的な設定リロード**: `SIGHUP`シグナルを受信すると、アプリケーションを停止することなく設定ファイルを再読み込みします。
- **安全なシャットダウン**: `SIGINT` (Ctrl+C) や `SIGTERM` シグナルを捕捉し、リソースを解放して安全に終了します。
- **非同期処理**: `asyncio`を利用して、効率的な I/O 処理を実現しています。
- **堅牢なロギングとエラーハンドリング**:
  - アプリケーションの動作状況を標準出力にロギングします。
  - 予期せぬエラーでクラッシュした際には、詳細なスタックトレースを含むクラッシュレポートを`/var/tmp/`ディレクトリに保存します。

## 3. 設定 (`config.json`)

アプリケーションの動作は、以下の JSON 形式の設定ファイルで管理します。

```json
{
  "snmp": {
    "host": "0.0.0.0",
    "port": 162,
    "communities": ["public", "private"]
  },
  "kafka": {
    "bootstrap_servers": "localhost:9092",
    "topic": "snmp-traps",
    "security_protocol": "PLAINTEXT"
  }
}
```

- `snmp.host`: トラップを受信するリスニング IP アドレス。
- `snmp.port`: トラップを受信するリスニング UDP ポート。
- `snmp.communities`: 受け入れる SNMP コミュニティ名のリスト。
- `kafka.bootstrap_servers`: 接続先の Kafka ブローカーのリスト（カンマ区切り）。
- `kafka.topic`: メッセージを送信する Kafka トピック名。
- `kafka.security_protocol`: Kafka との接続に使用するセキュリティプロトコル（例: `PLAINTEXT`, `SSL`）。

## 4. Kafka へ送信されるデータフォーマット

Kafka に送信されるメッセージは、以下の情報を含む JSON 形式です。

```json
{
  "source_ip": "127.0.0.1",
  "source_port": 49152,
  "community": "public",
  "protocol_version": "v1/v2c",
  "timestamp": "2025-08-10T15:00:00.123456Z",
  "variables": [
    {
      "oid": "SNMPv2-MIB::sysUpTime.0",
      "oid_full": "1.3.6.1.2.1.1.3.0",
      "value": "12345",
      "value_type": "TimeTicks"
    },
    {
      "oid": "SNMPv2-MIB::snmpTrapOID.0",
      "oid_full": "1.3.6.1.6.3.1.1.4.1.0",
      "value": "PEAKFLOW-SP-MIB::peakflowDosAlertClear",
      "value_type": "ObjectIdentifier"
    }
  ]
}
```

## 5. 実行方法

### 5.1. 依存関係のインストール

`pyproject.toml`に記載された依存関係をインストールします。

```bash
# uvなどのパッケージ管理ツールを使用
pip install uv
uv pip install -r requirements.txt # もしくは pyproject.toml から直接
```

### 5.2. MIB のコンパイル

OID の名前解決を機能させるには、使用する MIB ファイルをコンパイルしておく必要があります。

```bash
# (必要に応じて `tools/compile_mib.py` などのスクリプトを実行)
```

### 5.3. 設定ファイルの準備

`config.json.sample`をコピーして`config.json`を作成し、環境に合わせて内容を編集します。

```bash
cp config.json.sample config.json
vi config.json
```

### 5.4. アプリケーションの起動

以下のコマンドでアプリケーションを起動します。

```bash
python snmp_kafka_forwarder.py
```

## 6. シグナルハンドリング

- **`SIGHUP`**: 設定ファイル `config.json` を再読み込みし、Kafka プロデューサーと SNMP リスナーを再初期化します。
- **`SIGINT`, `SIGTERM`**: アプリケーションを安全にシャットダウンします。

## 7. 技術スタック

- **プログラミング言語**: Python 3
- **非同期フレームワーク**: `asyncio`
- **主要ライブラリ**:
  - `pysnmp`: SNMP トラップの受信と解析
  - `kafka-python`: Kafka へのデータ送信
