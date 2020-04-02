#!/bin/bash
for (( ; ; ))
do
   gcloud pubsub topics publish $1 --message $RANDOM
   sleep $2
done