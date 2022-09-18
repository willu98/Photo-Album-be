FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv 
RUN pipenv shell
RUN pipenv install --dev --system --deploy

WORKDIR /app
COPY . /app
RUN cat .env

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]