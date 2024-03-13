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

  date = '2024-2-29' # 2024-2-13 had NONE values
  cur = conn.cursor()
  cur.execute(f"SELECT gage_val, discharge_val, disolved_val, ph_val, temp_val FROM river_data WHERE val_date = \'{date}\'")
  
  date_values = cur.fetchall()
  total_time_events = len(date_values)

  gage_sum = 0
  discharge_sum = 0
  disolved_sum = 0
  ph_sum = 0
  temp_sum = 0

  for time_event in date_values:
    # print(f"{time_event[0]} {time_event[1]} {time_event[2]} {time_event[3]} {time_event[4]}")
    
    gage_sum += time_event[0]
    discharge_sum += time_event[1]
    disolved_sum += time_event[2]
    ph_sum += time_event[3]
    temp_sum += time_event[4]

  print(f"{gage_sum / total_time_events} {discharge_sum / total_time_events} \
        {disolved_sum / total_time_events} {ph_sum / total_time_events} {temp_sum / total_time_events}")

  # cur.execute(f"SELECT * FROM river_data WHERE gage_val = NULL OR discharge_val = NULL OR disolved_val = NULL OR ph_val = NULL OR temp_val = NULL")
  # rows = cur.fetchall()
  # for row in rows:
  #   print(row)




  cur.close()
  conn.close()
