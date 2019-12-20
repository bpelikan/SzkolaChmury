# [Custom Image](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-3-compute-engine/images-hands-on/)


```bash
# Tworzenie image z dysku
gcloud compute images create my-image --source-disk=szk1-vm --source-disk-zone=europe-west2-a

# Eksport Custom Image na storage
gcloud compute images export --destination-uri gs://szkolachmury747/wpimage1.tar.gz --image my-image
```