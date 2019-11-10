# Praca Domowa nr 7

* [Przygotowanie środowiska](#przygotowanie-środowiska)
* [Część 1](#część-1---azure-disk)

---


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
bartosz@Azure:~/code$ resourceGroup="szkchm-zadanie7"
bartosz@Azure:~/code$ aksName="AKSZad7"
bartosz@Azure:~/code$ servicePrincipalClientId=$(jq -r ".appId" auth.json)
bartosz@Azure:~/code$ servicePrincipalClientSecret=$(jq -r ".password" auth.json)
```

#### Utworzenie Resource Group
```bash
bartosz@Azure:~/code$ az group create --location $location --name $resourceGroup
```

#### Utworzenie klastra z RBAC
```bash
bartosz@Azure:~/code$ az aks get-versions --location westeurope --output table
bartosz@Azure:~/code$ az aks create --enable-rbac --generate-ssh-keys -g $resourceGroup -n $aksName --node-count 1 --location $location --service-principal $servicePrincipalClientId --client-secret $servicePrincipalClientSecret --kubernetes-version "1.14.8"
```

#### Pobranie credentials dla aks
```bash
bartosz@Azure:~/code$ az aks get-credentials --resource-group $resourceGroup --name $aksName
```

</details>

#### Zarejestrowanie providera dla Storage

```bash
bartosz@Azure:~/code$ az provider register --namespace 'Microsoft.Storage'
```

<details>
  <summary><b><i>Sprawdzenie providera</i></b></summary>

```bash
bartosz@Azure:~/code$ az provider show --namespace Microsoft.Storage -o table
Namespace          RegistrationPolicy    RegistrationState
-----------------  --------------------  -------------------
Microsoft.Storage  RegistrationRequired  Registered
```

![provider](./img/20191107224551.jpg "provider")

</details>

#### Utworzenie Storage Class dla Azure File
```bash
bartosz@Azure:~/code$ curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie7/code/azure-file-sc.yaml > azure-file-sc.yaml
bartosz@Azure:~/code$ kubectl apply -f azure-file-sc.yaml
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code$ kubectl get sc
NAME                PROVISIONER                AGE
azurefile           kubernetes.io/azure-file   6s
default (default)   kubernetes.io/azure-disk   37m
managed-premium     kubernetes.io/azure-disk   37m

bartosz@Azure:~/code$ kubectl describe sc/azurefile
Name:            azurefile
IsDefaultClass:  No
Annotations:     kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{},"name":"azurefile"},"mountOptions":["dir_mode=0777","file_mode=0777","uid=1000","gid=1000","mfsymlinks","nobrl","cache=none"],"parameters":{"skuName":"Standard_LRS"},"provisioner":"kubernetes.io/azure-file","reclaimPolicy":"Retain"}

Provisioner:           kubernetes.io/azure-file
Parameters:            skuName=Standard_LRS
AllowVolumeExpansion:  <unset>
MountOptions:
  dir_mode=0777
  file_mode=0777
  uid=1000
  gid=1000
  mfsymlinks
  nobrl
  cache=none
ReclaimPolicy:      Retain
VolumeBindingMode:  Immediate
Events:             <none>

bartosz@Azure:~/code$ kubectl describe sc/default
Name:            default
IsDefaultClass:  Yes
Annotations:     kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"storage.k8s.io/v1beta1","kind":"StorageClass","metadata":{"annotations":{"storageclass.beta.kubernetes.io/is-default-class":"true"},"labels":{"kubernetes.io/cluster-service":"true"},"name":"default"},"parameters":{"cachingmode":"ReadOnly","kind":"Managed","storageaccounttype":"Standard_LRS"},"provisioner":"kubernetes.io/azure-disk"}
,storageclass.beta.kubernetes.io/is-default-class=true
Provisioner:           kubernetes.io/azure-disk
Parameters:            cachingmode=ReadOnly,kind=Managed,storageaccounttype=Standard_LRS
AllowVolumeExpansion:  <unset>
MountOptions:          <none>
ReclaimPolicy:         Delete
VolumeBindingMode:     Immediate
Events:                <none>
```

</details>

#### Utworzenie cluster role oraz binding
```bash
bartosz@Azure:~/code$ curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie7/code/azure-pvc-roles.yaml > azure-pvc-roles.yaml
bartosz@Azure:~/code$ kubectl apply -f azure-pvc-roles.yaml
```

## Część 1 - Azure Disk

#### 1.1 Folder dla kustomization
```bash
mkdir kustomizationDisk
cd kustomizationDisk
```

<!-- #### Utworzenie PVC
```bash
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie7/code/azure-file-pvc.yaml > azure-file-pvc.yaml
kubectl apply -f azure-file-pvc.yaml
kubectl get pvc azurefile
``` -->

#### 1.2 Utworzenie pliku kustomization oraz dodanie do niego Secret Generatora
```bash
bartosz@Azure:~/code$ cat <<EOF >./kustomization.yaml
secretGenerator:
- name: mysql-pass
  literals:
  - password={YOUR_PASSWORD}
EOF
```

#### 1.3 Pobranie pliku deploymentu dla mysql
```bash
bartosz@Azure:~/code$ curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie7/code/mysql-deployment.yaml > mysql-deployment.yaml
```
 <!-- curl -LO https://k8s.io/examples/application/wordpress/mysql-deployment.yaml -->

#### 1.4 Pobranie pliku deploymentu dla WordPressa
```bash
bartosz@Azure:~/code$ curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Zadanie7/code/wordpress-deployment.yaml > wordpress-deployment.yaml
```

#### 1.5 Dodanie deploymentów do kustomization
```bash
bartosz@Azure:~/code$ cat <<EOF >>./kustomization.yaml 
resources:
  - mysql-deployment.yaml
  - wordpress-deployment.yaml
EOF
```

#### 1.6 Uruchomienie kustomization
```bash
bartosz@Azure:~/code$ kubectl apply -k ./
secret/mysql-pass-bkkgtkbk46 created
service/wordpress-mysql created
service/wordpress created
deployment.apps/wordpress-mysql created
deployment.apps/wordpress created
persistentvolumeclaim/mysql-pv-claim created
persistentvolumeclaim/wp-pv-claim created
```



```bash
kubectl get secrets
kubectl get pvc
kubectl get pods
kubectl get services wordpress
kubectl get svc -o wide
#minikube service wordpress --url  http://172.27.166.34:31675
kubectl delete -k ./

kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard
az aks browse --resource-group $resourceGroup --name $aksName
``` 

kubectl exec -it wordpress-74c4dc55c5-vl9m2 /bin/bash
kubectl exec -it wordpress-mysql-6975d97df5-5d2lg /bin/bash
apt update
apt install cifs-utils
`kubectl exec -it <PodName>/bin/bash`

kubectl exec -it wordpress-76fb7887cc-fwlc8 /bin/bash

```
root@wordpress-76fb7887cc-fwlc8:/var/www/html# env
HOSTNAME=wordpress-76fb7887cc-fwlc8
KUBERNETES_PORT=tcp://10.0.0.1:443
KUBERNETES_PORT_443_TCP_PORT=443
TERM=xterm
PHP_INI_DIR=/usr/local/etc/php
PHP_ASC_URL=https://secure.php.net/get/php-5.6.32.tar.xz.asc/from/this/mirror
WORDPRESS_SERVICE_HOST=10.0.224.198
KUBERNETES_SERVICE_PORT=443
WORDPRESS_DB_PASSWORD=P@ssw0rdT#st!23
KUBERNETES_SERVICE_HOST=10.0.0.1
PHP_CFLAGS=-fstack-protector-strong -fpic -fpie -O2
WORDPRESS_PORT_80_TCP_PROTO=tcp
PHP_MD5=
PHPIZE_DEPS=autoconf            dpkg-dev                file            g++             gcc             libc-dev                libpcre3-dev            make            pkg-config              re2c
PHP_URL=https://secure.php.net/get/php-5.6.32.tar.xz/from/this/mirror
WORDPRESS_PORT_80_TCP_ADDR=10.0.224.198
WORDPRESS_DB_HOST=wordpress-mysql
WORDPRESS_VERSION=4.8.3
PHP_LDFLAGS=-Wl,-O1 -Wl,--hash-style=both -pie
APACHE_ENVVARS=/etc/apache2/envvars
WORDPRESS_PORT_80_TCP=tcp://10.0.224.198:80
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3
PHP_CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2
PWD=/var/www/html
WORDPRESS_PORT=tcp://10.0.224.198:80
WORDPRESS_PORT_80_TCP_PORT=80
SHLVL=1
HOME=/root
PHP_SHA256=8c2b4f721c7475fb9eabda2495209e91ea933082e6f34299d11cba88cd76e64b
WORDPRESS_SHA1=8efc0b9f6146e143ed419b5419d7bb8400a696fc
KUBERNETES_PORT_443_TCP_PROTO=tcp
APACHE_CONFDIR=/etc/apache2
KUBERNETES_SERVICE_PORT_HTTPS=443
PHP_EXTRA_BUILD_DEPS=apache2-dev
KUBERNETES_PORT_443_TCP_ADDR=10.0.0.1
KUBERNETES_PORT_443_TCP=tcp://10.0.0.1:443
PHP_VERSION=5.6.32
WORDPRESS_SERVICE_PORT=80
PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2
_=/usr/bin/env
```


kubectl exec -it wordpress-mysql-7cf8b8647c-sgwcq /bin/bash
kubectl exec -it wordpress-mysql-6975d97df5-j2x5k /bin/bash
```
root@wordpress-mysql-6975d97df5-j2x5k:/# env
WORDPRESS_SERVICE_PORT=80
HOSTNAME=wordpress-mysql-6975d97df5-j2x5k
WORDPRESS_PORT_80_TCP_PROTO=tcp
WORDPRESS_PORT_80_TCP_PORT=80
WORDPRESS_PORT=tcp://10.0.224.198:80
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_ADDR=10.0.0.1
MYSQL_ROOT_PASSWORD=P@ssw0rdT#st!23
KUBERNETES_PORT=tcp://10.0.0.1:443
PWD=/
HOME=/root
MYSQL_MAJOR=5.6
GOSU_VERSION=1.7
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP_PORT=443
MYSQL_VERSION=5.6.46-1debian9
KUBERNETES_PORT_443_TCP=tcp://10.0.0.1:443
TERM=xterm
SHLVL=1
KUBERNETES_SERVICE_PORT=443
WORDPRESS_PORT_80_TCP=tcp://10.0.224.198:80
WORDPRESS_SERVICE_HOST=10.0.224.198
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_SERVICE_HOST=10.0.0.1
WORDPRESS_PORT_80_TCP_ADDR=10.0.224.198
_=/usr/bin/env
```
---

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

# Linki

* [mysql-wordpress-persistent-volume](https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/)
* [azure-files-dynamic-pv](https://docs.microsoft.com/en-us/azure/aks/azure-files-dynamic-pv)
* [operator-best-practices-storage](https://docs.microsoft.com/en-us/azure/aks/operator-best-practices-storage)
* [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)