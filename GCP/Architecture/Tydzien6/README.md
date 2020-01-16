# [CLOUD STORAGE](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-6-cloud-storage/)

## [Creating and Using Cloud Storage Buckets](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-6-cloud-storage/creating-and-using-cloud-storage-buckets/)
```bash
bucketName="tydzien6bucketbp"
bucketName2="tydzien6bucketbp2"
bucketLocation="europe-west3"
#bucketURL="gs://${bucketName}/"
#bucketURL2="gs://${bucketName2}/"

# Utworzenie bucketa
gsutil mb -c STANDARD -l $bucketLocation gs://${bucketName}/
gsutil mb -c STANDARD -l $bucketLocation gs://${bucketName2}/

# Utworzenie przykładowych plików
mkdir example
cd example
for i in {1..6}; do echo "plik ${i} : ${RANDOM}" > test$i.txt; done

# Kopiowanie plików
gsutil -m cp * gs://${bucketName}/

# Rozmiar bucketa
gsutil du -s gs://${bucketName}/
gsutil du -chs gs://${bucketName}/

# Metadane bucketa
gsutil ls -L -b gs://${bucketName}/

# Skopiowanie plików
gsutil -m cp gs://${bucketName}/** gs://${bucketName2}/

# Lista plików
gsutil ls -r gs://${bucketName2}/

# Zmiana klasy storage
gsutil defstorageclass set nearline gs://${bucketName2}/
echo "testowy plik nearline class" > testnearline.txt
gsutil cp testnearline.txt gs://${bucketName2}/

# Usunięcie
gsutil rm -r gs://${bucketName}/
gsutil rm -r gs://${bucketName2}/
rm -rf ../example
```

## [Regulating Storage Access + Hands On](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-6-cloud-storage/regulating-storage-access-hands-on/)
```bash
bucketName="tydzien6bucketbp"
gsutil mb -c STANDARD -l $bucketLocation gs://${bucketName}/
mkdir example
cd example
for i in {1..6}; do echo "plik ${i} : ${RANDOM}" > test$i.txt; done
gsutil -m cp * gs://${bucketName}/

# Retencja
gsutil retention set 60s gs://${bucketName}/
gsutil rm gs://${bucketName}/test1.txt

# publikacja pliku
gsutil acl ch -u AllUsers:R gs://${bucketName}/test2.txt

# utworzenie SAS

# instalacja
sudo pip install pyopenssl
# pobranie nazwy domyślnego service accounta
gcloud iam service-accounts list
serviceAccount="162512192576-compute@developer.gserviceaccount.com"
# wygenerowanie klucza prywatnego do podpisania URL
gcloud iam service-accounts keys create key.json --iam-account $serviceAccount
# utworzenie URL
gsutil signurl -d 1m key.json gs://${bucketName}/test4.txt

gsutil rm -r gs://${bucketName}/
rm -rf ../example
```

## [Object Versioning and Lifecycle Management](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-6-cloud-storage/object-versioning-and-lifecycle-management-hands-on/)
```bash
bucketName="tydzien6bucketbp"
gsutil mb gs://${bucketName}/

# utworzenie polityki
gsutil lifecycle set policy1.json gs://${bucketName}/

# pobranie polityki
gsutil lifecycle get gs://${bucketName}/

# sprawdzenie wersjonowania plików
gsutil versioning get gs://${bucketName}/

# włączenie wersjonowania
gsutil versioning set on gs://${bucketName}/

# zmiana polityki
gsutil lifecycle set policy2.json gs://${bucketName}/

# test wersjonowania plików
gsutil cp policy1.json gs://${bucketName}/policy/policy1.json
gsutil rm gs://${bucketName}/policy/policy1.json

# przywrócenie pliku
gsutil ls -a gs://${bucketName}/
gsutil ls -a gs://${bucketName}/policy
fileGeneration="1579209893318558"
gsutil cp gs://${bucketName}/policy/policy1.json#$fileGeneration gs://${bucketName}/policy/policy-restore.json
```

policy1.json
```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {
        "type": "SetStorageClass",
        "storageClass": "NEARLINE"
        },
        "condition": {
          "age": 365,
          "matchesStorageClass": ["MULTI_REGIONAL", "STANDARD", "DURABLE_REDUCED_AVAILABILITY"]
        }
      },
      {
        "action": {
        "type": "SetStorageClass",
        "storageClass": "COLDLINE"
        },
        "condition": {
          "age": 1095,
          "matchesStorageClass": ["NEARLINE"]
        }
      }
    ]
  }
}
```

policy2.json
```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 30,
          "isLive": true
        }
      },
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 10,
          "isLive": false
        }
      }
    ]
  }
}
```
