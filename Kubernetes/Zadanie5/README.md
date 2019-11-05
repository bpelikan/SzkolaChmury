# Praca Domowa nr 5

# Wynik 1

```PowerShell
PS C:\Users\bpelikan> kubectl get pods -l=env=prod
NAME            READY   STATUS    RESTARTS   AGE
my-nginx-prod   1/1     Running   1          21m
```

# Wynik 2

```PowerShell
PS C:\Users\bpelikan> kubectl get pods -l=env=prod
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7984cd655c-fxhfm   1/1     Running   0          27s
nginx-deployment-7984cd655c-kmd45   1/1     Running   0          27s
nginx-deployment-7984cd655c-qqdjr   1/1     Running   0          11m
nginx-deployment-7984cd655c-shrqw   1/1     Running   0          27s
```

# Wynik 3

```PowerShell
PS C:\Users\bpelikan> kubectl get service
NAME               TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
nginx-deployment   ClusterIP   10.107.5.118   <none>        80/TCP    6m36s
```

# Wynik 4

### nslookup przed usunięciem
```PowerShell
# nslookup web-0.nginx
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local
Name:      web-0.nginx
Address 1: 10.1.0.204 web-0.nginx.homework5.svc.cluster.local
```
```PowerShell
# nslookup web-1.nginx
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local
Name:      web-1.nginx
Address 1: 10.1.0.205 web-1.nginx.homework5.svc.cluster.local
```

### nslookup po usunięciu
```PowerShell
# nslookup web-0.nginx
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local
Name:      web-0.nginx
Address 1: 10.1.0.207 web-0.nginx.homework5.svc.cluster.local
```
```PowerShell
# nslookup web-1.nginx
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local
Name:      web-1.nginx
Address 1: 10.1.0.208 web-1.nginx.homework5.svc.cluster.local
```
