import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from config.config import roleslevel
from config import config
from utils import mcpermsapi


class mcperms(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(guild_ids=config.slash_mcperms_grant, base="mcperms", name="grant", options=[
        create_option(
            name="server",
            description="The server were the users should get the Permission(GLOBAL for all Servers).",
            option_type=3,
            required=True
        ), create_option(
            name="permission",
            description="The permission the user should recive",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                    name="builder",
                    value="builder"
                ),
                create_choice(
                    name="builder+",
                    value="builder+"
                ),
                create_choice(
                    name="private",
                    value="private"
                )
            ]
        ), create_option(
            name="mcname",
            description="The ign of the user e.g. N00bBot.",
            option_type=3,
            required=True

        ),
        create_option(
            name="discorduser",
            description="The discord user.",
            option_type=6,
            required=True
        )
    ])
    @commands.has_any_role(*roleslevel.ppa)
    async def _grant(self, ctx: SlashContext, server: str, permission: str, mcname: str, discorduser: discord.User):
        suc, res = mcpermsapi.grantperms(server, permission, mcname, discorduser.id)
        if suc:
            await ctx.send(f"{res['permission']} granted to {discorduser.mention} for {res['mcname']} ({res['uuid']}) on {res['server']}")
            return
        await ctx.send(res)


def setup(bot):
    bot.add_cog(mcperms(bot))
