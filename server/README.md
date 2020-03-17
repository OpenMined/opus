# Running Commands

To easily interact with the application via the `flask` CLI, simply run `docker-compose exec server bash` from the root of this project.

To interact with the postgres DB via the CLI, you can use the following command: `docker exec -it private-identity-server_db_1 psql -U postgres`.

# Database migrations
1. `docker-compose exec server bash`
2. `flask db upgrade` from inside the above bash session.
