# [Fluentd](https://szkolachmury.pl/kubernetes/tydzien-13-premium-aplikacje-w-kontenerach/fluentd/)
```bash
# Custom resource, operator, RBAC roles
kubectl apply -f https://download.elastic.co/downloads/eck/1.0.0-beta1/all-in-one.yaml

# Elasticsearch cluster
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1beta1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 7.5.1
  nodeSets:
  - name: default
    count: 1
    config:
      node.master: true
      node.data: true
      node.ingest: true
      node.store.allow_mmap: false
EOF

# Sprawdzenie stanu
kubectl get elasticsearch

# Pod
kubectl get pods --selector='elasticsearch.k8s.elastic.co/cluster-name=quickstart'
kubectl logs -f quickstart-es-default-0

# Pobranie adresu IP
kubectl get service quickstart-es-http
esipaddress="10.0.233.217"

# Pobranie hasła dla użytkownika elastic
PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)

# Kibana
cat <<EOF | kubectl apply -f -
apiVersion: kibana.k8s.elastic.co/v1beta1
kind: Kibana
metadata:
  name: quickstart
spec:
  version: 7.5.1
  count: 1
  elasticsearchRef:
    name: quickstart
EOF

# Sprawdzenie
kubectl get kibana
kubectl get pod --selector='kibana.k8s.elastic.co/name=quickstart'
kubectl get service quickstart-kb-http

# Konfiguracja Fluentd
curl https://raw.githubusercontent.com/fluent/fluentd-kubernetes-daemonset/master/fluentd-daemonset-elasticsearch.yaml > fluentd-daemonset-elasticsearch.yaml

sed -i "s|elasticsearch-logging|${esipaddress}|g" fluentd-daemonset-elasticsearch.yaml
sed -i "s|changeme|${PASSWORD}|g" fluentd-daemonset-elasticsearch.yaml
sed -i "s|http|https|g" fluentd-daemonset-elasticsearch.yaml

kubectl create clusterrolebinding defaultclusteradmin --clusterrole=cluster-admin --serviceaccount=kube-system:default
kubectl apply -f fluentd-daemonset-elasticsearch.yaml

# Udostępnienie Kibany
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Lekcja101/code/kibana-lb.yaml > kibana-lb.yaml
kubectl apply -f kibana-lb.yaml

# Pobranie adresu IP do Kibany
kibanaIP=$(kubectl get svc quickstart-service-lb -o json | jq -r ".status.loadBalancer.ingress[0].ip")

# Zalogowanie się do Kibany
# url | user:password
echo "https://$kibanaIP | elastic:$PASSWORD"
```

## Materiały
* [Quickstart](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-quickstart.html)
* [Azure AKS startup script](../StartupScripts/AzureAKS.sh)

## Pliki
* [kibana-lb.yaml](./code/kibana-lb.yaml)

