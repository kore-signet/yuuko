[miku]
token = "" # discord token
prefix = "salmon!" # discord command prefix
extinction_messages = [
  "congratz, your fave is an environmental criminal",
  "salmon is now Unstable!",
  "which means they're about as good Jessica Telephone at this",
]

[db]
setup_sql = "db/setup.sql" # Database creation SQL
path = "db/yuuko.db"
archive_results = false # whether to archive full CRiSP results for players or not

[salmon]
total_sims = 20 # total simulation cases to run on command
api_url = "https://crisp.sibr.dev/api/sim" # WEBCrisp API url (include endpoint!)
