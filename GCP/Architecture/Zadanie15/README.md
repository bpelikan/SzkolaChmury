# [Zadanie domowe nr 15](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-15-backup-i-recovery/zadanie-domowe-nr-15/)


#### Utworzenie projektu
```bash
PROJECT_NAME="zadanie15"
gcloud projects create $PROJECT_NAME
```


#### Deployment manager files
<details>
  <summary><b><i>network.jinja</i></b></summary>

```jinja
resources:
- name: {{ env["name"] }}
  type: compute.v1.network
  properties:
    autoCreateSubnetworks: false
```
</details>

<details>
  <summary><b><i>subnetwork.jinja</i></b></summary>

```jinja
resources:
- name: {{ env["name"] }}
  type: compute.v1.subnetwork
  properties:
    ipCidrRange: {{ properties["ipCidrRange"] }}
    network: {{ properties["network"] }}
    region: {{ properties["region"] }}
```
</details>