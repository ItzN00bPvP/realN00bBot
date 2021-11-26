import json
import time
import re
import requests
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from config import config
from config.config import cloudflare_header, cloudflare_procrastinatingathomezoneid


class procrastinating(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(guild_ids=config.slash_procrastinating, name="procrastinating", description="Makes a procrastinating domain for a User.", options=[
        create_option(
            name="name",
            description="The user who is procrastinating.",
            option_type=3,
            required=True,
        ), create_option(
            name="verb",
            description="is / are / am",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="is",
                    value="is"
                ),
                create_choice(
                    name="are",
                    value="are"
                ),
                create_choice(
                    name="am",
                    value="am"
                )
            ]
        )])
    async def _bald(self, ctx: SlashContext, name: str, verb: str):
        if not re.compile("^[A-Za-z0-9](?:[A-Za-z0-9\-]{0,58}[A-Za-z0-9])?$").match(name):
            await ctx.send("Invalid Name!")
            return

        body = {"type": "CNAME", "name": f"{name}-{verb}", "content": "proxy.mcatho.me", "ttl": 1, "proxied": True}
        req = requests.post(f"https://api.cloudflare.com/client/v4/zones/{cloudflare_procrastinatingathomezoneid}/dns_records",
                            headers=cloudflare_header, data=json.JSONEncoder().encode(body))

        if req.json()['result'] is None and req.json()['errors'][0]['code'] == 81053:
            await ctx.send(content=f"https://{name}-{verb}.procrastinatingathome.com/")
            return

        m = await ctx.send("3")
        time.sleep(1)
        await m.edit(content=f"2")
        time.sleep(1)
        await m.edit(content=f"1")
        time.sleep(1)
        await m.edit(content=f"https://{name}-{verb}.procrastinatingathome.com/")



def setup(bot):
    bot.add_cog(procrastinating(bot))
