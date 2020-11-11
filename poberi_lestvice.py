import re
import requests
import datetime
import orodja

STEVILO_TEDNOV = 52

def nalozi_stran(url):
    print(f'Nalagam {url}...')
    odziv = requests.get(url)
    return odziv.text

vzorec_bloka = re.compile(
    r'<!--div class="icon"></div-->'
    r'.*?'
    r'<div class="link"><a href="#" class="menu"><span>Artist Info.</span></a></div>',
    flags=re.DOTALL
)

vzorec_pesmi = re.compile(
    r'<div class="ranking"><span class="hidden">Ranking: </span><strong>'
    r'(?P<mesto>\d+)'
    r'</strong>.*?<div class="tit"><strong>'
    r'(?P<naslov>.+?)'
    r'</strong>.*?<a href="'
    r'.*?seq='
    r'(?P<sifra_umetnika>\d+)'
    r'.*?>'
    r'(?P<ime_umetnika>.+?)'
    r'</a>',
    flags=re.DOTALL
)

vzorec_zalozba = re.compile(
    r'Labels:.*?</strong>'
    r'(?P<zalozba>.+?)'
    r'(&nbsp;)?</p>'
)

vzorec_debut = re.compile(
    r'[Debut|Active from]:.*?</strong>'
    r'(?P<debut>\d{4})'
    r'.*?(&nbsp;)?</p>',
)

vzorec_clani = re.compile(
    r'Members:.*?</strong>'
    r'(?P<clani>.+?)'
    r'(&nbsp;)?</p>',
)

vzorec_biografija = re.compile(
    r'"fr-fic fr-dib fr-fil"></p><p>'
    r'(?P<biografija>\w.*?)'
    r'( &nbsp;)?</p>'
)

vzorec = re.compile(
    r'<div class="ranking"><span class="hidden">Ranking: </span><strong>'
    r'(?P<mesto>\d+)'
    r'</strong>.*?<div class="tit"><strong>'
    r'(?P<naslov>.+?)'
    r'</strong>.*?<a href="'
    r'.*?seq='
    r'(?P<sifra_umetnika>\d+)'
    r'.*?>'
    r'(?P<ime_umetnika>.+?)'
    r'</a>',
    flags=re.DOTALL
)

for teden in range(STEVILO_TEDNOV):
    datum = datetime.datetime(2020, 11, 8) - datetime.timedelta(days=7 * teden)
    url = f'http://world.kbs.co.kr/service/musictop10.htm?lang=e&start_year={datum.year}&rank_date={datum.year}-{datum.month}-{datum.day}'
    vsebina = nalozi_stran(url)
    with open(f'teden_zacensi_z_{datum.year}-{datum.month}-{datum.day}.html', 'w', encoding='utf8') as d:
        d.write(vsebina)
    with open(f'teden_zacensi_z_{datum.year}-{datum.month}-{datum.day}.html', encoding='utf8') as d:
        vsebina = d.read()


def lestvica(datum):
    url = f'http://world.kbs.co.kr/service/musictop10.htm?lang=e&start_year={datum.year}&rank_date={datum.year}-{datum.month}-{datum.day}'
    ime_datoteke = f'teden_zacensi_z_{datum.year}-{datum.month}-{datum.day}.html'
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izlusci_podatke_pesmi(blok.group(0))

def izlusci_podatke_pesmi(blok):
    pesem = vzorec_pesmi.search(blok).groupdict()
    pesem['mesto'] = int(pesem['mesto'])
    pesem['sifra_umetnika'] = int(pesem['sifra_umetnika'])
    return pesem    

pesmi = []
for teden in range(52):
    for pesem in lestvica(datum):
        pesmi.append(pesem)
orodja.zapisi_json(pesmi, 'obdelani-podatki/pesmi.json')
orodja.zapisi_csv(
    pesmi,
    ['mesto', 'naslov', 'sifra_umetnika', 'ime_umetnika'], 'obdelani-podatki/pesmi.csv'
)
