# Variation two: Run the source mapped in from the host
FROM python:3.6.7-alpine3.8
# Since we are creating a small web server, let us home it in the /srv treee
WORKDIR /srv/viewer/
# Instead of copying all of the source, we only want to copy what we will need
# to execute container build commands. In this case, thats the Python
# requirements file. The rest of our server code will be mapped in at container
# run time
COPY viewer/requirements.txt .
# We need gcc to build the mysqlclient package
# TODO Look into mechanisms whereby we don't have to include the build-level
# requirements in the production container
RUN ["apk", "add", "build-base"]
# We need mariadb-dev to use the mysqlclient package
RUN ["apk", "add", "mariadb-dev"]
RUN pip install -r requirements.txt
ENV FLASK_APP="viewer"
ENV FLASK_DEBUG=1
# EXPOSE tells the world what port(s) we are planning on communicating outward
# over, but the actual mapping takes place at container run time
EXPOSE 5000
CMD  ["python", "-m", "flask", "run", "--host=0.0.0.0"]
