# [Zadanie domowe nr 13](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-13-serverless-i-big-data/zadanie-domowe-nr-13/)



#### Wymagania klienta
Wymagania:
* Dane archiwalne przechowywane przez 5 lat.
* Dostęp do danych archiwalnych przy pomocy zapytań SQL
* Możliwość szybkiego odczytu i odpytywania danych z ostatnich 10 dni
* Raz na 3 dni wymagane jest stworzenie raportów porównawczych, pokazujących średnią dzienną pracę silnika przez ostatnie 3 miesiące, oraz jego obciążenie.
* Należy powiadomić użytkownika poprzez dedykowane zdarzenie o przegrzaniach silnika (temperatura powyżej 110 stopni celcjusza utrzymująca się ponad 5 min)

Dodatkowo:
* zdarzenia o przegrzaniach powinny być wysyłane do topica pub/sub
* przegranie silnika po stronie chmury
* obciążenie na poziomie 100 000 urządzeń
* rozwiązanie optymalne kosztowo

<details>
  <summary><b><i>Architektura</i></b></summary>

![schemat](./img/schemat.jpg)
</details>

#### Utworzenie projektu
```bash
PROJECT_NAME="zadanie13"
gcloud projects create $PROJECT_NAME
PROJECT_ID=$(gcloud config get-value core/project)
```

#### Utworzenie topica w Cloud Pub/Sub
```bash
TOPIC_NAME="rawdata"
gcloud pubsub topics create $TOPIC_NAME
```

#### Utworzenie Bucketa na dane archiwalne
```bash
BUCKET_NAME=$PROJECT_ID-bucket
REGION="us-central1"

gsutil mb -c STANDARD -l $REGION gs://${BUCKET_NAME}/
```

#### Utworzenie BigQuery Dataset
```bash
DATASET_NAME_10="IoTData_10"
DATASET_NAME_90="IoTData_90"
BG_LOCATION="us-east1"

bq mk --dataset --location $BG_LOCATION \
--default_table_expiration 864000 \
$PROJECT_ID:$DATASET_NAME_10

bq mk --dataset --location $BG_LOCATION \
--default_table_expiration 7948800 \
$PROJECT_ID:$DATASET_NAME_90
```

#### Przygotowanie środowiska dla Apache Beam
```bash
sudo pip3 install -U pip
sudo pip3 install --upgrade virtualenv
virtualenv -p python3.7 env
source env/bin/activate

pip install apache-beam[gcp]
pip install strict_rfc3339

# deactivate
```

#### Uruchomienie streamingu danych
```bash
python beam.py \
  --project $PROJECT_ID \
  --topic projects/$PROJECT_ID/topics/$TOPIC_NAME \
  --output_bucket gs://$BUCKET_NAME/samples/output \
  --output_bigquery $PROJECT_ID:$DATASET_NAME_10.engine \
  --output_bigquery_avg $PROJECT_ID:$DATASET_NAME_90.engine_avr \
  --runner DirectRunner
```

#### Symulacja działania urządzenia IoT
```bash
git clone https://github.com/damiansmazurek/gcp-pubsub-iotdevice.git
sed -i "s|\"PROJECT_ID\"|${PROJECT_ID}|g" gcp-pubsub-iotdevice/Dockerfile
sed -i "s|\"TOPIC_NAME\"|${TOPIC_NAME}|g" gcp-pubsub-iotdevice/Dockerfile

# zbudowanie obrazu za pomocą Cloud Build i umieszczenie go w Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/iotdevice gcp-pubsub-iotdevice

# deploy obrazu do Cloud Run
gcloud run deploy --image gcr.io/$PROJECT_ID/iotdevice --platform managed --region=us-central1
```
  --input gs://dataflow-samples/shakespeare/kinglear.txt \
  --output gs://$BUCKET_NAME/wordcount/outputs \
  --runner DataflowRunner
```
```
```