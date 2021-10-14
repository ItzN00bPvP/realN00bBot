from discord.ext import commands
from discord_slash import SlashCommand

from config.config import bottoken

# command prefix isn't really needed because there a no normal commands
bot = commands.Bot(command_prefix="!!")
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


async def notauthorized(ctx):
    await ctx.send("You're not authorized!\ncc: <@374245848659263488>")
    return


@bot.event
async def on_ready():
    print("Bot running: " + str(bot.user))


def load_cogs(bot, cogs: list):
    for cog in cogs:
        bot.load_extension(cog)
    print("loaded cogs: " + str(cogs))


load_cogs(bot,
          [
              "cogs.admin",
              "cogs.microboinc",
              "cogs.i2s",
              "cogs.fix",
              "cogs.ping",
              "cogs.mcperms"
          ])
bot.run(bottoken)
