import duckdb

conn = duckdb.connect('data/paper_data.duckdb')

tables = conn.execute("SHOW TABLES").fetchall()
print("Tables found:")
for t in tables:
    print(f"- {t[0]}")

conn.close()
