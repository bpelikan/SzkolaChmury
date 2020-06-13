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

<details>
  <summary><b><i>firewall-allow-ssh.jinja</i></b></summary>

```jinja
resources:
- name: {{ env["name"] }}
  type: compute.v1.firewall
  properties:
    network: {{ properties["network"] }}
    {% if properties["sourceRanges"] is defined %}sourceRanges: {{ properties["sourceRanges"] }}{% endif %}
    {% if properties["targetTags"] is defined %}targetTags: {{ properties["targetTags"] }}{% endif %}
    {% if properties["sourceTags"] is defined %}sourceTags: {{ properties["sourceTags"] }}{% endif %}
    allowed:
    - IPProtocol: TCP
      ports: [22]
```
</details>

<details>
  <summary><b><i>firewall-deny.jinja</i></b></summary>

```jinja
resources:
- name: {{ env["name"] }}
  type: compute.v1.firewall
  properties:
    network: {{ properties["network"] }}
    sourceRanges: {{ properties["sourceRanges"] }}
    priority: {% if properties["priority"] is defined %} {{ properties["priority"] }} {% else %} 1000 {% endif %}
    denied:
    - IPProtocol: {{ properties["IPProtocol"] }}
      ports: {{ properties["Port"] }}
```
</details>
