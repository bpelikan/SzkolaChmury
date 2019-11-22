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

<details>
  <summary><b><i>Przed symulacją</i></b></summary>

```PowerShell
PS C:\WINDOWS\system32> kubectl get hpa -w
NAME   REFERENCE        TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web    Deployment/web   0%/80%    1         10        1          9m38s

PS C:\WINDOWS\system32> kubectl get pod
NAME                   READY   STATUS    RESTARTS   AGE
web-5658897b65-82gk8   1/1     Running   0          13m
```
</details>

<details>
  <summary><b><i>W trakcie symulacji</i></b></summary>

```PowerShell
PS C:\WINDOWS\system32> kubectl get hpa -w
NAME   REFERENCE        TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web    Deployment/web   0%/80%    1         10        1          11m
web    Deployment/web   236%/80%   1         10        1          11m
web    Deployment/web   236%/80%   1         10        3          12m
web    Deployment/web   150%/80%   1         10        3          12m
web    Deployment/web   150%/80%   1         10        4          13m
web    Deployment/web   74%/80%    1         10        4          13m 

PS C:\WINDOWS\system32> kubectl get pod
NAME                   READY   STATUS    RESTARTS   AGE
web-5658897b65-82gk8   1/1     Running   0          16m
web-5658897b65-d9xgj   1/1     Running   0          2m50s
web-5658897b65-fkqhw   1/1     Running   0          110s
web-5658897b65-qw7h5   1/1     Running   0          2m50s
```
</details>


<details>
  <summary><b><i>Po zakończeniu symulacji</i></b></summary>

```PowerShell
PS C:\WINDOWS\system32> kubectl get hpa -w
NAME   REFERENCE        TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
web    Deployment/web   75%/80%   1         10        4          17m
web    Deployment/web   0%/80%    1         10        4          17m
web    Deployment/web   0%/80%    1         10        4          22m
web    Deployment/web   0%/80%    1         10        1          22m

PS C:\WINDOWS\system32> kubectl get pod
NAME                   READY   STATUS    RESTARTS   AGE
web-5658897b65-82gk8   1/1     Running   0          25m
```
</details>


# 3. Zadanie Dodatkowe

#### 3.1 HPA z symulacji nr 1
```
PS C:\WINDOWS\system32> kubectl describe hpa web
Name:                                                  web
Namespace:                                             default
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Fri, 22 Nov 2019 22:11:24 +0100
Reference:                                             Deployment/web
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  0% (0) / 80%
Min replicas:                                          1
Max replicas:                                          10
Deployment pods:                                       4 current / 4 desired
Conditions:
  Type            Status  Reason               Message
  ----            ------  ------               -------
  AbleToScale     True    ScaleDownStabilized  recent recommendations were higher than current one, applying the highest recent recommendation
  ScalingActive   True    ValidMetricFound     the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  False   DesiredWithinRange   the desired count is within the acceptable range
Events:
  Type    Reason             Age    From                       Message
  ----    ------             ----   ----                       -------
  Normal  SuccessfulRescale  8m37s  horizontal-pod-autoscaler  New size: 3; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  7m36s  horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
```


#### 3.2 HPA z symulacji nr 2
```
PS C:\WINDOWS\system32> kubectl describe hpa web
Name:                                                  web
Namespace:                                             default
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Fri, 22 Nov 2019 22:40:53 +0100
Reference:                                             Deployment/web
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  0% (0) / 80%
Min replicas:                                          1
Max replicas:                                          10
Deployment pods:                                       1 current / 1 desired
Conditions:
  Type            Status  Reason            Message
  ----            ------  ------            -------
  AbleToScale     True    ReadyForNewScale  recommended size matches current size
  ScalingActive   True    ValidMetricFound  the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  True    TooFewReplicas    the desired replica count is increasing faster than the maximum scale rate
Events:
  Type    Reason             Age   From                       Message
  ----    ------             ----  ----                       -------
  Normal  SuccessfulRescale  14m   horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  23s   horizontal-pod-autoscaler  New size: 1; reason: All metrics below target
```


# Wyczyszczenie środowiska

<details>
  <summary><b><i>Wyczyszczenie środowiska</i></b></summary>

#### Usunięcie Resource group
```bash
bartosz@Azure:~/code$ az group delete --name $resourceGroup --no-wait
```

#### Usunięcie Service Principal
```bash
bartosz@Azure:~/code$ az ad sp delete --id $servicePrincipalClientId
```

#### Usunięcie pliku
```bash
bartosz@Azure:~/code$ rm auth.json
```

</details>

# Pliki

* [pod.yaml](./code/pod.yaml)