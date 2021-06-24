install_requirements:
	pip install -r ./.requirements/common.txt

install_linters:
	pip install -r ./.requirements/linters.txt
	pre-commit install
	pre-commit install --hook-type commit-msg
	pre-commit autoupdate


migrate:
	alembic upgrade head

init_db:
	docker-compose up --build db
	make install_requirements
	make migrate
