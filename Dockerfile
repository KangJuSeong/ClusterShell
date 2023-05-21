FROM python:3.9.10
WORKDIR /app
COPY ./requirements.txt /app
COPY ./node.py /app
COPY ./fifo.py /app
COPY ./test.py /app
RUN mkdir shared; pip install -r ./requirements.txt; python -m pip install --upgrade pip
CMD python node.py