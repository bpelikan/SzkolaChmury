# Praca Domowa nr 8

<details>
  <summary><b><i>Przygotowanie contextu oraz namespace</i></b></summary>

#### Utworzenie namespace
```PowerShell
PS C:\WINDOWS\system32> kubectl create namespace homework8
namespace/homework8 created
```

#### Zmiana contextu na utworzony namepsace
```PowerShell
PS C:\WINDOWS\system32> kubectl config set-context --current --namespace=homework8
Context "minikube" modified.

PS C:\WINDOWS\system32> kubectl config get-contexts
CURRENT   NAME                 CLUSTER          AUTHINFO                              NAMESPACE
          docker-desktop       docker-desktop   docker-desktop
          docker-for-desktop   docker-desktop   docker-desktop
*         minikube             minikube         minikube                              homework8
```

</details>

#### 1. Wykonanie deploymentu
```PowerShell
PS C:\Users\bpelikan> kubectl apply -f depl.yaml
deployment.apps/nginx-deployment created
```

<details>
  <summary><b><i>Sprawdzenie deploymentu</i></b></summary>

#### 1.1 Sprawdzenie deploymentu
```PowerShell
PS C:\Users\bpelikan> kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           94s
```

#### 1.2 Sprawdzenie statusu deploymentu
```PowerShell
PS C:\Users\bpelikan> kubectl rollout status deployment nginx-deployment
deployment "nginx-deployment" successfully rolled out
```

#### 1.3 Sprawdzenie ReplicaSetu
```PowerShell
PS C:\Users\bpelikan> kubectl get rs
NAME                          DESIRED   CURRENT   READY   AGE
nginx-deployment-54f57cf6bf   3         3         3       4m37s
```

#### 1.4 Przejrzenie labeli utworzonych dla podów
```PowerShell
PS C:\Users\bpelikan> kubectl get pods --show-labels
NAME                                READY   STATUS    RESTARTS   AGE     LABELS
nginx-deployment-54f57cf6bf-8zt4j   1/1     Running   0          6m32s   app=nginx,pod-template-hash=54f57cf6bf
nginx-deployment-54f57cf6bf-lxpkr   1/1     Running   0          6m32s   app=nginx,pod-template-hash=54f57cf6bf
nginx-deployment-54f57cf6bf-sfcvg   1/1     Running   0          6m32s   app=nginx,pod-template-hash=54f57cf6bf
```

</details>

#### 2. Wystawienie portu kontenera na zewnątrz
Wystawienie portu 80 kontenera na zewnątrz za pomocą portu 8080
```PowerShell
PS C:\Users\bpelikan> kubectl port-forward nginx-deployment-54f57cf6bf-8zt4j 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

![nginx](./img/20191116234548.jpg "nginx")

</details>


#### 
```PowerShell

```

#### 
```PowerShell

```





#### 
```PowerShell

```







# Pliki

* [depl.yaml](./code/depl.yaml)
* [depl2.yaml](./code/depl2.yaml)