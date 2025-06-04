
FROM python:3.11


WORKDIR /space-ml


COPY ./requirements.txt /space-ml/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /space-ml/requirements.txt


COPY ./app /space-ml/app
COPY ./parse_module.py /space-ml/parse_module.py

CMD ["fastapi", "run", "app/main.py", "--port", "80"]