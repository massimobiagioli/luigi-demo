.PHONY: run-local

run-local:
ifdef nonce
	poetry run luigi --module luigi_demo.tasks.get_weather_data_task GetWeatherDataTask --local-scheduler --nonce $(nonce)
else
	poetry run luigi --module luigi_demo.tasks.get_weather_data_task GetWeatherDataTask --local-scheduler
endif

test:
ifdef filter
	poetry run pytest $(filter) -vv
else
	poetry run pytest -vv
endif