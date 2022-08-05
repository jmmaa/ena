import os
import dotenv
import logging

import hikari as hk
import lightbulb as lb

from aiocache.plugins import HitMissRatioPlugin
from aiocache.plugins import TimingPlugin

from ena.decors import mount_listeners
from ena.decors import mount_database
from ena.decors import mount_plugins
from ena.decors import mount_cache

from ena.listeners import _on_guild_leave
from ena.listeners import _on_guild_join
from ena.listeners import _load_presence
from ena.listeners import _on_starting


dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)


TOKEN = os.getenv("TOKEN") or "NONE"

DSN = os.getenv("DB_STRING") or "NONE"
SCHEMA = "db/schema.psql"

DEFAULT_GUILDS = (957116703374979093, 938374580244979764)

INTENTS = (
    hk.Intents.ALL_PRIVILEGED
    | hk.Intents.DM_MESSAGE_REACTIONS
    | hk.Intents.GUILD_MESSAGE_REACTIONS
    | hk.Intents.GUILD_MESSAGES
    | hk.Intents.GUILD_MEMBERS
    | hk.Intents.GUILDS
)


cache = mount_cache(
    namespace="enabot:",
    plugins=[
        HitMissRatioPlugin(),
        TimingPlugin(),
    ],
)

extensions = mount_plugins(
    plugins=[
        "plugins.debug",
        "plugins.greet",
        "plugins.react_role",
    ]
)


database = mount_database(
    dsn=DSN,
    schema=SCHEMA,
)


listeners = mount_listeners(
    listeners=[
        _on_guild_leave,
        _on_guild_join,
        _load_presence,
        _on_starting,
    ],
)


@cache
@database
@listeners
@extensions
def build_bot() -> lb.BotApp:

    bot = lb.BotApp(
        token=TOKEN,
        intents=INTENTS,
        default_enabled_guilds=DEFAULT_GUILDS,
    )

    return bot
