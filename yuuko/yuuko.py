from discord.ext import commands
import logging
import toml
import typing
import discord

logging.basicConfig(level=logging.DEBUG)

config = {}
with open("yuuko.toml") as f:
    config = toml.load(f)

bot = commands.Bot(command_prefix=config["miku"].get("prefix", "$"))
bot.config = config
bot.remove_command("help")


@bot.listen("on_ready")
async def load_dbs():
    await bot.get_cog("SalmonCog").load_db()


@bot.command()
async def help(ctx, *, command: typing.Optional[str]):
    h = f"""
🐟 |        **{ctx.prefix}fish** [player name]

    """

    about = """
    *Yuuko is built using the [CRiSP Harvest Chinook Salmon Harvesting Model](http://www.cbr.washington.edu/analysis/archive/harvest/crispharvest),*
    *[SIBR's salmon_lib](https://github.com/Society-for-Internet-Blaseball-Research/salmon_lib), and [Onomancer](https://onomancer.sibr.dev)*
    *by allie ([cat-girl.gay](https://cat-girl.gay) | sapphicfettucine#6248)*
    """

    embed = discord.Embed(title="**salmon help**", description=h + about)
    await ctx.send(embed=embed)


bot.load_extension("clockwork.salmon")
bot.run(config["miku"]["token"])
