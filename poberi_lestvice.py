import datetime
import orodja

ZACETNI_DATUM = datetime.datetime(2015, 1, 11)
KONCNI_DATUM = datetime.datetime(2020, 12, 27)


trenutni_datum = ZACETNI_DATUM
while trenutni_datum != KONCNI_DATUM:
    trenutni_datum += datetime.timedelta(days=7)
    leto = trenutni_datum.year
    mesec = trenutni_datum.month
    dan = trenutni_datum.day
    url = f'http://world.kbs.co.kr/service/musictop10.htm?lang=e&start_year={leto}&rank_date={leto}-{mesec}-{dan}'
    datoteka = f'kpop-lestvice/{leto}-{mesec}-{dan}.html' 
    orodja.shrani_spletno_stran(url, datoteka)