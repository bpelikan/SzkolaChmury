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
                "equals": "true"
            }
        ]
    },
    "then": {
        "effect": "deny"
    }
  }
}
```