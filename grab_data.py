import requests
import psycopg2
import os

if __name__ == "__main__":
  # JSON format urls
  gage_url = "https://waterservices.usgs.gov/nwis/iv/?sites=09163500&agencyCd=USGS&parameterCd=00065&period=P30D&siteStatus=all&format=json"
  discharge_url = "https://waterservices.usgs.gov/nwis/iv/?sites=09163500&agencyCd=USGS&parameterCd=00060&period=P30D&siteStatus=all&format=json"
  disolved_url = "https://waterservices.usgs.gov/nwis/iv/?sites=09163500&agencyCd=USGS&parameterCd=00300&period=P30D&siteStatus=all&format=json"
  ph_url = "https://waterservices.usgs.gov/nwis/iv/?sites=09163500&agencyCd=USGS&parameterCd=00400&period=P30D&siteStatus=all&format=json"
  temp_url = "https://waterservices.usgs.gov/nwis/iv/?sites=09163500&agencyCd=USGS&parameterCd=00010&period=P30D&siteStatus=all&format=json"
  
  url_list = [gage_url, discharge_url, disolved_url, ph_url, temp_url]
  column_names = [
    "gage_val",
    "discharge_val",
    "disolved_val",
    "ph_val",
    "temp_val"
    ]

  conn = psycopg2.connect(
    dbname = os.getenv('POSTGRES_DB'),
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    host = os.getenv('POSTGRES_HOST'),
    port = 5432
  )
  cur = conn.cursor()

  for i, url in enumerate(url_list):
    response = requests.get(url)

    if response.status_code == 200:
      raw_data = response.json()
      station_data = raw_data["value"]["timeSeries"][0]["values"][0]["value"]

      for item in station_data:
        date_raw = item["dateTime"]  # yyyy-mm-ddThr:min:sec-xx:xx
        date_info = date_raw.split("T")  # ['yyyy-mm-dd', hr:min:sec-xx:xx']
        date_info = date_info[:1] + date_info[1].split("-")  # ['yyyy-mm-dd', 'hr:min:sec', 'xx:xx']
        value = item["value"]

        cur.execute(f"SELECT 1 FROM river_data WHERE val_date = '{date_info[0]}' AND val_time = '{date_info[1]}'")
        if cur.fetchone() is not None:
          cur.execute(f"UPDATE river_data SET {column_names[i]} = {value} WHERE val_date = '{date_info[0]}' AND val_time = '{date_info[1]}'")

        else:
          cur.execute(f"INSERT INTO river_data (val_date, val_time, {column_names[i]}) VALUES (\'{date_info[0]}\', \'{date_info[1]}\', {value})")

      conn.commit()
    else:
      print('Error:', response.status_code)

    
  cur.close()
  conn.close()
  
    