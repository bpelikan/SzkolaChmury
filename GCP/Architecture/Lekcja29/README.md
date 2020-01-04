# [Managing roles and permissions](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-4-cloud-identity-and-access-management/managing-roles-and-permissions-hands-on/)


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