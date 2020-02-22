# [Zadanie domowe nr 10](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-10-cloud-hybrid-connectivity/zadanie-domowe-nr-10/)

## 1. Zadanie 1
Utworzenie projektu przed przystąpieniem do zadania:
```bash
gcloud projects create "zadanie10"
```

### 1.1 Utworzenie sieci VPC w celu symulacji sieci lokalnej oraz produkcyjnej
```bash
vpcNetwork1="cloud"
vpcNetwork2="on-prem"

gcloud compute networks create $vpcNetwork1 --subnet-mode=custom --bgp-routing-mode=global
gcloud compute networks create $vpcNetwork2 --subnet-mode=custom --bgp-routing-mode=global
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~ (zadanie10)$ gcloud compute networks list
NAME     SUBNET_MODE  BGP_ROUTING_MODE  IPV4_RANGE  GATEWAY_IPV4
cloud    CUSTOM       GLOBAL
on-prem  CUSTOM       GLOBAL
```
</details>

### 1.3 Utworzenie podsieci
```bash
vpc1subnet1="vpcnetwork1-sub1"
vpc1subnet2="vpcnetwork1-sub2"

gcloud compute networks subnets create $vpc1subnet1 --network=$vpcNetwork1 --region=$vpcRegion --range=10.1.0.0/16
gcloud compute networks subnets create $vpc1subnet2 --network=$vpcNetwork2 --region=$vpcRegion --range=10.2.0.0/16
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~ (zad10-268721)$ gcloud compute networks subnets list
NAME              REGION                   NETWORK  RANGE
vpcnetwork1-sub1  europe-west1             cloud    10.1.0.0/16
vpcnetwork1-sub2  europe-west1             on-prem  10.2.0.0/16
```
</details>
