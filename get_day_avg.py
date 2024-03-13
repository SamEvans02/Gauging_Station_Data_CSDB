import requests
import psycopg2
import os

if __name__ == "__main__":
  conn = psycopg2.connect(
    dbname = os.getenv('POSTGRES_DB'),
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    host = os.getenv('POSTGRES_HOST'),
    port = 5432
  )
  cur = conn.cursor()
  cur.execute("SELECT * FROM river_data")
  rows = cur.fetchall()
  for row in rows:
    print(row)

  cur.close()
  conn.close()
