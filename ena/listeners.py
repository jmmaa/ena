import hikari as hk
import lightbulb as lb

import logging

from ena.database import EnaDatabase


logging = logging.getLogger(__name__)  # type:ignore


def _load_presence(bot: lb.BotApp):
    async def load_presence(_: hk.StartedEvent):

        await bot.update_presence(
            status=hk.Status.ONLINE,
            activity=hk.Activity(
                name="/help",
                type=hk.ActivityType.LISTENING,
            ),
        )

    return hk.StartedEvent, load_presence


def _on_starting(bot: lb.BotApp):
    async def on_starting(_: hk.StartingEvent):

        logging.info("initializing...")
        database: EnaDatabase = bot.d.ENA_DATABASE

        await database.connect()
        await database.create_schema()
        await database.insert_default_guild_ids(bot.default_enabled_guilds)

        logging.info("done initializing")

    return hk.StartingEvent, on_starting


def _on_guild_join(bot: lb.BotApp):
    async def on_guild_join(event: hk.GuildJoinEvent):
        database: EnaDatabase = bot.d.ENA_DATABASE

        guild_id = event.guild_id
        await database.execute("INSERT INTO guilds VALUES ($1)", guild_id)
        logging.info("added guild '{}'".format(guild_id))

    return hk.GuildJoinEvent, on_guild_join


def _on_guild_leave(bot: lb.BotApp):
    async def on_guild_leave(event: hk.GuildLeaveEvent):
        database: EnaDatabase = bot.d.ENA_DATABASE
        guild_id = event.guild_id

        await database.execute("DELETE FROM guilds WHERE id = $1", guild_id)
        logging.info("removed guild '{}'".format(guild_id))

    return hk.GuildLeaveEvent, on_guild_leave
