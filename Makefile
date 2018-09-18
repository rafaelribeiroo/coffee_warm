# First of all
# alias m='make'

# Remover os caches que o PY gera
clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -rf {} \;

# Rodando em todos os pc's conectados na mesma rede
run:
	python manage.py runserver localhost:8000

# Migração de banco de dados
te:
	python manage.py migrate
	python manage.py migrate posts
	python manage.py migrate accounts
	
tions:
	python manage.py makemigrations
	python manage.py makemigrations posts
	python manage.py makemigrations accounts

off_tions:
	# find . -type d -name 'migrations' -prune -exec rm -rf {} \;
	cd /src/apps/accounts && rm -rf migrations
	cd /src/apps/posts && rm -rf migrations

# Criando o super usuário
user:
	python manage.py createsuperuser

# Interagindo com o shell no django
shell:
	python manage.py shell

# Coletando os arquivos estáticos de todas apps para um único diretório
staticfiles:
	python manage.py collectstatic

# Limpar os registros do banco
del:
	python manage.py sqlflush