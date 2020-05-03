sudo docker-compose -f deploy_postgres.yml up -d

python3 manage.py db migrate
python3 manage.py db upgrade

python3 main.py
