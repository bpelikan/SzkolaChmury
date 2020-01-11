# [INSTANCE GROUPS I AUTOSKALOWANIE](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/)


## [Instance Templates](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/instance-templates-hands-on/)
```bash
instanceGroupName="instance-vm-group"

# Konfiguracja autoskalowania
gcloud compute instance-groups managed set-autoscaling $instanceGroupName --min-num-replicas 5 --max-num-replicas 10 --zone=us-central1-a
```

## [Rolling Updates](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/rolling-updates-hands-on/)
```bash
# Utworzenie szablonu
templateName1="vmtemplate1"
templateName2="vmtemplate2"
gcloud compute instance-templates create $templateName1 --image-family debian-9 --image-project debian-cloud --machine-type=f1-micro
gcloud compute instance-templates create $templateName2 --image-family debian-10 --image-project debian-cloud --machine-type=f1-micro

# Utworzenie instance group
instanceGroupName="vm-group"
gcloud compute instance-groups managed create $instanceGroupName --base-instance-name=$instanceGroupName --template=$templateName1 --size=5 --zone=us-central1-a

# Aktualizacja
gcloud compute instance-groups managed rolling-action start-update $instanceGroupName --version template=$templateName2 --max-unavailable 2 --zone=us-central1-a

# Usunięcie
gcloud compute instance-groups managed delete $instanceGroupName --zone=us-central1-a
gcloud compute instance-templates delete $templateName1
gcloud compute instance-templates delete $templateName2
```

## [Canary Testing](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/canary-testing-hands-on/)
```bash
templateName1="vmtemplate1"
templateName2="vmtemplate2"

# Utworzenie 2 wersji szablonu
gcloud compute instance-templates create $templateName1 --image-family debian-9 --image-project debian-cloud --machine-type=f1-micro
gcloud compute instance-templates create $templateName2 --image-family debian-10 --image-project debian-cloud --machine-type=f1-micro

# Utworzenie instance group
instanceGroupName="vm-group"
gcloud compute instance-groups managed create $instanceGroupName --base-instance-name=$instanceGroupName --template=$templateName1 --size=4 --zone=us-central1-a

# Canary update
gcloud compute instance-groups managed rolling-action start-update $instanceGroupName --version template=$templateName1 --canary-version template=$templateName2,target-size=50% --zone us-central1-a

gcloud compute instance-groups managed rolling-action start-update $instanceGroupName --version template=$templateName2 --max-unavailable 100% --zone=us-central1-a

# Usunięcie zasobów
gcloud compute instance-groups managed delete $instanceGroupName --zone=us-central1-a
gcloud compute instance-templates delete $templateName1
gcloud compute instance-templates delete $templateName2
```

## [Regional and Zonal Managed Instance Groups](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/regional-and-zonal-managed-instance-groups-hands-on/)
```bash
templateName="vminsttempl"
# Template
gcloud compute instance-templates create $templateName --image-family debian-9 --image-project debian-cloud --machine-type=f1-micro

# Instance group
migRegion="us-central1"
migZones="us-central1-a,us-central1-b"

# losowe 3 AZ
regionalMig1="vminstgrp1"
gcloud compute instance-groups managed create $regionalMig1 --template $templateName --base-instance-name $templateName --size 3 --region $migRegion

# Wybrane AZ
regionalMig2="vminstgrp2"
gcloud compute instance-groups managed create $regionalMig2 --template $templateName --base-instance-name $templateName --size 3 --zones $migZones

# Wyłączenie modelu redystrybucji
regionalMig3="vminstgrp3"
gcloud beta compute instance-groups managed create $regionalMig3 --template $templateName --base-instance-name $templateName --size 3 --zones $migZones --instance-redistribution-type NONE

# Usunięcie
gcloud compute instance-groups managed delete $regionalMig1 --region $migRegion
gcloud compute instance-groups managed delete $regionalMig2 --region $migRegion
gcloud compute instance-groups managed delete $regionalMig3 --region $migRegion
gcloud compute instance-templates delete $templateName

```