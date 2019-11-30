# [Lekcja 84](https://szkolachmury.pl/kubernetes/tydzien-10-role-i-uprawnienia/azure-key-vault/)

<details>
  <summary><b><i>Skrypt</i></b></summary>

```bash
mkdir code
cd code
# code .

# Utworzenie Service Principal
az ad sp create-for-rbac --skip-assignment -o json > auth.json

# zmienne
location="westeurope"
resourceGroup="szkchmtyg10"
aksName="AKStyg10"
servicePrincipalClientId=$(jq -r ".appId" auth.json)
servicePrincipalClientSecret=$(jq -r ".password" auth.json)

# Utworzenie resource group
az group create --location $location --name $resourceGroup

# Utworzenie Key Vault
keyVaultName="szkchmtyg10keyvault"
az keyvault create --location $location --name $keyVaultName --resource-group $resourceGroup -o json > keyVault.json

# Pobranie ID Key Vault
keyVaultId=$(jq -r ".id" keyVault.json)

# Utworzenie secretu w KeyVault
secretName="test-key"
az keyvault secret set --name $secretName --vault-name $keyVaultName --value "moj sekretny value :)"

# Utworzenie klastra AKS
az aks create --enable-rbac --generate-ssh-keys -g $resourceGroup -n $aksName --node-count 1 --location $location --service-principal $servicePrincipalClientId --client-secret $servicePrincipalClientSecret

# Pobranie credentials AKS
az aks get-credentials --resource-group $resourceGroup --name $aksName

# Instalacja FlexVolume
curl https://raw.githubusercontent.com/Azure/kubernetes-keyvault-flexvol/master/deployment/kv-flexvol-installer.yaml > kv-flexvol-installer.yaml
kubectl create -f kv-flexvol-installer.yaml

# Sprawdzenie
kubectl get DaemonSet -n kv
kubectl get pod -n kv
kubectl describe pod keyvault-flexvolume-mjlwq -n kv
kubectl describe daemonset keyvault-flexvolume -n kv

#Instalacja AAD POD Identity
curl https://raw.githubusercontent.com/Azure/aad-pod-identity/master/deploy/infra/deployment-rbac.yaml > deployment-rbac.yaml
kubectl create -f deployment-rbac.yaml

# Sprawdzenie
kubectl get pod -A

# Stworzenie Managed Identity
managedIdentityName="managedidentityszkchm"
az identity create -g $resourceGroup -n $managedIdentityName -o json > managedIdentity.json

# Podranie wartości z MI
managedIdentityClientId=$(jq -r ".clientId" managedIdentity.json)
managedIdentityId=$(jq -r ".id" managedIdentity.json)

# Przypisanie roli Managed Identity Operator dla MI
# servicePrincipalClientId=$(az aks show -g $resourceGroup -n $aksName --query servicePrincipalProfile.clientId -o tsv) 
# Powyższe polecenie jest konieczne w przypadku stworzenia AKS bez podawania Service Principal (kiedy AKS sam domyślnie utworzył dla siebie Service Principal)
az role assignment create --role "Managed Identity Operator" --assignee $servicePrincipalClientId --scope $managedIdentityId

# Dodanie roli dla MI do odczytu zawartości KeyVaulta
az role assignment create --role Reader --assignee $managedIdentityClientId --scope $keyVaultId

# Utworzenie polityki w Key Vault
az keyvault set-policy -n $keyVaultName --secret-permissions get --spn $managedIdentityClientId

# Utworzenie Azure Identity w AKS
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Lekcja84/code/01_aadpi.yaml > 01_aadpi.yaml
miName="pod-id-1"
sed -i "s|<mi_name>|${miName}|g" 01_aadpi.yaml
sed -i "s|<clientId>|${managedIdentityClientId}|g" 01_aadpi.yaml
sed -i "s|<managedIdentityId>|${managedIdentityId}|g" 01_aadpi.yaml
kubectl apply -f 01_aadpi.yaml

# Utworzenie Azure Identity Binding
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Lekcja84/code/02_binding.yaml > 02_binding.yaml
selectorLabel="pod-with-identity"
sed -i "s|<mi_name>|${miName}|g" 02_binding.yaml
sed -i "s|<selector_label>|${selectorLabel}|g" 02_binding.yaml
kubectl apply -f 02_binding.yaml

# Przygotowanie pliku deploymentu
curl https://raw.githubusercontent.com/bpelikan/SzkolaChmury/master/Kubernetes/Lekcja84/code/03_deployment.yaml > 03_deployment.yaml
az account show -o json > subscription.json
subscriptionId=$(jq -r ".id" subscription.json)
tenantId=$(jq -r ".tenantId" subscription.json)
sed -i "s|<selector_label>|${selectorLabel}|g" 03_deployment.yaml
sed -i "s|<kv_name>|${keyVaultName}|g" 03_deployment.yaml
sed -i "s|<secret_name>|${secretName}|g" 03_deployment.yaml
sed -i "s|<rg_name>|${resourceGroup}|g" 03_deployment.yaml
sed -i "s|<subscription_id>|${subscriptionId}|g" 03_deployment.yaml
sed -i "s|<tenant_id>|${tenantId}|g" 03_deployment.yaml
kubectl apply -f 03_deployment.yaml

# Sprawdzenie
kubectl get pod
kubectl exec -it nginx-pod-id cat /kvmnt/$secretName
```


```bash
# Wyczyszczenie środowiska
az group delete --name $resourceGroup --no-wait
az ad sp delete --id $servicePrincipalClientId
# cd ..
# rm -rf ./code
```
</details>



# Pliki

* [01_aadpi.yaml](./code/01_aadpi.yaml)
* [02_binding.yaml](./code/02_binding.yaml)
* [03_deployment.yaml](./code/03_deployment.yaml)

# Dodatkowe materiały

* [Key Vault FlexVolume](https://github.com/Azure/kubernetes-keyvault-flexvol)
* [AAD Pod Identity](https://github.com/Azure/aad-pod-identity)
