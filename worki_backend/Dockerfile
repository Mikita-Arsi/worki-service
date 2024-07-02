FROM python:3.11.4
WORKDIR /worki_backend
COPY req.txt req.txt
RUN pip install --upgrade pip && pip install -r req.txt && chmod 755 .
COPY . .
ENV TZ Europe/Moscow
CMD ["python3", "app.py"]`
