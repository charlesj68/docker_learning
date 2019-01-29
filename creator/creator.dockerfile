FROM python:3.6.7-alpine3.8
WORKDIR /home/creator/
# Instead of copying all of the source, we only want to copy what we will need
# to execute container build commands. In this case, thats the Python
# requirements file. The rest of our server code will be mapped in at container
# run time
COPY source/requirements.txt .
# We need gcc to build the mysqlclient package
RUN ["apk", "add", "build-base"]
# We need mysql-devel to use the mysqlclient package
RUN ["apk", "add", "mariadb-dev"]
RUN pip install -r requirements.txt
# Run the python script with unbuffed output (-u)
# Without this the various print() outputs will not
# appear in the docker logs
CMD  ["python", "-u", "creator.py"]
