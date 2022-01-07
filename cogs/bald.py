import json
import time
import re
import requests
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from config import config
from config.config import cloudflare_header, cloudflare_isbaldzoneid


class bald(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(guild_ids=config.slash_bald, name="bald", description="Makes some one bald.", options=[
        create_option(
            name="name",
            description="The you want to make bald.",
            option_type=3,
            required=True,
        )])
    async def _bald(self, ctx: SlashContext, name: str):
        if not re.compile("^[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?$").match(name):
            await ctx.send("Invalid Name!")
            return

        body = {"type": "CNAME", "name": name, "content": "proxy.mcatho.me", "ttl": 1, "proxied": True}
        req = requests.post(f"https://api.cloudflare.com/client/v4/zones/{cloudflare_isbaldzoneid}/dns_records",
                            headers=cloudflare_header, data=json.JSONEncoder().encode(body))

        if req.json()['result'] is None and  req.json()['errors'][0]['code'] == 81053:
            await ctx.send(content=f"https://{name}.isbald.com/")
            return

        m = await ctx.send("3")
        time.sleep(1)
        await m.edit(content=f"2")
        time.sleep(1)
        await m.edit(content=f"1")
        time.sleep(1)
        await m.edit(content=f"https://{name}.isbald.com/")



def setup(bot):
    bot.add_cog(bald(bot))
