#!/usr/bin/env python3

from prometheus_client import (
    Gauge, Counter
)
from typing import (
    Optional, Dict
)


# Difficulty metrics
QTUM_DIFFICULTY: Gauge = Gauge(
    "qtum_difficulty", "The current difficulty"
)

# Hash per second metrics
QTUM_HASH_PS_GAUGES: Dict[int, Gauge] = { }


def hash_ps_gauge(num_blocks: int) -> Gauge:
    gauge: Optional[Gauge] = QTUM_HASH_PS_GAUGES.get(num_blocks)

    def hashps_gauge_suffix(nblocks):
        if nblocks < 0:
            return f"_neg{-nblocks}"
        if nblocks == 120:
            return ""
        return f"_{nblocks}"

    if gauge is None:
        desc_end: str = (
            "since the last difficulty change" if num_blocks == -1 else f"for the last {num_blocks} blocks"
        )
        gauge: Gauge = Gauge(
            f"qtum_hash_ps{hashps_gauge_suffix(num_blocks)}",
            f"Estimated network hash rate per second {desc_end}",
        )
        QTUM_HASH_PS_GAUGES[num_blocks] = gauge
    return gauge


# Memory info metrics
QTUM_MEMINFO_USED: Gauge = Gauge(
    "qtum_meminfo_used", "Number of bytes used"
)
QTUM_MEMINFO_FREE: Gauge = Gauge(
    "qtum_meminfo_free", "Number of bytes available in current arenas"
)
QTUM_MEMINFO_TOTAL: Gauge = Gauge(
    "qtum_meminfo_total", "Total number of bytes managed"
)
QTUM_MEMINFO_LOCKED: Gauge = Gauge(
    "qtum_meminfo_locked", "Amount of bytes that succeeded locking. If this number is smaller than total, "
                           "locking pages failed at some point and key data could be swapped to disk."
)
QTUM_MEMINFO_CHUNKS_USED: Gauge = Gauge(
    "qtum_meminfo_chunks_used", "Number of allocated chunks"
)
QTUM_MEMINFO_CHUNKS_FREE: Gauge = Gauge(
    "qtum_meminfo_chunks_free", "Number of unused chunks"
)

# Blockchain info metrics
QTUM_BLOCKS: Gauge = Gauge(
    "qtum_blocks", "The current number of blocks processed in the server"
)
QTUM_SIZE_ON_DISK: Gauge = Gauge(
    "qtum_size_on_disk", "The estimated size of the block and undo files on disk"
)
QTUM_VERIFICATION_PROGRESS: Gauge = Gauge(
    "qtum_verification_progress", "Estimate of verification progress [0..1]"
)

# Latest block stats metrics
QTUM_LATEST_BLOCK_SIZE: Gauge = Gauge(
    "qtum_latest_block_size", "Size of latest block in bytes"
)
QTUM_LATEST_BLOCK_TXS: Gauge = Gauge(
    "qtum_latest_block_txs", "Number of transactions in latest block"
)
QTUM_LATEST_BLOCK_HEIGHT: Gauge = Gauge(
    "qtum_latest_block_height", "Height or index of latest block"
)
QTUM_LATEST_BLOCK_WEIGHT: Gauge = Gauge(
    "qtum_latest_block_weight", "Weight of latest block according to BIP 141"
)
QTUM_LATEST_BLOCK_INPUTS: Gauge = Gauge(
    "qtum_latest_block_inputs", "Number of inputs in transactions of latest block"
)
QTUM_LATEST_BLOCK_OUTPUTS: Gauge = Gauge(
    "qtum_latest_block_outputs", "Number of outputs in transactions of latest block"
)
QTUM_LATEST_BLOCK_VALUE: Gauge = Gauge(
    "qtum_latest_block_value", "Qtum value of all transactions in the latest block"
)
QTUM_LATEST_BLOCK_FEE: Gauge = Gauge(
    "qtum_latest_block_fee", "Total fee to process the latest block"
)

# List banned metrics
QTUM_BAN_CREATED: Gauge = Gauge(
    "qtum_ban_created", "Time the ban was created", labelnames=["address", "reason"]
)
QTUM_BANNED_UNTIL: Gauge = Gauge(
    "qtum_banned_until", "Time the ban expires", labelnames=["address", "reason"]
)

# Network info metrics
QTUM_SERVER_VERSION: Gauge = Gauge(
    "qtum_server_version", "The server version"
)
QTUM_PROTOCOL_VERSION: Gauge = Gauge(
    "qtum_protocol_version", "The protocol version of the server"
)
QTUM_CONNECTIONS: Gauge = Gauge(
    "qtum_connections", "The number of connections or peers"
)
QTUM_CONNECTIONS_IN: Gauge = Gauge(
    "qtum_connections_in", "The number of connections in"
)
QTUM_CONNECTIONS_OUT: Gauge = Gauge(
    "qtum_connections_out", "The number of connections out"
)
QTUM_WARNINGS: Counter = Counter(
    "qtum_warnings", "Number of network or blockchain warnings detected"
)

# Chain tx stats metrics
QTUM_TX_COUNT: Gauge = Gauge(
    "qtum_tx_count", "Number of TX since the genesis block"
)

# Mempool info metrics
QTUM_MEMPOOL_BYTES: Gauge = Gauge(
    "qtum_mempool_bytes", "Size of mempool in bytes"
)
QTUM_MEMPOOL_SIZE: Gauge = Gauge(
    "qtum_mempool_size", "Number of unconfirmed transactions in mempool"
)
QTUM_MEMPOOL_USAGE: Gauge = Gauge(
    "qtum_mempool_usage", "Total memory usage for the mempool"
)
QTUM_MEMPOOL_UNBROADCAST: Gauge = Gauge(
    "qtum_mempool_unbroadcast", "Number of transactions waiting for acknowledgment"
)

# Chain tips metrics
QTUM_NUM_CHAIN_TIPS: Gauge = Gauge(
    "qtum_num_chain_tips", "Number of known blockchain branches"
)

# Estimate smart fee metrics
QTUM_ESTIMATED_SMART_FEE_GAUGES: Dict[int, Gauge] = { }


def estimate_smart_fee_gauge(num_blocks: int) -> Gauge:
    gauge: Optional[Gauge] = QTUM_ESTIMATED_SMART_FEE_GAUGES.get(num_blocks)
    if gauge is None:
        gauge: Gauge = Gauge(
            f"qtum_estimate_smart_fee_{num_blocks}",
            f"Estimated smart fee per kilobyte for confirmation in {num_blocks} blocks"
        )
        QTUM_ESTIMATED_SMART_FEE_GAUGES[num_blocks] = gauge
    return gauge


# Network totals metrics
QTUM_TOTAL_BYTES_RECV: Gauge = Gauge(
    "qtum_total_bytes_recv", "Total bytes received"
)
QTUM_TOTAL_BYTES_SENT: Gauge = Gauge(
    "qtum_total_bytes_sent", "Total bytes sent"
)

# Uptime metrics
QTUM_UPTIME: Gauge = Gauge(
    "qtum_uptime", "The number of seconds that the server has been running"
)

# Qtum exporters metrics
EXPORTER_ERRORS: Counter = Counter(
    "qtum_exporter_errors", "Number of errors encountered by the exporter", labelnames=["type"]
)
PROCESS_TIME: Counter = Counter(
    "qtum_exporter_process_time", "Time spent processing metrics from qtum node"
)
