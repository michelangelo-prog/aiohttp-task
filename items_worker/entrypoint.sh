#!/bin/bash
echo "Waiting for rabbitmq..."

while ! nc -z 'rabbitmq' 5672; do sleep 3; done

echo "RabbitMQ started"