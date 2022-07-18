# flake8: noqa
from .plugin import plugin
from .models import *


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)