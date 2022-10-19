#!/usr/bin/env python3

from prometheus_client import Gauge

import decimal

from .rpc import RPC
from .config import Config
from .metrics import (
    # Difficulty
    QTUM_DIFFICULTY,
    # Hash per second
    QTUM_HASH_PS_GAUGES, hash_ps_gauge,
    # Memory info
    QTUM_MEMINFO_USED, QTUM_MEMINFO_FREE, QTUM_MEMINFO_TOTAL, QTUM_MEMINFO_LOCKED,
    QTUM_MEMINFO_CHUNKS_USED, QTUM_MEMINFO_CHUNKS_FREE,
    # Blockchain info
    QTUM_BLOCKS, QTUM_SIZE_ON_DISK, QTUM_VERIFICATION_PROGRESS,
    # Latest block
    QTUM_LATEST_BLOCK_SIZE, QTUM_LATEST_BLOCK_TXS, QTUM_LATEST_BLOCK_HEIGHT, QTUM_LATEST_BLOCK_WEIGHT,
    QTUM_LATEST_BLOCK_INPUTS, QTUM_LATEST_BLOCK_OUTPUTS, QTUM_LATEST_BLOCK_VALUE, QTUM_LATEST_BLOCK_FEE,
    # List banned metrics
    QTUM_BAN_CREATED, QTUM_BANNED_UNTIL,
    # Network info
    QTUM_SERVER_VERSION, QTUM_PROTOCOL_VERSION, QTUM_WARNINGS, 
    QTUM_CONNECTIONS, QTUM_CONNECTIONS_IN, QTUM_CONNECTIONS_OUT,
    # Chain tx stats
    QTUM_TX_COUNT,
    # Mempool info
    QTUM_MEMPOOL_BYTES, QTUM_MEMPOOL_SIZE, QTUM_MEMPOOL_USAGE, QTUM_MEMPOOL_UNBROADCAST,
    # Chain tips
    QTUM_NUM_CHAIN_TIPS,
    # Estimate smart fee
    QTUM_ESTIMATED_SMART_FEE_GAUGES, estimate_smart_fee_gauge,
    # Network_totals,
    QTUM_TOTAL_BYTES_RECV, QTUM_TOTAL_BYTES_SENT,
    # Uptime
    QTUM_UPTIME
)


def collect() -> None:

    with RPC(
        url=f"http://{Config.QTUM_RPC_HOST}:{Config.QTUM_RPC_PORT}",
        rpc_user=Config.QTUM_RPC_USER,
        rpc_password=Config.QTUM_RPC_PASSWORD
    ) as rpc:

        # Set difficulty values
        difficulty: dict = rpc.get_difficulty()
        QTUM_DIFFICULTY.set(difficulty["proof-of-stake"])

        # Set hash per second values
        for hash_ps_block in Config.HASH_PS_BLOCKS:
            hash_ps: int = rpc.get_network_hash_ps(num_blocks=hash_ps_block)
            if hash_ps is not None:
                gauge: Gauge = hash_ps_gauge(num_blocks=hash_ps_block)
                gauge.set(hash_ps)

        # Set memory info values
        memory_info: dict = rpc.get_memory_info()
        QTUM_MEMINFO_USED.set(memory_info["locked"]["used"])
        QTUM_MEMINFO_FREE.set(memory_info["locked"]["free"])
        QTUM_MEMINFO_TOTAL.set(memory_info["locked"]["total"])
        QTUM_MEMINFO_LOCKED.set(memory_info["locked"]["locked"])
        QTUM_MEMINFO_CHUNKS_USED.set(memory_info["locked"]["chunks_used"])
        QTUM_MEMINFO_CHUNKS_FREE.set(memory_info["locked"]["chunks_free"])
        
        # Set blockchain info values
        blockchain_info: dict = rpc.get_blockchain_info()
        QTUM_BLOCKS.set(blockchain_info["blocks"])
        # QTUM_DIFFICULTY.set(blockchain_info["difficulty"])
        QTUM_SIZE_ON_DISK.set(blockchain_info["size_on_disk"])
        QTUM_VERIFICATION_PROGRESS.set(blockchain_info["verificationprogress"])
        
        # Set latest block stats values
        latest_block_stats: dict = rpc.get_block_stats(
            blockchain_info["bestblockhash"], "total_size", "total_weight", "totalfee", "txs", "height", "ins", "outs", "total_out"
        )
        if latest_block_stats is not None:
            QTUM_LATEST_BLOCK_SIZE.set(latest_block_stats["total_size"])
            QTUM_LATEST_BLOCK_TXS.set(latest_block_stats["txs"])
            QTUM_LATEST_BLOCK_HEIGHT.set(latest_block_stats["height"])
            QTUM_LATEST_BLOCK_WEIGHT.set(latest_block_stats["total_weight"])
            QTUM_LATEST_BLOCK_INPUTS.set(latest_block_stats["ins"])
            QTUM_LATEST_BLOCK_OUTPUTS.set(latest_block_stats["outs"])
            QTUM_LATEST_BLOCK_VALUE.set(latest_block_stats["total_out"] / decimal.Decimal(1e8))
            QTUM_LATEST_BLOCK_FEE.set(latest_block_stats["totalfee"] / decimal.Decimal(1e8))
        
        # Set network info values
        list_banned: list = rpc.list_banned()
        for banned in list_banned:
            QTUM_BAN_CREATED.labels(
                address=banned["address"], reason=banned.get("ban_reason", "manually added")
            ).set(banned["ban_created"])
            QTUM_BANNED_UNTIL.labels(
                address=banned["address"], reason=banned.get("ban_reason", "manually added")
            ).set(banned["banned_until"])
        
        # Set network info values
        network_info: dict = rpc.get_network_info()
        QTUM_SERVER_VERSION.set(network_info["version"])
        QTUM_PROTOCOL_VERSION.set(network_info["protocolversion"])
        if network_info["warnings"]:
            QTUM_WARNINGS.inc()
        QTUM_CONNECTIONS.set(network_info["connections"])
        if "connections_in" in network_info:
            QTUM_CONNECTIONS_IN.set(network_info["connections_in"])
        if "connections_out" in network_info:
            QTUM_CONNECTIONS_OUT.set(network_info["connections_out"])

        # Set chain tx stats values
        chain_tx_stats: dict = rpc.get_chain_tx_stats()
        QTUM_TX_COUNT.set(chain_tx_stats["txcount"])

        # Set mempool info values
        mempool_info: dict = rpc.get_mempool_info()
        QTUM_MEMPOOL_BYTES.set(mempool_info["bytes"])
        QTUM_MEMPOOL_SIZE.set(mempool_info["size"])
        QTUM_MEMPOOL_USAGE.set(mempool_info["usage"])
        if "unbroadcastcount" in mempool_info:
            QTUM_MEMPOOL_UNBROADCAST.set(mempool_info["unbroadcastcount"])

        # Set chain tips values
        chain_tips: list = rpc.get_chain_tips()
        QTUM_NUM_CHAIN_TIPS.set(len(chain_tips))

        # Set estimate smart fee values
        for smart_fee_block in Config.SMART_FEE_BLOCKS:
            estimated_smart_fee: dict = rpc.estimate_smart_fee(num_blocks=smart_fee_block)
            if estimated_smart_fee.get("feerate") is not None:
                gauge: Gauge = estimate_smart_fee_gauge(num_blocks=smart_fee_block)
                gauge.set(estimated_smart_fee["feerate"])
        
        # Set network totals values
        network_totals: dict = rpc.get_network_totals()
        QTUM_TOTAL_BYTES_RECV.set(network_totals["totalbytesrecv"])
        QTUM_TOTAL_BYTES_SENT.set(network_totals["totalbytessent"])

        # Set uptime values
        uptime: int = rpc.get_uptime()
        QTUM_UPTIME.set(uptime)
