# a discord bot for salmon
*by allie ([cat-girl.gay](https://cat-girl.gay) | sapphicfettucine#6248)*

yuuko is built using
* the [CRiSP Harvest Chinook Salmon Harvesting Model](http://www.cbr.washington.edu/analysis/archive/harvest/crispharvest),
* [SIBR's salmon_lib](https://github.com/Society-for-Internet-Blaseball-Research/salmon_lib), and
* [Onomancer](https://onomancer.sibr.dev).


## Installing

### make your own discord bot
- follow [these instructions](https://discordpy.readthedocs.io/en/latest/discord.html) to make a new bot
- copy your application's id
- go to https://discord.com/oauth2/authorize?scope=bot&permissions=117824&client_id=YOUR_APPLICATION_CLIENT_ID
  - replace `YOUR_APPLICATION_CLIENT_ID` with your application's id

### how to run it
- `pip install -r requirements.txt`
- copy yuuko.toml.ex to yuuko.toml
- get the auth token for your bot and set that in yuuko.toml
- `token = 'YOURBOTTOKENHERE'`
- then simply run `python yuuko/yuuko.py`
