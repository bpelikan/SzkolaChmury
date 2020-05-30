# [Zadanie domowe nr 13](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-13-serverless-i-big-data/zadanie-domowe-nr-13/)



![schemat](./img/schemat.jpg)


#### Utworzenie projektu
```bash
PROJECT_NAME="zadanie13"
gcloud projects create $PROJECT_NAME
PROJECT_ID=$(gcloud config get-value core/project)
```

#### Utworzenie topica w Cloud Pub/Sub
```bash
# Topic
TOPIC_NAME="rawdata"
gcloud pubsub topics create $TOPIC_NAME
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

#### Utworzenie Bucketa
```bash
BUCKET_NAME=$PROJECT_ID-bucket
REGION="us-central1"

gsutil mb -c STANDARD -l $REGION gs://${BUCKET_NAME}/
```

#### Przygotowanie środowiska dla Apache Beam
```bash
sudo pip3 install -U pip
sudo pip3 install --upgrade virtualenv
virtualenv -p python3.7 env
source env/bin/activate

pip install apache-beam[gcp]
```

#### Uruchomienie
```bash
python beam.py \
  --project $PROJECT_ID \
  --topic projects/$PROJECT_ID/topics/$TOPIC_NAME \
  --output gs://$BUCKET_NAME/samples/output \
  --runner DirectRunner 
```
  --input gs://dataflow-samples/shakespeare/kinglear.txt \
  --output gs://$BUCKET_NAME/wordcount/outputs \
  --runner DataflowRunner
```
```
```