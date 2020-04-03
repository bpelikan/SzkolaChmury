# [Zadanie domowe nr 12](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-12-monitoring-with-stackdriver/zadanie-domowe-nr-12/)

#### 1. Utworzenie projektu
```bash
projectName="zadanie12"
gcloud projects create $projectName
```

<details>
  <summary><b><i>Utworzenie Cloud Pub/Sub</i></b></summary>

#### Topic
```bash
topicName="topicName"
gcloud pubsub topics create $topicName
```

#### Subskrypcja
```bash
subscriptionName="subscriptionName"
gcloud pubsub subscriptions create $subscriptionName --topic $topicName --ack-deadline=20
```

#### Sprawdzenie
```bash
bartosz@cloudshell:~ (zadanie12)$ gcloud pubsub topics list
---
name: projects/zadanie12/topics/topicName
bartosz@cloudshell:~ (zadanie12)$ gcloud pubsub subscriptions list
---
ackDeadlineSeconds: 20
expirationPolicy:
  ttl: 2678400s
messageRetentionDuration: 604800s
name: projects/zadanie12/subscriptions/subscriptionName
pushConfig: {}
topic: projects/zadanie12/topics/topicName
```
</details>

#### Utworzenie Instance Template
Instancja VM pobierać będzie 1 wiadomość na 10 sekund.
```bash
templateName="vm-template"

gcloud compute instance-templates create $templateName \
--image-family debian-9 \
--image-project debian-cloud \
--machine-type=f1-micro \
--metadata=startup-script=\#\!/bin/bash$'\n'wget\ https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/GCP/Architecture/Zadanie12/code/read.sh$'\n'bash\ read.sh\ $subscriptionName\ 1\ 10
```
```
