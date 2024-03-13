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

  cur.execute(
    'CREATE TABLE river_data ( \
    val_date DATE, val_time TIME, PRIMARY KEY (val_date, val_time), \
    gage_val DECIMAL(3, 2), \
    discharge_val INTEGER, \
    disolved_val DECIMAL(3, 1), \
    ph_val DECIMAL(2, 1), \
    temp_val DECIMAL(2, 1) \
    )'
  )

  # cur.execute('INSERT INTO river_data (val_date, val_time) VALUES (\'2024-01-01\', \'10:10:10\')')

  # cur.execute("SELECT * FROM river_data")
  # rows = cur.fetchall()
  # for row in rows:
  #     print(row)

  conn.commit()
  cur.close()
  conn.close()

