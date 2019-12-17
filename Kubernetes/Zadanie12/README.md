# Praca Domowa nr 12

## Przygotowanie środowiska

<details>
  <summary><b><i>Przygotowanie AKS</i></b></summary>

#### Utworzenie folderu na pliki
```bash
bartosz@Azure:~$ mkdir code
bartosz@Azure:~$ cd code
# bartosz@Azure:~$ code .
```

#### Utworzenie Service Principal
```bash
bartosz@Azure:~/code$ az ad sp create-for-rbac --skip-assignment -o json > auth.json
```

#### Przypisanie zmiennych
```bash
bartosz@Azure:~/code$ location="westeurope"
bartosz@Azure:~/code$ resourceGroup="szkchm-zadanie12"
bartosz@Azure:~/code$ aksName="AKSZad12"
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


## Instalacja Istio

<details>
  <summary><b><i>Instalacja Istio</i></b></summary>

#### Pobranie paczki z Istio
```bash
bartosz@Azure:~/code$ wget https://github.com/istio/istio/releases/download/1.4.0/istio-1.4.0-linux.tar.gz
```

<details>
  <summary><b><i>Sprawdzenie czy paczka została pobrana</i></b></summary>

```bash
bartosz@Azure:~/code$ ls
auth.json  istio-1.4.0-linux.tar.gz
```
</details>

#### Wypakowanie paczki
```bash
bartosz@Azure:~/code$ tar -xvf istio-1.4.0-linux.tar.gz
bartosz@Azure:~/code$ cd istio-1.4.0
```

#### Dodanie Istio do ścieżki
```bash
bartosz@Azure:~/code/istio-1.4.0$ export PATH=$PWD/bin:$PATH
```

<details>
  <summary><b><i>Sprawdzenie czy Istio działa</i></b></summary>

```bash
bartosz@Azure:~/code/istio-1.4.0$ istioctl
Istio configuration command line utility for service operators to
debug and diagnose their Istio mesh.

Usage:
  istioctl [command]

Available Commands:
  authn           Interact with Istio authentication policies
  authz           (authz is experimental.  Use `istioctl experimental authz`)
  convert-ingress Convert Ingress configuration into Istio VirtualService configuration
  dashboard       Access to Istio web UIs
  deregister      De-registers a service instance
  experimental    Experimental commands that may be modified or deprecated
  help            Help about any command
  kube-inject     Inject Envoy sidecar into Kubernetes pod resources
  manifest        Commands related to Istio manifests
  profile         Commands related to Istio configuration profiles
  proxy-config    Retrieve information about proxy configuration from Envoy [kube only]
  proxy-status    Retrieves the synchronization status of each Envoy in the mesh [kube only]
  register        Registers a service instance (e.g. VM) joining the mesh
  validate        Validate Istio policy and rules
  verify-install  Verifies Istio Installation Status or performs pre-check for the cluster before Istio installation
  version         Prints out build version information

Flags:
      --context string            The name of the kubeconfig context to use
  -h, --help                      help for istioctl
  -i, --istioNamespace string     Istio system namespace (default "istio-system")
  -c, --kubeconfig string         Kubernetes configuration file
      --log_output_level string   Comma-separated minimum per-scope logging level of messages to output, in the form of <scope>:<level>,<scope>:<level>,... where scope can be one of [ads, all, analysis, attributes, authn, cacheLog, citadelClientLog, configMapController, conversions, default, googleCAClientLog, grpcAdapter, kube, kube-converter, mcp, meshconfig, model, name, patch, processing, rbac, resource, runtime, sdsServiceLog, secretFetcherLog, source, stsClientLog, tpath, translator, util, validation, vaultClientLog] and level can be one of [debug, info, warn, error, fatal, none] (default "default:info,validation:error,processing:error,source:error,analysis:warn")
  -n, --namespace string          Config namespace

Use "istioctl [command] --help" for more information about a command.
```
</details>


#### Istalacja Istio
```bash
bartosz@Azure:~/code/istio-1.4.0$ kubectl apply -f ./install/kubernetes/istio-demo.yaml
```

<details>
  <summary><b><i>Sprawdzenie instalacji Istio na klastrze</i></b></summary>

```bash
bartosz@Azure:~/code/istio-1.4.0$ kubectl -n istio-system get pods
NAME                                      READY   STATUS      RESTARTS   AGE
grafana-6bb6bcf99f-pxd5q                  1/1     Running     0          3m59s
istio-citadel-66ddfd755-w98k6             1/1     Running     0          3m58s
istio-egressgateway-74bd664ff7-v4r6s      1/1     Running     0          3m59s
istio-galley-5f49858479-6vt96             1/1     Running     0          3m59s
istio-grafana-post-install-1.4.0-zm7h2    0/1     Completed   0          4m1s
istio-ingressgateway-f5cc4fb98-nlgcb      1/1     Running     0          3m59s
istio-pilot-65fd859486-62jnl              2/2     Running     3          3m59s
istio-policy-6cb85c5fc-trvn7              2/2     Running     5          3m59s
istio-security-post-install-1.4.0-jrst8   0/1     Completed   0          4m1s
istio-sidecar-injector-7984b6f548-qxf78   1/1     Running     0          3m58s
istio-telemetry-bd87b484c-ckh29           2/2     Running     5          3m59s
istio-tracing-56c7f85df7-5ph6d            1/1     Running     0          3m58s
kiali-7b5c8f79d8-bhzzk                    1/1     Running     0          3m59s
prometheus-74d8b55f54-kcv9j               1/1     Running     0          3m59s
```

```bash
bartosz@Azure:~/code/istio-1.4.0$ kubectl -n istio-system get svc
NAME                     TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                                                                                                                                      AGE
grafana                  ClusterIP      10.0.218.214   <none>           3000/TCP                                                                                                                                     4m25s
istio-citadel            ClusterIP      10.0.195.33    <none>           8060/TCP,15014/TCP                                                                                                                           4m25s
istio-egressgateway      ClusterIP      10.0.10.99     <none>           80/TCP,443/TCP,15443/TCP                                                                                                                     4m25s
istio-galley             ClusterIP      10.0.7.145     <none>           443/TCP,15014/TCP,9901/TCP                                                                                                                   4m25s
istio-ingressgateway     LoadBalancer   10.0.31.159    40.119.147.200   15020:32691/TCP,80:31380/TCP,443:31390/TCP,31400:31400/TCP,15029:31537/TCP,15030:30324/TCP,15031:32365/TCP,15032:30853/TCP,15443:31673/TCP   4m25s
istio-pilot              ClusterIP      10.0.66.77     <none>           15010/TCP,15011/TCP,8080/TCP,15014/TCP                                                                                                       4m25s
istio-policy             ClusterIP      10.0.246.15    <none>           9091/TCP,15004/TCP,15014/TCP                                                                                                                 4m25s
istio-sidecar-injector   ClusterIP      10.0.200.128   <none>           443/TCP,15014/TCP                                                                                                                            4m25s
istio-telemetry          ClusterIP      10.0.16.109    <none>           9091/TCP,15004/TCP,15014/TCP,42422/TCP                                                                                                       4m25s
jaeger-agent             ClusterIP      None           <none>           5775/UDP,6831/UDP,6832/UDP                                                                                                                   4m23s
jaeger-collector         ClusterIP      10.0.230.132   <none>           14267/TCP,14268/TCP,14250/TCP                                                                                                                4m23s
jaeger-query             ClusterIP      10.0.237.99    <none>           16686/TCP                                                                                                                                    4m23s
kiali                    ClusterIP      10.0.168.204   <none>           20001/TCP                                                                                                                                    4m25s
prometheus               ClusterIP      10.0.190.165   <none>           9090/TCP                                                                                                                                     4m25s
tracing                  ClusterIP      10.0.108.214   <none>           9411/TCP                                                                                                                                     4m23s
zipkin                   ClusterIP      10.0.105.80    <none>           9411/TCP                                                                                                                                     4m23s

```
</details>

#### Instalacja przykładowej aplikacji
```bash
bartosz@Azure:~/code/istio-1.4.0$ kubectl apply -f ./samples/bookinfo/platform/kube/bookinfo.yaml
```

<details>
  <summary><b><i>Sprawdzenie</i></b></summary>

```bash
bartosz@Azure:~/code/istio-1.4.0$ kubectl get pod
NAME                             READY   STATUS    RESTARTS   AGE
details-v1-c5b5f496d-q9g65       1/1     Running   0          80s
productpage-v1-c7765c886-cclxr   1/1     Running   0          80s
ratings-v1-f745cf57b-dg285       1/1     Running   0          80s
reviews-v1-75b979578c-cbjn9      1/1     Running   0          80s
reviews-v2-597bf96c8f-kdg4f      1/1     Running   0          81s
reviews-v3-54c6c64795-tbg7w      1/1     Running   0          81s
```
</details>

</details>

```

</details>


