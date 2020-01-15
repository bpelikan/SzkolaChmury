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