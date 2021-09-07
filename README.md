# Analiza korejske kpop lestvice

## Kaj je cilj naloge?

Projektna naloga se bo ukvarjala z analizo spletne glasbene lestvice [radia KBS](https://world.kbs.co.kr/service/musictop10.htm?lang=e). Lestvica vključuje le pesmi, ki spadajo pod žanr korejskega popa, bolje znanega kot kpop. Lestvica prikazuje 10 najbolj popularnih pesmi posameznega tedna, obravnaval bom pa obdobje 2015-2020.

## Katere podatke bom zajel?

* naslov pesmi
* zaporedno število tedna, ko se pesem nahaja na lestvici
* ime izvajalca in njegov tip (skupina oz. solo pevec/ka)
* v primeru, ko je izvajalec skupina, tudi število članov
* agencija, pri kateri se nahaja izvajalec
* datum debitiranja
* biografija

## Hipoteze

* Koliko časa je po navadi minilo, odkar so izvajalci na lestvici debitirali? Ali imajo res vedno prednost mlajši?
* Kdo prevladuje na lestvici, soloisti ali skupine?
* Ali obstaja korelacija med številom članov in popularnostjo skupine?
* Ali res prevladujejo izvajalci, ki pripadajo eni izmed top 3 agencij (SM, JYP in YG)?

## Navodila

Za ogled analize enostavno odprite datoteko analiza.ipynb. Koda, s katero sem pobral spletne strani, iz njih izluščil podatke in jih shranil v datoteke csv se nahaja v poberi_lestvice.py. Pomožna orodja pa se nahajajo v orodja.py.