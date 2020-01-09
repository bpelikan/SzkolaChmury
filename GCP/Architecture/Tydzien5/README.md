# [INSTANCE GROUPS I AUTOSKALOWANIE](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/)


#### [Instance Templates](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/instance-templates-hands-on/)
```bash
instanceGroupName="instance-vm-group"

# Konfiguracja autoskalowania
gcloud compute instance-groups managed set-autoscaling $instanceGroupName --min-num-replicas 5 --max-num-replicas 10 --zone=us-central1-a
```
