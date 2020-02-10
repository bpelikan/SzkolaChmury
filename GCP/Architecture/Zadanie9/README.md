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

#### 1.3 Utworzenie podsieci
```bash
vpc1subnet1="vpcnetwork1-sub1"
vpc2subnet2="vpcnetwork2-sub2"

gcloud compute networks subnets create $vpc1subnet1 --network=$vpcNetwork1 --region=europe-west1 --range=10.1.0.0/16 --project=$projectId1
gcloud compute networks subnets create $vpc2subnet2 --network=$vpcNetwork2 --region=europe-west2 --range=10.2.0.0/16 --project=$projectId2
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute networks subnets list --project=$projectId1
NAME              REGION                   NETWORK      RANGE
default           us-west2                 default      10.168.0.0/20
default           asia-northeast1          default      10.146.0.0/20
default           asia-northeast2          default      10.174.0.0/20
default           us-west1                 default      10.138.0.0/20
default           southamerica-east1       default      10.158.0.0/20
default           europe-west6             default      10.172.0.0/20
default           europe-west4             default      10.164.0.0/20
default           asia-east1               default      10.140.0.0/20
default           europe-north1            default      10.166.0.0/20
default           asia-southeast1          default      10.148.0.0/20
default           us-east4                 default      10.150.0.0/20
default           europe-west1             default      10.132.0.0/20
vpcnetwork1-sub1  europe-west1             vpcnetwork1  10.1.0.0/16
default           europe-west2             default      10.154.0.0/20
default           europe-west3             default      10.156.0.0/20
default           australia-southeast1     default      10.152.0.0/20
default           asia-south1              default      10.160.0.0/20
default           asia-northeast3          default      10.178.0.0/20
default           us-east1                 default      10.142.0.0/20
default           us-central1              default      10.128.0.0/20
default           asia-east2               default      10.170.0.0/20
default           northamerica-northeast1  default      10.162.0.0/20
bartosz@cloudshell:~$ gcloud compute networks subnets list --project=$projectId2
NAME              REGION                   NETWORK      RANGE
default           us-west2                 default      10.168.0.0/20
default           asia-northeast1          default      10.146.0.0/20
default           asia-northeast2          default      10.174.0.0/20
default           us-west1                 default      10.138.0.0/20
default           southamerica-east1       default      10.158.0.0/20
default           europe-west6             default      10.172.0.0/20
default           europe-west4             default      10.164.0.0/20
default           asia-east1               default      10.140.0.0/20
default           europe-north1            default      10.166.0.0/20
default           asia-southeast1          default      10.148.0.0/20
default           us-east4                 default      10.150.0.0/20
default           europe-west1             default      10.132.0.0/20
default           europe-west2             default      10.154.0.0/20
vpcnetwork2-sub2  europe-west2             vpcnetwork2  10.2.0.0/16
default           europe-west3             default      10.156.0.0/20
default           australia-southeast1     default      10.152.0.0/20
default           asia-south1              default      10.160.0.0/20
default           asia-northeast3          default      10.178.0.0/20
default           us-east1                 default      10.142.0.0/20
default           us-central1              default      10.128.0.0/20
default           asia-east2               default      10.170.0.0/20
default           northamerica-northeast1  default      10.162.0.0/20
```
</details>

#### 1.4 Utworzenie reguł Firewall
```bash
gcloud compute firewall-rules create $vpcNetwork1-allow-icmp --direction=INGRESS --priority=65534 --network=$vpcNetwork1 --action=ALLOW --rules=icmp --source-ranges=0.0.0.0/0 --project=$projectId1
gcloud compute firewall-rules create $vpcNetwork2-allow-icmp --direction=INGRESS --priority=65534 --network=$vpcNetwork2 --action=ALLOW --rules=icmp --source-ranges=0.0.0.0/0 --project=$projectId2
gcloud compute firewall-rules create $vpcNetwork2-allow-ssh --direction=INGRESS --priority=65534 --network=$vpcNetwork1 --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0 --project=$projectId1
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute firewall-rules list --project=$projectId1
NAME                    NETWORK      DIRECTION  PRIORITY  ALLOW                         DENY  DISABLED
default-allow-icmp      default      INGRESS    65534     icmp                                False
default-allow-internal  default      INGRESS    65534     tcp:0-65535,udp:0-65535,icmp        False
default-allow-rdp       default      INGRESS    65534     tcp:3389                            False
default-allow-ssh       default      INGRESS    65534     tcp:22                              False
vpcnetwork1-allow-icmp  vpcnetwork1  INGRESS    65534     icmp                                False
vpcnetwork2-allow-ssh   vpcnetwork1  INGRESS    65534     tcp:22                              False

To show all fields of the firewall, please show in JSON format: --format=json
To show all fields in table format, please see the examples in --help.

bartosz@cloudshell:~$ gcloud compute firewall-rules list --project=$projectId2
NAME                    NETWORK      DIRECTION  PRIORITY  ALLOW                         DENY  DISABLED
default-allow-icmp      default      INGRESS    65534     icmp                                False
default-allow-internal  default      INGRESS    65534     tcp:0-65535,udp:0-65535,icmp        False
default-allow-rdp       default      INGRESS    65534     tcp:3389                            False
default-allow-ssh       default      INGRESS    65534     tcp:22                              False
vpcnetwork2-allow-icmp  vpcnetwork2  INGRESS    65534     icmp                                False

To show all fields of the firewall, please show in JSON format: --format=json
To show all fields in table format, please see the examples in --help.
```
</details>

#### 1.5 Utworzenie VM
```bash
vmName1="zad9vm1"
vmZone1="europe-west1-b"
vmName2="zad9vm2"
vmZone2="europe-west2-b"
vmType="f1-micro"

gcloud compute instances create $vmName1 --zone=$vmZone1 --machine-type=$vmType --network-interface=network=$vpcNetwork1,subnet=$vpc1subnet1 --image-project=debian-cloud --image=debian-9-stretch-v20191210 --project=$projectId1
gcloud compute instances create $vmName2 --zone=$vmZone2 --machine-type=$vmType --network-interface=network=$vpcNetwork2,subnet=$vpc2subnet2 --image-project=debian-cloud --image=debian-9-stretch-v20191210 --project=$projectId2
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute instances list --project=$projectId1
NAME     ZONE            MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
zad9vm1  europe-west1-b  f1-micro                   10.1.0.2     35.240.22.166  RUNNING
bartosz@cloudshell:~$ gcloud compute instances list --project=$projectId2
NAME     ZONE            MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP   STATUS
zad9vm2  europe-west2-b  f1-micro                   10.2.0.2     34.89.72.188  RUNNING
```
</details>
