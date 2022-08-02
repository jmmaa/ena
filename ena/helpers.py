from dataclasses import dataclass
import typing as t
import re
import hashlib


T = t.TypeVar("T")
DISCORD_MESSAGE_BASE_URL = "https://discord.com/channels"

NUMBER_REGEX = re.compile("([0-9]+)")


@dataclass
class MessageData:
    message_id: int
    channel_id: int
    guild_id: int


def create_hash(*args) -> str:
    raw = "".join([str(arg) for arg in args])
    hash = hashlib.md5(raw.encode()).hexdigest()

    return hash


def create_cache_key(*args) -> str:

    key = ":".join([f"{arg}" for arg in args])
    return key


def create_emoji_code(emoji_id: int, emoji_name: str, is_animated: bool):

    if is_animated:
        emoji = f"<a:{emoji_name}:{emoji_id}>"

    else:
        emoji = f"<:{emoji_name}:{emoji_id}>"

    return emoji


def create_message_link(guild_id: int, channel_id: int, message_id: int):
    return f"{DISCORD_MESSAGE_BASE_URL}/{guild_id}/{channel_id}/{message_id}"


def parse_message_from_link(message_link: str) -> MessageData:
    ids = NUMBER_REGEX.findall(message_link)
    guild_id = int(ids[0])
    channel_id = int(ids[1])
    message_id = int(ids[2])

    return MessageData(message_id, channel_id, guild_id)


def serialize(serializer: t.Type[T], **kwargs) -> T:
    data = serializer(**kwargs)
    return data