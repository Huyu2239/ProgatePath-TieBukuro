import discord
from discord.ext import commands

from mylib import database
from mylib.constant import EXTENTIONS, PREFIX, TOKEN


class TieBukuro(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=discord.Intents.all(),
        )
        self.help_command = None
        self.room_owner_dict = {}

    async def setup_hook(self):
        await database.init_db()
        await self.load_extension("jishaku")
        for extention in EXTENTIONS:
            await self.load_extension(extention)
        await self.tree.sync()


if __name__ == "__main__":
    bot = TieBukuro()
    bot.run(token=TOKEN)
