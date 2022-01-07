import re
import requests

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from config.config import roleslevel
from config import config


class recreationserver(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(guild_ids=config.slash_recreation_create, base="recreationserver", name="create", options=[
        create_option(
            name="project",
            description="The Name of the project / server.",
            option_type=3,
            required=True
        )
    ])
    @commands.has_any_role(*roleslevel.ppa)
    async def _create(self, ctx: SlashContext, project: str):
        if not re.compile("^[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?$").match(project):
            await ctx.send("Invalid Name!")
            return
        req = requests.request("POST", f"https://api.mcathome.dev/recreationserver/create/{project}/",
                               headers={'auth': config.apimcathomedev_authtoken})
        if req.status_code != 200:
            await ctx.send(f"Something went wrong status: {req.status_code}")
        respjson = req.json()
        address = respjson["address"]
        await ctx.send(f"Server {project} created.\nServeraddress:```{address}```")


def setup(bot):
    bot.add_cog(recreationserver(bot))
