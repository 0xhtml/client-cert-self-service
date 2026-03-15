FROM alpine:3.23 AS scss
RUN apk add --no-cache sassc
COPY scss scss
RUN sassc -t compressed scss/style.scss style.css

FROM python:3-alpine3.23
RUN --mount=type=cache,target=/root/.cache/pip --mount=source=requirements.txt,dst=requirements.txt pip install -r requirements.txt
COPY client_cert_self_service client_cert_self_service
COPY templates templates
COPY static static
COPY --from=scss style.css static/.
ADD https://unpkg.com/htmx.org@2.0.8/dist/htmx.min.js static/.
EXPOSE 80
CMD ["uvicorn", "client_cert_self_service:app", "--host", "0.0.0.0", "--port", "80"]
