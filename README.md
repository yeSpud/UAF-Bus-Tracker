# UAF Bus Tracker
Tracks when the UAF campus shuttles arrive at stops.

## How to...

### Build and run the script
run `docker compose up --build -d`

### Build the script
run `docker compose build`

### Run the script
run `docker compose up -d`

### View running docker containers
run `docker ps`

### View logs
run `docker logs -f [CONTAINER-NAME]`

### Stop the script
run `docker compose stop`

**DO NOT RUN `docker compose down` - THAT DELETES THE DATABASE**

### Launch a shell in the container
run `docker compose exec trackerbash`

### Initialize the database
1. Make sure the database is **up and running**
2. Launch a shell in the container
3. run `python3 initalization.py`
    * Be sure this is run when all routes are available on [BusWhere](https://buswhere.com/uaf/) to populate the stops

### Export the data
Coming soon:tm: