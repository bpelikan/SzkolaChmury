# Praca Domowa nr 8

<details>
  <summary><b><i>Przygotowanie contextu oraz namespace</i></b></summary>

#### Utworzenie namespace
```PowerShell
PS C:\Users\bpelikan> kubectl create namespace homework8
namespace/homework8 created
```

#### Zmiana contextu na utworzony namepsace
```PowerShell
PS C:\Users\bpelikan> kubectl config set-context --current --namespace=homework8
Context "minikube" modified.

PS C:\Users\bpelikan> kubectl config get-contexts
CURRENT   NAME                 CLUSTER          AUTHINFO                              NAMESPACE
          docker-desktop       docker-desktop   docker-desktop
          docker-for-desktop   docker-desktop   docker-desktop
*         minikube             minikube         minikube                              homework8
```

</details>

# Zadanie 1

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

# Zadanie 2

#### 2. Wystawienie portu kontenera na zewnątrz
Wystawienie portu 80 kontenera na zewnątrz za pomocą portu 8080
```PowerShell
PS C:\Users\bpelikan> kubectl port-forward nginx-deployment-54f57cf6bf-8zt4j 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

#### 2.1 Sprawdzenie nagłówków
```PowerShell
PS C:\Users\bpelikan> bash
ubpelikan@DESKTOP:/mnt/c/Users/bpelikan$ curl -I -X GET http://localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.7.9
Date: Sat, 16 Nov 2019 22:48:51 GMT
Content-Type: text/html
Content-Length: 612
Last-Modified: Tue, 23 Dec 2014 16:25:09 GMT
Connection: keep-alive
ETag: "54999765-264"
Accept-Ranges: bytes
```

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