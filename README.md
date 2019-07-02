## 常用命令

- 生成超级管理员

```
docker-compose run --rm building_knowledge_stack  python manage.py createsuperuser
```

- 生成migrations

```shell
python manage.py makemigrations customers  subjects questions   

```

- 同步数据库

```
python manage.py migrate
```

- docker-compose

```shell
# 生成迁移文件
docker-compose run --rm building_knowledge_stack  python manage.py makemigrations customers  subjects questions

# 同步数据库
docker-compose run --rm building_knowledge_stack  python manage.py migrate

```