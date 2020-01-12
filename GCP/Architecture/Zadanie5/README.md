# [Zadanie domowe nr 5](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-5-instance-groups-i-autoskalowanie/zadanie-domowe-nr-5/)

1. Na ten moment firma nie może zrezygnować z maszyn wirtualnych, dlatego nowa architektura musi korzystać z wirtualnych maszyn postawionych z niestandardowego obrazu, dostarczonego bezpośrednio przez firmę.
2. Rozwiązanie musi dynamicznie skalować się w górę lub w dół w zależności od aktywności w grze - bez większej ingerencji specjalistów
3. Gracze korzystający z funkcjonalności firmy pochodzą z całego świata, a w szczególności z Stanów Zjednoczonych oraz Europy. Poprzez odpowiednie umiejscowienie rozwiązania MountKirk chce zredukować opóźnienie jakie występuje dla osób łączących się z US.
4. Rozwiązanie musi zapobiegać jakiejkolwiek przerwie w dostarczaniu funkcjonalności na wypadek awarii np. regionu Google Cloud.
5. Rozwiązanie musi umożliwość łatwe i bezpiecznie wdrażanie nowych wersji oprogramowania do instancji bez konieczności wpływania na całe środowisko.

# 1. Rozwiązanie
Użycie [Managed Instance Groups](https://cloud.google.com/compute/docs/instance-groups/) pozwoli spełnić powyższe założenia:
* Zapewnienie **High availability**:
  * **Keeping instances running** - w przypadku niezamierzonego wyłączenia/usunięcia maszyny, VM zostanie automatycznie odtworzona na nowo
  * [**Autohealing**](https://cloud.google.com/compute/docs/instance-groups/#autohealing) - w przypadku błędnego kodu odpowiedzi z aplikacji, maszyna zostanie usunięta i odtworzona na nowo
  * [**Regional (multiple zone) coverage**](https://cloud.google.com/compute/docs/instance-groups/#types_of_managed_instance_groups) - umieszczenie maszyn w różnych strefach pozwala na zabezpieczenie się przed awarią jednego z nich oraz rozłożeniem ruchu pomiędzy strefy. Natomiast umieszczenie w różnych regionach pomaga zmniejszyć opóźnienie w przypadku posiadania użytkowników z różnych części świata. W wyborze regionów pomóc może zbieranie metryk z informacją o lokalizacji użytkownika, ich ilości w danym regionie oraz występujących opóźnieniach.
  * [**Load balancing**](https://cloud.google.com/compute/docs/instance-groups/#load_balancing) - równomierne rozłożenie ruchu pomiędzy maszynami w danej strefie oraz pomiędzy samymi strefami. Wybór regionu do którego użytkownik zostanie przekierowany na podstawie najkrótszego opóźnienia. W przypadku awarii regionu/strefy tymczasowe przekierowanie ruchu do działającego regionu/strefy (zapewnienie **HA**).
* [**Scalability**](https://cloud.google.com/compute/docs/instance-groups/#autoscaling) - **MIG** automatycznie zeskaluje środowisko w zależności od obciążenia oraz naszej [polityki skalowania](https://cloud.google.com/compute/docs/autoscaler/#policies).
* [**Automated updates**](https://cloud.google.com/compute/docs/instance-groups/#automatic_updating) - umożliwia wykonanie **Rolling updates** oraz **Canary updates**, czyli wykonanie aktualizacji w dość bezpieczny sposób z możliwością łatwego przywrócenia poprzedniej wersji.

