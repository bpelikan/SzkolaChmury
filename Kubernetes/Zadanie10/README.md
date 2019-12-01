# Praca Domowa nr 10 - Role i uprawnienia

* [Przygotowanie środowiska](#1-przygotowanie-środowiska)
* [Zapoznanie się z RBAC](#2-zapoznanie-się-z-rbac)
* [Zadanie](#3-zadanie)
* [Wyczyszczenie środowiska](#4-wyczyszczenie-środowiska)
* [Pliki](#pliki)

## 1. [Przygotowanie środowiska](https://docs.microsoft.com/en-us/azure/aks/azure-ad-integration-cli)

<details>
  <summary><b><i>Przygotowanie środowiska</i></b></summary>

#### 1.0 Przygotowanie folderu oraz zmiennych
```bash
mkdir code
cd code

location="westeurope"
resourceGroup="szkchm-zadanie10"
aksName="akszad10"
```

### 1.1 `Azure AD Application` dla serwera

#### 1.1.1 Utworzenie `Azure AD Application` dla serwera
```bash
az ad app create --display-name "${aksName}Server" --identifier-uris "https://${aksName}Server" -o json > serverapp.json
serverApplicationId=$(jq -r ".appId" serverapp.json)
```
<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130155206.jpg "portal")
</details>

#### 1.1.2 Aktualizacja `Application Group Memebership Claims`
```bash
az ad app update --id $serverApplicationId --set groupMembershipClaims=All
```
<details>
  <summary><b><i>Portal</i></b></summary>

Na zmianę w portalu trzeba chwilkę poczekać
![portal](./img/20191130155505.jpg "portal")
</details>

#### 1.1.3 Utworzenie `Service Principal` dla aplikacji serwera
```bash
az ad sp create --id $serverApplicationId
```

#### 1.1.4 Pobranie sekretu z utworzonego `Service Principal`
```bash
az ad sp credential reset --name $serverApplicationId --credential-description "AKSPassword" -o json > serverSPsecret.json
serverApplicationSecret=$(jq -r ".password" serverSPsecret.json)
```
<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130160307.jpg "portal")
</details>

#### 1.1.5 Dodanie uprawnień
```bash
az ad app permission add --id $serverApplicationId --api 00000003-0000-0000-c000-000000000000 --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope 06da0dbc-49e2-44d2-8312-53f166ab848a=Scope 7ab1d382-f21e-4acd-a863-ba3e13f7da61=Role
```

#### 1.1.6 Przyznanie uprawnień
```bash
az ad app permission grant --id $serverApplicationId --api 00000003-0000-0000-c000-000000000000
az ad app permission admin-consent --id $serverApplicationId
```
Niestety nie znalazłem listy z opisem Guidów z `--api-permissions`. Na GitHubie w chwili obecnej jest otwarty [Issue](https://github.com/Azure/azure-cli/issues/11354).
Dodatkowo polecenie `az ad app permission admin-consent --id` w chwili obecnej nie działa w Cloud Shell, należy wykorzystać lokalne CLI lub wyklikać w Portalu ([Issue](https://github.com/Azure/azure-cli/issues/8912)).
<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130163838.jpg "portal")
</details>

### 1.2 `Azure AD Application` dla klienta

#### 1.2.1 Utworzenie `Azure AD Application` dla klienta
```bash
az ad app create --display-name "${aksName}Client" --native-app --reply-urls "https://${aksName}Client" -o json > clientapp.json
clientApplicationId=$(jq -r ".appId" clientapp.json)
```

<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130164750.jpg "portal")
</details>

#### 1.2.2 Utworzenie `Service Principal` dla klienta
```bash
az ad sp create --id $clientApplicationId
```

#### 1.2.3 Pobranie `oAuth2 ID` z `Azure AD Application` serwera
```bash
az ad app show --id $serverApplicationId -o json > clientSP.json
oAuthPermissionId=$(jq -r ".oauth2Permissions[0].id" clientSP.json)
```

#### 1.2.4 Dodanie uprawnień dla klienta
Dodanie uprawnień dla klienta do komunikacji (z wykorzystaniem `oAuth2 communication flow`) z serwerem .
```bash
az ad app permission add --id $clientApplicationId --api $serverApplicationId --api-permissions $oAuthPermissionId=Scope
```

#### 1.2.5 Przyznanie uprawnień dla klienta
Przyznanie uprawnień dla klienta do komunikacji z serwerem.
```bash
az ad app permission grant --id $clientApplicationId --api $serverApplicationId
```
<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130170621.jpg "portal")
</details>

### 1.3 Utworzenie AKS

#### 1.3.1 Utworznie Resource Group
```bash
az group create --location $location --name $resourceGroup
```
#### 1.3.2 Pobranie Tenant ID
```bash
az account show -o json > accountInfo.json
tenantId=$(jq -r ".tenantId" accountInfo.json)
```

#### 1.3.3 Utworzenie `Service Principal`
```bash
az ad sp create-for-rbac --skip-assignment -o json > auth.json
servicePrincipalClientId=$(jq -r ".appId" auth.json)
servicePrincipalClientSecret=$(jq -r ".password" auth.json)
```

#### 1.3.4 Utworzenie klastra
```bash
az aks create --generate-ssh-keys -g $resourceGroup -n $aksName --node-count 1 --location $location --aad-server-app-id $serverApplicationId --aad-server-app-secret $serverApplicationSecret --aad-client-app-id $clientApplicationId --aad-tenant-id $tenantId --service-principal $servicePrincipalClientId --client-secret $servicePrincipalClientSecret 
```

#### 1.3.5 Pobranie credentials dla AKS
```bash
az aks get-credentials --resource-group $resourceGroup --name $aksName --admin
```

#### 1.3.6 Dodanie obecnie zalogowanego użytkownika jako Cluster Admin
```bash
az ad signed-in-user show -o json > signedUser.json
userPrincipalName=$(jq -r ".userPrincipalName" signedUser.json)

curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/basic-azure-ad-binding.yaml > basic-azure-ad-binding.yaml
sed -i "s|<userPrincipalName>|${userPrincipalName}|g" basic-azure-ad-binding.yaml
kubectl apply -f basic-azure-ad-binding.yaml
```
</details>

## 2. [Zapoznanie się z RBAC](https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac)

<details>
  <summary><b><i>Zapoznanie się z RBAC</i></b></summary>

#### 2.1 Pobranie AKS ID
```bash
az aks show --resource-group $resourceGroup --name $aksName -o json > aksInfo.json
AKS_ID=$(jq -r ".id" aksInfo.json)
```

#### 2.2 Utworzenie grup `dev` oraz `ops` w AAD
```bash
devGroupName="appdev"
az ad group create --display-name $devGroupName --mail-nickname $devGroupName -o json > appdev.json
APPDEV_ID=$(jq -r ".objectId" appdev.json)

opsGroupName="opssre"
az ad group create --display-name $opsGroupName --mail-nickname $opsGroupName -o json > opssre.json
OPSSRE_ID=$(jq -r ".objectId" opssre.json)
```

#### 2.3 Przypisanie ról do grup
Przypisanie ról do grup dev oraz ops w celu umożliwienia korzystania z AKS
```bash
az role assignment create --assignee $APPDEV_ID --role "Azure Kubernetes Service Cluster User Role" --scope $AKS_ID

az role assignment create --assignee $OPSSRE_ID --role "Azure Kubernetes Service Cluster User Role" --scope $AKS_ID
```

#### 2.4 Utworzenie kont
```bash
domainName="<Nawa domeny>" #należy wpisać nazwę swojej domeny AAD, można ją znaleźć wchodząc w Azure Active Directory -> w zakładce Manage: Custom domain names
defaultUserPassword="<Domyślne hasło>"

az ad user create --display-name "AKS Dev" --user-principal-name "aksdev@${domainName}" --password $defaultUserPassword -o json > user1.json
az ad user create --display-name "AKS SRE" --user-principal-name "akssre@${domainName}" --password $defaultUserPassword -o json > user2.json

AKSDEV_ID=$(jq -r ".objectId" user1.json)
AKSSRE_ID=$(jq -r ".objectId" user2.json)
```

#### 2.5 Przypisanie kont do grup
```bash
az ad group member add --group $devGroupName --member-id $AKSDEV_ID
az ad group member add --group $opsGroupName --member-id $AKSSRE_ID
```

#### 2.6 Utworzenie namespace dla grup w AKS
```bash
kubectl create namespace dev
kubectl create namespace sre
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code$ kubectl get namespace
NAME          STATUS   AGE
default       Active   118m
dev           Active   8m40s
kube-public   Active   118m
kube-system   Active   118m
sre           Active   7s
```
</details>

#### 2.7 Utworzenie ról w AKS
```bash
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/role-dev-namespace.yaml > role-dev-namespace.yaml
kubectl apply -f role-dev-namespace.yaml

curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/role-sre-namespace.yaml > role-sre-namespace.yaml
kubectl apply -f role-sre-namespace.yaml
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code$ kubectl get role -A
NAMESPACE     NAME                                             AGE
dev           dev-user-full-access                             7m38s
kube-public   system:controller:bootstrap-signer               120m
kube-system   extension-apiserver-authentication-reader        120m
kube-system   kubernetes-dashboard-minimal                     119m
kube-system   system::leader-locking-kube-controller-manager   120m
kube-system   system::leader-locking-kube-scheduler            120m
kube-system   system:controller:bootstrap-signer               120m
kube-system   system:controller:cloud-provider                 120m
kube-system   system:controller:token-cleaner                  120m
sre           sre-user-full-access                             2s
```
</details>

#### 2.8 Role binding dla grup
```bash
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/rolebinding-dev-namespace.yaml > rolebinding-dev-namespace.yaml
sed -i "s|<groupObjectId>|${APPDEV_ID}|g" rolebinding-dev-namespace.yaml
kubectl apply -f rolebinding-dev-namespace.yaml

curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/rolebinding-sre-namespace.yaml > rolebinding-sre-namespace.yaml
sed -i "s|<groupObjectId>|${OPSSRE_ID}|g" rolebinding-sre-namespace.yaml
kubectl apply -f rolebinding-sre-namespace.yaml
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code$ kubectl get rolebinding -A
NAMESPACE     NAME                                             AGE
dev           dev-user-access                                  4m18s
kube-public   system:controller:bootstrap-signer               122m
kube-system   kubernetes-dashboard-minimal                     121m
kube-system   metrics-server-auth-reader                       121m
kube-system   node-view                                        121m
kube-system   system::leader-locking-kube-controller-manager   122m
kube-system   system::leader-locking-kube-scheduler            122m
kube-system   system:controller:bootstrap-signer               122m
kube-system   system:controller:cloud-provider                 122m
kube-system   system:controller:token-cleaner                  122m
kube-system   tunnelfront                                      121m
sre           sre-user-access                                  4s
```
</details>

#### 2.9 Zalogowanie się na użytkownika `aksdev`
```bash
PS C:\WINDOWS\system32> az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing
PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-dev --image=nginx --namespace dev

To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code CAUH6PZEZ to authenticate.
```

> Zalogowanie się na użytkownika `aksdev` i sprawdzenie jakie operacje może wykonać.

```bash
PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-dev --image=nginx --namespace dev
pod/nginx-dev created

PS C:\WINDOWS\system32> kubectl get pods --namespace dev
NAME        READY   STATUS    RESTARTS   AGE
nginx-dev   1/1     Running   0          36s

PS C:\WINDOWS\system32> kubectl get pods
Error from server (Forbidden): pods is forbidden: User "aksdev@<...>.onmicrosoft.com" cannot list resource "pods" in API group "" in the namespace "default"

PS C:\WINDOWS\system32> kubectl get pods -A
Error from server (Forbidden): pods is forbidden: User "aksdev@<...>.onmicrosoft.com" cannot list resource "pods" in API group "" at the cluster scope

PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-dev --image=nginx --namespace sre
Error from server (Forbidden): pods is forbidden: User "aksdev@<...>.onmicrosoft.com" cannot create resource "pods" in API group "" in the namespace "sre"
```
Jak można zauważyć użytkownik ten może wykonywać operacje tylko w namespace `dev`.


#### 2.10 Zalogowanie się na użytkownika `akssre`
```bash
PS C:\WINDOWS\system32> az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing
PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-sre --image=nginx --namespace sre
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code CDKFUSJUW to authenticate.
pod/nginx-sre created
```
> Zalogowanie się na użytkownika `akssre` i sprawdzenie jakie operacje może wykonać.

```bash
PS C:\WINDOWS\system32> kubectl get pods --namespace sre
NAME        READY   STATUS    RESTARTS   AGE
nginx-sre   1/1     Running   0          38s

PS C:\WINDOWS\system32> kubectl get pods --all-namespaces
Error from server (Forbidden): pods is forbidden: User "akssre@<...>.onmicrosoft.com" cannot list resource "pods" in API group "" at the cluster scope

PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-sre --image=nginx --namespace dev
Error from server (Forbidden): pods is forbidden: User "akssre@<...>.onmicrosoft.com" cannot create resource "pods" in API group "" in the namespace "dev"
```
Jak widać użytkownik nie ma uprawnień do wykonywania operacji na innym namespace niż `sre`.

</details>

## 3. Zadanie

<details>
  <summary><b><i>Zadanie</i></b></summary>

#### 3.1 Utworzenie nowych użytkowników
```bash
az ad user create --display-name "Test user 1" --user-principal-name "testuser1@${domainName}" --password $defaultUserPassword -o json > user3.json
az ad user create --display-name "Test user 2" --user-principal-name "testuser2@${domainName}" --password $defaultUserPassword -o json > user4.json

USER3_NAME=$(jq -r ".userPrincipalName" user3.json)
USER4_NAME=$(jq -r ".userPrincipalName" user4.json)
```

#### 3.2 Utworzenie roli `pod reader` w namespace `default`
```bash
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/role-pod-reader.yaml > role-pod-reader.yaml
kubectl apply -f role-pod-reader.yaml
```

<details> 
  <summary><b><i>Sprawdzenie</i></b></summary> 

```bash
bartosz@Azure:~/code$ kubectl get role -A
NAMESPACE     NAME                                             AGE
default       pod-reader                                       8m33s
dev           dev-user-full-access                             46m
kube-public   system:controller:bootstrap-signer               159m
kube-system   extension-apiserver-authentication-reader        159m
kube-system   kubernetes-dashboard-minimal                     158m
kube-system   system::leader-locking-kube-controller-manager   159m
kube-system   system::leader-locking-kube-scheduler            159m
kube-system   system:controller:bootstrap-signer               159m
kube-system   system:controller:cloud-provider                 159m
kube-system   system:controller:token-cleaner                  159m
sre           sre-user-full-access                             38m
```
</details> 

#### 3.3 Utworzenie roli `cluster reader`
```bash
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/cluster-role-reader.yaml > cluster-role-reader.yaml
kubectl apply -f cluster-role-reader.yaml
```

<details> 
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code$ kubectl get clusterrole
NAME                                                                   AGE
admin                                                                  159m
cluster-admin                                                          159m
cluster-reader                                                         17s
container-health-log-reader                                            159m
edit                                                                   159m
(...)
view                                                                   159m
```
</details> 

### 3.4 Binding

#### 3.4.1 `Pod reader role binding`
```bash
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/rolebinding-pod-reader.yaml > rolebinding-pod-reader.yaml
sed -i "s|<UserName>|${USER3_NAME}|g" rolebinding-pod-reader.yaml
kubectl apply -f rolebinding-pod-reader.yaml
```

<details> 
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code$ kubectl get RoleBinding -A
NAMESPACE     NAME                                             AGE
default       read-pods                                        6s
dev           dev-user-access                                  48m
kube-public   system:controller:bootstrap-signer               166m
kube-system   kubernetes-dashboard-minimal                     166m
kube-system   metrics-server-auth-reader                       166m
kube-system   node-view                                        166m
kube-system   system::leader-locking-kube-controller-manager   166m
kube-system   system::leader-locking-kube-scheduler            166m
kube-system   system:controller:bootstrap-signer               166m
kube-system   system:controller:cloud-provider                 166m
kube-system   system:controller:token-cleaner                  166m
kube-system   tunnelfront                                      166m
sre           sre-user-access                                  44m
```
</details> 


#### 3.4.2 `Cluster role reader binding`
```bash
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie10/code/clusterrolebinding-reader.yaml > clusterrolebinding-reader.yaml
sed -i "s|<UserName>|${USER4_NAME}|g" clusterrolebinding-reader.yaml
kubectl apply -f clusterrolebinding-reader.yaml
```

<details> 
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code$ kubectl get ClusterRoleBinding
NAME                                                   AGE
aks-cluster-admin-binding                              168m
cluster-admin                                          168m
cluster-reader                                         20s
container-health-read-logs-global                      168m
contoso-cluster-admins                                 122m
metrics-server:system:auth-delegator                   168m
system:aks-client-node-proxier                         167m
```
</details> 


#### 3.5 Zalogowanie się na użytkownika `testuser1` - sprawdzenie dozwolonych operacji
```bash
PS C:\WINDOWS\system32> az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing
PS C:\WINDOWS\system32> kubectl get pod
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code CYR7A4U6B to authenticate.
No resources found.

PS C:\WINDOWS\system32> kubectl get pod -n default
No resources found.

PS C:\WINDOWS\system32> kubectl get svc
Error from server (Forbidden): services is forbidden: User "testuser1@<...>.onmicrosoft.com" cannot list resource "services" in API group "" in the namespace "default"

PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-sre --image=nginx
Error from server (Forbidden): pods is forbidden: User "testuser1@<...>.onmicrosoft.com" cannot create resource "pods" in API group "" in the namespace "default"

PS C:\WINDOWS\system32> kubectl get pod -A
Error from server (Forbidden): pods is forbidden: User "testuser1@<...>.onmicrosoft.com" cannot list resource "pods" in API group "" at the cluster scope
```
Użytkownik `testuser1` ma dostęp tylko do odczytu podów w namespace `default`.


#### 3.6 Zalogowanie się na użytkownika `testuser2` - sprawdzenie dozwolonych operacji
```bash
PS C:\WINDOWS\system32> az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing
PS C:\WINDOWS\system32> kubectl get pod
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code CSPRFQLCH to authenticate.
No resources found.

PS C:\WINDOWS\system32> kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.0.0.1     <none>        443/TCP   172m

PS C:\WINDOWS\system32> kubectl get pod -A
NAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGE
dev           nginx-dev                               1/1     Running   0          39m
kube-system   coredns-866fc6b6c8-ph8dm                1/1     Running   0          168m
kube-system   coredns-866fc6b6c8-xlbsx                1/1     Running   0          172m
kube-system   coredns-autoscaler-5d5695b54f-x9xm8     1/1     Running   0          172m
kube-system   kube-proxy-mnfx7                        1/1     Running   0          168m
kube-system   kubernetes-dashboard-6f697bd9f5-lthnb   1/1     Running   0          172m
kube-system   metrics-server-566bd9b4f7-p5n5c         1/1     Running   0          172m
kube-system   tunnelfront-5c47554cbf-zvhg4            1/1     Running   0          172m
sre           nginx-sre                               1/1     Running   0          34m

PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-sre --image=nginx
Error from server (Forbidden): pods is forbidden: User "testuser2@<...>.onmicrosoft.com" cannot create resource "pods" in API group "" in the namespace "default"
```
Użytkownik `testuser2` ma dostęp do odczytu wszystkich obiektów w klastrze AKS, nie ma uprawnień do tworzenia obiektów.

</details>

## 4. Wyczyszczenie środowiska

<details>
  <summary><b><i>Wyczyszczenie środowiska</i></b></summary>

#### Usunięcie Resource groupy
```bash
bartosz@Azure:~/code$ az group delete --name $resourceGroup --no-wait
```

#### Usunięcie użytkowników
```bash
bartosz@Azure:~/code$ az ad user delete --id $AKSDEV_ID
bartosz@Azure:~/code$ az ad user delete --id $AKSSRE_ID
bartosz@Azure:~/code$ az ad user delete --id $USER3_NAME
bartosz@Azure:~/code$ az ad user delete --id $USER4_NAME
```

#### Usunięcie utworzonych grup w AD
```bash
bartosz@Azure:~/code$ az ad group delete --group appdev
bartosz@Azure:~/code$ az ad group delete --group opssre
```

#### Usunięcie Service Principal
```bash
bartosz@Azure:~/code$ az ad app delete --id $serverApplicationId
bartosz@Azure:~/code$ az ad app delete --id $clientApplicationId
bartosz@Azure:~/code$ az ad sp delete --id $servicePrincipalClientId
```

#### Usunięcie plików
```bash
bartosz@Azure:~/code$ cd ..
bartosz@Azure:~$ rm -rf ./code
```

</details>

## Pliki

* [basic-azure-ad-binding.yaml](./code/basic-azure-ad-binding.yaml)
* [cluster-role-reader.yaml.yaml](./code/cluster-role-reader.yaml.yaml)
* [clusterrolebinding-reader.yaml.yaml](./code/clusterrolebinding-reader.yaml.yaml)
* [role-dev-namespace.yaml.yaml](./code/role-dev-namespace.yaml.yaml)
* [role-pod-reader.yaml.yaml](./code/role-pod-reader.yaml.yaml)
* [role-sre-namespace.yaml.yaml](./code/role-sre-namespace.yaml.yaml)
* [rolebinding-dev-namespace.yaml.yaml](./code/rolebinding-dev-namespace.yaml.yaml)
* [rolebinding-pod-reader.yaml.yaml](./code/rolebinding-pod-reader.yaml.yaml)
* [rolebinding-sre-namespace.yaml.yaml](./code/rolebinding-sre-namespace.yaml.yaml)