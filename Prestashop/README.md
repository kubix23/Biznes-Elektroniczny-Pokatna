
# Biznes-Elektroniczny-Pokatna

  

Jest to krótki tutorial jak uruchomić Prestashop

Musimy rozróżnić dwa przypadki:

- Windows

- Linux

  

Jeżeli używany jest linux można pominąć etap konfiguracji WSL

  

## Konfiguracja WSL

- [Docker](https://docs.docker.com/desktop/wsl/)

- [Windows](https://learn.microsoft.com/en-us/windows/wsl/install)

  

Powyżej wymienione są dwa linki do poradnika jak to zrobić, ale poniżej pokrótce to przedstawię.

  

1. Używamy komendy `wsl --install` w PowerShell. Jeżeli jest już zainstalowany Docker nie powinno to być konieczne

2. Wpisujemy `wsl.exe --set-default-version 2`, aby każda dokonana instalacja była w wersji 2

3. Instalujemy teraz dystrybucję Linuxa, polecam skorzystać po prostu z Ubuntu `wsl --install -d Ubuntu`

4. W moim przypadku konieczne było podniesiecie wersji do 2, ale można sprawdzić wersje swojej dystrybucji tą komendą `wsl.exe -l -v`

- Podnosimy wersję korzystając z tego `wsl.exe --set-version Ubuntu 2`

5. Ustawiamy naszą dystrybucję jako domyślną `wsl --set-default Ubuntu`

6. W **Settings** > **Resources** > **WSL Integration** ustawiamy naszą dystrybucję

![](docker.png)

  

## Uruchomienie Prestashop

  

Po pobraniu plików źródłowych wystarczy umieścić je w dowolnym (w przypadku WSL, to w dowolnym, ale na WSL) folderze. Następnie znajdując się w terminalu w wybranym folderze nadajemy uprawnienia 777 wszystkim plikom i uruchamiamy `docker-compose up` i dzieje się magia. Uruchomi na się plik konfiguracyjny _docker-compose.yml_, który zainstaluje wymagane kontenery. Powinno to zająć około minuty, po tym czasie będzie możliwość wejścia w stronę sklepu.
**Uwaga doatkowy krok przy pierwszym uruchomieniu:**
Po uruchomieniu sklepu konieczne jest cofnięcie zmian, aby być 1:1 z stanem jaki występuje na GitHub. Najpierw ustawiamy uprawnienia plików na 777, następnie pomocne może być skorzystanie z polecenia `Git reset --hard`. 
Od tego momentu można korzystać z standardowych komend do uruchamiania i wyłączania dockera.

- Uruchamianie: `docker-compose up`

- Wyłączanie: `docker-compose down`

- Login do bazy danych: **root**

- Hasło do bazy danych: **prestashop**

- Login administratora: **demo@prestashop.com**

- Hasło administratora: **12345678**

- Adres do:

- [Prestashop](http://localhost:8080)

- [Panelu administratora](http://localhost:8080/admin-dev)

- [PhpMyAdmin]( http://localhost:8081)
