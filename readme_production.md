# 部署

## web 服务

```shell
apt install -y docker.io docker-compse
```

```shell

mkdir -p /root/server
cd /root/server
git clone https://github.com/largerbigsuper/Building_Knowledge_Stack.git
```


```shell

cd /root/server/Building_Knowledge_Stack

docker-compose -f docker-compose.production.yml build

docker-compose -f docker-compose.production.yml run --rm building_knowledge_stack  python manage.py migrate

ocker-compose -f docker-compose.production.yml run --rm building_knowledge_stack  python manage.py createsuperuser

docker-compose -f docker-compose.production.yml run --rm building_knowledge_stack  python manage.py makemigrations customers  subjects questions sms articles feedback

docker-compose -f docker-compose.production.yml run --rm building_knowledge_stack  python manage.py migrate

docker-compose -f docker-compose.production.yml up -d

```