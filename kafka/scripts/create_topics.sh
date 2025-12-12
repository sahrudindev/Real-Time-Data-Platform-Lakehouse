#!/bin/bash
# =============================================================================
# KAFKA TOPIC CREATION SCRIPT
# =============================================================================
# Creates all required Kafka topics for the enterprise data platform
# =============================================================================

set -e

KAFKA_BOOTSTRAP_SERVER="${KAFKA_BOOTSTRAP_SERVER:-localhost:29092}"
TOPICS_CONFIG_FILE="${TOPICS_CONFIG_FILE:-/opt/kafka/config/topics.json}"

echo "=============================================="
echo "  Kafka Topic Creation Script"
echo "=============================================="
echo "Bootstrap Server: ${KAFKA_BOOTSTRAP_SERVER}"
echo ""

# Function to create a topic
create_topic() {
    local topic_name=$1
    local partitions=$2
    local replication_factor=$3
    local retention_ms=$4
    local cleanup_policy=$5
    local compression_type=$6
    
    echo "Creating topic: ${topic_name}"
    
    # Check if topic exists
    if kafka-topics --bootstrap-server ${KAFKA_BOOTSTRAP_SERVER} --list | grep -q "^${topic_name}$"; then
        echo "  Topic ${topic_name} already exists. Skipping..."
        return 0
    fi
    
    # Create the topic
    kafka-topics --bootstrap-server ${KAFKA_BOOTSTRAP_SERVER} \
        --create \
        --topic ${topic_name} \
        --partitions ${partitions} \
        --replication-factor ${replication_factor} \
        --config retention.ms=${retention_ms} \
        --config cleanup.policy=${cleanup_policy} \
        --config compression.type=${compression_type}
    
    echo "  Topic ${topic_name} created successfully!"
}

echo "Creating e-commerce data topics..."
echo ""

# Raw data topics
create_topic "raw.ecommerce.orders" 6 1 604800000 "delete" "lz4"
create_topic "raw.ecommerce.customers" 3 1 604800000 "compact" "lz4"
create_topic "raw.ecommerce.products" 3 1 604800000 "compact" "lz4"
create_topic "raw.ecommerce.clickstream" 12 1 259200000 "delete" "snappy"
create_topic "raw.ecommerce.inventory" 3 1 604800000 "compact" "lz4"
create_topic "raw.ecommerce.payments" 6 1 2592000000 "delete" "lz4"

# Processed topics
create_topic "processed.orders.enriched" 6 1 604800000 "delete" "lz4"
create_topic "processed.analytics.realtime" 3 1 86400000 "delete" "lz4"

# System topics
create_topic "alerts.data-quality" 1 1 604800000 "delete" "gzip"
create_topic "dlq.processing-errors" 3 1 2592000000 "delete" "gzip"

echo ""
echo "=============================================="
echo "  All topics created successfully!"
echo "=============================================="

# List all topics
echo ""
echo "Current topics:"
kafka-topics --bootstrap-server ${KAFKA_BOOTSTRAP_SERVER} --list
