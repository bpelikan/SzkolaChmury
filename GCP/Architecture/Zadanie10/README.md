# [Zadanie domowe nr 10](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-10-cloud-hybrid-connectivity/zadanie-domowe-nr-10/)

## 1. Zadanie 1
### 1.1 Utworzenie VPC w celu symulacji sieci lokalnej oraz produkcyjnej
```bash
vpcNetwork1="cloud"
vpcNetwork2="on-prem"
vpcRegion="europe-west1"

gcloud compute networks create $vpcNetwork1 --subnet-mode=custom
gcloud compute networks create $vpcNetwork2 --subnet-mode=custom
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~ (zad10-268721)$ gcloud compute networks list
NAME     SUBNET_MODE  BGP_ROUTING_MODE  IPV4_RANGE  GATEWAY_IPV4
cloud    CUSTOM       REGIONAL
on-prem  CUSTOM       REGIONAL
```
</details>