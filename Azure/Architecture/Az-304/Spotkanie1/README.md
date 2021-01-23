# [Zadanie domowe ze spotkania 1](https://szkolachmury.pl/az-304-microsoft-azure-architect-design/design-landing-zone-basics/zadanie-domowe/)


## 1. Zadanie 1

#### 1.1 Polityka zabrania stworzenia konta typu Azure Storage, które umożliwia dostępu z tzw. Public Endpoints

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

#### 1.2 Polityka zabrania tworzenia serwerów Azure SQL, dostępnych publicznie

* Tworzenie serwera bezpośrednio z portalu nie uwzględnia parametru `publicNetworkAccess`, więc konieczna jest edycja ARM template, żeby móc utworzyć zasób.
* Pomimo dodania wartości `"publicNetworkAccess": "Disabled"` po utworzeniu serwera w ustawieniach firewall nadal nie ma ustawionej wartości `Deny public network access` na `Yes`, przez co w policy compliance serwer oznaczony jest jako niespełniający polityki.

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

