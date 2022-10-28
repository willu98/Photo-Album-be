# Photo-Album-be
Photo album repository, backend written in Python using FastAPI with postgres for SQL DB.
Hosted on AWS EC2 using Docker and NGINX. File storage is done using AWS S3.

## Run in Docker container
~~~~
create .env file with necessary credentials
docker build -t <Docker Image name> . 

docker run --name <Container Name> -d -p <Port on local>:<Port in container> <Docker Image name>
~~~~
## Run on Local
### To install dependencies and run
~~~~
create .env file with necessary credentials
pipenv shell
pipenv install
uvicorn main:app --reload
~~~~
