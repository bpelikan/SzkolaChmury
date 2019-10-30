# Zadanie 4

# 1. Uruchomienie Minikube

#### 1.1 Sprawdzenie statusu
```PowerShell
PS C:\Users\bpelikan> minikube status
host: Stopped
kubelet:
apiserver:
kubectl:
```

#### 1.2 Uruchomienie
```PowerShell
PS C:\Users\bpelikan> minikube start
* minikube v1.4.0 on Microsoft Windows 10 Education N 10.0.17134 Build 17134
* Tip: Use 'minikube start -p <name>' to create a new cluster, or 'minikube delete' to delete this one.
* Starting existing hyperv VM for "minikube" ...
* Waiting for the host to be provisioned ...
* Preparing Kubernetes v1.16.0 on Docker 18.09.9 ...
* Relaunching Kubernetes using kubeadm ...
* Waiting for: apiserver proxy etcd scheduler controller dns
* Done! kubectl is now configured to use "minikube"

PS C:\Users\bpelikan> minikube status
host: Running
kubelet: Running
apiserver: Running
kubectl: Correctly Configured: pointing to minikube-vm at 192.168.36.75
````

#### 1.3 Sprawdzenie informacji o klastrze
```PowerShell
PS C:\Users\bpelikan> kubectl cluster-info
Kubernetes master is running at https://192.168.36.75:8443
KubeDNS is running at https://192.168.36.75:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

PS C:\Users\bpelikan> kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
minikube   Ready    master   25h   v1.16.0
PS C:\Users\bpelikan> kubectl get pods
NAME                     READY   STATUS             RESTARTS   AGE
hello-7bc6cfc69d-j7dfc   0/1     CrashLoopBackOff   21         25h

PS C:\Users\bpelikan> kubectl get pods --all-namespaces
NAMESPACE              NAME                                         READY   STATUS      RESTARTS   AGE
default                hello-7bc6cfc69d-j7dfc                       0/1     Completed   22         25h
kube-system            coredns-5644d7b6d9-tg4tn                     1/1     Running     1          25h
kube-system            coredns-5644d7b6d9-z44kw                     1/1     Running     1          25h
kube-system            etcd-minikube                                1/1     Running     0          2m3s
kube-system            kube-addon-manager-minikube                  1/1     Running     1          25h
kube-system            kube-apiserver-minikube                      1/1     Running     0          2m4s
kube-system            kube-controller-manager-minikube             1/1     Running     1          25h
kube-system            kube-proxy-tpc95                             1/1     Running     1          25h
kube-system            kube-scheduler-minikube                      1/1     Running     1          25h
kube-system            nginx-ingress-controller-57bf9855c8-n4lp5    1/1     Running     1          25h
kube-system            storage-provisioner                          1/1     Running     2          25h
kubernetes-dashboard   dashboard-metrics-scraper-76585494d8-b9ltx   1/1     Running     1          25h
kubernetes-dashboard   kubernetes-dashboard-57f4cb4545-649rw        1/1     Running     2          25h
````

#### 1.4 Zatrzymanie Minikube
```PowerShell
PS C:\Users\bpelikan> minikube stop
* Stopping "minikube" in hyperv ...
* Powering off "minikube" via SSH ...
* "minikube" stopped.
```


# 2. AKS with ARM

* [ARM template deployaks.json](./code/deployaks.json)

* [ARM template CleanARMTemlpate.json](./code/CleanARMTemlpate.json)

#### 2.1 Utworzenie service principal
```PowerShell
PS C:\Users\bpelikan> az ad sp create-for-rbac --skip-assignment
{
  "appId": "4a41afaa-0000-0000-0000-000000000000",
  "displayName": "azure-cli-2019-10-15-19-56-43",
  "name": "http://azure-cli-2019-10-15-19-56-43",
  "password": "9fca4cfe-0000-0000-0000-000000000000",
  "tenant": "{...}"
}
```

#### 2.2 Zdefiniowanie zmiennych
```PowerShell
PS C:\Users\bpelikan> $location="westeurope"
PS C:\Users\bpelikan> $resourceGroup="KubernetesZad4"
PS C:\Users\bpelikan> $resourceName="KubernetesClusterZad4"
PS C:\Users\bpelikan> $dnsPrefix="$($resourceName)-dns"
PS C:\Users\bpelikan> $servicePrincipalClientId="4a41afaa-0000-0000-0000-000000000000"
PS C:\Users\bpelikan> $servicePrincipalClientSecret="9fca4cfe-0000-0000-0000-000000000000"
PS C:\Users\bpelikan> $templateURI="https://gist.githubusercontent.com/bpelikan/7c8a92faadcccdce1af637065bff2abe/raw/41ce45e9ce8d3c42bb297bafc4904079b298ae6d/deployaks.json"
PS C:\Users\bpelikan> $cleanTemplateURI="https://gist.githubusercontent.com/bpelikan/4ff12e675ddf4ace141227d4cf7a9c11/raw/27064c2215e11a57520740a98dd4c519c2f97fda/CleanARMTemlpate.json"
```

#### 2.3 Utworzenie resource group
```PowerShell
PS C:\Users\bpelikan> az group create --location $location --name $resourceGroup
{
  "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4",
  "location": "westeurope",
  "managedBy": null,
  "name": "KubernetesZad4",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": null
}
```

#### 2.4 Walidacja ARM template
```PowerShell
PS C:\Users\bpelikan> az group deployment validate --resource-group $resourceGroup --template-uri $templateURI --parameters resourceName=$resourceName --parameters location=$location --parameters dnsPrefix=$dnsPrefix --parameters servicePrincipalClientId=$servicePrincipalClientId --parameters servicePrincipalClientSecret=$servicePrincipalClientSecret --parameters kubernetesVersion="1.13.11"
{
  "error": null,
  "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.Resources/deployments/deployment_dry_run",
  "name": "deployment_dry_run",
  "properties": {
    "correlationId": "41fe6c73-0000-0000-0000-000000000000",
    "debugSetting": null,
    "dependencies": [],
    "duration": "PT0S",
    "mode": "Incremental",
    "onErrorDeployment": null,
    "outputs": null,
    "parameters": {
      "agentCount": {
        "type": "Int",
        "value": 3
      },
      "agentVMSize": {
        "type": "String",
        "value": "Standard_D2_v2"
      },
      "dnsPrefix": {
        "type": "String",
        "value": "KubernetesClusterZad4-dns"
      },
      "enableHttpApplicationRouting": {
        "type": "Bool",
        "value": true
      },
      "enableRBAC": {
        "type": "Bool",
        "value": true
      },
      "kubernetesVersion": {
        "type": "String",
        "value": "1.13.11"
      },
      "location": {
        "type": "String",
        "value": "westeurope"
      },
      "maxPods": {
        "type": "Int",
        "value": 2
      },
      "networkPlugin": {
        "type": "String",
        "value": "kubenet"
      },
      "osDiskSizeGB": {
        "type": "Int",
        "value": 0
      },
      "osType": {
        "type": "String",
        "value": "Linux"
      },
      "resourceName": {
        "type": "String",
        "value": "KubernetesClusterZad4"
      },
      "servicePrincipalClientId": {
        "type": "SecureString"
      },
      "servicePrincipalClientSecret": {
        "type": "SecureString"
      }
    },
    "parametersLink": null,
    "providers": [
      {
        "id": null,
        "namespace": "Microsoft.ContainerService",
        "registrationState": null,
        "resourceTypes": [
          {
            "aliases": null,
            "apiVersions": null,
            "locations": [
              "westeurope"
            ],
            "properties": null,
            "resourceType": "managedClusters"
          }
        ]
      }
    ],
    "provisioningState": "Succeeded",
    "template": null,
    "templateHash": "12854681205621073267",
    "templateLink": {
      "contentVersion": "1.0.0.0",
      "uri": "https://gist.githubusercontent.com/bpelikan/7c8a92faadcccdce1af637065bff2abe/raw/41ce45e9ce8d3c42bb297bafc4904079b298ae6d/deployaks.json"
    },
    "timestamp": "2019-10-15T23:03:31.748450+00:00",
    "validatedResources": [
      {
        "apiVersion": "2019-06-01",
        "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.ContainerService/managedClusters/KubernetesClusterZad4",
        "location": "westeurope",
        "name": "KubernetesClusterZad4",
        "properties": {
          "addonProfiles": {
            "httpApplicationRouting": {
              "enabled": true
            }
          },
          "agentPoolProfiles": [
            {
              "count": 3,
              "name": "agentpool",
              "osDiskSizeGB": 0,
              "osType": "Linux",
              "storageProfile": "ManagedDisks",
              "vmSize": "Standard_D2_v2"
            }
          ],
          "dnsPrefix": "KubernetesClusterZad4-dns",
          "enableRBAC": true,
          "kubernetesVersion": "1.13.11",
          "networkProfile": {
            "networkPlugin": "kubenet"
          },
          "servicePrincipalProfile": {
            "ClientId": "4a41afaa-0000-0000-0000-000000000000",
            "Secret": "9fca4cfe-0000-0000-0000-000000000000"
          }
        },
        "resourceGroup": "KubernetesZad4",
        "tags": {},
        "type": "Microsoft.ContainerService/managedClusters"
      }
    ]
  },
  "resourceGroup": "KubernetesZad4"
}
```

#### 2.5 Utworzenie klastra
```PowerShell
PS C:\Users\bpelikan> az group deployment create --resource-group $resourceGroup --template-uri $templateURI --parameters resourceName=$resourceName --parameters location=$location --parameters dnsPrefix=$dnsPrefix --parameters servicePrincipalClientId=$servicePrincipalClientId --parameters servicePrincipalClientSecret=$servicePrincipalClientSecret --parameters kubernetesVersion="1.13.11"
{
  "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.Resources/deployments/deployaks",
  "location": null,
  "name": "deployaks",
  "properties": {
    "correlationId": "9a1265ec-0000-0000-0000-000000000000",
    "debugSetting": null,
    "dependencies": [],
    "duration": "PT8M18.7395126S",
    "mode": "Incremental",
    "onErrorDeployment": null,
    "outputResources": [
      {
        "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.ContainerService/managedClusters/KubernetesClusterZad4",
        "resourceGroup": "KubernetesZad4"
      }
    ],
    "outputs": {
      "controlPlaneFQDN": {
        "type": "String",
        "value": "kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io"
      }
    },
    "parameters": {
      "agentCount": {
        "type": "Int",
        "value": 3
      },
      "agentVMSize": {
        "type": "String",
        "value": "Standard_D2_v2"
      },
      "dnsPrefix": {
        "type": "String",
        "value": "KubernetesClusterZad4-dns"
      },
      "enableHttpApplicationRouting": {
        "type": "Bool",
        "value": true
      },
      "enableRBAC": {
        "type": "Bool",
        "value": true
      },
      "kubernetesVersion": {
        "type": "String",
        "value": "1.13.11"
      },
      "location": {
        "type": "String",
        "value": "westeurope"
      },
      "maxPods": {
        "type": "Int",
        "value": 2
      },
      "networkPlugin": {
        "type": "String",
        "value": "kubenet"
      },
      "osDiskSizeGB": {
        "type": "Int",
        "value": 0
      },
      "osType": {
        "type": "String",
        "value": "Linux"
      },
      "resourceName": {
        "type": "String",
        "value": "KubernetesClusterZad4"
      },
      "servicePrincipalClientId": {
        "type": "SecureString"
      },
      "servicePrincipalClientSecret": {
        "type": "SecureString"
      }
    },
    "parametersLink": null,
    "providers": [
      {
        "id": null,
        "namespace": "Microsoft.ContainerService",
        "registrationState": null,
        "resourceTypes": [
          {
            "aliases": null,
            "apiVersions": null,
            "locations": [
              "westeurope"
            ],
            "properties": null,
            "resourceType": "managedClusters"
          }
        ]
      }
    ],
    "provisioningState": "Succeeded",
    "template": null,
    "templateHash": "12854681205621073267",
    "templateLink": {
      "contentVersion": "1.0.0.0",
      "uri": "https://gist.githubusercontent.com/bpelikan/7c8a92faadcccdce1af637065bff2abe/raw/41ce45e9ce8d3c42bb297bafc4904079b298ae6d/deployaks.json"
    },
    "timestamp": "2019-10-15T23:17:55.483219+00:00"
  },
  "resourceGroup": "KubernetesZad4",
  "type": null
}
```

#### 2.6 Nieudana próba pobrania informacji o klastrze
```PowerShell
PS C:\Users\bpelikan> kubectl get nodes
```

#### 2.7 Sprawdzenie kontekstu
```PowerShell
PS C:\Users\bpelikan> kubectl config get-contexts
CURRENT   NAME                 CLUSTER          AUTHINFO         NAMESPACE
          docker-desktop       docker-desktop   docker-desktop
          docker-for-desktop   docker-desktop   docker-desktop
*         minikube             minikube         minikube
```

#### 2.8 Konfiguracja kontekstu na AKS
```PowerShell
PS C:\Users\bpelikan> az aks get-credentials --resource-group $resourceGroup --name $resourceName
A different object named KubernetesClusterZad4 already exists in your kubeconfig file.
Overwrite? (y/n): y
A different object named clusterUser_KubernetesZad4_KubernetesClusterZad4 already exists in your kubeconfig file.
Overwrite? (y/n): y
Merged "KubernetesClusterZad4" as current context in C:\Users\bpelikan\.kube\config

PS C:\Users\bpelikan> kubectl config get-contexts
CURRENT   NAME                    CLUSTER                 AUTHINFO                                           NAMESPACE
*         KubernetesClusterZad4   KubernetesClusterZad4   clusterUser_KubernetesZad4_KubernetesClusterZad4
          docker-desktop          docker-desktop          docker-desktop
          docker-for-desktop      docker-desktop          docker-desktop
          minikube                minikube                minikube
```

#### 2.9 Pobranie informacji o klastrze
```PowerShell
PS C:\Users\bpelikan> kubectl cluster-info
Kubernetes master is running at https://kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io:443
addon-http-application-routing-default-http-backend is running at https://kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io:443/api/v1/namespaces/kube-system/services/addon-http-application-routing-default-http-backend/proxy
addon-http-application-routing-nginx-ingress is running at http://13.95.0.184:80 http://13.95.0.184:443 
CoreDNS is running at https://kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io:443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
kubernetes-dashboard is running at https://kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io:443/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy
Metrics-server is running at https://kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io:443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

PS C:\Users\bpelikan> kubectl get nodes
NAME                       STATUS   ROLES   AGE   VERSION
aks-agentpool-19464462-0   Ready    agent   20m   v1.13.11
aks-agentpool-19464462-1   Ready    agent   20m   v1.13.11
aks-agentpool-19464462-2   Ready    agent   20m   v1.13.11

PS C:\Users\bpelikan> kubectl get pods
No resources found.

PS C:\Users\bpelikan> kubectl get pods --all-namespaces
NAMESPACE     NAME                                                              READY   STATUS    RESTARTS   AGE
kube-system   addon-http-application-routing-default-http-backend-74698crp8vd   1/1     Running   0          23m
kube-system   addon-http-application-routing-external-dns-5c788779-9wfz7        1/1     Running   0          23m
kube-system   addon-http-application-routing-nginx-ingress-controller-786b6gx   1/1     Running   0          23m
kube-system   coredns-696c4d987c-fzlhh                                          1/1     Running   0          23m
kube-system   coredns-696c4d987c-p9b9z                                          1/1     Running   0          20m
kube-system   coredns-autoscaler-657d77ffbf-b52kz                               1/1     Running   0          23m
kube-system   kube-proxy-tws8m                                                  1/1     Running   0          20m
kube-system   kube-proxy-wzbwx                                                  1/1     Running   0          20m
kube-system   kube-proxy-zx79b                                                  1/1     Running   0          21m
kube-system   kubernetes-dashboard-6f697bd9f5-zqknf                             1/1     Running   0          23m
kube-system   metrics-server-58699455bc-7rv65                                   1/1     Running   1          23m
kube-system   tunnelfront-d7d5f6c85-x8zgp                                       1/1     Running   0          23m
```

### 2.10 Przeskalowanie klastra do 1 noda
#### 2.10.1 Walidacja
```PowerShell
PS C:\Users\bpelikan> az group deployment validate --resource-group $resourceGroup --template-uri $templateURI --parameters resourceName=$resourceName --parameters location=$location --parameters dnsPrefix=$dnsPrefix --parameters servicePrincipalClientId=$servicePrincipalClientId --parameters servicePrincipalClientSecret=$servicePrincipalClientSecret --parameters kubernetesVersion="1.13.11" --parameters agentCount=1
{
  "error": null,
  "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.Resources/deployments/deployment_dry_run",
  "name": "deployment_dry_run",
  "properties": {
    "correlationId": "26746a3e-0000-0000-0000-000000000000",
    "debugSetting": null,
    "dependencies": [],
    "duration": "PT0S",
    "mode": "Incremental",
    "onErrorDeployment": null,
    "outputs": null,
    "parameters": {
      "agentCount": {
        "type": "Int",
        "value": 1
      },
      "agentVMSize": {
        "type": "String",
        "value": "Standard_D2_v2"
      },
      "dnsPrefix": {
        "type": "String",
        "value": "KubernetesClusterZad4-dns"
      },
      "enableHttpApplicationRouting": {
        "type": "Bool",
        "value": true
      },
      "enableRBAC": {
        "type": "Bool",
        "value": true
      },
      "kubernetesVersion": {
        "type": "String",
        "value": "1.13.11"
      },
      "location": {
        "type": "String",
        "value": "westeurope"
      },
      "maxPods": {
        "type": "Int",
        "value": 2
      },
      "networkPlugin": {
        "type": "String",
        "value": "kubenet"
      },
      "osDiskSizeGB": {
        "type": "Int",
        "value": 0
      },
      "osType": {
        "type": "String",
        "value": "Linux"
      },
      "resourceName": {
        "type": "String",
        "value": "KubernetesClusterZad4"
      },
      "servicePrincipalClientId": {
        "type": "SecureString"
      },
      "servicePrincipalClientSecret": {
        "type": "SecureString"
      }
    },
    "parametersLink": null,
    "providers": [
      {
        "id": null,
        "namespace": "Microsoft.ContainerService",
        "registrationState": null,
        "resourceTypes": [
          {
            "aliases": null,
            "apiVersions": null,
            "locations": [
              "westeurope"
            ],
            "properties": null,
            "resourceType": "managedClusters"
          }
        ]
      }
    ],
    "provisioningState": "Succeeded",
    "template": null,
    "templateHash": "12854681205621073267",
    "templateLink": {
      "contentVersion": "1.0.0.0",
      "uri": "https://gist.githubusercontent.com/bpelikan/7c8a92faadcccdce1af637065bff2abe/raw/41ce45e9ce8d3c42bb297bafc4904079b298ae6d/deployaks.json"
    },
    "timestamp": "2019-10-15T23:38:26.820479+00:00",
    "validatedResources": [
      {
        "apiVersion": "2019-06-01",
        "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.ContainerService/managedClusters/KubernetesClusterZad4",
        "location": "westeurope",
        "name": "KubernetesClusterZad4",
        "properties": {
          "addonProfiles": {
            "httpApplicationRouting": {
              "enabled": true
            }
          },
          "agentPoolProfiles": [
            {
              "count": 1,
              "name": "agentpool",
              "osDiskSizeGB": 0,
              "osType": "Linux",
              "storageProfile": "ManagedDisks",
              "vmSize": "Standard_D2_v2"
            }
          ],
          "dnsPrefix": "KubernetesClusterZad4-dns",
          "enableRBAC": true,
          "kubernetesVersion": "1.13.11",
          "networkProfile": {
            "networkPlugin": "kubenet"
          },
          "servicePrincipalProfile": {
            "ClientId": "4a41afaa-0000-0000-0000-000000000000",
            "Secret": "9fca4cfe-0000-0000-0000-000000000000"
          }
        },
        "resourceGroup": "KubernetesZad4",
        "tags": {},
        "type": "Microsoft.ContainerService/managedClusters"
      }
    ]
  },
  "resourceGroup": "KubernetesZad4"
}
```

#### 2.10.2 Przeskalowanie
```PowerShell
PS C:\Users\bpelikan> az group deployment create --resource-group $resourceGroup --template-uri $templateURI --parameters resourceName=$resourceName --parameters location=$location --parameters dnsPrefix=$dnsPrefix --parameters servicePrincipalClientId=$servicePrincipalClientId --parameters servicePrincipalClientSecret=$servicePrincipalClientSecret --parameters kubernetesVersion="1.13.11" --parameters agentCount=1
{
  "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.Resources/deployments/deployaks",
  "location": null,
  "name": "deployaks",
  "properties": {
    "correlationId": "d958831a-0000-0000-0000-000000000000",
    "debugSetting": null,
    "dependencies": [],
    "duration": "PT5M42.3028463S",
    "mode": "Incremental",
    "onErrorDeployment": null,
    "outputResources": [
      {
        "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.ContainerService/managedClusters/KubernetesClusterZad4",
        "resourceGroup": "KubernetesZad4"
      }
    ],
    "outputs": {
      "controlPlaneFQDN": {
        "type": "String",
        "value": "kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io"
      }
    },
    "parameters": {
      "agentCount": {
        "type": "Int",
        "value": 1
      },
      "agentVMSize": {
        "type": "String",
        "value": "Standard_D2_v2"
      },
      "dnsPrefix": {
        "type": "String",
        "value": "KubernetesClusterZad4-dns"
      },
      "enableHttpApplicationRouting": {
        "type": "Bool",
        "value": true
      },
      "enableRBAC": {
        "type": "Bool",
        "value": true
      },
      "kubernetesVersion": {
        "type": "String",
        "value": "1.13.11"
      },
      "location": {
        "type": "String",
        "value": "westeurope"
      },
      "maxPods": {
        "type": "Int",
        "value": 2
      },
      "networkPlugin": {
        "type": "String",
        "value": "kubenet"
      },
      "osDiskSizeGB": {
        "type": "Int",
        "value": 0
      },
      "osType": {
        "type": "String",
        "value": "Linux"
      },
      "resourceName": {
        "type": "String",
        "value": "KubernetesClusterZad4"
      },
      "servicePrincipalClientId": {
        "type": "SecureString"
      },
      "servicePrincipalClientSecret": {
        "type": "SecureString"
      }
    },
    "parametersLink": null,
    "providers": [
      {
        "id": null,
        "namespace": "Microsoft.ContainerService",
        "registrationState": null,
        "resourceTypes": [
          {
            "aliases": null,
            "apiVersions": null,
            "locations": [
              "westeurope"
            ],
            "properties": null,
            "resourceType": "managedClusters"
          }
        ]
      }
    ],
    "provisioningState": "Succeeded",
    "template": null,
    "templateHash": "12854681205621073267",
    "templateLink": {
      "contentVersion": "1.0.0.0",
      "uri": "https://gist.githubusercontent.com/bpelikan/7c8a92faadcccdce1af637065bff2abe/raw/41ce45e9ce8d3c42bb297bafc4904079b298ae6d/deployaks.json"
    },
    "timestamp": "2019-10-15T23:44:44.924018+00:00"
  },
  "resourceGroup": "KubernetesZad4",
  "type": null
}
````

#### 2.10.3 Pobranie informacji o klastrze
```PowerShell
PS C:\Users\bpelikan> kubectl get nodes
NAME                       STATUS   ROLES   AGE   VERSION
aks-agentpool-19464462-0   Ready    agent   31m   v1.13.11

PS C:\Users\bpelikan> kubectl get pods
No resources found.

PS C:\Users\bpelikan> kubectl get pods --all-namespaces
NAMESPACE     NAME                                                              READY   STATUS    RESTARTS   AGE
kube-system   addon-http-application-routing-default-http-backend-74698c6pvjk   1/1     Running   0          2m55s
kube-system   addon-http-application-routing-external-dns-5c788779-jcjw2        1/1     Running   0          2m55s
kube-system   addon-http-application-routing-nginx-ingress-controller-78bzcg7   1/1     Running   0          2m55s
kube-system   coredns-696c4d987c-59w5x                                          1/1     Running   0          2m56s
kube-system   coredns-696c4d987c-978n7                                          1/1     Running   0          5m17s
kube-system   coredns-autoscaler-657d77ffbf-g2bhx                               1/1     Running   0          2m56s
kube-system   kube-proxy-wzbwx                                                  1/1     Running   0          31m
kube-system   kubernetes-dashboard-6f697bd9f5-ct69p                             1/1     Running   0          5m16s
kube-system   metrics-server-58699455bc-724f5                                   1/1     Running   0          5m16s
kube-system   tunnelfront-d7d5f6c85-c5pg6                                       1/1     Running   0          5m16s
```

### 2.11 Usunięcie
#### 2.11.1 ARM
```PowerShell
PS C:\Users\bpelikan> az group deployment validate --resource-group $resourceGroup --template-uri $cleanTemplateURI --mode Complete
{
  "error": null,
  "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.Resources/deployments/deployment_dry_run",
  "name": "deployment_dry_run",
  "properties": {
    "correlationId": "4322a0d0-0000-0000-0000-000000000000",
    "debugSetting": null,
    "dependencies": [],
    "duration": "PT0S",
    "mode": "Complete",
    "onErrorDeployment": null,
    "outputs": null,
    "parameters": {},
    "parametersLink": null,
    "providers": [],
    "provisioningState": "Succeeded",
    "template": null,
    "templateHash": "3699958335004038476",
    "templateLink": {
      "contentVersion": "1.0.0.0",
      "uri": "https://gist.githubusercontent.com/bpelikan/4ff12e675ddf4ace141227d4cf7a9c11/raw/27064c2215e11a57520740a98dd4c519c2f97fda/CleanARMTemlpate.json"
    },
    "timestamp": "2019-10-16T00:01:22.116840+00:00",
    "validatedResources": []
  },
  "resourceGroup": "KubernetesZad4"
}
```

```PowerShell
PS C:\Users\bpelikan> az group deployment create --resource-group $resourceGroup --template-uri $cleanTemplateURI --mode Complete
{
  "id": "/subscriptions/616bb79e-0000-0000-0000-000000000000/resourceGroups/KubernetesZad4/providers/Microsoft.Resources/deployments/CleanARMTemlpate",
  "location": null,
  "name": "CleanARMTemlpate",
  "properties": {
    "correlationId": "3a0113dd-0000-0000-0000-000000000000",
    "debugSetting": null,
    "dependencies": [],
    "duration": "PT11M4.6073688S",
    "mode": "Complete",
    "onErrorDeployment": null,
    "outputResources": [],
    "outputs": {},
    "parameters": {},
    "parametersLink": null,
    "providers": [],
    "provisioningState": "Succeeded",
    "template": null,
    "templateHash": "3699958335004038476",
    "templateLink": {
      "contentVersion": "1.0.0.0",
      "uri": "https://gist.githubusercontent.com/bpelikan/4ff12e675ddf4ace141227d4cf7a9c11/raw/27064c2215e11a57520740a98dd4c519c2f97fda/CleanARMTemlpate.json"
    },
    "timestamp": "2019-10-16T00:12:55.626288+00:00"
  },
  "resourceGroup": "KubernetesZad4",
  "type": null
}
```

#### 2.11.2 CLI
```PowerShell
PS C:\Users\bpelikan> az aks delete --resource-group $resourceGroup --name $resourceName
```

### 2.12 Czyszczenie
* Uruchomienie [skryptu](https://github.com/bpelikan/AzureAutomationScripts/blob/master/PeriodicallyDeleteResourceGroups.ps1) w Azure Automation do wyczyszczenia pozostałych resource grup
* Usunięcie Service Principal
* Przywrócenie  kontekstu
```PowerShell
PS C:\Users\bpelikan> kubectl config get-contexts
CURRENT   NAME                    CLUSTER                 AUTHINFO                                           NAMESPACE
*         KubernetesClusterZad4   KubernetesClusterZad4   clusterUser_KubernetesZad4_KubernetesClusterZad4
          docker-desktop          docker-desktop          docker-desktop
          docker-for-desktop      docker-desktop          docker-desktop
          minikube                minikube                minikube
PS C:\Users\bpelikan> kubectl config delete-context KubernetesClusterZad4
warning: this removed your active context, use "kubectl config use-context" to select a different one
deleted context KubernetesClusterZad4 from C:\Users\bpelikan/.kube/config

PS C:\Users\bpelikan> kubectl config use-context minikube
Switched to context "minikube".

PS C:\Users\bpelikan> kubectl config get-contexts
CURRENT   NAME                 CLUSTER          AUTHINFO         NAMESPACE
          docker-desktop       docker-desktop   docker-desktop
          docker-for-desktop   docker-desktop   docker-desktop
*         minikube             minikube         minikube
```

Zauważyłem, że na koniec w `$HOME/.kube/config` pozostały jeszcze konfiguracje dla klastra oraz użytkownika AKS związane z `KubernetesClusterZad4`:

```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {...}
    server: https://kubernetesclusterzad4-dns-42efd8b2.hcp.westeurope.azmk8s.io:443
  name: KubernetesClusterZad4
- cluster:
    certificate-authority-data: {...}
    server: https://kubernetes.docker.internal:6443
  name: docker-desktop
- cluster:
    certificate-authority: {...}\.minikube\ca.crt
    server: https://192.168.36.75:8443
  name: minikube
contexts:
- context:
    cluster: docker-desktop
    user: docker-desktop
  name: docker-desktop
- context:
    cluster: docker-desktop
    user: docker-desktop
  name: docker-for-desktop
- context:
    cluster: minikube
    user: minikube
  name: minikube
current-context: minikube
kind: Config
preferences: {}
users:
- name: clusterUser_KubernetesZad4_KubernetesClusterZad4
  user:
    client-certificate-data: {...}
    client-key-data: 
    token: {...}
- name: docker-desktop
  user:
    client-certificate-data: {...}
    client-key-data: 
- name: minikube
  user:
    client-certificate: {...}\.minikube\client.crt
    client-key: {...}\.minikube\client.key
```