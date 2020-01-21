#########
# Utworzenie AKS
#########
mkdir code
cd code
# code ..

# Service Principal
az ad sp create-for-rbac --skip-assignment -o json > auth.json

# Zmienne
location="westeurope"
resourceGroup="szkchm-rg"
aksName="szkchm-aks"
servicePrincipalClientId=$(jq -r ".appId" auth.json)
servicePrincipalClientSecret=$(jq -r ".password" auth.json)

# Resource Group
az group create --location $location --name $resourceGroup

# AKS
az aks create --generate-ssh-keys -g $resourceGroup -n $aksName --node-count 1 --location $location --service-principal $servicePrincipalClientId --client-secret $servicePrincipalClientSecret 

# Pobranie configa do AKS
az aks get-credentials --resource-group $resourceGroup --name $aksName

#########
# Usunięcie
#########
az group delete --name $resourceGroup --no-wait
az ad sp delete --id $servicePrincipalClientId
cd ..
rm -rf ./code