FROM python:3.7.0

LABEL Name=building_knowledge_stack Version=0.0.1

RUN mkdir -p /app/logs

ADD requirements.txt /app

WORKDIR /app

RUN python3 -m pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --no-cache-dir

RUN python3 -m pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --no-cache-dir

ADD . /app

EXPOSE 8000
# CMD ["/bin/bash", "run_web.sh"]

