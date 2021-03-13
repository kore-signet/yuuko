# a discord bot for salmon
*by allie ([cat-girl.gay](https://cat-girl.gay) | sapphicfettucine#6248)*

Yuuko is built using
* the [CRiSP Harvest Chinook Salmon Harvesting Model](http://www.cbr.washington.edu/analysis/archive/harvest/crispharvest),
* [SIBR's salmon_lib](https://github.com/Society-for-Internet-Blaseball-Research/salmon_lib), and
* [Onomancer](https://onomancer.sibr.dev).


## Installing

### Make your own Discord bot
* Follow [these instructions](https://discordpy.readthedocs.io/en/latest/discord.html) to make a new bot
* Copy your application's ID
* Go to https://discord.com/oauth2/authorize?scope=bot&permissions=117824&client_id=YOUR_APPLICATION_CLIENT_ID
  * Replace `YOUR_APPLICATION_CLIENT_ID` with your application's ID

### Set up the local repo
```
cd ./yuuko
pip3 install -r requirements.txt
cp yuuko.toml{.ex,}
nano yuuko.toml
# Paste in your bot's token into yuuko.toml, under [miku] > token
```

### Run the bot locally
```
python3 yuuko/yuuko.py
```
