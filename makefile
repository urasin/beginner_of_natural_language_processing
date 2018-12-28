run:
	docker-compose run python pipenv run python main.py
bash:
	docker-compose run python bash

fix-lint:
	docker-compose run python pipenv run autopep8 --in-place --aggressive --aggressive main.py
lint:
	docker-compose run python pipenv run pycodestyle main.py

pipenv-install:
	docker-compose run python pipenv install
# 不要なイメージと使われていないvolumeを削除
clean:
	docker image prune
	docker volume prune
	docker rmi -f `docker images -f "dangling=true" -q`