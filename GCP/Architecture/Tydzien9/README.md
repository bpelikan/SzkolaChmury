# [UNDERSTANDING VPC NETWORKS](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-9-understanding-vpc-networks/)

## [VPC Network Peering](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-9-understanding-vpc-networks/vpc-network-peering-hands-on/)
```bash
# Utworzenie sieci VPC
vpcNetworkName1="vpcnetwork1"
vpcNetworkName2="vpcnetwork2"
gcloud compute networks create $vpcNetworkName1 --subnet-mode=custom
gcloud compute networks create $vpcNetworkName2 --subnet-mode=custom

# Utworzenie podsieci
subnetName1="vpcnetwork1-ew1"
subnetName2="vpcnetwork2-ew1"
gcloud compute networks subnets create $subnetName2 --network=$vpcNetworkName2 --region=europe-west1 --range=172.16.0.0/20

# Regułu firewall
firewallRuleName1="vpcnetwork1-allow-icmp"
firewallRuleName2="vpcnetwork2-allow-icmp"
gcloud compute firewall-rules create $firewallRuleName1 --direction=INGRESS --priority=65534 --network=$vpcNetworkName1 --action=ALLOW --rules=icmp --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create $firewallRuleName2 --direction=INGRESS --priority=65534 --network=$vpcNetworkName2 --action=ALLOW --rules=icmp --source-ranges=0.0.0.0/0
gcloud compute firewall-rules create $vpcNetworkName1-allow-ssh --direction=INGRESS --priority=65534 --network=$vpcNetworkName1 --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0
```