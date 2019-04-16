# MKRI - Hašovací funkce

## Abstrakt
Projekt do předmětu MKRI má za cíl vyvořit program implementujíci šoučasně používaný hašovací algoritmus. Pro tyto účely byl implemntován hašovací algoritmus MD5 v zdrojovém souboru mkrihash.py a pro porovnání výstupů a demonstraci jiných hašovacích algoritmů byl použit zdrojový soubor mkrihash_lib.py.

## Závislosti
### Spuštění přes příkazový řádek
* Python 3.7.2 nebo vyšší (z důvodu implementace Blake2 a SHA3, při spuštení na GNU/LINUX změňte výchozí symlink python3 na minimální požadovanou verzi, nebo přímo /usr/bin/python37 mkrihash.py ... příp. python.exe mkrihash.py...) 
* argparse
* hashlib
* sys

### Spuštění přes JAVA GUI
* Java JDK 1.8.0_181

## Důležité upozornění
* Java GUI nemusí korektně fungovat pod GNU/LINUX
* Kódování textového vstupu se předpokládá UTF-8 

## Spuštění programu
    ./mkrihash.py [-h] [-v] [-m] [-d] (-t FILE | -b BINARY_FILE | -i INLINE_TEXT)

    Volitelné argumenty:
      -h, --help                                  vytiskne nápovědu
      -v, --version                               vytiskne verzi programu
      -m, --machine-readable                      vytiskne pouze výsledný haš, bez informaci o vstupu
      -d, --debug                                 debugovací mód, vytiskne všcehny mezivýpočty v každé rundě

    Povinné argumenty:
      -t FILE, --text-file FILE                   specifikace textového souboru, který bude zahašovaný
      -b FILE, --binary-file FILE                 specifikace binárního souboru, který bude zahašovaný
      -i INLINE_TEXT, --inline-text INLINE_TEXT   specifikace textu v příkazovém řadku, který bude zahašován
---
    ./mkrihash_lib.py [-h] [-v] [-m] [-d] -a {md5,sha1,sha2,sha3,blake2} (-t FILE | -b BINARY_FILE | -i INLINE_TEXT)

    Volitelné argumenty:
      -h, --help                                  vytiskne nápovědu
      -v, --version                               vytiskne verzi programu
      -m, --machine-readable                      vytiskne pouze výsledný haš, bez informaci o vstupu
      -d, --debug                                 debugovací mód, vytiskne všchne mezivýpočty v každé rundě

    Povinné argumenty:
      -t FILE, --text-file FILE                   specifikace textového souboru, který bude zahašovaný
      -b FILE, --binary-file FILE                 specifikace binárního souboru, který bude zahašovaný
      -i INLINE_TEXT, --inline-text INLINE_TEXT   specifikace textu v příkazovém řadku, který bude zahašován
      -a {md5,sha1,sha2,sha3,blake2}              spcifikace algoritmu použitého pro hašování

## Příklady spuštění
---
    Hašování řetězce zadaného v příkazové řádce

    ./mkrihash.py -i "MY TEXT I WANT TO HASH"


---
    Hašování textového souboru so specifikovanou cestou

    ./mkrihash.py -t "/home/user/text.txt"


---
    Hašování binárního souboru so specifikovanou cestou

    ./mkrihash.py -b "/bin/cp"


---
    Hašování textového souboru pomocí knihovny hashlib a algoritmu MD5

    ./mkrihash_lib.py -t "/home/user/text.txt" -a md5


---
    Hašování textového souboru pomocí knihovny hashlib a algoritmu SHA3-512

    ./mkrihash_lib.py -t "/home/user/text.txt" -a sha3


---
    Spuštení GUI(nad rámec zadání)

    java -jar md5.jar

---
    Black box testování
    
    cd Tests
    ./test_black_box.py

---
    White box testování

    !!POZOR!! Vygeneruje soubory, které mají v součtu více jak 1GB, kterých řádky se porovnávají, je to výstup registrů a funkcí MD5 v každé iteraci.

    cd Tests
    ./test_white_box.py