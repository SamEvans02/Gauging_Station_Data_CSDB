CREATE TABLE river_info (
  val_date DATE,
  val_time TIME,
  PRIMARY KEY (val_date, val_time),
  gage_val DECIMAL(3, 2),
  discharge_val INTEGER,
  disolved_val DECIMAL(3, 1),
  ph_val DECIMAL(2, 1),
  temp_val DECIMAL(2, 1)
);

