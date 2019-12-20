# [Snapshot](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-3-compute-engine/snapshots/)

## Profile konfiguracyjne
```bash
# Lista projektów
gcloud projects list

# Sprawdzenie profilu konfiguracyjnego - domyślne wartości
gcloud config list

# Lista konfiguracji
gcloud config configurations list

# Tworzenie nowej konfiguracji
gcloud config configurations create szkolachmury

# Ustawienie projektu
gcloud config set project <Nazwa lub ID projektu>

# Lista dostępnych regionów
gcloud compute regions list

# Ustawienie domyślnego regionu dla compute
gcloud config set compute/region us-central1
```

## Tworzenie VM
```bash
# Stworzenie instancji VM
gcloud compute instances create vm1a --machine-type=f1-micro --zone=us-central1-a

# Stworzenie dysku
gcloud compute disks create vmdisk1a --size=50GB --zone-us=central1-a

# Lista dysków
gcloud compute disks list

# Podpięcie dysku do VM
gcloud compute instances attach-disk vm1a --disk=vmdisk1a --zone=us-central1-a
```

### Połączenie się do VM przez SSH
```bash
# podgląd dysków
sudo lsblk
# formatowanie dysku
sudo mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb

# podpięcie dysku do folderu
sudo mkdir -p /disk2
sudo mount -o discard,defaults /dev/sdb /disk2
sudo chmod a+w /disk2

# utworzenie pliku na dysku
cd /disk2
echo "test1" > file1.txt
cat file1.txt
```

## Tworzenie snapshota

```bash
Stworzenie snapshota dysku
gcloud compute disks snapshot vmdisk1a --snapshot-names vmdisk1a-snapshot-1 --zone=us-central1-a

Sprawdzenie snapshotów
gcloud compute snapshots list
```

## Wykorzystanie snapshota do utworzenia nowego dysku
```bash
# Utworzenie nowej instancji VM
gcloud compute instances create vm1c --machine-type=f1-micro --zone=us-central1-c

# Utworznie dysku ze snapshota
gcloud compute disks create vmdisk1c --source-snapshot=vmdisk1a-snapshot-1 --zone=us-central1-c

# Podpięcie dysku do VM
gcloud compute instances attach-disk vm1c --disk vmdisk1c --zone us-central1-c
```