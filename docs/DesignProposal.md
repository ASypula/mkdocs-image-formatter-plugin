# 23Z - ZPRP

## Design Proposal

Zespół:

- Julia Jodczyk
- Aleksandra Sypuła
- Mateusz Wasilewski

### Temat

Plug-in do MkDocs ułatwiający ustawianie rozmiarów obrazów w dokumentacji.

### Harmonogram

| Tydzień     | Cel                                                                       |
| ----------- | ------------------------------------------------------------------------- |
| 23.10-29.10 | Badanie tematu i planowanie projektu                                      |
| 30.10-05.11 | Rozpisanie gramatyki do leksera                                           |
| 06.11-12.11 | Implementacja leksera                                                     |
| 13.11-19.11 | Implementacja parsera                                                     |
| 20.11-26.11 | Implementacja interpretera                                                |
| 27.11-03.12 | Integracja rozwiązania jako plugin MkDocs                                 |
| 04.12-10.12 | Dopracowanie dokumentacji projektu                                        |
| 11.12-17.12 | Testy akceptacyjne na kilku wersjach interpretera                         |
| 18.12-22.12 | Prace końcowe nad projektem oraz wystawienie PR (zarejestrowanie plugina) |

### Bibliografia

- [oficjalna strona MkDocs](https://www.mkdocs.org/dev-guide/)
- [repozytorium projektu MkDocs](https://github.com/mkdocs/mkdocs)
- [issue na GitHubie opisujące problem](https://github.com/mkdocs/mkdocs/issues/1678)

### Planowane funkcjonalności programu

- możliwość konfiguracji wymiarów obrazów:
  ```
  # Dodanie odpowiednich wpisów konfiguracyjnych:
  image_sizes:
    large:
      - width: 100px
        height: 50px
    small:
      - width: 80px
        height: 40px
  ```
- automatyczne ustawianie wymiarów obrazów poprzez zdefiniowane tagi
  ```
  @small
  (../images/b.png)
  ```

### Stack technologiczny

- język programowania: Python
- git (GitHub)
  - konwencja commitów:
    - czas przeszły
    - <typ>: [funkcjonalność] opis
      np. feat: [parser] Added token
  - nazewnictwo branchy:
    - przymiotniki odpowiadające funkcjonalnościom
      np. parser, interpreter
- dokumentacja: mkdocs
- autoformatter: black (z flagą `-l 120`)
- linter: flake8
- środowisko wirtualne: venv
- budowanie i testowanie aplikacji z wykorzystaniem `make`
- budowanie paczki - `setup.py` (zgodnie z konwencją pluginów MkDocs)
- wersjonowanie plugina zgodne z [Semantic Versioning 2.0.0](https://semver.org/)
- zapisywanie historii modyfikacji w kolejnych wersjach w pliku [CHANGELOG](https://keepachangelog.com/en/1.1.0/)
- licencja zgodna z licencją [projektu mkdocs](https://github.com/mkdocs/mkdocs/blob/master/LICENSE)
