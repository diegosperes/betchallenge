# BetBright

TLDR; The solution is a mix of messaging architecture and a restful application.


## Thoughts

I was wondering what would be the best solution to solve this problem at the same time to scale up the application without overhead a database, due to it, a good solution would be a mix of nginx, sanic, rabbitmq, workers, MongoDB, Redis, and docker. I know is a bunch of technologies but don't be scared, is easy like a piece of cake.

![Alt text](data/img.png?raw=true "Image")

- Nginx is responsible to make round robin to a restful app, also only allow http://external-host:8080 to access the endpoint /api/match and http://security-host:8080 to access the endpoint /message/.* to register a message.
- Restful app registers a message and retrieves any event in databases.
- Redis is the place where every message will be saved before the workers process it.
- Broker is the rabbitmq
- Worker process any message and save it in MongoDB
- MongoDB is the database responsible to keep all the data.


## Production

To simulate the production environment, you just need to run the following command ``` make run-prod ```

#### Insert new message
``` curl -i -X POST -d @data/new_event.json http://security-host:8080/message/ ```

#### Update message
``` curl -i -X POST -d @data/update_event.json http://security-host:8080/message/ ```

#### Get message status
Every message post will return a Location header with a path to figure out the message status.
``` curl -i http://security-host:8080/message/{_id} ```

#### Get event by id
Every message post will return a Location header with a path to figure out the message status.
``` curl -i http://external-host:8080/api/match/994839351740 ```

#### Get event by attr
Every message post will return a Location header with a path to figure out the message status.
``` curl -i http://external-host:8080/api/match/?name=Real%20Madrid%20vs%20Barcelona ```

#### Get event by sport and sort the result
Every message post will return a Location header with a path to figure out the message status.
``` curl -i http://external-host:8080/api/match/Football?ordering=startTime ```

## Tests

To test the application on your computer, you need to set up your environment installing all the services:
    - RabbitMq
    - Redis
    - MongoDB

After that, you just need to run ``` make tests ```

## What would I improve?

- Validate a message content pattern.
- Integrate with a CI/CD
- Benchmark to measure how many works should I use.
- Refactor application, the integration with the worker.
- Refactor models
- Some bugs
