from discord.ext import commands
import logging, typing
import toml, discord

logging.basicConfig(level=logging.DEBUG)

# [coin voice] HelpCog is a mess
# this should be an implementation of HelpCommand, not a cog,
# but this is a rush fix!
class HelpCog(commands.Cog):
    @commands.command()
    async def help(self,ctx, *, command: typing.Optional[str]):
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

class Yuuko(commands.Bot):
    def __init__(self,**kwargs):
        with open("yuuko.toml") as f:
            self.config = toml.load(f)

        super().__init__(command_prefix=self.config["miku"].get("prefix", "$"),help_command=None)
        self.load_extension('clockwork.salmon')
        self.add_cog(HelpCog())

    async def on_ready(self):
        await self.get_cog('SalmonCog').load_db()

    async def close(self):
        await self.get_cog('SalmonCog').close_db()
        await super().close()

bot = Yuuko()
bot.run(bot.config['miku']['token'])
