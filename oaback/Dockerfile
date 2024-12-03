FROM python:3.12.3

COPY . /www/

WORKDIR /www

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

RUN pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple  

RUN pip install --upgrade PyJWT

RUN mkdir -p /data/log
RUN mkdir -p /data/sock

EXPOSE 8000

ENTRYPOINT python manage.py makemigrations; \ 
python manage.py migrate; \
python manage.py initdepartments; \
python manage.py inituser; \
python manage.py initabsenttype; \
celery -A oaback worker -l INFO --detach; \
uwsgi --ini uwsgi.ini