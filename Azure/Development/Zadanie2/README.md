# [Zadanie domowe nr 2](https://szkolachmury.pl/microsoft-azure-software-development/tydzien-2-czym-jest-chmura-publiczna-z-perspektywy-developera/praca-domowa/)

## 1. Utworzenie `Resource Group`

### 1.1 Azure Portal

<details>
  <summary><b><i>Screenshots</i></b></summary>

![azure portal create resource group][img-azure-portal-create-resource-group]
![azure portal review creating resource group][img-azure-portal-review-creating-resource-group]
![azure portal list of resource group][img-azure-portal-list-of-resource-group]
</details>

### 1.2 Azure CLI
```bash
RG_NAME="rg-azdev-zad2-cli"
RG_LOCATION="westeurope"

az group create -n $RG_NAME -l $RG_LOCATION 
```

<details>
  <summary><b><i>Output</i></b></summary>

```bash
bartosz@Azure:~$ az account list-locations -o table
DisplayName           Latitude    Longitude    Name
--------------------  ----------  -----------  ------------------
East Asia             22.267      114.188      eastasia
Southeast Asia        1.283       103.833      southeastasia
Central US            41.5908     -93.6208     centralus
East US               37.3719     -79.8164     eastus
East US 2             36.6681     -78.3889     eastus2
West US               37.783      -122.417     westus
North Central US      41.8819     -87.6278     northcentralus
South Central US      29.4167     -98.5        southcentralus
North Europe          53.3478     -6.2597      northeurope
West Europe           52.3667     4.9          westeurope
Japan West            34.6939     135.5022     japanwest
Japan East            35.68       139.77       japaneast
Brazil South          -23.55      -46.633      brazilsouth
Australia East        -33.86      151.2094     australiaeast
Australia Southeast   -37.8136    144.9631     australiasoutheast
South India           12.9822     80.1636      southindia
Central India         18.5822     73.9197      centralindia
West India            19.088      72.868       westindia
Canada Central        43.653      -79.383      canadacentral
Canada East           46.817      -71.217      canadaeast
UK South              50.941      -0.799       uksouth
UK West               53.427      -3.084       ukwest
West Central US       40.890      -110.234     westcentralus
West US 2             47.233      -119.852     westus2
Korea Central         37.5665     126.9780     koreacentral
Korea South           35.1796     129.0756     koreasouth
France Central        46.3772     2.3730       francecentral
France South          43.8345     2.1972       francesouth
Australia Central     -35.3075    149.1244     australiacentral
Australia Central 2   -35.3075    149.1244     australiacentral2
UAE Central           24.466667   54.366669    uaecentral
UAE North             25.266666   55.316666    uaenorth
South Africa North    -25.731340  28.218370    southafricanorth
South Africa West     -34.075691  18.843266    southafricawest
Switzerland North     47.451542   8.564572     switzerlandnorth
Switzerland West      46.204391   6.143158     switzerlandwest
Germany North         53.073635   8.806422     germanynorth
Germany West Central  50.110924   8.682127     germanywestcentral
Norway West           58.969975   5.733107     norwaywest
Norway East           59.913868   10.752245    norwayeast
bartosz@Azure:~$ RG_NAME="rg-azdev-zad2-cli"
bartosz@Azure:~$ RG_LOCATION="westeurope"
bartosz@Azure:~$ az group create -n $RG_NAME -l $RG_LOCATION
{
  "id": "/subscriptions/748173f1-20c4-4e68-ac58-641f67a83501/resourceGroups/rg-azdev-zad2-cli",
  "location": "westeurope",
  "managedBy": null,
  "name": "rg-azdev-zad2-cli",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}
bartosz@Azure:~$ az group list -o table
Name                            Location    Status
------------------------------  ----------  ---------
rg-automation                   westeurope  Succeeded
rg-azdev-zad2-portal            westeurope  Succeeded
cloud-shell-storage-westeurope  westeurope  Succeeded
rg-azdev-zad2-cli               westeurope  Succeeded
```
</details>

### 1.3 PowerShell
```PowerShell
$RG_NAME="rg-azdev-zad2-powershell"
$RG_LOCATION="westeurope"

New-AzureRmResourceGroup -Name $RG_NAME -Location $RG_LOCATION
```

<details>
  <summary><b><i>Output</i></b></summary>

```PowerShell
PS /home/bartosz> $RG_NAME="rg-azdev-zad2-powershell"
PS /home/bartosz> $RG_LOCATION="westeurope"
PS /home/bartosz> New-AzureRmResourceGroup -Name $RG_NAME -Location $RG_LOCATION

ResourceGroupName : rg-azdev-zad2-powershell
Location          : westeurope
ProvisioningState : Succeeded
Tags              :
ResourceId        : /subscriptions/748173f1-20c4-4e68-ac58-641f67a83501/resourceGroups/rg-azdev-zad2-powershell

PS /home/bartosz> Get-AzureRmResourceGroup

ResourceGroupName : rg-automation
Location          : westeurope
ProvisioningState : Succeeded
Tags              :
                    Name    Value
                    ======  =====
                    Locked  yes

ResourceId        : /subscriptions/748173f1-20c4-4e68-ac58-641f67a83501/resourceGroups/rg-automation

ResourceGroupName : rg-azdev-zad2-portal
Location          : westeurope
ProvisioningState : Succeeded
Tags              :
ResourceId        : /subscriptions/748173f1-20c4-4e68-ac58-641f67a83501/resourceGroups/rg-azdev-zad2-portal

ResourceGroupName : cloud-shell-storage-westeurope
Location          : westeurope
ProvisioningState : Succeeded
Tags              :
ResourceId        : /subscriptions/748173f1-20c4-4e68-ac58-641f67a83501/resourceGroups/cloud-shell-storage-westeurope

ResourceGroupName : rg-azdev-zad2-cli
Location          : westeurope
ProvisioningState : Succeeded
Tags              :
ResourceId        : /subscriptions/748173f1-20c4-4e68-ac58-641f67a83501/resourceGroups/rg-azdev-zad2-cli

ResourceGroupName : rg-azdev-zad2-powershell
Location          : westeurope
ProvisioningState : Succeeded
Tags              :
ResourceId        : /subscriptions/748173f1-20c4-4e68-ac58-641f67a83501/resourceGroups/rg-azdev-zad2-powershell
```
</details>

### 1.4 Azure Rest API

<details>
  <summary><b><i>Postman</i></b></summary>

![azure rest api create resource group][img-azure-rest-api-create-resource-group]
![azure rest api list of resource group][img-azure-rest-api-list-of-resource-group]
</details>



[img-azure-portal-create-resource-group]: ./img/azure-portal-create-resource-group.jpg
[img-azure-portal-review-creating-resource-group]: ./img/azure-portal-review-creating-resource-group.jpg
[img-azure-portal-list-of-resource-group]: ./img/azure-portal-list-of-resource-group.jpg
[img-azure-rest-api-create-resource-group]: ./img/azure-rest-api-create-resource-group.jpg
[img-azure-rest-api-list-of-resource-group]: ./img/azure-rest-api-list-of-resource-group.jpg