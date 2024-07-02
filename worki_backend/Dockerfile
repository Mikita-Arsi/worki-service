FROM python:3.11.4
WORKDIR /worki_backend
COPY req.txt req.txt
RUN poetry install && chmod 755 .
COPY . .
ENV TZ Europe/Moscow
CMD ["uvicorn", "app:app", "--reload"]`
