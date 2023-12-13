Scraper służy do zbierania zawartości ze strony xkom.com.

Kod przegląda wszystkie kategorie sklepu xkom, do których linki są zdefiniowane w liście paths w main,
w poszukiwaniu nazwy kategorii oraz nazw wszystkich przynależnych jej subkategorii.
Wynik przeglądu zostaje zapisany w ScraperResults/categoriesAndSubcategories.txt. Kategorie są w oddzielnych liniach, a ich subkategorie rozdzielone znakiem ';'.

Format
Kategoria1;subkategoria1.1;subkategoria1.2\n
Kategoria2;subkategoria2.1;subkategoria2.2\n


Następnie program iteruje po kategoriach i ich produktach.
Następnie analizowane są podstrony zawartych w niej produktów.
Ze stron list produktów danej kategorii każdemu produktowi przypisywane są: Kategoria, nazwa i lista atrybutów.

Program wchodzi również na stronę każdego przeglądanego produktu.

Ze strony produktu zostają wyciągnięte kategoria, przynależność do subkategorii, obrazek większej rozdzielczości w formie linka oraz krótki i długi opis.

Wszystkie dane poza opisami są zapisane w ScraperResults/products.txt. Każdy produkt znajduje się w osobnej linii, a jego właściwości są rozdzielone znakiem ';'.

Format
kategoria;subkategoria;nazwa;atrybut1;atrybut2;atrybut3;obrazek_małej_rozdzielczości;obrazek_duz_rozdzielczości\n

Liczba atrybutów jest zmienna, do dostępu do obrazków zalecane jest używanie ujemnych indeksów.

Opisy są zapisane w ScraperResults/desc.txt, ze względu na ich rozmiar i występowanie znaku nowej linii, poszczególne opisy są rozdzielone linią '---\n'.
Pierwsza linijka opisu służy za opis krótki, połączona z resztą stanowi opis długi. 