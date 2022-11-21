CREATE TABLE weather_forecast (
	id serial PRIMARY KEY,
	detection_date DATE NOT NULL,
	detection_hour INTEGER NOT NULL,
	city VARCHAR ( 100 ) NOT NULL,
	province VARCHAR ( 2 ) NOT NULL,
	temperature VARCHAR ( 20 ) NOT NULL,
	precipitation VARCHAR ( 20 ) NOT NULL,
	humidity VARCHAR ( 20 ) NOT NULL,
	wind VARCHAR ( 20 ) NOT NULL
);

CREATE UNIQUE INDEX weather_forecast_city_detection_date_detection_hour_idx ON weather_forecast ( city, detection_date, detection_hour );