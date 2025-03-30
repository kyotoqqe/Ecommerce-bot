FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app/admin
COPY requirements.txt /usr/src/app/admin
RUN pip install -r /usr/src/app/admin/requirements.txt
COPY . /usr/src/app/admin