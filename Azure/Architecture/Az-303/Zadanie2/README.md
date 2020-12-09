# [Zadanie domowe nr 2](https://szkolachmury.pl/az-303-microsoft-azure-architect-technologies/tydzien-2-application-architecture-patterns-in-azure/praca-domowa/)

## Zadanie 2.1 

| Resource        | Naming convention                                                | Example                              |
|-----------------|------------------------------------------------------------------|--------------------------------------|
| Resource group  | \<klient\>-\<env\>-rg                                            | cl1-prod-rg                          |
| VNET            | \<klient\>-\<env\>-\<project/app\>-\<region\>-vnet               | cl1-prod-szkchm-ne-vnet              |
| VM              | \<klient\>-\<env\>-\<project/app\>-\<region\>-\<OS\>-vm\<number\>| cl1-prod-szkchm-ne-ubuntu-vm1        |
| Disk            | \<vm-name\>-disk\<number\>                                       | cl1-prod-szkchm-ne-ubuntu-vm1-disk1  |
| Storage account | \<klient\>\<env\><project/app>sa\<uniqueID\>                     | cl1prodszkchmsa0912                  |
