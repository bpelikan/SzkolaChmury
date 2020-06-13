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

<details>
  <summary><b><i>vm-instances.jinja</i></b></summary>

```jinja
resources:
- name: {{ env["name"] }}
  type: compute.v1.instance
  properties:
    machineType: zones/{{ properties["zone"] }}/machineTypes/{{ properties["machineType"] }}
    zone: {{ properties["zone"] }}
    tags: 
      items: [ {% for i in properties["tags"] %}
                {{ i }},
               # {% if not loop.last %},{% endif %}
               {% endfor %}
             ]
      #{{ properties["tags"] }}
    networkInterfaces:
     - network: {{ properties["network"] }}
       subnetwork: {{ properties["subnetwork"] }}
       accessConfigs:
       - name: External NAT
         type: ONE_TO_ONE_NAT
    disks:
     - deviceName: {{ env["name"] }}
       type: PERSISTENT
       boot: true
       autoDelete: true
       initializeParams:
         sourceImage: https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/family/debian-9
```
</details>

<details>
  <summary><b><i>config.yaml</i></b></summary>

```yaml
imports:
- path: network.jinja
- path: subnetwork.jinja
- path: vm-instance.jinja
- path: firewall-allow-ssh.jinja

resources:
- name: vpcnetwork1
  type: network.jinja

- name: vpcnetwork1-sub1
  type: subnetwork.jinja
  properties:
    ipCidrRange: 10.128.0.0/20
    network: $(ref.vpcnetwork1.selfLink)
    region: us-central1

- name: allow-ssh-to-bastion
  type: firewall-allow-ssh.jinja
  properties:
    network: $(ref.vpcnetwork1.selfLink)
    sourceRanges: ["0.0.0.0/0"]
    targetTags: [bastion]

- name: allow-ssh-from-bastion
  type: firewall-allow-ssh.jinja
  properties:
    network: $(ref.vpcnetwork1.selfLink)
    sourceTags: [bastion]

- name: vm1
  type: vm-instance.jinja
  properties:
    zone: us-central1-b
    machineType: f1-micro
    network: $(ref.vpcnetwork1.selfLink)
    subnetwork: $(ref.vpcnetwork1-sub1.selfLink)

- name: vm2
  type: vm-instance.jinja
  properties:
    zone: us-central1-b
    machineType: f1-micro
    network: $(ref.vpcnetwork1.selfLink)
    subnetwork: $(ref.vpcnetwork1-sub1.selfLink)

- name: vmbastion
  type: vm-instance.jinja
  properties:
    zone: us-central1-b
    tags: [bastion, test2]
    machineType: f1-micro
    network: $(ref.vpcnetwork1.selfLink)
    subnetwork: $(ref.vpcnetwork1-sub1.selfLink)

```
</details>

#### Pobranie plików
```bash
wget https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/GCP/Architecture/Zadanie15/code/download-files.sh
sh download-files.sh
```

#### Create Deployment
```bash
DEPLOYMENT_NAME="bastionvm"
gcloud deployment-manager deployments create $DEPLOYMENT_NAME --config=config.yaml
```