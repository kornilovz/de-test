FROM python:3.12-slim-bookworm
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY ./main.py ./main.py
CMD ["python", "main.py"]