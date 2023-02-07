# [Zadanie domowe nr 2](https://portal.szkolachmury.pl/products/microsoft-azure-data-engineer/categories/2147545641/posts/2147968150)

Narysuj architekturę usług, skupiając się na usługach danych w Microsoft Azure.

Założenia:
* aplikacja jest uruchomiona w jednym regionie - West Europe - w Microsoft Azure
* aplikacja jest klientem w wersji na przeglądarkę, który pozwala przechowywać użytkownikom notatki
* aplikacja została napisana w ASP.NET i jest uruchomiona na Azure AppService

Wymagania:
* aplikacja potrzebuje przechowywać dane w dowolnej bazie relacyjnej
* dane z tej bazy muszą być dostępne w minimum dwóch inny regionach (w trybie do odczytu)
* bezpieczeństwo jest bardzo istotne, do bazy powinno się móc połączyć tylko z aplikacji. Ruch z internetu powinien być zablokowany.
* baza musi się łatwo skalować - w przyszłości prognozowany jest 10-krotny wzrost liczby użytkowników
* całe rozwiązanie powinno być efektywne kosztowo (co nie znaczy najtańsze, ma spełniać wszystkie wymagania przede wszystkim)

## 1. 
