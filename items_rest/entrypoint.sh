#!/bin/bash
echo "Waiting for rabbitmq..."

while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do sleep 3; done

echo "RabbitMQ started"