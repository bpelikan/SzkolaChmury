# [Zadanie domowe nr 9](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-9-understanding-vpc-networks/praca-domowa-nr-9/)

### 1. W tym zadaniu stworzymy dwa przykładowe projekty, a następnie w każdym projekcie utworzymy odpowiednie środowiska sieciowe. Następnie, kiedy będziemy mieć już odpowiednie komponenty w każdym z projektów wykonamy parowanie wzajemne naszych sieci
#### 1.1 Utworzenie projektów
```bash
projectId1="zadanie9bp-1"
projectId2="zadanie9bp-2"

gcloud projects create $projectId1
gcloud projects create $projectId2
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud projects list
PROJECT_ID            NAME                           PROJECT_NUMBER
resonant-idea-261413  Szkola Chmury - GCP Architect  162512192576
zadanie9bp-1          zadanie9bp-1                   492134302499
zadanie9bp-2          zadanie9bp-2                   121362761339
```
</details>

#### 1.2 Utworzenie sieci VPC w każdym z projektów
```bash
vpcNetwork1="vpcnetwork1"
vpcNetwork2="vpcnetwork2"

gcloud compute networks create $vpcNetwork1 --subnet-mode=custom --project=$projectId1
gcloud compute networks create $vpcNetwork2 --subnet-mode=custom --project=$projectId2
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute networks list --project=$projectId1
NAME         SUBNET_MODE  BGP_ROUTING_MODE  IPV4_RANGE  GATEWAY_IPV4
default      AUTO         REGIONAL
vpcnetwork1  CUSTOM       REGIONAL
bartosz@cloudshell:~$ gcloud compute networks list --project=$projectId2
NAME         SUBNET_MODE  BGP_ROUTING_MODE  IPV4_RANGE  GATEWAY_IPV4
default      AUTO         REGIONAL
vpcnetwork2  CUSTOM       REGIONAL
```
</details>
