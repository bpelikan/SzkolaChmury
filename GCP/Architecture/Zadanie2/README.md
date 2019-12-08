# Zadanie domowe nr 2

# Billing

## 1. Eksport danych rozliczeniowych do BigQuery

#### 1.1 Utworzenie Datasetu w BigQuery

<details>
  <summary><b><i>Pokaż</i></b></summary>

![BigQuery](./img/20191208191122.jpg "BigQuery")
![BigQuery](./img/20191208190913.jpg "BigQuery")
</details>

#### 1.2 Eksport bilingu do BigQuery

<details>
  <summary><b><i>Pokaż</i></b></summary>

![BillingExport](./img/20191208184604.jpg "BillingExport")
![BillingExport](./img/20191208185404.jpg "BillingExport")
![BillingExport](./img/20191208185448.jpg "BillingExport")
</details>

## 2. Eksport danych rozliczeniowych do pliku

#### 2.1 Utworzenie Bucketa w Cloud Storage

<details>
  <summary><b><i>Pokaż</i></b></summary>

![CloudStorage](./img/20191208192059.jpg "CloudStorage")
![CloudStorage](./img/20191208192350.jpg "CloudStorage")
![CloudStorage](./img/20191208192457.jpg "CloudStorage")
![CloudStorage](./img/20191208192434.jpg "CloudStorage")
</details>

#### 2.1 Eksport danych do pliku CSV

<details>
  <summary><b><i>Pokaż</i></b></summary>

![CloudStorage](./img/20191208192726.jpg "CloudStorage")
![CloudStorage](./img/20191208192928.jpg "CloudStorage")
![CloudStorage](./img/20191208192936.jpg "CloudStorage")
</details>


# Compute Engine

## 3.1 Utworzenie oraz uruchamianie instancji

<details>
  <summary><b><i>Pokaż</i></b></summary>

![ComputeEngine](./img/20191208194255.jpg "ComputeEngine")
![ComputeEngine](./img/20191208194713.jpg "ComputeEngine")
![ComputeEngine](./img/20191208194821.jpg "ComputeEngine")
</details>

## 3.2 Odłączenie dysku startowego

<details>
  <summary><b><i>Pokaż</i></b></summary>

![ComputeEngine](./img/20191208195218.jpg "ComputeEngine")
![ComputeEngine](./img/20191208195232.jpg "ComputeEngine")
![ComputeEngine](./img/20191208195408.jpg "ComputeEngine")
</details>

## 3.3 Ponowne podłączenie dysku startowego

<details>
  <summary><b><i>Pokaż</i></b></summary>

![ComputeEngine](./img/20191208195425.jpg "ComputeEngine")
![ComputeEngine](./img/20191208195456.jpg "ComputeEngine")
![ComputeEngine](./img/20191208195520.jpg "ComputeEngine")
</details>

## 3.4 Snapshot dysku

<details>
  <summary><b><i>Pokaż</i></b></summary>

![ComputeEngine](./img/20191208200523.jpg "ComputeEngine")
![ComputeEngine](./img/20191208200614.jpg "ComputeEngine")
![ComputeEngine](./img/20191208200703.jpg "ComputeEngine")
</details>

## 3.5 Przenoszenie instancji pomiędzy strefami

```
gcloud compute instances move instance-1 --zone europe-west3-b --destination-zone europe-west3-a
```

<details>
  <summary><b><i>Pokaż</i></b></summary>

![ComputeEngine](./img/20191208201456.jpg "ComputeEngine")
![ComputeEngine](./img/20191208201813.jpg "ComputeEngine")
</details>