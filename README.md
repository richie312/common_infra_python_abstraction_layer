# Retirement Portfolio Solution
Retirement Portfolio Solution service plan using kafka, api, redis and backend jobs managed by airflow.
![alt text](.\images\distributed_system.png)- 

## Backend Jobs Managed By Airflow

![alt text](./images/AI_YouTube_Video_Upload.png)

## Timeline
![alt text](./images/microservice_actions_over_time.png)


## Kafka Streaming Service

    a. An api subscribed to kafka topic.
    b. An api sourcing the kafka producer to produce messages on a topic.

## API

    a. Flask Server
    b. Has an api for user_interface(Chat bot integration) which takes the messages and source it to the kafka producer.
    c. Has an api which is listening to subscribed kafka topic.
    d. Flask-Redis configuration to reply immediately from redis cache server.

## Database

    a. Database for kafka, airflow and redis.
    b. Database for API, preffeably mongo or cosmos db.

## Container

All of the services are running on containers and final built image is published to the docker hub.

## Kubernetes Deployment

The entire deployment is through kubernetes. Each of the above container will be pulled as an image to deploy pod as service in kubernetes environment.
