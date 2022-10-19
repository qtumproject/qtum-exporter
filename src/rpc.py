#!/usr/bin/env python3

from types import TracebackType
from httpx import (
    Client, Timeout
)
from logging import (
    Logger, Formatter, StreamHandler
)
from typing import (
    Any, List, Optional, Type, Union
)

import logging
import itertools
import json

from .config import Config

logger: Logger = logging.getLogger("qtum-exporter-rpc")
logger.setLevel(level=Config.LOGGING_LEVEL)
formatter: Formatter = logging.Formatter(
    fmt="%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
stream_handler: StreamHandler = logging.StreamHandler()
stream_handler.setFormatter(fmt=formatter)
logger.addHandler(stream_handler)

# Helper to generate new rpc ids
# This uses itertools.count() instead of a "+= 1" operation because the latter
# is not thread safe. See bpo-11866 for a longer explanation.
_next_rpc_id = itertools.count(1).__next__


class RPCError(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code: int = code
        self.message: str = message


class RPC:
    __slots__ = (
        "_url", "_client", "_logger"
    )

    def __init__(
        self, url: str, rpc_user: str, rpc_password: str, **kwargs: Any
    ) -> None:
        self._url = url
        self._client = self._configure_client(rpc_user, rpc_password, **kwargs)

    def __enter__(self) -> "RPC":
        return self

    def __exit__(
        self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType
    ) -> None:
        self.close()

    @staticmethod
    def _configure_client(
        rpc_user: str, rpc_password: str, **kwargs: Any
    ) -> Client:

        auth: tuple = (rpc_user, rpc_password)
        headers: dict = {
            "content-type": "application/json"
        }

        if not kwargs:
            return Client(auth=auth, headers=headers)

        if "auth" in kwargs:
            del kwargs["auth"]

        if "headers" in kwargs:
            _additional_headers = dict(kwargs.pop("headers"))
            headers.update(_additional_headers)
            # guard against content-type overwrite
            headers["content-type"] = "application/json"

        return Client(auth=auth, headers=headers, **kwargs)

    @property
    def url(self) -> str:
        return self._url

    @property
    def client(self) -> Client:
        return self._client

    @property
    def logger(self) -> Logger:
        return self._logger

    def close(self) -> None:
        self.client.close()

    def call(
        self, method: str, params: List[Union[str, int, List[str], None]], **kwargs: Any
    ) -> Union[dict, int, float, str, list]:
        logger.debug(f"Call: Method '{method}' | Params '{params}'")
        request: Any = self.client.post(
            url=self.url,
            content=json.dumps({
                "jsonrpc": "1.0", "id": _next_rpc_id(), "method": method, "params": params
            }), **kwargs
        )
        response: dict = json.loads(
            request.content
        )

        if response["error"] is not None:
            raise RPCError(
                code=response["error"]["code"], message=response["error"]["message"]
            )
        logger.debug(f"Result: {response}")
        return response["result"]

    def get_memory_info(self) -> dict:
        return self.call("getmemoryinfo", [])

    def get_mempool_info(self) -> dict:
        return self.call("getmempoolinfo", [])

    def get_mining_info(self) -> dict:
        return self.call("getmininginfo", [])

    def get_network_info(self) -> dict:
        return self.call("getnetworkinfo", [])

    def get_blockchain_info(self) -> dict:
        return self.call("getblockchaininfo", [])

    def get_connection_count(self) -> dict:
        return self.call("getconnectioncount", [])

    def get_chain_tx_stats(self) -> dict:
        return self.call("getchaintxstats", [])

    def get_chain_tips(self) -> list:
        return self.call("getchaintips", [])

    def get_difficulty(self) -> dict:
        return self.call("getdifficulty", [])

    def get_best_block_hash(self) -> dict:
        return self.call("getbestblockhash", [])

    def get_block_hash(self, height: int) -> dict:
        return self.call("getblockhash", [height])

    def get_block_count(self) -> dict:
        return self.call("getblockcount", [])

    def get_block_header(
            self, block_hash: str, verbose: bool = True
    ) -> dict:
        return self.call(
            "getblockheader", [block_hash, verbose]
        )

    def get_block_stats(
        self, hash_or_height: Union[int, str], *keys: str, timeout: Optional[float] = Config.TIMEOUT
    ) -> dict:
        return self.call(
            "getblockstats", [hash_or_height, list(keys) or None], timeout=Timeout(timeout)
        )

    def get_network_totals(self) -> dict:
        return self.call("getnettotals", [])

    def list_banned(self) -> list:
        return self.call("listbanned", [])

    def get_block(
        self, block_hash: str, verbosity: int = 1, timeout: Optional[float] = Config.TIMEOUT
    ) -> dict:
        return self.call(
            "getblock", [block_hash, verbosity], timeout=Timeout(timeout)
        )

    def estimate_smart_fee(
        self, num_blocks: int, timeout: Optional[float] = Config.TIMEOUT
    ) -> dict:
        return self.call(
            "estimatesmartfee", [num_blocks], timeout=Timeout(timeout)
        )

    def get_raw_transaction(
        self, txid: str, verbose: bool = True, block_hash: Optional[str] = None, timeout: Optional[float] = Config.TIMEOUT
    ) -> dict:
        return self.call(
            "getrawtransaction", [txid, verbose, block_hash], timeout=Timeout(timeout)
        )

    def get_network_hash_ps(
        self, num_blocks: int = -1, height: Optional[int] = None, timeout: Optional[float] = Config.TIMEOUT
    ) -> int:
        return self.call(
            "getnetworkhashps", [num_blocks, height], timeout=Timeout(timeout)
        )

    def get_uptime(self) -> int:
        return self.call("uptime", [])
