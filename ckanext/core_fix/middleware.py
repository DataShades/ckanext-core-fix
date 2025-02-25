from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypeVar, Union, cast

import msgspec
from flask_session.redis import RedisSessionInterface
from markupsafe import Markup


# Create a recursive type for the decoded values
T = TypeVar("T")
DecodedValue = Union[
    Markup,
    datetime,
    dict[str, "DecodedValue"],
    list["DecodedValue"],
    tuple["DecodedValue", ...],
    T,
]


@dataclass
class MarkupWrapper:
    content: str
    type: str = "__markup__"


@dataclass
class DatetimeWrapper:
    content: str
    type: str = "__datetime__"


class MsgspecSerializer:
    """Serializer using msgspec"""

    def __init__(self):
        self.encoder = msgspec.msgpack.Encoder()
        self.decoder = msgspec.msgpack.Decoder()

    def encode(self, obj: dict[str, Any]) -> bytes:
        def convert(o):
            if isinstance(o, Markup):
                return MarkupWrapper(str(o)).__dict__

            if isinstance(o, datetime):
                return DatetimeWrapper(o.isoformat()).__dict__

            if isinstance(o, dict):
                return {k: convert(v) for k, v in o.items()}

            if isinstance(o, (list, tuple)):
                return [convert(i) for i in o]
            return o

        converted_obj = convert(obj)
        return self.encoder.encode(converted_obj)
    
    def decode(self, data: bytes) -> dict[str, DecodedValue]:
        def convert_back(obj) -> DecodedValue:
            if isinstance(obj, dict):
                if obj.get("type") == "__markup__":
                    return Markup(obj["content"])
                if obj.get("type") == "__datetime__":
                    return datetime.fromisoformat(obj["content"])
                return {k: convert_back(v) for k, v in obj.items()}

            if isinstance(obj, (list, tuple)):
                return [convert_back(i) for i in obj]

            return obj

        decoded = self.decoder.decode(data)
        return cast(dict[str, DecodedValue], convert_back(decoded))


class OEHRedisSessionInterface(RedisSessionInterface):
    """Custom Redis session interface that handles Markup and datetime objects.
    Overrides default Flask-Session Redis interface to fix serialization errors
    with Markup objects (flash messages).
    """

    def __init__(self, app):
        """Initialize with custom msgspec serializer for handling special types."""
        super().__init__(
            app,
            app.config["SESSION_REDIS"],
            app.config["SESSION_KEY_PREFIX"],
            app.config["SESSION_USE_SIGNER"],
            app.config["SESSION_PERMANENT"],
            serialization_format="msgpack",
        )
        # Override the serializer with our custom implementation
        self.serializer = MsgspecSerializer()
