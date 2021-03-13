CREATE TABLE IF NOT EXISTS player_cache (
  name TEXT,
  stlats TEXT
);

CREATE TABLE IF NOT EXISTS result_archive (
  player TEXT,
  result BLOB,
  timestamp INTEGER -- this is UTC
);
