FROM python:3-slim AS build-env
MAINTAINER PiotrUz
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
CMD /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./main.py ./main.py


FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
WORKDIR /app
ENTRYPOINT ["python3", "./main.py"]
ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages
