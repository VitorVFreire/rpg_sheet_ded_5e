# Use the official PostgreSQL image
FROM postgres:latest

# Environment variables for PostgreSQL
ENV POSTGRES_DB rpg
ENV POSTGRES_USER rpg
ENV POSTGRES_PASSWORD 123

# Expose the default PostgreSQL port
EXPOSE 5432

#sudo docker build -t postegsqlrpgimage .
#sudo docker run -d -p 5432:5432 --name postegsqlrpgcontainer postegsqlrpgimage
