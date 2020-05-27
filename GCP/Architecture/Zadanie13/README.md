# [Zadanie domowe nr 13](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-13-serverless-i-big-data/zadanie-domowe-nr-13/)



![schemat](./img/schemat.jpg)


#### Utworzenie projektu
```bash
projectName="zadanie13"
gcloud projects create $projectName
```

#### Utworzenie Cloud Pub/Sub
```bash
# Topic
topicName="rawdata"
gcloud pubsub topics create $topicName

# Subskrypcja
subscriptionName="rawdatasub"
gcloud pubsub subscriptions create $subscriptionName --topic $topicName --ack-deadline=20
```
