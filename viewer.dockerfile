FROM python:3.6.7-alpine3.8
WORKDIR /root/
COPY viewer.py  .
# We need gcc to build the mysqlclient package
RUN ["apk", "add", "build-base"]
# We need mariadb-dev to use the mysqlclient package
RUN ["apk", "add", "mariadb-dev"]
COPY viewer_requirements.txt .
RUN pip install -r viewer_requirements.txt
ENV FLASK_APP="viewer.py"
EXPOSE 5000
CMD  ["python", "-m", "flask", "run", "--host=0.0.0.0"]
