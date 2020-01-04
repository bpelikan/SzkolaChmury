## [Managing roles and permissions](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-4-cloud-identity-and-access-management/managing-roles-and-permissions-hands-on/)


```bash
# Zmienne
projectId=""
userEmail=""
userRole="roles/viewer"

# Dodanie użytkownika
gcloud projects add-iam-policy-binding $projectId --member user:$userEmail --role $userRole

# Usunięcie użytkownika
gcloud projects remove-iam-policy-binding $projectId --member user:$userEmail --role $userRole

# Przegląd policy
gcloud projects get-iam-policy $projectId --format json > $HOME/policy.json
```

## [Service Accounts](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-4-cloud-identity-and-access-management/service-accounts-hands-on/)

```bash
# Zmienne
name="testserviceaccount"
description="Opis service account ..."
displayName="Testowy Service Account"
projectId=""

# Tworzenie Service Account
gcloud iam service-accounts create $name --description "$description" --display-name "$displayName"

# Lista Service Account
gcloud iam service-accounts list

# Dodanie klucza
gcloud iam service-accounts keys create $HOME/key.json --iam-account $name@$projectId.iam.gserviceaccount.com

# Usunięcie
gcloud iam service-accounts delete $name@$projectId.iam.gserviceaccount.com
rm $HOME/key.json
```

# [Roles and Custom Roles](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-4-cloud-identity-and-access-management/roles-and-custom-roles-hands-on/)

* [Creating a custom role](https://cloud.google.com/iam/docs/creating-custom-roles#creating_a_custom_role)

```bash
# Zmienne
projectId=""
roleId="roleviewertestid"
roleTitle="Test Role Viewer"
roleDescription="My custom role description."
roleStage="ALPHA" #ALPHA, BETA, GA

# Utworzenie pliku yaml z rolą
cat <<EOF > role.yaml
title: "$roleTitle"
description: "$roleDescription"
stage: "$roleStage"
includedPermissions:
- iam.roles.get
- iam.roles.list
EOF

# Utworzenie roli
gcloud iam roles create $roleId --project $projectId --file role.yaml

# Lista ról
gcloud iam roles list

# Opis roli
gcloud iam roles describe $roleId --project $projectId

# Usunięcie
gcloud iam roles delete $roleId --project $projectId
rm role.yaml
```