# [Zadanie domowe nr 14](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-14-kontenery-w-gcp/zadanie-domowe-nr-14/)


### 1. Utworzenie projektu
```bash
PROJECT_NAME="zadanie14"
gcloud projects create $PROJECT_NAME
```

### Utworzenie klastra Google Kubernetes Engine
```bash
CLUSTER_NANE="cluster-zad14"
CLUSTER_ZONE="us-central1-c"
# utworzenie klastra
gcloud container clusters create $CLUSTER_NANE --num-nodes 3 --zone $CLUSTER_ZONE --machine-type "n1-standard-1"
# pobranie credantiali
gcloud container clusters get-credentials $CLUSTER_NANE --zone $CLUSTER_ZONE --project $PROJECT_NAME
```

### Deployment
```bash
wget https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/GCP/Architecture/Zadanie14/code/deployment.yaml
kubectl apply -f deployment.yaml
```
