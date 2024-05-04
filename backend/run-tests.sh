cd ./src
alembic -x test=true upgrade 37e18e3672ae
pytest -v
