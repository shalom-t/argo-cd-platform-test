FROM python:3.12

WORKDIR /app

COPY ./poetry.lock .
COPY pyproject.toml .
COPY . .

RUN pip install poetry==2.0.1

RUN poetry config virtualenvs.create false
RUN poetry install
ENV PATH="/app/.venv/bin:${PATH}" 

EXPOSE 80
# If running behind a proxy like Nginx or Traefik add --proxy-headers
CMD ["uvicorn", "my_service.main:app", "--port", "80", "--proxy-headers"]