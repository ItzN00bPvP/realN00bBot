from discord.ext import commands


class ping(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(name="ping", )
    async def COMMAND(self, ctx: commands.Context):
        await ctx.send("PONG!")

def setup(bot: commands.Bot):
    bot.add_cog(ping(bot))