FROM apify/actor-python:3.12

COPY . /usr/src/app

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

ENV PYTHONPATH=/usr/src/app

CMD ["python", "-m", "src.main"]
