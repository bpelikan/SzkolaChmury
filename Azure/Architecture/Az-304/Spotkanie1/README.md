# [Zadanie domowe ze spotkania 1](https://szkolachmury.pl/az-304-microsoft-azure-architect-design/design-landing-zone-basics/zadanie-domowe/)

## 1. Zadanie 1

> 1) Spróbuj utworzyć zestaw polityk, które spełniają następujące oczekiwania i zapisz swoje wymiki prac:
> * polityka zabrania stworzenia konta typu Azure Storage, które umożliwia dostępu z tzw. Public Endpoints
> * polityka zabrania tworzenia serwerów Azure SQL, dostępnych publicznie
> * polityka zabrania tworzenia zasobów, które nie mają Tag’u o nazwie Project
> * polityka zabrania tworzenia zasobów, które nie mają Tag’u o nazwie Owner i którego zawartość nie zawiera maila np. w domenie abc.pl. Czyli tag Owner o wartości michal@abc.pl jest OK. ale tag o wartości michal@asd.com już nie
> * polityka wymusza by każda stworzona maszyna była od razu podłączona do usługi Azure Log Analytics, które będzie parameterem polityki

> [Azure Policy built-in policy definitions](https://docs.microsoft.com/en-us/azure/governance/policy/samples/built-in-policies)

```
$RG_NAME=""
az policy state trigger-scan --resource-group $RG_NAME --no-wait
az policy state trigger-scan --no-wait
```

### 1.1 Polityka zabrania stworzenia konta typu Azure Storage, które umożliwia dostępu z tzw. Public Endpoints

* [ASC_Storage_DisallowPublicBlobAccess_Audit.json](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Storage/ASC_Storage_DisallowPublicBlobAccess_Audit.json)
* [VirtualNetworkServiceEndpoint_StorageAccount_Audit.json](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Network/VirtualNetworkServiceEndpoint_StorageAccount_Audit.json) - ustawiając `deny` nadal mogę przypisać dostęp dla publicznego IP

<details>
  <summary><b><i>Polityka 1.1</i></b></summary>

```json
{
  "policyRule": {
    "if": {
        "allOf": [{
                "field": "type",
                "equals": "Microsoft.Storage/storageAccounts"
            },
            {
                "field": "Microsoft.Storage/storageAccounts/allowBlobPublicAccess",
                "notEquals": "false"
            }
        ]
    },
    "then": {
        "effect": "deny"
    }
  }
}
```
</details>

### 1.2 Polityka zabrania tworzenia serwerów Azure SQL, dostępnych publicznie

* [SqlServer_PublicNetworkAccess_Audit.json](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/SQL/SqlServer_PublicNetworkAccess_Audit.json)
* Tworzenie serwera bezpośrednio z portalu nie uwzględnia parametru `publicNetworkAccess`, więc konieczna jest edycja ARM template, żeby móc utworzyć zasób.
* Pomimo dodania wartości `"publicNetworkAccess": "Disabled"` po utworzeniu serwera w ustawieniach firewall nadal nie ma ustawionej wartości `Deny public network access` na `Yes`, przez co w policy compliance serwer oznaczony jest jako niespełniający polityki.

<details>
  <summary><b><i>Polityka 1.2</i></b></summary>

```json
{
  "policyRule": {
    "if": {
        "allOf": [{
                "field": "type",
                "equals": "Microsoft.Sql/servers"
            },
            {
                "field": "Microsoft.Sql/servers/publicNetworkAccess",
                "notEquals": "Disabled"
            }
        ]
    },
    "then": {
        "effect": "deny"
    }
  }
}
```
</details>

### 1.3 Polityka zabrania tworzenia zasobów, które nie mają Tag’u o nazwie Project
* [RequireTag_Deny.json](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Tags/RequireTag_Deny.json)
* Warto pamiętać o `"mode": "Indexed"`, bo w przypadku `"mode": "All",` i przypisania poliyki do rg, nie będziemy mieli możliwości przypisania polityk do rg.

<details>
  <summary><b><i>Polityka 1.3</i></b></summary>

```json
{
  "mode": "Indexed",
  "parameters": {
      "tagName": {
        "type": "String",
        "metadata": {
            "displayName": "Tag Name",
            "description": "Name of the tag"
        }
      }
  },
  "policyRule": {
    "if": {
        "field": "[concat('tags[', parameters('tagName'), ']')]",
        "notLike": "*"
    },
    "then": {
        "effect": "deny"
    }
  }
}
```
</details>

### 1.4 Polityka zabrania tworzenia zasobów, które nie mają Tag’u o nazwie Owner i którego zawartość nie zawiera maila

<details>
  <summary><b><i>Polityka 1.4</i></b></summary>

```json
{
  "mode": "Indexed",
  "parameters": {
      "emailDomain": {
        "type": "String",
        "metadata": {
            "displayName": "Email domain",
            "description": "Name of email domain"
        }
      }
  },
  "policyRule": {
    "if": {
        "field": "[tags['Owner']]",
        "notLike": "[concat('*@', parameters('emailDomain'))]"
    },
    "then": {
        "effect": "deny"
    }
  }
}
```
</details>

### 1.5 polityka wymusza by każda stworzona maszyna była od razu podłączona do usługi Azure Log Analytics, które będzie parameterem polityki

* [Provisions the Log Analytics by Azure Security Center](https://docs.microsoft.com/en-us/azure/virtual-machines/extensions/oms-windows#azure-security-center)
* [DeployIfNotExists](https://docs.microsoft.com/en-us/azure/governance/policy/concepts/effects#deployifnotexists)
* [Azure built-in roles](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles)
* [Policy functions](https://docs.microsoft.com/en-us/azure/governance/policy/concepts/definition-structure#policy-functions)
* [VirtualMachines_LogAnalyticsAgent_AuditIfNotExists.json](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Monitoring/VirtualMachines_LogAnalyticsAgent_AuditIfNotExists.json)
* [LogAnalyticsExtension_Windows_VM_Deploy.json](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Monitoring/LogAnalyticsExtension_Windows_VM_Deploy.json)
* [LogAnalyticsExtension_Linux_VM_Deploy.json](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Monitoring/LogAnalyticsExtension_Linux_VM_Deploy.json)
* polityka przepina obecne VM na podany w parametrze Log Analytics Workspace ID po wykonaniu remediation task
* dodatkowy parametr `logAnalyticsWorkspaceID` konieczny był ze względu na brak możliwości wykorzystania funkcji `[reference(parameters('logAnalytics'), '2015-03-20').customerId]` w polityce - [Policy functions](https://docs.microsoft.com/en-us/azure/governance/policy/concepts/definition-structure#policy-functions). W polityce dla Linuxa parametr pominąłem, bo pojawiały się problemy z przepinaniem Log Analytics.

<details>
  <summary><b><i>Polityka 1.5.1 - Windows</i></b></summary>

```json
{
  "mode": "Indexed",
  "parameters": {
    "logAnalytics": {
        "type": "String",
        "metadata": {
          "displayName": "Log Analytics workspace",
          "description": "Select Log Analytics workspace from dropdown list. If this workspace is outside of the scope of the assignment you must manually grant 'Log Analytics Contributor' permissions (or similar) to the policy assignment's principal ID.",
          "strongType": "omsWorkspace",
          "assignPermissions": true
        }
    },
    "logAnalyticsWorkspaceID": {
      "type": "String",
      "metadata": {
          "displayName": "Log Analytics workspace ID",
          "description": "Log Analytics workspace ID"
      }
    },
    "listOfImageIdToInclude": {
        "type": "Array",
        "defaultValue": [],
        "metadata": {
          "displayName": "Optional: List of VM images that have supported Windows OS to add to scope",
          "description": "Example values: '/subscriptions/<subscriptionId>/resourceGroups/YourResourceGroup/providers/Microsoft.Compute/images/ContosoStdImage'"
        }
    }
  },
  "policyRule": {
    "if": {
        "allOf": [
          {
              "field": "type",
              "equals": "Microsoft.Compute/virtualMachines"
          },
          {
              "anyOf": [
                {
                    "field": "Microsoft.Compute/imageId",
                    "in": "[parameters('listOfImageIdToInclude')]"
                },
                {
                    "allOf": [
                      {
                          "field": "Microsoft.Compute/imagePublisher",
                          "equals": "MicrosoftWindowsServer"
                      },
                      {
                          "field": "Microsoft.Compute/imageOffer",
                          "equals": "WindowsServer"
                      },
                      {
                          "field": "Microsoft.Compute/imageSKU",
                          "in": [
                            "2008-R2-SP1",
                            "2008-R2-SP1-smalldisk",
                            "2012-Datacenter",
                            "2012-Datacenter-smalldisk",
                            "2012-R2-Datacenter",
                            "2012-R2-Datacenter-smalldisk",
                            "2016-Datacenter",
                            "2016-Datacenter-Server-Core",
                            "2016-Datacenter-Server-Core-smalldisk",
                            "2016-Datacenter-smalldisk",
                            "2016-Datacenter-with-Containers",
                            "2016-Datacenter-with-RDSH",
                            "2019-Datacenter",
                            "2019-Datacenter-Core",
                            "2019-Datacenter-Core-smalldisk",
                            "2019-Datacenter-Core-with-Containers",
                            "2019-Datacenter-Core-with-Containers-smalldisk",
                            "2019-Datacenter-smalldisk",
                            "2019-Datacenter-with-Containers",
                            "2019-Datacenter-with-Containers-smalldisk",
                            "2019-Datacenter-zhcn"
                          ]
                      }
                    ]
                },
                {
                    "allOf": [
                      {
                          "field": "Microsoft.Compute/imagePublisher",
                          "equals": "MicrosoftWindowsDesktop"
                      },
                      {
                          "field": "Microsoft.Compute/imageOffer",
                          "equals": "Windows-10"
                      }
                    ]
                }
              ]
          }
        ]
    },
    "then": {
        "effect": "deployIfNotExists",
        "details": {
          "type": "Microsoft.Compute/virtualMachines/extensions",
          "roleDefinitionIds": [
              "/providers/microsoft.authorization/roleDefinitions/92aaf0da-9dab-42b6-94a3-d43ce8d16293"
          ],
          "existenceCondition": {
              "allOf": [
                {
                    "field": "Microsoft.Compute/virtualMachines/extensions/type",
                    "equals": "MicrosoftMonitoringAgent"
                },
                {
                    "field": "Microsoft.Compute/virtualMachines/extensions/publisher",
                    "equals": "Microsoft.EnterpriseCloud.Monitoring"
                },
                {
                    "field": "Microsoft.Compute/virtualMachines/extensions/provisioningState",
                    "equals": "Succeeded"
                },
                { 
                  "field": "Microsoft.Compute/virtualMachines/extensions/settings.workspaceId",
                  "equals": "[parameters('logAnalyticsWorkspaceID')]"
                }
              ]
          },
          "deployment": {
              "properties": {
                "mode": "incremental",
                "template": {
                    "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                    "contentVersion": "1.0.0.0",
                    "parameters": {
                      "vmName": {
                          "type": "string"
                      },
                      "location": {
                          "type": "string"
                      },
                      "logAnalytics": {
                          "type": "string"
                      }
                    },
                    "variables": {
                      "vmExtensionName": "MicrosoftMonitoringAgent",
                      "vmExtensionPublisher": "Microsoft.EnterpriseCloud.Monitoring",
                      "vmExtensionType": "MicrosoftMonitoringAgent",
                      "vmExtensionTypeHandlerVersion": "1.0"
                    },
                    "resources": [
                      {
                          "name": "[concat(parameters('vmName'), '/', variables('vmExtensionName'))]",
                          "type": "Microsoft.Compute/virtualMachines/extensions",
                          "location": "[parameters('location')]",
                          "apiVersion": "2018-06-01",
                          "properties": {
                            "publisher": "[variables('vmExtensionPublisher')]",
                            "type": "[variables('vmExtensionType')]",
                            "typeHandlerVersion": "[variables('vmExtensionTypeHandlerVersion')]",
                            "autoUpgradeMinorVersion": true,
                            "settings": {
                                "workspaceId": "[reference(parameters('logAnalytics'), '2015-03-20').customerId]",
                                "stopOnMultipleConnections": "true"
                            },
                            "protectedSettings": {
                                "workspaceKey": "[listKeys(parameters('logAnalytics'), '2015-03-20').primarySharedKey]"
                            }
                          }
                      }
                    ],
                    "outputs": {
                      "policy": {
                          "type": "string",
                          "value": "[concat('Enabled extension for VM', ': ', parameters('vmName'), 'Log Analytics Param: ', parameters('logAnalytics'))]"
                      }
                    }
                },
                "parameters": {
                    "vmName": {
                      "value": "[field('name')]"
                    },
                    "location": {
                      "value": "[field('location')]"
                    },
                    "logAnalytics": {
                      "value": "[parameters('logAnalytics')]"
                    }
                }
              }
          }
        }
    }
  }
}
```
</details>

<details>
  <summary><b><i>Polityka 1.5.2 - Linux</i></b></summary>

```json
{
    "mode": "Indexed",
    "parameters": {
        "logAnalytics": {
            "type": "String",
            "metadata": {
                "displayName": "Log Analytics workspace",
                "description": "Select Log Analytics workspace from dropdown list. If this workspace is outside of the scope of the assignment you must manually grant 'Log Analytics Contributor' permissions (or similar) to the policy assignment's principal ID.",
                "strongType": "omsWorkspace",
                "assignPermissions": true
            }
        },
        "listOfImageIdToInclude": {
            "type": "Array",
            "defaultValue": [],
            "metadata": {
                "displayName": "Optional: List of VM images that have supported Linux OS to add to scope",
                "description": "Example value: '/subscriptions/<subscriptionId>/resourceGroups/YourResourceGroup/providers/Microsoft.Compute/images/ContosoStdImage'"
            }
        }
    },
    "policyRule": {
        "if": {
            "allOf": [
                {
                    "field": "type",
                    "equals": "Microsoft.Compute/virtualMachines"
                },
                {
                    "anyOf": [
                        {
                            "field": "Microsoft.Compute/imageId",
                            "in": "[parameters('listOfImageIdToInclude')]"
                        },
                        {
                            "allOf": [
                                {
                                    "field": "Microsoft.Compute/imagePublisher",
                                    "equals": "Canonical"
                                },
                                {
                                    "field": "Microsoft.Compute/imageOffer",
                                    "in": [
                                        "UbuntuServer",
                                        "0001-com-ubuntu-server-focal"
                                    ]
                                },
                                {
                                    "anyOf": [
                                        {
                                            "field": "Microsoft.Compute/imageSKU",
                                            "like": "14.04*LTS"
                                        },
                                        {
                                            "field": "Microsoft.Compute/imageSKU",
                                            "like": "16.04*LTS"
                                        },
                                        {
                                            "field": "Microsoft.Compute/imageSKU",
                                            "like": "16_04*lts-gen2"
                                        },
                                        {
                                            "field": "Microsoft.Compute/imageSKU",
                                            "like": "18.04*LTS"
                                        },
                                        {
                                            "field": "Microsoft.Compute/imageSKU",
                                            "like": "18_04*lts-gen2"
                                        },
                                        {
                                            "field": "Microsoft.Compute/imageSKU",
                                            "like": "20_04*lts"
                                        },
                                        {
                                            "field": "Microsoft.Compute/imageSKU",
                                            "like": "20_04*lts-gen2"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "then": {
            "effect": "deployIfNotExists",
            "details": {
                "type": "Microsoft.Compute/virtualMachines/extensions",
                "roleDefinitionIds": [
                    "/providers/microsoft.authorization/roleDefinitions/92aaf0da-9dab-42b6-94a3-d43ce8d16293"
                ],
                "existenceCondition": {
                    "allOf": [
                        {
                            "field": "Microsoft.Compute/virtualMachines/extensions/type",
                            "equals": "OmsAgentForLinux"
                        },
                        {
                            "field": "Microsoft.Compute/virtualMachines/extensions/publisher",
                            "equals": "Microsoft.EnterpriseCloud.Monitoring"
                        },
                        {
                            "field": "Microsoft.Compute/virtualMachines/extensions/provisioningState",
                            "equals": "Succeeded"
                        }
                    ]
                },
                "deployment": {
                    "properties": {
                        "mode": "incremental",
                        "template": {
                            "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                            "contentVersion": "1.0.0.0",
                            "parameters": {
                                "vmName": {
                                    "type": "string"
                                },
                                "location": {
                                    "type": "string"
                                },
                                "logAnalytics": {
                                    "type": "string"
                                }
                            },
                            "variables": {
                                "vmExtensionName": "OMSAgentForLinux",
                                "vmExtensionPublisher": "Microsoft.EnterpriseCloud.Monitoring",
                                "vmExtensionType": "OmsAgentForLinux",
                                "vmExtensionTypeHandlerVersion": "1.13"
                            },
                            "resources": [
                                {
                                    "name": "[concat(parameters('vmName'), '/', variables('vmExtensionName'))]",
                                    "type": "Microsoft.Compute/virtualMachines/extensions",
                                    "location": "[parameters('location')]",
                                    "apiVersion": "2018-06-01",
                                    "properties": {
                                        "publisher": "[variables('vmExtensionPublisher')]",
                                        "type": "[variables('vmExtensionType')]",
                                        "typeHandlerVersion": "[variables('vmExtensionTypeHandlerVersion')]",
                                        "autoUpgradeMinorVersion": true,
                                        "settings": {
                                            "workspaceId": "[reference(parameters('logAnalytics'), '2015-03-20').customerId]",
                                            "stopOnMultipleConnections": "true"
                                        },
                                        "protectedSettings": {
                                            "workspaceKey": "[listKeys(parameters('logAnalytics'), '2015-03-20').primarySharedKey]"
                                        }
                                    }
                                }
                            ],
                            "outputs": {
                                "policy": {
                                    "type": "string",
                                    "value": "[concat('Enabled extension for VM', ': ', parameters('vmName'), 'Log Analytics Param: ', parameters('logAnalytics'))]"
                                }
                            }
                        },
                        "parameters": {
                            "vmName": {
                                "value": "[field('name')]"
                            },
                            "location": {
                                "value": "[field('location')]"
                            },
                            "logAnalytics": {
                                "value": "[parameters('logAnalytics')]"
                            }
                        }
                    }
                }
            }
        }
    }
}

```
</details>