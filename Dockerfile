FROM python:3.10.8
WORKDIR /app
COPY req.txt req.txt
RUN apt-get update && apt-get upgrade -y && apt-get install virtualenv pkg-config -y
RUN python -m venv venv && venv/bin/pip install --upgrade pip wheel setuptools
RUN venv/bin/pip install -r req.txt
COPY . /app
ENTRYPOINT [ "/app/venv/bin/python","/app/Dashboard.py" ]