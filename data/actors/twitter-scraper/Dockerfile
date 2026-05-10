FROM apify/actor-python-playwright:3.12

COPY . /usr/src/app

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

RUN python3 -m playwright install chromium 2>&1 | tail -3

ENV PYTHONPATH=/usr/src/app

CMD ["python", "-m", "src.main"]
