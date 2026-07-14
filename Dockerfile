FROM python:3.12-alpine3.21

RUN addgroup -S app && adduser -S -G app -u 10001 app

WORKDIR /app
COPY --chown=app:app service_a.py /app/service_a.py
USER app
EXPOSE 8080
CMD ["python", "/app/service_a.py"]
