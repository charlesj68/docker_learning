FROM python:3.6.7-alpine3.8
WORKDIR /home/creator/
# Instead of copying all of the source, we only want to copy what we will need
# to execute container build commands. In this case, thats the Python
# requirements file. The rest of our server code will be mapped in at container
# run time
COPY source/requirements.txt .
# We need gcc to build the mysqlclient package
# TODO Look into mechanisms whereby we don't have to include the build-level
# requirements in the production container
RUN ["apk", "add", "build-base"]
# We need mariadb-dev to use the mysqlclient package
RUN ["apk", "add", "mariadb-dev"]
RUN pip install -r requirements.txt
CMD  ["python", "creator.py"]
