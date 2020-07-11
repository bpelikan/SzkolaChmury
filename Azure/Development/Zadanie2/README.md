# [Zadanie domowe nr 2](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-2-podstawy-pracy-z-gcp/zadanie-domowe-nr-2/)

## 1. Utworzenie `Resource Group`

#### 1.1 Azure Portal

![](./img/20200711200638.jpg)
![](./img/20200711200653.jpg)
![](./img/20200711200854.jpg)
#### 1.2 Azure CLI

```bash
RG_NAME="rg-azdev-zad2-cli"
RG_LOCATION="westeurope"

az group create -n $RG_NAME -l $RG_LOCATION 
```