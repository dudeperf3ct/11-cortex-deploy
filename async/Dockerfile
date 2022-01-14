FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY setup.py /app/setup.py

# trunk-ignore(hadolint/DL3042)
RUN pip install .

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "project.app:app"]