# Praca Domowa nr 10

* [Przygotowanie środowiska](#1-przygotowanie-środowiska)
* [Zapoznanie się z RBAC](#2-zapoznanie-się-z-rbac)
* [Zadanie](#1-zadanie)
* [Pliki](#pliki)

## 1. Przygotowanie środowiska

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

### 1.1 Azure AD application dla serwera

#### 1.1.1 Utworzenie Azure AD application dla serwera
```bash
az ad app create --display-name "${aksName}Server" --identifier-uris "https://${aksName}Server" -o json > serverapp.json
serverApplicationId=$(jq -r ".appId" serverapp.json)
```
<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130155206.jpg "portal")
</details>

#### 1.1.2 Aktualizacja application group memebership claims
```bash
az ad app update --id $serverApplicationId --set groupMembershipClaims=All
```
<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130155505.jpg "portal")
</details>

#### 1.1.3 Utworzenie Service Principal
```bash
az ad sp create --id $serverApplicationId
```

#### 1.1.4 Pobranie sekretu z utworzonego Service Principal
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
az ad app permission admin-consent --id  $serverApplicationId
```
<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130163838.jpg "portal")
</details>

### 1.2 Azure AD application dla klienta

#### 1.2.1 Utworzenie Azure AD application dla klienta
```bash
az ad app create --display-name "${aksName}Client" --native-app --reply-urls "https://${aksName}Client" -o json > clientapp.json
clientApplicationId=$(jq -r ".appId" clientapp.json)
```

<details>
  <summary><b><i>Portal</i></b></summary>

![portal](./img/20191130164750.jpg "portal")
</details>

#### 1.2.2 Utworzenie Service Principal
```bash
az ad sp create --id $clientApplicationId
```

#### 1.2.3 Pobranie oAuth2 ID z Azure AD application serwera
```bash
az ad app show --id $serverApplicationId -o json > clientSP.json
oAuthPermissionId=$(jq -r ".oauth2Permissions[0].id" clientSP.json)
```

#### 1.2.4 Dodanie uprawnień dla klienta
Dodanie uprawnień dla klienta do komunikacji z serwerem z wykorzystaniem `oAuth2 communication flow`.
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

#### 1.3.3 Utworzenie Service Principal
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

## 2. Zapoznanie się z RBAC

#### 2.1 Pobranie AKS ID
```bash
az aks show --resource-group $resourceGroup --name $aksName -o json > aksInfo.json
AKS_ID=$(jq -r ".id" aksInfo.json)
```

#### 2.2 Utworzenie grup `dev` oraz `ops` w AD
```bash
devGroupName="appdev"
az ad group create --display-name $devGroupName --mail-nickname $devGroupName -o json > appdev.json
APPDEV_ID=$(jq -r ".objectId" appdev.json)

opsGroupName="opssre"
az ad group create --display-name $opsGroupName --mail-nickname $opsGroupName -o json > opssre.json
OPSSRE_ID=$(jq -r ".objectId" opssre.json)
```

#### 2.3 Przypisanie ról dla grup
Przypisanie ról do grup dev oraz ops w celu umożliwienia korzystania z AKS
```bash
az role assignment create --assignee $APPDEV_ID --role "Azure Kubernetes Service Cluster User Role" --scope $AKS_ID

az role assignment create --assignee $OPSSRE_ID --role "Azure Kubernetes Service Cluster User Role" --scope $AKS_ID
```

#### 2.4 Utworzenie kont
```bash
domainName="<Nawa domeny>"
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

#### 2.9 Zalogowanie się na `aksdev`
```bash
PS C:\WINDOWS\system32> az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing
PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-dev --image=nginx --namespace dev

To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code CAUH6PZEZ to authenticate.
```

> Zalogowanie się na `aksdev` i sprawdzenie jakie operacje może wykonać.

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


#### 2.10 Zalogowanie się na `akssre`
```bash
PS C:\WINDOWS\system32> az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing
PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-sre --image=nginx --namespace sre
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code CDKFUSJUW to authenticate.
pod/nginx-sre created
```
> Zalogowanie się na `akssre` i sprawdzenie jakie operacje może wykonać.

```bash
PS C:\WINDOWS\system32> kubectl get pods --namespace sre
NAME        READY   STATUS    RESTARTS   AGE
nginx-sre   1/1     Running   0          38s

PS C:\WINDOWS\system32> kubectl get pods --all-namespaces
Error from server (Forbidden): pods is forbidden: User "akssre@<...>.onmicrosoft.com" cannot list resource "pods" in API group "" at the cluster scope

PS C:\WINDOWS\system32> kubectl run --generator=run-pod/v1 nginx-sre --image=nginx --namespace dev
Error from server (Forbidden): pods is forbidden: User "akssre@<...>.onmicrosoft.com" cannot create resource "pods" in API group "" in the namespace "dev"
```

```

#### 2.4 Utworzenie grupy ops w AD
```bash
opsGroupName="opssre"
az ad group create --display-name $opsGroupName --mail-nickname $opsGroupName -o json > opssre.json
OPSSRE_ID=$(jq -r ".objectId" opssre.json)
```

#### 2.5 Przypisanie roli dla grupy ops
```bash
az role assignment create --assignee $OPSSRE_ID --role "Azure Kubernetes Service Cluster User Role" --scope $AKS_ID
```








<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

---

## Wyczyszczenie środowiska

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

* [depl.yaml](./code/depl.yaml)