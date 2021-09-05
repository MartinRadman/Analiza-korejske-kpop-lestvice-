import re

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

with open('2_teden_oktobra_2020.html', encoding='utf8') as d:
    vsebina = d.read()

def izlusci_podatke_pesmi(blok):
    pesem = vzorec_pesmi.search(blok).groupdict()
    pesem['mesto'] = int(pesem['mesto'])
    pesem['sifra_umetnika'] = int(pesem['sifra_umetnika'])
    return pesem

count = 0
for blok in vzorec_bloka.finditer(vsebina):
    print(izlusci_podatke_pesmi(blok.group(0)))
    count += 1
print(count)

