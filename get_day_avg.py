import requests
import psycopg2
import os

def get_avg(date):
  conn = psycopg2.connect(
    dbname = os.getenv('POSTGRES_DB'),
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    host = os.getenv('POSTGRES_HOST'),
    port = 5432
  )
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

  cur.close()
  conn.close()

  gage_avg = gage_sum / total_time_events
  discharge_avg = discharge_sum / total_time_events
  disolved_avg = disolved_sum / total_time_events
  ph_avg = ph_sum / total_time_events
  temp_avg = temp_sum / total_time_events
  
  print(f"date: {date}")
  print(f"{round(gage_avg, 2)} {round(discharge_avg, 2)} {round(disolved_avg, 2)} {round(ph_avg, 2)} {round(temp_avg, 2)}")

if __name__ == "__main__":
  date = '2024-3-2' # 2024-2-13 had NONE values
  get_avg(date)
