# [Migration, Duplication and Moving Machines](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-3-compute-engine/migration-duplication-and-moving-machines-hands-on/)

### Przeniesienie VM pomiędzy zonami w tym samym regionie
```bash
# Lista instancji
gcloud compute instances list

# Przeniesienie instancji wordpress-1a-vm z us-central1-a do us-central1-b
gcloud compute instances move wordpress-1a-vm --zone=us-central1-a --destination-zone=us-central1-b
```

### Przeniesienie VM do innego regionu
```bash
# Lista dostępnych regionów
gcloud compute zones list

# Lista instancji VM
gcloud compute instances list

# Lista dysków
gcloud compute disks list

# Wyłączenie auto-delete dysku
gcloud compute instances set-disk-auto-delete wordpress-1a-vm --zone us-central1-b --disk wordpress-1a-vm --no-auto-delete

# Snapshot dysku
gcloud compute disks snapshot wordpress-1a-vm --snapshot-names backup-snapshot-wordpress-1a-vm --zone us-central1-b
gcloud compute disks snapshot wordpress-1a-vm --snapshot-names snapshot-wordpress-1a-vm --zone us-central1-b

# Lista snapshotów
gcloud compute snapshots list

# Stworzenie dysku w nowym regionie
gcloud compute disks create wordpress-2a --source-snapshot snapshot-wordpress-1a-vm --zone europe-west1-b

# Stworzenie VM w nowym regionie
gcloud compute instances create wordpress-2a-vm --machine-type=f1-micro --zone europe-west1-b --disk name=wordpress-2a,boot=yes,mode=rw

# Dodanie reguły firewall
gcloud compute instances add-tags wordpress-2a-vm --zone europe-west1-b --tags http-server
```


