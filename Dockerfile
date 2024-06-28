FROM python:3.12

WORKDIR /app

COPY requirements_3.12.txt .

RUN pip install --upgrade pip &&\
    pip install -r requirements_3.12.txt

COPY . .

CMD ["python", "-m", "main"]
