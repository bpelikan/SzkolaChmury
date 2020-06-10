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

<details>
  <summary><b><i>kubectl describe deployment web</i></b></summary>

```bash
bartosz@cloudshell:~/zad14 (zadanie14)$ kubectl describe deployment web
Name:                   web
Namespace:              default
CreationTimestamp:      Wed, 10 Jun 2020 22:06:07 +0200
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               1 desired | 1 updated | 1 total | 0 available | 1 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:      nginx:latest
    Port:       80/TCP
    Host Port:  0/TCP
    Limits:
      cpu:     300m
      memory:  500Mi
    Requests:
      cpu:        100m
      memory:     250Mi
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  <none>
NewReplicaSet:   web-c7759f966 (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  5s    deployment-controller  Scaled up replica set web-c7759f966 to 1
```
</details>


## Zadanie 1

### Horizontal Pod Autoscaler
```bash
wget https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/GCP/Architecture/Zadanie14/code/web-hpa.yaml
kubectl apply -f web-hpa.yaml
```

<details>
  <summary><b><i>kubectl get hpa</i></b></summary>

```bash
bartosz@cloudshell:~/zad14 (zadanie14)$ kubectl get hpa
NAME   REFERENCE        TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
web    Deployment/web   <unknown>/80%   1         10        0          4s
```
</details>

<details>
  <summary><b><i>kubectl describe hpa web</i></b></summary>

```bash
bartosz@cloudshell:~/zad14 (zadanie14)$ kubectl describe hpa web
Name:                     web
Namespace:                default
Labels:                   <none>
Annotations:              autoscaling.alpha.kubernetes.io/conditions:
                            [{"type":"AbleToScale","status":"True","lastTransitionTime":"2020-06-10T20:08:06Z","reason":"ScaleDownStabilized","message":"recent recomm...
                          autoscaling.alpha.kubernetes.io/current-metrics:
                            [{"type":"Resource","resource":{"name":"cpu","currentAverageUtilization":0,"currentAverageValue":"0"}}]
CreationTimestamp:        Wed, 10 Jun 2020 22:08:01 +0200
Reference:                Deployment/web
Target CPU utilization:   80%
Current CPU utilization:  0%
Min replicas:             1
Max replicas:             10
Deployment pods:          1 current / 1 desired
Events:                   <none>
```
</details>


### Podłączenie się do kontenera

<details>
  <summary><b><i>kubectl get pod</i></b></summary>

```bash
bartosz@cloudshell:~/zad14 (zadanie14)$ kubectl get pod
NAME                  READY   STATUS    RESTARTS   AGE
web-c7759f966-jd54k   1/1     Running   0          2m29s
```
</details>

```bash
kubectl exec -it web-c7759f966-jd54k /bin/bash
```

#### Symulacja obciążenia
```
apt-get update
apt-get install stress
stress -c 5
```

<details>
  <summary><b><i>kubectl get pod</i></b></summary>

```bash
bartosz@cloudshell:~/zad14 (zadanie14)$ kubectl get pod
NAME                  READY   STATUS    RESTARTS   AGE
web-c7759f966-jd54k   1/1     Running   0          2m29s
```
</details>