import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from utils import mattapi


class Microboinc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="microboinc", name="createapikey", options=[
        create_option(
            name="nickname",
            description="The nickname for microboinc!",
            option_type=3,
            required=True
        ),
        create_option(
            name="user",
            description="Only needed if you want to create an API-Key for some one else!",
            option_type=6,
            required=False
        )
    ])
    async def _microboinc_createapikay(self, ctx: SlashContext, nickname: str, user: discord.Member = None):
        apifor = ctx.author
        if user is not None:
            # check if user has api 2+
            await ctx.send("Not implemented yet!")
            apifor = user
            return

        success, res = mattapi.register(nickname, apifor.id)
        if not success:
            await ctx.send("Something went wrong:\n" + res)
            return

        apikey = res
        try:
            await apifor.send(content=f"Microboinc account created:\nNickname: {nickname}\nAPI-Key: {apikey}")
            await ctx.send(content=f"API for {nickname}({apifor.mention}) created and send to their DMs.")
        except discord.Forbidden:
            await ctx.send(hidden=True, content=f"!Coun't send API-Key to DMS!\n"
                                                f"!THIS MESSAGE IS ONLY VISIBLE TO YOU!\n"
                                                f"Microboinc account created for {apifor.mention}:\n"
                                                f"Nickname: {nickname}\n"
                                                f"API-Key: {apikey}")


def setup(bot):
    bot.add_cog(Microboinc(bot))
