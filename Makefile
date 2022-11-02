.PHONY: run-local

run-local:
	poetry run luigi --module luigi_demo.tasks.weather-forecast WeatherForecastTask --local-scheduler