FROM docker.redpanda.com/redpandadata/redpanda:latest

EXPOSE 9092 8081 8082

CMD ["redpanda", "start", "--smp", "1", "--memory", "1G", "--overprovisioned", "--set", "redpanda.auto_create_topics_enabled=true"]