.PHONY: up down run-local test

up:
	docker compose up -d --remove-orphans

down:
	docker compose down --remove-orphans

run-local:
ifdef nonce
	poetry run luigi --module luigi_demo.tasks.store_weather_data_task StoreWeatherDataTask --local-scheduler --nonce $(nonce)
else
	poetry run luigi --module luigi_demo.tasks.store_weather_data_task StoreWeatherDataTask --local-scheduler
endif

test:
ifdef filter
	poetry run pytest $(filter) -vv
else
	poetry run pytest -vv
endif