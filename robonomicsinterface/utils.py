import hashlib
import logging

import substrateinterface as substrate
import typing as tp

from base58 import b58decode, b58encode
from enum import Enum
from scalecodec.types import GenericCall, GenericExtrinsic
from scalecodec.base import RuntimeConfiguration, ScaleBytes, ScaleType
from substrateinterface.exceptions import ExtrinsicFailedException
from websocket import WebSocketConnectionClosedException

from .constants import REMOTE_WS, TYPE_REGISTRY
from .decorators import connect_close_substrate_node
from .exceptions import NoPrivateKey, DigitalTwinMapError

DatalogTyping = tp.Tuple[int, tp.Union[int, str]]
LiabilityTyping = tp.Dict[str, tp.Union[tp.Dict[str, tp.Union[str, int]], str]]
ReportTyping = tp.Dict[str, tp.Union[int, str, tp.Dict[str, str]]]
NodeTypes = tp.Dict[str, tp.Dict[str, tp.Union[str, tp.Any]]]

logger = logging.getLogger(__name__)


def create_keypair(seed: str) -> substrate.Keypair:
    """
    Create a keypair for further use.

    :param seed: Account seed (mnemonic or raw) as a key to sign transactions.

    :return: A Keypair instance used by substrate to sign transactions.

    """

    if seed.startswith("0x"):
        return substrate.Keypair.create_from_seed(seed_hex=hex(int(seed, 16)), ss58_format=32)
    else:
        return substrate.Keypair.create_from_mnemonic(seed, ss58_format=32)


def dt_encode_topic(topic: str) -> str:
    """
    Encode any string to be accepted by Digital Twin setSource. Use byte encoding and sha256-hashing.

    :param topic: Topic name to be encoded.

    :return: Hashed-encoded topic name

    """

    return f"0x{hashlib.sha256(topic.encode('utf-8')).hexdigest()}"
