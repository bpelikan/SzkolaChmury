# [Zadanie domowe z tygodnia 2](https://szkolachmury.pl/az-303-microsoft-azure-architect-technologies/tydzien-2-application-architecture-patterns-in-azure/praca-domowa/)

## Zadanie 3.1 

| Resource        | Naming convention                                                | Example                              |
|-----------------|------------------------------------------------------------------|--------------------------------------|
| Resource group  | \<klient\>-\<env\>-rg                                            | cl1-prod-rg                          |
| VNET            | \<klient\>-\<env\>-\<project/app\>-\<region\>-vnet               | cl1-prod-szkchm-ne-vnet              |
| VM              | \<klient\>-\<env\>-\<project/app\>-\<region\>-\<OS\>-vm\<number\>| cl1-prod-szkchm-ne-ubuntu-vm1        |
| Disk            | \<vm-name\>-disk\<number\>                                       | cl1-prod-szkchm-ne-ubuntu-vm1-disk1  |
| Storage account | \<klient\>\<env\><project/app>sa\<uniqueID\>                     | cl1prodszkchmsa0912                  |


## Zadanie 3.2

![Screen](./img/20201216212102.jpg "Screen")

### 3.2.1 Utworzenie Resource Group
```bash
RG_NAME="cl1-prod-rg"
LOCATION="westeurope"
az group create --name $RG_NAME --location $LOCATION
```

### 3.2.2 Utworzenie Key Vault oraz sekretów
```bash
# create Key Vault for secrets
RG_NAME_VAULT="cl1-prod-kv-rg"
VAULT_NAME="cl1-prod-szkchm-we-kv"
ADMIN_LOGIN="vmadminlogin$RANDOM"
ADMIN_PASS="AdminPassword$RANDOM"
az group create --name $RG_NAME_VAULT --location $LOCATION
az keyvault create --location $LOCATION --name $VAULT_NAME --resource-group $RG_NAME_VAULT
az keyvault update --name $VAULT_NAME --resource-group $RG_NAME_VAULT --enabled-for-template-deployment true

az keyvault secret set --name "vmAdminUsername" --vault-name $VAULT_NAME --value $ADMIN_LOGIN
az keyvault secret set --name "vmAdminPassword" --vault-name $VAULT_NAME --value $ADMIN_PASS
```
