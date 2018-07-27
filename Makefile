# Remover os caches que o PY gera
clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -rf {} \;i

# Rodando em todos os pc's conectados na mesma rede
run:
	python manage.py runserver 127.0.0.1:8000

# Migração de banco de dados
migrate:
	python manage.py migrate
	python manage.py migrate posts
	
migrations:
	python manage.py makemigrations
	python manage.py makemigrations posts

# Criando o super usuário
user:
	python manage.py createsuperuser

# Interagindo com o shell no django
shell:
	python manage.py shell

# Coletando os arquivos estáticos de todas apps para um único diretório
staticfiles:
	python manage.py collectstatic
