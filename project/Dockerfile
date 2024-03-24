FROM python:3.10.0

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt
ENV run_env=docker
EXPOSE 8001
CMD gunicorn -c gunicorn.py -k uvicorn.workers.UvicornWorker main:app
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]