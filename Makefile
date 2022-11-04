.PHONY: run-local

run-local:
	poetry run luigi --module luigi_demo.tasks.get_weather_data_task GetWeatherDataTask --local-scheduler

test:
ifdef filter
	poetry run pytest $(filter) -vv
else
	poetry run pytest -vv
endif