# [Zadanie domowe nr 9](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-9-understanding-vpc-networks/praca-domowa-nr-9/)

## 1. W tym zadaniu stworzymy dwa przykładowe projekty, a następnie w każdym projekcie utworzymy odpowiednie środowiska sieciowe. Następnie, kiedy będziemy mieć już odpowiednie komponenty w każdym z projektów wykonamy parowanie wzajemne naszych sieci

### 1.1 Utworzenie projektów
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

### 1.2 Utworzenie sieci VPC w każdym z projektów
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

### 1.3 Utworzenie podsieci
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

### 1.4 Utworzenie reguł Firewall
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

### 1.5 Utworzenie VM
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

### 1.6 Utworzenie VPC network peering
```bash
peeringvpc1tovpc2="vpc1-vpc2"
peeringvpc2tovpc1="vpc2-vpc1"

gcloud compute networks peerings create $peeringvpc1tovpc2 --network=$vpcNetwork1 --peer-network=$vpcNetwork2 --auto-create-routes --peer-project=$projectId2 --project=$projectId1
gcloud compute networks peerings create $peeringvpc2tovpc1 --network=$vpcNetwork2 --peer-network=$vpcNetwork1 --auto-create-routes --peer-project=$projectId1 --project=$projectId2
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute networks peerings list --project=$projectId1
NAME       NETWORK      PEER_PROJECT  PEER_NETWORK  AUTO_CREATE_ROUTES  STATE   STATE_DETAILS
vpc1-vpc2  vpcnetwork1  zadanie9bp-2  vpcnetwork2   True                ACTIVE  [2020-02-10T14:50:46.142-08:00]: Connected.
bartosz@cloudshell:~$ gcloud compute networks peerings list --project=$projectId2
NAME       NETWORK      PEER_PROJECT  PEER_NETWORK  AUTO_CREATE_ROUTES  STATE   STATE_DETAILS
vpc2-vpc1  vpcnetwork2  zadanie9bp-1  vpcnetwork1   True                ACTIVE  [2020-02-10T14:50:46.142-08:00]: Connected.
```
</details>

### 1.7 Sprawdzenie połączenia
Podłączenie się do VM w podsieci 1 i wykonanie próby połączenia się do VM w podsieci 2 (zad9vm1 -> zad9vm2 | 10.1.0.2 -> 10.2.0.2)

<details>
  <summary><b><i>Console output</i></b></summary>

```bash
Connected, host fingerprint: ssh-rsa 0 {...}
Linux zad9vm1 4.9.0-11-amd64 #1 SMP Debian 4.9.189-3+deb9u2 (2019-11-11) x86_64
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.

bartosz@zad9vm1:~$ ping -c 3 10.2.0.2
PING 10.2.0.2 (10.2.0.2) 56(84) bytes of data.
64 bytes from 10.2.0.2: icmp_seq=1 ttl=64 time=7.98 ms
64 bytes from 10.2.0.2: icmp_seq=2 ttl=64 time=6.85 ms
64 bytes from 10.2.0.2: icmp_seq=3 ttl=64 time=6.85 ms

--- 10.2.0.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 6.851/7.228/7.982/0.541 ms
```
</details>

### 1.8 Pytanie

> Jak zbudujesz połączenie pomiędzy sieciami tak, aby umożliwić dotarcie z Projektu B do świata zewnętrznego wychodząc przez urządzenie wirtualne w Projekcie A?

1. Zablokować ruch wychodzący do sieci publicznej z projektu B
2. Włączyć peering do projektu A (co jest już zrobione)
3. W tablicach routingu jako bramę domyślną ustawić urządzenie wirtualne w projekcie A lub połączyć się przez SSH do maszyny w projekcie A

### 1.9 Usunięcie projektów
```bash
gcloud projects delete $projectId1
gcloud projects delete $projectId2
```

## 2. Realizacja schematu architektury

<details>
  <summary><b><i>Schemat architektury</i></b></summary>

![Diagram](./img/schemat.png "schemat architektury")
![Diagram](./img/schemat-p.png "schemat architektury poprawiony")

</details>

### 2.1 Utworzenie projektów
```bash
projectA="zadanie9proja"
projectB="zadanie9projb"
projectC="zadanie9projc"

gcloud projects create $projectA
gcloud projects create $projectB
gcloud projects create $projectC
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud projects list
PROJECT_ID            NAME                           PROJECT_NUMBER
resonant-idea-261413  Szkola Chmury - GCP Architect  162512192576
zadanie9proja         zadanie9proja                  14187841242
zadanie9projb         zadanie9projb                  1031943103857
zadanie9projc         zadanie9projc                  295955672230
```
</details>

### 2.2 Utworzenie sieci VPC w każdym z projektów
```bash
vpcNetworkA="vpcnetworka"
vpcNetworkB="vpcnetworkb"
vpcNetworkC="vpcnetworkc"

gcloud compute networks create $vpcNetworkA --subnet-mode=custom --project=$projectA
gcloud compute networks create $vpcNetworkB --subnet-mode=custom --project=$projectB
gcloud compute networks create $vpcNetworkC --subnet-mode=custom --project=$projectC
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute networks list --project=$projectA
NAME         SUBNET_MODE  BGP_ROUTING_MODE  IPV4_RANGE  GATEWAY_IPV4
default      AUTO         REGIONAL
vpcnetworka  CUSTOM       REGIONAL
bartosz@cloudshell:~$ gcloud compute networks list --project=$projectB
NAME         SUBNET_MODE  BGP_ROUTING_MODE  IPV4_RANGE  GATEWAY_IPV4
default      AUTO         REGIONAL
vpcnetworkb  CUSTOM       REGIONAL
bartosz@cloudshell:~$ gcloud compute networks list --project=$projectC
NAME         SUBNET_MODE  BGP_ROUTING_MODE  IPV4_RANGE  GATEWAY_IPV4
default      AUTO         REGIONAL
vpcnetworkc  CUSTOM       REGIONAL
```
</details>

### 2.3 Utworzenie podsieci
```bash
vpcSubnetA1="vpcnetworka-sub1"
vpcSubnetA2="vpcnetworka-sub2"
vpcSubnetB1="vpcnetworkb-sub1"
vpcSubnetB2="vpcnetworkb-sub2"
vpcSubnetC1="vpcnetworka-sub1"

gcloud compute networks subnets create $vpcSubnetA1 --network=$vpcNetworkA --region=us-central1 --range=10.128.0.0/20 --project=$projectA
gcloud compute networks subnets create $vpcSubnetA2 --network=$vpcNetworkA --region=europe-west1 --range=10.132.0.0/20 --project=$projectA
gcloud compute networks subnets create $vpcSubnetB1 --network=$vpcNetworkB --region=us-central1 --range=172.16.0.0/20 --project=$projectB
gcloud compute networks subnets create $vpcSubnetB2 --network=$vpcNetworkB --region=us-central1 --range=172.20.0.0/20 --project=$projectB
gcloud compute networks subnets create $vpcSubnetC1 --network=$vpcNetworkC --region=europe-west1 --range=10.130.0.0/20 --project=$projectC
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute networks subnets list --project=$projectA
NAME              REGION                   NETWORK      RANGE
vpcnetworka-sub2  europe-west1             vpcnetworka  10.132.0.0/20
vpcnetworka-sub1  us-central1              vpcnetworka  10.128.0.0/20
{...}

bartosz@cloudshell:~$ gcloud compute networks subnets list --project=$projectB
NAME              REGION                   NETWORK      RANGE
vpcnetworkb-sub1  us-central1              vpcnetworkb  172.16.0.0/20
vpcnetworkb-sub2  us-central1              vpcnetworkb  172.20.0.0/20
{...}

bartosz@cloudshell:~$ gcloud compute networks subnets list --project=$projectC
NAME              REGION                   NETWORK      RANGE
vpcnetworka-sub1  europe-west1             vpcnetworkc  10.130.0.0/20
{...}
```
</details>

### 2.4 Utworzenie VPC network peering
```bash
peeringvpcAB="peeringvpcab"
peeringvpcBA="peeringvpcba"
peeringvpcBC="peeringvpcbc"
peeringvpcCB="peeringvpccb"

gcloud compute networks peerings create $peeringvpcAB --network=$vpcNetworkA --peer-network=$vpcNetworkB --auto-create-routes --peer-project=$projectB --project=$projectA
gcloud compute networks peerings create $peeringvpcBA --network=$vpcNetworkB --peer-network=$vpcNetworkA --auto-create-routes --peer-project=$projectA --project=$projectB
gcloud compute networks peerings create $peeringvpcBC --network=$vpcNetworkB --peer-network=$vpcNetworkC --auto-create-routes --peer-project=$projectC --project=$projectB
gcloud compute networks peerings create $peeringvpcCB --network=$vpcNetworkC --peer-network=$vpcNetworkB --auto-create-routes --peer-project=$projectB --project=$projectC
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
gcloud compute networks peerings list --project=$projectA
gcloud compute networks peerings list --project=$projectB
gcloud compute networks peerings list --project=$projectC

bartosz@cloudshell:~$ gcloud compute networks peerings list --project=$projectA
NAME          NETWORK      PEER_PROJECT   PEER_NETWORK  AUTO_CREATE_ROUTES  STATE   STATE_DETAILS
peeringvpcab  vpcnetworka  zadanie9projb  vpcnetworkb   True                ACTIVE  [2020-02-12T12:55:18.716-08:00]: Connected.
bartosz@cloudshell:~$ gcloud compute networks peerings list --project=$projectB
NAME          NETWORK      PEER_PROJECT   PEER_NETWORK  AUTO_CREATE_ROUTES  STATE   STATE_DETAILS
peeringvpcba  vpcnetworkb  zadanie9proja  vpcnetworka   True                ACTIVE  [2020-02-12T12:55:18.716-08:00]: Connected.
peeringvpcbc  vpcnetworkb  zadanie9projc  vpcnetworkc   True                ACTIVE  [2020-02-12T12:55:35.840-08:00]: Connected.
bartosz@cloudshell:~$ gcloud compute networks peerings list --project=$projectC
NAME          NETWORK      PEER_PROJECT   PEER_NETWORK  AUTO_CREATE_ROUTES  STATE   STATE_DETAILS
peeringvpccb  vpcnetworkc  zadanie9projb  vpcnetworkb   True                ACTIVE  [2020-02-12T12:55:35.840-08:00]: Connected.
```
</details>

### 2.5 Utworzenie VM
```bash
vmNameA1="zad9vma1"
vmNameA2="zad9vma2"
vmNameB1="zad9vmb1"
vmNameB2="zad9vmb2"
vmNameC1="zad9vmc1"
vmType="f1-micro"

gcloud compute instances create $vmNameC1 --zone=europe-west1-b --machine-type=$vmType --network-interface=no-address,network=$vpcNetworkC,subnet=$vpcSubnetC1 --image-project=debian-cloud --image=debian-9-stretch-v20191210 --project=$projectC

gcloud compute instances create $vmNameB1 --zone=us-central1-b --machine-type=$vmType --network-interface=no-address,network=$vpcNetworkB,subnet=$vpcSubnetB1 --image-project=debian-cloud --image=debian-9-stretch-v20191210 --project=$projectB
gcloud compute instances create $vmNameB2 --zone=us-central1-b --machine-type=$vmType --network-interface=no-address,network=$vpcNetworkB,subnet=$vpcSubnetB2 --image-project=debian-cloud --image=debian-9-stretch-v20191210 --project=$projectB

gcloud compute instances create $vmNameA1 --zone=us-central1-b --machine-type=$vmType --network-interface=no-address,network=$vpcNetworkA,subnet=$vpcSubnetA1 --image-project=debian-cloud --image=debian-9-stretch-v20191210 --project=$projectA
gcloud compute instances create $vmNameA2 --zone=europe-west1-b --machine-type=$vmType --network-interface=network=$vpcNetworkA,subnet=$vpcSubnetA2 --image-project=debian-cloud --image=debian-9-stretch-v20191210 --project=$projectA
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
gcloud compute instances list --project=$projectA
gcloud compute instances list --project=$projectB
gcloud compute instances list --project=$projectC

bartosz@cloudshell:~$ gcloud compute instances list --project=$projectA
NAME      ZONE            MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP   STATUS
zad9vma2  europe-west1-b  f1-micro                   10.132.0.4   34.76.98.238  RUNNING
zad9vma1  us-central1-b   f1-micro                   10.128.0.2                 RUNNING
bartosz@cloudshell:~$ gcloud compute instances list --project=$projectB
NAME      ZONE           MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP  STATUS
zad9vmb1  us-central1-b  f1-micro                   172.16.0.2                RUNNING
zad9vmb2  us-central1-b  f1-micro                   172.20.0.2                RUNNING
bartosz@cloudshell:~$ gcloud compute instances list --project=$projectC
NAME      ZONE            MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP  STATUS
zad9vmc1  europe-west1-b  f1-micro                   10.130.0.2                RUNNING
```
</details>

### 2.6 Utworzenie reguł Firewall
```bash
gcloud compute firewall-rules create $vpcNetworkC-allow-ssh --direction=INGRESS --priority=65534 --network=$vpcNetworkC --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0 --project=$projectC
gcloud compute firewall-rules create $vpcNetworkB-allow-ssh --direction=INGRESS --priority=65534 --network=$vpcNetworkB --action=ALLOW --rules=tcp:22 --source-ranges=10.130.0.0/20,172.20.0.0/20 --project=$projectB
gcloud compute firewall-rules create $vpcNetworkA-allow-ssh --direction=INGRESS --priority=65534 --network=$vpcNetworkA --action=ALLOW --rules=tcp:22 --source-ranges=172.16.0.0/20,10.128.0.0/20 --project=$projectA
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@cloudshell:~$ gcloud compute firewall-rules list --project=$projectA
NAME                   NETWORK      DIRECTION  PRIORITY  ALLOW   DENY  DISABLED
vpcnetworka-allow-ssh  vpcnetworka  INGRESS    65534     tcp:22        False

bartosz@cloudshell:~$ gcloud compute firewall-rules list --project=$projectB
NAME                   NETWORK      DIRECTION  PRIORITY  ALLOW   DENY  DISABLED
vpcnetworkb-allow-ssh  vpcnetworkb  INGRESS    65534     tcp:22        False

bartosz@cloudshell:~$ gcloud compute firewall-rules list --project=$projectC
NAME                   NETWORK      DIRECTION  PRIORITY  ALLOW   DENY  DISABLED
vpcnetworkc-allow-ssh  vpcnetworkc  INGRESS    65534     tcp:22        False
```
</details>

### 2.7 Sprawdzenie połączenia
1. Dodanie kluczy SSH do metadanych projektów (niezalecane podejście)
2. Połączenie się przez SSH do C1->B2->B1->A1->A2
3. Sprawdzenie połączenia do internetu

<details>
  <summary><b><i>Console output</i></b></summary>

```bash
Connected, host fingerprint: ssh-rsa 0 {...}
Linux zad9vmc1 4.9.0-11-amd64 #1 SMP Debian 4.9.189-3+deb9u2 (2019-11-11) x86_64

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 12 21:11:27 2020 from 35.235.241.178
bartosz@zad9vmc1:~$ ssh 172.20.0.2 -i ~/.ssh/gcp
Linux zad9vmb2 4.9.0-11-amd64 #1 SMP Debian 4.9.189-3+deb9u2 (2019-11-11) x86_64

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 12 21:32:46 2020 from 10.130.0.2
bartosz@zad9vmb2:~$ ssh 172.16.0.2 -i ~/.ssh/gcp
Linux zad9vmb1 4.9.0-11-amd64 #1 SMP Debian 4.9.189-3+deb9u2 (2019-11-11) x86_64

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 12 21:33:42 2020 from 172.20.0.2
bartosz@zad9vmb1:~$ ssh 10.128.0.2 -i ~/.ssh/gcp
Linux zad9vma1 4.9.0-11-amd64 #1 SMP Debian 4.9.189-3+deb9u2 (2019-11-11) x86_64

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 12 21:37:13 2020 from 172.16.0.2
bartosz@zad9vma1:~$ ssh 10.132.0.4 -i ~/.ssh/gcp
Warning: Identity file /home/bartosz/.ssh/gcp not accessible: No such file or directory.
^C
bartosz@zad9vma1:~$ ssh-keygen -t rsa -f ~/.ssh/gcp -C $email
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/bartosz/.ssh/gcp.
Your public key has been saved in /home/bartosz/.ssh/gcp.pub.
The key fingerprint is:
SHA256:2h5fCGggD1JetLLarJ+A9YVrmSKqWDWTb36EVwjM7VM {...}
The key's randomart image is:
+---[RSA 2048]----+
|  ..oo .         |
| o . .+ . E      |
|. = o  o o       |
| . * + .+ .      |
|  o B +.So       |
|.= o X.oo. .     |
|= = * +oo . .    |
|o= + o ..o .     |
|*.o   ... .      |
+----[SHA256]-----+
bartosz@zad9vma1:~$ cat ~/.ssh/gcp.pub
ssh-rsa {...}
bartosz@zad9vma1:~$ ssh 10.132.0.4 -i ~/.ssh/gcp
^C
bartosz@zad9vma1:~$ ssh 10.132.0.4 -i ~/.ssh/gcp
The authenticity of host '10.132.0.4 (10.132.0.4)' can't be established.
ECDSA key fingerprint is SHA256:kCNVvjlXMIOEfP94X/KX5HrNUcETayPpg62W+F8J/sQ.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.132.0.4' (ECDSA) to the list of known hosts.
Linux zad9vma2 4.9.0-11-amd64 #1 SMP Debian 4.9.189-3+deb9u2 (2019-11-11) x86_64

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
bartosz@zad9vma2:~$ ping www.wp.pl
PING www.wp.pl (212.77.98.9) 56(84) bytes of data.
64 bytes from www.wp.pl (212.77.98.9): icmp_seq=1 ttl=54 time=21.9 ms
64 bytes from www.wp.pl (212.77.98.9): icmp_seq=2 ttl=54 time=22.0 ms
64 bytes from www.wp.pl (212.77.98.9): icmp_seq=3 ttl=54 time=22.3 ms
^C
--- www.wp.pl ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 21.976/22.114/22.324/0.228 ms
```
</details>

### 2.8 Usunięcie projektów
```bash
gcloud projects delete $projectA
gcloud projects delete $projectB
gcloud projects delete $projectC
```

