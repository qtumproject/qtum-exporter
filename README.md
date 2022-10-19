
# Qtum Exporter

[![PyPI License](https://img.shields.io/pypi/l/hdwallet?color=black)](https://pypi.org/project/hdwallet)
[![Docker Image Version](https://img.shields.io/docker/v/meherett/qtum-exporter)](https://github.com/qtumproject/qtum-exporter)
[![Docker Image Size](https://img.shields.io/docker/image-size/meherett/qtum-exporter)](https://github.com/qtumproject/qtum-exporter)

A [Prometheus](https://prometheus.io) exporter for Qtum nodes.

## Installation

To get started, just fork this repository, clone it locally, and build docker image:

```shell
docker build --tag meherett/qtum-exporter:latest .
```

Or, after cloning it locally, and run:

```shell
python -m pip install -r requirements.txt
```

To use the pre-built image just pull it:

```shell
docker pull meherett/qtum-exporter:latest
```

## Quick Usage
 
To run qtum-exporter from source code:

```shell
python moniter.py
```

Or, to run qtum-exporter from docker:

```shell
docker run -d -p 6363:6363 \
  -e QTUM_RPC_HOST="0.0.0.0" \
  -e QTUM_RPC_PORT="3889" \
  -e QTUM_RPC_USER="<qtumd_username>" \
  -e QTUM_RPC_PASSWORD="<qtumd_password>" \
  -e REFRESH_SECONDS=5 \
  meherett/qtum-exporter:latest
```

Then visit [http://localhost:6363](http://localhost:6363) to view the metrics.

## Screenshot

On Prometheus

![Prometheus Screenshot](https://raw.githubusercontent.com/qtumproject/qtum-exporter/master/prometheus.png)

On Grafana

![Grafana Screenshot](https://raw.githubusercontent.com/qtumproject/qtum-exporter/master/grafana.png)

## Environment Variables

Here are the following environment variables with default values:

| Keys              | Description                                                           | Default Values |
|-------------------|-----------------------------------------------------------------------|----------------|
| QTUM_RPC_HOST     | Bind to given address to listen for JSON-RPC connections              | ``0.0.0.0``    |
| QTUM_RPC_PORT     | Listen for JSON-RPC connections on port                               | ``3889``       |
| QTUM_RPC_USER     | Username for JSON-RPC connections                                     | ``qtum``       |
| QTUM_RPC_PASSWORD | Password for JSON-RPC connections                                     | ``testpasswd`` |
| HASH_PS_BLOCKS    | Estimated network hash rate per second                                | ``-1,1,120``   |
| SMART_FEE_BLOCKS  | Estimated smart fee per kilobyte for confirmation in {nblocks} blocks | ``2,3,5,20``   |
| METRICS_ADDRESS   | Bind to given address to listen for Qtum-Exporter connections.        | ``0.0.0.0``    |
| METRICS_PORT      | Listen for Qtum-Exporter connections on port                          | ``6363``       |
| TIMEOUT           | The maximum time allocated to collect data in seconds                 | ``15``         |
| REFRESH_SECONDS   | Refreshing time set to collect data in seconds                        | ``5``          |
| LOGGING_LEVEL     | Determines which severity of messages it will pass to its handlers    | ``INFO``       |

## Prometheus Config

The prometheus.yml settings looks like:

```yaml
scrape_configs:
  - job_name: "qtum-exporter"
    static_configs:
      - targets: ["0.0.0.0:6363"]

```

## Exported Metrics

Here are available exported metrics:

| Metric                                | Meaning                                                                                                                                                 | Type    |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| ``qtum_difficulty``                   | The current difficulty                                                                                                                                  | Gauge   |
| ``qtum_hash_ps_{nblocks}``            | Estimated network hash rate per second                                                                                                                  | Gauge   |
| ``qtum_meminfo_used``                 | Number of bytes used                                                                                                                                    | Gauge   |
| ``qtum_meminfo_free``                 | Number of bytes available in current arenas                                                                                                             | Gauge   |
| ``qtum_meminfo_total``                | Total number of bytes managed                                                                                                                           | Gauge   |
| ``qtum_meminfo_locked``               | Amount of bytes that succeeded locking. If this number is smaller than total, locking pages failed at some point and key data could be swapped to disk. | Gauge   |
| ``qtum_meminfo_chunks_used``          | Number of allocated chunks                                                                                                                              | Gauge   |
| ``qtum_meminfo_chunks_free``          | Number of unused chunks                                                                                                                                 | Gauge   |
| ``qtum_blocks``                       | The current number of blocks processed in the server                                                                                                    | Gauge   |
| ``qtum_size_on_disk``                 | The estimated size of the block and undo files on disk                                                                                                  | Gauge   |
| ``qtum_verification_progress``        | Estimate of verification progress [0..1]                                                                                                                | Gauge   |
| ``qtum_latest_block_size``            | Size of latest block in bytes                                                                                                                           | Gauge   |
| ``qtum_latest_block_txs``             | Number of transactions in latest block                                                                                                                  | Gauge   |
| ``qtum_latest_block_height``          | Height or index of latest block                                                                                                                         | Gauge   |
| ``qtum_latest_block_weight``          | Weight of latest block according to BIP 141                                                                                                             | Gauge   |
| ``qtum_latest_block_inputs``          | Number of inputs in transactions of latest block                                                                                                        | Gauge   |
| ``qtum_latest_block_outputs``         | Number of outputs in transactions of latest block                                                                                                       | Gauge   |
| ``qtum_latest_block_value``           | Qtum value of all transactions in the latest block                                                                                                      | Gauge   |
| ``qtum_latest_block_fee``             | Total fee to process the latest block                                                                                                                   | Gauge   |
| ``qtum_ban_created``                  | Time the ban was created                                                                                                                                | Gauge   |
| ``qtum_banned_until``                 | Time the ban expires                                                                                                                                    | Gauge   |
| ``qtum_server_version``               | The server version                                                                                                                                      | Gauge   |
| ``qtum_protocol_version``             | The protocol version of the server                                                                                                                      | Gauge   |
| ``qtum_connections``                  | The number of connections or peers                                                                                                                      | Gauge   |
| ``qtum_connections_in``               | The number of connections in                                                                                                                            | Gauge   |
| ``qtum_connections_out``              | The number of connections out                                                                                                                           | Gauge   |
| ``qtum_warnings``                     | Number of network or blockchain warnings detected                                                                                                       | Counter |
| `qtum_tx_count`                       | Number of TX since the genesis block                                                                                                                    | Gauge   |
| ``qtum_mempool_bytes``                | Size of mempool in bytes                                                                                                                                | Gauge   |
| ``qtum_mempool_size``                 | Number of unconfirmed transactions in mempool                                                                                                           | Gauge   |
| ``qtum_mempool_usage``                | Total memory usage for the mempool                                                                                                                      | Gauge   |
| ``qtum_mempool_unbroadcast``          | Number of transactions waiting for acknowledgment                                                                                                       | Gauge   |
| ``qtum_num_chain_tips``               | Number of known blockchain branches                                                                                                                     | Gauge   |
| ``qtum_estimate_smart_fee_{nblocks}`` | Estimated smart fee per kilobyte for confirmation in {nblocks} blocks                                                                                   | Gauge   |
| ``qtum_total_bytes_recv``             | Total bytes received                                                                                                                                    | Gauge   |
| ``qtum_total_bytes_sent``             | Total bytes sent                                                                                                                                        | Gauge   |
| ``qtum_uptime``                       | The number of seconds that the server has been running                                                                                                  | Gauge   |
| ``qtum_exporter_errors``              | Number of errors encountered by the exporter                                                                                                            | Counter |
| ``qtum_exporter_process_time``        | Time spent processing metrics from qtum node                                                                                                            | Counter |

## License

Distributed under the [MIT](https://github.com/qtumproject/qtum-exporter/blob/master/LICENSE) license. See ``LICENSE`` for more information.
