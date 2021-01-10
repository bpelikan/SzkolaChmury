# [Zadanie domowe z tygodnia 3](https://szkolachmury.pl/az-303-microsoft-azure-architect-technologies/tydzien-3-deploying-resources-with-azure-resource-manager/praca-domowa/)

> WAŻNE! Na początku utwórz proste środowisko składające się z systemów Windows oraz Ubuntu. Możesz posłużyć się już znanym Tobie środowiskiem

## 1. Zadanie 4.1
> #TYDZIEN4.1 „Przeanalizuj proszę Azure Security i zainstaluj Endpoint protection na wcześniej utworzonych Vmkach. Przejrzyj usługę Azure Security Center oraz poszukaj opcję rekomendacji pod względem spełniania regulacji - Regulatory Compliance PCI DSS. W miarę możliwości postaraj się wdrożyć dane rekomendacje i podziel się swoimi wnioskami!”

<details>
  <summary><b><i>Utworzone środowisko</i></b></summary>

![Screen](./img/20210109160110.jpg "Screen")
</details>

### 1.1 Przeanalizowanie Azure Security

Jak widać na ponizszych screenach samo uruchomienie VM w chmurze nie gwarantuje ich bezpieczeństwa, 
konieczne jest podjęcie dalszych działań z naszej strony w celu ich zabezpieczeia.

<details>
  <summary><b><i>Azure Security Center</i></b></summary>

![Screen](./img/20210109155421.jpg "Screen")
![Screen](./img/20210109155332.jpg "Screen")
</details>

### 1.2 Zainstalowanie Endpoint protection

<details>
  <summary><b><i>Instalacja Endpoint protection z poziomu Security Center</i></b></summary>

![Screen](./img/20210109145306.jpg "Screen")
![Screen](./img/20210109145443.jpg "Screen")
</details>

Jak widać VM z Ubuntu nie została ujęta w rekomendacjach dotyczących Endpoint protection.<br>
Niestety w moim przypadku ten sposób instalacji dla `vm1` oraz `vm3` się nie powiódł - po zostawieniu VM na noc status instalacji pozostał bez zmian.
Najprawdopodobniej powodem było wyłączenie VM (z racji posiadanej subskrypcji) zaraz po rozpoczęciu instalacji.
Konieczne więc było ręczne zainstalowanie rozszerzenia dla tych VM:

<details>
  <summary><b><i>Instalacja Endpoint protection z poziomu zakładki Extensions dla VM1 oraz VM3</i></b></summary>

![Screen](./img/20210109145715.jpg "Screen")
![Screen](./img/20210109145720.jpg "Screen")
</details>

Dla testów uruchomiłem `vm4`, na której udało mi się zainstalować Endpoint protection z poziomu Security Center:
<details>
  <summary><b><i>Instalacja Endpoint protection z poziomu Security Center dla VM4</i></b></summary>

![Screen](./img/20210109145555.jpg "Screen")
![Screen](./img/20210109161223.jpg "Screen")
</details>

### 1.3 Regulatory Compliance PCI DSS

<details>
  <summary><b><i>Lista wymagań do spełnienia</i></b></summary>

![Screen](./img/20210109162841.jpg "Screen")
</details>

Ze względu na to, że punkt 5 z listy został wykonany w poprzednim ćwiczeniu postanowiłem zaszyfrować dyski maszyn wirtualnych:

<details>
  <summary><b><i>Informacja o konieczności włączenia szyfrowania dysków maszyn</i></b></summary>

![Screen](./img/20210109171402.jpg "Screen")
![Screen](./img/20210109174258.jpg "Screen")
</details>

Szyfrowania dysku dla Ubuntu nie mogłem wykonać - użyta wielkość maszyny `Standard B1ls (1 vcpus, 0.5 GiB memory)` nie jest wspierana przy szyfrowaniu dysku [Supported VMs and operating systems](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/disk-encryption-overview#supported-vms-and-operating-systems).

<details>
  <summary><b><i>Po zaszyfrowaniu</i></b></summary>

![Screen](./img/20210110153244.jpg "Screen")
![Screen](./img/20210110153533.jpg "Screen")
</details>
