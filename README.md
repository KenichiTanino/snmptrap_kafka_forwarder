# SNMP Trap to Kafka Forwarder

This project contains a Python application to receive SNMP traps and forward them to a Kafka topic.

## Setup

1.  Create a virtual environment:
    ```bash
    uv venv
    ```
2.  Activate the environment:
    ```bash
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    uv pip install pysnmp kafka-python
    ```

## Running the application

```bash
python3 snmp_kafka_forwarder.py
```

Or using uv:
```bash
uv run snmp_kafka_forwarder.py
```

---

## Test Execution History

### 2025-07-19

**Command:**

```bash
.venv/bin/python3 -m unittest discover tests
```

**Result:** `OK`

**Output:**

```
/home/tanino/gemini-cli/20250719_snmptrap/snmp_kafka_forwarder.py:71: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  "timestamp": datetime.utcnow().isoformat() + 'Z',
........
----------------------------------------------------------------------
Ran 8 tests in 0.016s

OK
```

## Running Redpanda with Docker

To run a Redpanda (Kafka-compatible) instance using Docker:

1.  **Build the Docker image:**
    ```bash
    docker build -t my-redpanda-instance ./docker
    ```
2.  **Run the Docker container:**
    ```bash
    docker run -d --name redpanda -p 9092:9092 -p 8081:8081 -p 8082:8082 my-redpanda-instance
    ```

This will start a Redpanda container in the background, accessible on your host machine at `localhost:9092`, `localhost:8081`, and `localhost:8082`.

## 単体テストツール

以下を使って実際の 単体テスト用ツールを作る。実際に送信してもらう

https://github.com/librenms/librenms/blob/master/mibs/arbornet/ARBORNET-PEAKFLOW-SP-MIB

v3 用の実装をつくる
