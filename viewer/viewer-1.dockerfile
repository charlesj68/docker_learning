# Variation one: Package the source into the container itself
FROM python:3.6.7-alpine3.8
# Since we are creating a small web server, let us home it in the /srv treee
WORKDIR /srv/viewer/
# Copy the source for the viewer app into the workdir
COPY source .
# We need gcc to build the mysqlclient package
# TODO Look into mechanisms whereby we don't have to include the build-level
# requirements in the production container
RUN ["apk", "add", "build-base"]
# We need mariadb-dev to use the mysqlclient package
RUN ["apk", "add", "mariadb-dev"]
RUN pip install -r viewer_requirements.txt
ENV FLASK_APP="viewer.py"
ENV FLASK_DEBUG=1
# EXPOSE tells the world what port(s) we are planning on communicating outward
# over, but the actual mapping takes place at container run time
EXPOSE 5000
CMD  ["python", "-m", "flask", "run", "--host=0.0.0.0"]
