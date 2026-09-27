# Python 3.12.12 on Alpine 3.21; the digest is the enforced identity.
FROM python:3.12-alpine3.21@sha256:d4f9227f21409479c7fe92288f2e40b1a56ae591c8ad3b5446dfeaef90f67857

RUN addgroup -S app && adduser -S -G app -u 10001 app

WORKDIR /app
COPY --chown=app:app service_a.py /app/service_a.py
USER app
EXPOSE 8080
CMD ["python", "/app/service_a.py"]
