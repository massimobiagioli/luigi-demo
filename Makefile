.PHONY: up down run-local test

up:
	docker compose up -d --remove-orphans

down:
	docker compose down --remove-orphans

run-local:
ifdef nonce
	ENV=dev poetry run luigi --module luigi_demo.tasks.store_weather_data_task StoreWeatherDataTask --local-scheduler --nonce $(nonce)
else
	ENV=dev poetry run luigi --module luigi_demo.tasks.store_weather_data_task StoreWeatherDataTask --local-scheduler
endif

test:
ifdef filter
	ENV=test poetry run pytest $(filter) -vv
else
	ENV=test poetry run pytest -vv
endif