[miku]
token = "" # discord token
prefix = "salmon!" # discord command prefix
extinction_messages = [
  "congratz, your fave is an environmental criminal",
  "salmon is now Unstable!",
  "which means they're about as good as Jessica Telephone at this",
]
successful_messages = [
  "**HEY!** turns out, **{name}** isn't half bad at this salmon thing?",
]

[db]
setup_sql = "db/setup.sql" # Database creation SQL
path = "db/yuuko.db"

[salmon]
total_sims = 20 # total simulation cases to run on command
api_url = "https://crisp.sibr.dev/api/sim" # WEBCrisp API url (include endpoint!)
