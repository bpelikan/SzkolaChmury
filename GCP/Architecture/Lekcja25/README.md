# [Migration, Duplication and Moving Machines](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-3-compute-engine/migration-duplication-and-moving-machines-hands-on/)

### Przeniesienie VM pomiędzy zonami w tym samym regionie
```bash
# Lista instancji
gcloud compute instances list

# Przeniesienie instancji wordpress-1a-vm z us-central1-a do us-central1-b
gcloud compute instances move wordpress-1a-vm --zone=us-central1-a --destination-zone=us-central1-b
```

