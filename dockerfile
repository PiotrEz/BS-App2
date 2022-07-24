FROM python:3.10
MAINTAINER PiotrUz
COPY requirements.txt /usr/src/app/requirements.txt
CMD /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt
COPY main.py /usr/src/app
#CMD ["python3", "/usr/src/app/main.py", "i" , "-q", "(queue)", "-p", "(app_port)"]
ENTRYPOINT ["python3", "/usr/src/app/main.py"]
