migrate:
	flask db migrate
	flask db upgrade

vars:
	sudo nano ./konek/config.py