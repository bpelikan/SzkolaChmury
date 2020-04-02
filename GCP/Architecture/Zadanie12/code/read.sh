#!/bin/bash
for (( ; ; ))
do
   gcloud pubsub subscriptions pull --auto-ack --limit=$2 $1
   sleep $3
done