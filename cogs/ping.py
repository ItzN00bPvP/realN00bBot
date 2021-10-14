from discord.ext import commands

from config import config


class ping(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(guild_ids=config.slash_ping, name="ping")
    async def _ping(self, ctx: commands.Context):
        await ctx.send("PONG!")


def setup(bot: commands.Bot):
    bot.add_cog(ping(bot))
