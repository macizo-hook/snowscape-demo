FROM python:3.9

WORKDIR /usr/src/app

# We need Spanner
RUN pip install google-cloud-spanner

# Mount glcloud creds to container
COPY ./credentials.json /usr/src/app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/credentials.json

COPY ./setup_spanner.py .

# Default args for ENTRYPOINT
CMD ["--instance_id", "instance-id", "--database_id", "database-id"]

ENTRYPOINT ["python", "./setup_spanner.py"]
