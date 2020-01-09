# [INSTANCE GROUPS I AUTOSKALOWANIE](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/)


#### [Instance Templates](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/instance-templates-hands-on/)
```bash
instanceGroupName="instance-vm-group"

# Konfiguracja autoskalowania
gcloud compute instance-groups managed set-autoscaling $instanceGroupName --min-num-replicas 5 --max-num-replicas 10 --zone=us-central1-a
```

#### [Rolling Updates](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/rolling-updates-hands-on/)
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