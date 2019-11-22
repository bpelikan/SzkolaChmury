# Praca Domowa nr 9

## Przygotowanie środowiska

<details>
  <summary><b><i>Przygotowanie AKS</i></b></summary>

#### Utworzenie Service Principal
```bash
bartosz@Azure:~/code$ az ad sp create-for-rbac --skip-assignment -o json > auth.json
```

#### Przypisanie zmiennych
```bash
bartosz@Azure:~/code$ location="westeurope"
bartosz@Azure:~/code$ resourceGroup="szkchm-zadanie9"
bartosz@Azure:~/code$ aksName="AKSZad9"
bartosz@Azure:~/code$ servicePrincipalClientId=$(jq -r ".appId" auth.json)
bartosz@Azure:~/code$ servicePrincipalClientSecret=$(jq -r ".password" auth.json)
```

#### Utworzenie Resource Group
```bash
bartosz@Azure:~/code$ az group create --location $location --name $resourceGroup
```

#### Utworzenie klastra
```bash
bartosz@Azure:~/code$ az aks create --generate-ssh-keys -g $resourceGroup -n $aksName --node-count 1 --location $location --service-principal $servicePrincipalClientId --client-secret $servicePrincipalClientSecret 
```

#### Pobranie credentials dla aks

```bash
bartosz@Azure:~/code$ az aks get-credentials --resource-group $resourceGroup --name $aksName
```

</details>

#### Utworzenie deploymentu
```bash
bartosz@Azure:~/code$ curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie9/code/depl.yaml > depl.yaml
bartosz@Azure:~/code$ kubectl apply -f depl.yaml
```

# Zadanie 1

### 1.1 Stworzenie Horizontal Pod Autoscaler
```
bartosz@Azure:~/code$ kubectl autoscale deployment web --cpu-percent=80 --min=1 --max=10
horizontalpodautoscaler.autoscaling/web autoscaled
```


<details>
  <summary><b><i>Sprawdzenie</i></b></summary>
  
```bash
bartosz@Azure:~/code$ kubectl get hpa
NAME   REFERENCE        TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web    Deployment/web   0%/80%    1         10        1          16s
```
</details>

### 1.2 Symulacja obciążenia

#### 1.2.1 Zalogowanie się do poda oraz wykonanie symulacji obciążenia

```bash
bartosz@Azure:~/code$ kubectl get po
NAME                   READY   STATUS    RESTARTS   AGE
web-5658897b65-82gk8   1/1     Running   0          6m39s
```

```bash
bartosz@Azure:~/code$ kubectl exec -it web-5658897b65-82gk8 /bin/bash
root@web-5658897b65-82gk8:/# apt-get update
root@web-5658897b65-82gk8:/# apt-get install stress
root@web-5658897b65-82gk8:/# stress -c 5
```




---
<details>
  <summary><b><i>Sprawdzenie</i></b></summary>



</details>


# Pliki

* [pod.yaml](./code/pod.yaml)