from salmon_lib import *
from discord.ext import commands
from datetime import datetime, timezone
import numpy as np
import json, math, random, typing, lzma, asyncio
import aiosqlite, aiohttp, discord

class SalmonCog(commands.Cog):
    def __init__(self, config):
        self.config = config
        self.db = None

    @commands.command()
    async def fish(self, ctx, *, name: typing.Optional[str]):
        if not name:
            await ctx.send("please specify a name ):")
            return

        if name.lower() in ["steve", "steve!", "salmon steve"]:
            await ctx.send("steve!", file=discord.File("yuuko/steve.png"))
            return

        res = f"alright! running {self.config['salmon']['total_sims']} possible salmon cases..."
        m = await ctx.send(res)

        player = await self.load_player(name)
        results = await self.run_n_sims(player, self.config["salmon"]["total_sims"])
        year_by_year = results["year-by-year"]

        res += "\n" + ("-" * len(res)) + "\n"
        res += (
            f"in __{results['extinction_percent']:.2f}%__ of cases, **{name}** caused an extinction of all salmon"
            + "\n"
        )
        if results["extinction_percent"] == 100:
            res += random.choice(self.config["miku"]["extinction_messages"]).format(name=name)
        elif year_by_year < 0:
            res += f"the average year-by-year decrease in salmon stocks run by **{name}** was __{year_by_year:.2f}%__"
        elif math.isnan(year_by_year):
            res += f"i couldn't calculate the average year-by-year decrease in salmon stocks run by **{name}**. this is a cryptic and worrying situation."
        else:
            res += f"the average year-by-year _increase_ in salmon stocks run by **{name}** was __{year_by_year:.2f}%__" + "\n"
            res += random.choice(self.config["miku"]["successful_messages"]).format(name=name) + "\n"

        await m.edit(content=res)

    async def load_db(self):
        config = self.config["db"]
        self.db = await aiosqlite.connect(config["path"])
        with open(config["setup_sql"]) as sql_file:
            await self.db.executescript(sql_file.read())
        self.db.row_factory = aiosqlite.Row

    async def close_db(self):
        await self.db.close()

    async def archive_result(self,player,results):
        results_compressed = lzma.compress(results.encode("utf-8"),preset=lzma.PRESET_EXTREME)
        time = int(datetime.now(tz=timezone.utc).timestamp())
        await self.db.execute(
            "INSERT INTO result_archive (player,result,timestamp) VALUES (?,?,?)",
            [player['name'],results_compressed,time]
        )
        await self.db.commit()

    async def load_player(self, name):
        cursor = await self.db.execute(
            "SELECT * FROM  player_cache WHERE name = ?", [name]
        )
        player = await cursor.fetchone()
        if player:
            return json.loads(player["stlats"])
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://onomancer.sibr.dev/api/getOrGenerateStats",params={"name": name}) as response:
                    player_json = await response.json()
                    player_json['name'] = name
                    await self.db.execute(
                        "INSERT INTO player_cache (name,stlats) VALUES (?,?)",
                        [name, json.dumps(player_json)],
                    )
                    await self.db.commit()
                    print(player_json)
                    return player_json

    async def run_sim(self, player, session):
        rng = np.random.default_rng()
        mu, sigma = -0.6343, 1.0916
        # ORC cohorts: 522 290.5, 244 745.98, 120 525.05, 33 205.477
        baseCohorts = (
            (player["buoyancy"] / 2) + (player["pressurization"] / 2)
        ) * 10 ** 6  # age 2
        coh_three = baseCohorts / (rng.random() + 1)  # age 3
        coh_four = baseCohorts / (rng.random() + 3)  # age 4
        coh_five = baseCohorts / (rng.random() + 15)  # age 5

        # ORC mat rates:
        # 0.24387254  0.17917444  0.48070830  0.99999994 # ages 2, 3, 4, 5
        # these vary a lot, but the overall trend is age 2 and 3 usually in the 0.1 to 0.3 range (with some big exceptions), age 4 a bit higher, age 5 0.99 or 1
        # this is clownery, but i'm not math
        mat_two = player["chasiness"] / rng.random()
        mat_three = player["chasiness"] * rng.random() + 0.2
        mat_four = player["chasiness"] * (rng.random() + 2)
        mat_five = 0.99999999

        # ORC adult equiv:
        # 0.66822225E+00  0.80173504E+00  0.94807076E+00  0.99999994E+00
        adult_two = rng.lognormal(-player["indulgence"], 0.2)
        adult_three = rng.lognormal(-player["indulgence"] + 0.1, 0.2)
        adult_four = rng.lognormal(-player["indulgence"] + 0.3, 0.2)
        adult_five = 0.99999999

        # ORC exploit:
        # 0.46587971E+00  0.60243016E+00  0.19951671E+00  0.19620371E+00
        # this varies a ton by fishery so
        explt_two = rng.lognormal(-player["anticapitalism"], 0.4)
        explt_three = rng.lognormal(-player["anticapitalism"], 0.4)
        explt_four = rng.lognormal(-player["anticapitalism"], 0.4)
        explt_five = rng.lognormal(-player["anticapitalism"], 0.4)

        policy = 1.0
        param = rng.lognormal(-player["moxie"] + 1.6, 0.3)
        age_factor = rng.lognormal(-player["divinity"] + 1.6, 0.3)

        msy_esc = player["baseThirst"] * 10 ** 4
        ev_scalars = list(rng.lognormal(-player["indulgence"], sigma, 39))
        # print(ev_scalars)

        stock_config = {
            "name": "Salmon Institute T",
            "abbreviation": "SIBR",
            "hatchery_n": "Where the Salmon Are",
            "cohort_abundance": [baseCohorts, coh_three, coh_four, coh_five],
            "maturation_rate": [mat_two, mat_three, mat_four, mat_five],
            "adult_equivalent": [adult_two, adult_three, adult_four, adult_five],
            "maturation_by_year": [
                [(mat_two, adult_two), (mat_three, adult_three), (mat_four, adult_four)]
                for x in range(0, 39)
            ],
            "ev_scalars": ev_scalars,
            "log_p": ["Log", "Normal", "Indep", "-0.6343", "1.0916", "911"],
            "hatchery_flag": True,
            "msy_esc": 7000,
            "msh_flag": True,
            "idl": 1.0,
            "param": param,
            "age_factor": age_factor,
        }

        fishery_config = {
            "name": "Fishy T",
            "proportions": [
                rng.lognormal(-(player["watchfulness"] * 2), 0.3),
                rng.lognormal(-(player["watchfulness"] * 2), 0.3),
                rng.lognormal(-((player["watchfulness"] * 2) ** -5), 0.3),
                rng.lognormal(-((player["watchfulness"] * 2) ** -5), 0.3),
            ],
            "ocean_net": False,
            "exploitations": [
                ("SIBR", [explt_two, explt_three, explt_four, explt_five])
            ]
            * 39,
            "policy": [policy] * 39,
            "terminal": True,
        }

        sim = Sim()
        stock = Stock(sim, config=stock_config)
        fishery = Fishery(sim, config=fishery_config)
        stock.build()
        fishery.build()
        payload = json.dumps(sim.to_sibr_conf())

        async with session.post(
            self.config["salmon"]["api_url"],
            data=payload,
            headers={"content-type": "application/json"},
        ) as resp:
            results_s = await resp.text()

            if self.config["db"]["archive_results"]:
                await self.archive_result(player,results_s)

            results = json.loads(results_s)

            abds = np.array([int(r) for y, r in results["abundances"]["Fishy T"]])
            diff = abds[1:] - abds[:-1]
            changes = diff / abds[1:] * 100

            results = {
                "extinction": False,
                "averages": None,
                "abundance_decreases": None,
            }

            if abds[-1] < 1:
                results["extinction"] = True
            else:
                avg = np.average(changes)
                if not math.isnan(avg) and avg != float("inf") and avg != float("-inf"):
                    results["averages"] = np.average(changes)
                results["abundance_decreases"] = changes

            return results

    async def run_n_sims(self, player, n):
        session = aiohttp.ClientSession()

        tasks = [self.run_sim(player, session) for x in range(0, n)]

        extinctions = 0
        abundance_decreases = []
        averages = []

        for res in asyncio.as_completed(tasks):
            res = await res
            extinctions += int(res["extinction"])
            if res["averages"]:
                averages.append(res["averages"])

            abundance_decreases.append(res["abundance_decreases"])

        await session.close()
        return {
            "extinction_percent": (extinctions / n) * 100,
            "year-by-year": np.average(averages),
        }


def setup(bot):
    bot.add_cog(SalmonCog(bot.config))


def teardown(bot):
    asyncio.create_task(bot.get_cog("SalmonCog").close_db())
