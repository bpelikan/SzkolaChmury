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

## 3.6 Przenoszenie instancji pomiędzy regionami

#### 3.6.1 Stworzenie dysku ze snapshota
Wyświetlenie wszystkich dysków
```
bartosz@cloudshell:~ (resonant-idea-261413)$ gcloud compute disks list
NAME        LOCATION        LOCATION_SCOPE  SIZE_GB  TYPE         STATUS
instance-1  europe-west3-a  zone            10       pd-standard  READY
```

Wyświetlenie snapshotów
```
bartosz@cloudshell:~ (resonant-idea-261413)$ gcloud compute snapshots list
NAME        DISK_SIZE_GB  SRC_DISK                         STATUS
snapshot-1  10            europe-west3-b/disks/instance-1  READY
```

Sprawdzenie listy dostępnych zone:
```
bartoszpelikan@cloudshell:~ (resonant-idea-261413)$ gcloud compute zones list
NAME                       REGION                   STATUS  NEXT_MAINTENANCE  TURNDOWN_DATE
asia-northeast2-a          asia-northeast2          UP
```

Utworzenie nowego dysku ze snapshota
```
bartosz@cloudshell:~ (resonant-idea-261413)$ gcloud compute disks create instance-2 --source-snapshot snapshot-1 --zone asia-northeast2-a
Created [https://www.googleapis.com/compute/v1/projects/resonant-idea-261413/zones/asia-northeast2-a/disks/instance-2].
NAME        ZONE               SIZE_GB  TYPE         STATUS
instance-2  asia-northeast2-a  10       pd-standard  READY
```

#### 3.6.2 Utworzenie nowej instancji
Utworzenie nowej instancji VM:
```
bartosz@cloudshell:~ (resonant-idea-261413)$ gcloud compute instances create instance-2 --machine-type f1-micro --disk name=instance-2,boot=yes,mode=rw --zone asia-northeast2-a
Created [https://www.googleapis.com/compute/v1/projects/resonant-idea-261413/zones/asia-northeast2-a/instances/instance-2].
NAME        ZONE               MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
instance-2  asia-northeast2-a  f1-micro                   10.174.0.2   34.97.196.225  RUNNING
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

![ComputeEngine](./img/20191208205237.jpg "ComputeEngine")
</details>


## 4. Uruchomienie skryptów startowych

<details>
  <summary><b><i>Utworzenie nowej instancji VM</i></b></summary>

![ComputeEngine](./img/20191208211154.jpg "ComputeEngine")
![ComputeEngine](./img/20191208211249.jpg "ComputeEngine")
</details>

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

![ComputeEngine](./img/20191208211354.jpg "ComputeEngine")
</details>