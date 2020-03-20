# Running Commands

To easily interact with the application via the `flask` CLI, simply run `docker-compose exec server bash` from the root of this project.

To interact with the postgres DB via the CLI, you can use the following command: `docker exec -it private-identity-server_db_1 psql -U postgres`.

# Database migrations
## Generating a new migration ##
```
$ inv db.create -m "Awesome migration message"
```
## Getting migration to head version ##
```
$ inv db.up --revision head
```
## Downgrade one version ##
To downgrade once
```
$ inv db.down
```

To remove all migrations
```
$ inv db.down --revision base
```
