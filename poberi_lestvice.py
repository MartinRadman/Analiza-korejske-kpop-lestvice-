import datetime
import orodja
import re

ZACETNI_DATUM = datetime.datetime(2015, 1, 11)
KONCNI_DATUM = datetime.datetime(2020, 12, 27)


vzorec_bloka = re.compile(
    r'<div class="ranking">'
    r'.*?'
    r'<div class="link"><a href="#" class="menu"><span>Artist Info.</span></a></div>',
    flags=re.DOTALL
)

vzorec_pesmi1 = re.compile(
    r'<div class="ranking"><span class="hidden">Ranking: </span><strong>'
    r'(?P<mesto>\d+)'
    r'</strong>.*?<div class="tit"><strong>'
    r'(?P<naslov>.+?)'
    r'</strong>.*?target="_blank">'
    r'(?P<ime_umetnika>.*?)</a>',
    flags=re.DOTALL
)

vzorec_pesmi2 = re.compile(
    r'<div class="ranking"><span class="hidden">Ranking: </span><strong>'
    r'(?P<mesto>\d+)'
    r'</strong>.*?<div class="tit"><strong>'
    r'(?P<naslov>.+?)'
    r'</strong>.*?<span>'
    r'(?P<ime_umetnika>.*?)</span>',
    flags=re.DOTALL
)

vzorec_linka_in_sifre = re.compile(
    r'<a href="(?P<link_umetnika>.*?seq='
    r'(?P<sifra_umetnika>\d+)'
    r'.*?)"',
    flags=re.DOTALL
)

vzorec_zalozba = re.compile(
    r'(Labels|Record Label):.*?</strong>'
    r'(?P<zalozba>.+?)'
    r'(&nbsp;)?</p>'
)

vzorec_debut1 = re.compile(
    r'(Debut|Active from):.*?</strong>.*?'
    r'(?P<debut>\d{4})'
    r'.*?(&nbsp;)?</p>'
)

vzorec_debut2 = re.compile(
    r'(Debut|Active from|Debut Year/Debut Song).*?:.*?'
    r'(?P<debut>\d{4})'
)

vzorec_clani = re.compile(
    r'Members:.*?</strong>'
    r'(?P<clani>.+?)'
    r'(&nbsp;)?</p>',
)

vzorec_clani_za_x1_ker_so_tako_posebni = re.compile(
    r'content="Members:&nbsp;'
    r'(?P<clani>.+?)'
    r'  ..."',
)

vzorec_biografija1 = re.compile(
    r'"fr-fic fr-dib fr-fil"></p><p>'
    r'(?P<biografija>\w.*?)'
    r'( &nbsp;)?</p>'
)

vzorec_biografija2 = re.compile(
    r'biography.gif"></div></div>.*?\n'
    r'(?P<biografija>.+?)'
    r'<div class="img_box">',
    flags=re.DOTALL
)

vzorec_biografija3 = re.compile(
    r'class="artistInfo">Biography:?(?P<biografija>.+?)'
    r'<div class="albumInfo"',
    flags=re.DOTALL
)

def poberi_tedensko_lestvico(datum):
    leto = datum.year
    mesec = datum.month
    dan = datum.day
    url = f'http://world.kbs.co.kr/service/musictop10.htm?lang=e&start_year={leto}&rank_date={leto}-{mesec}-{dan}'
    datoteka = f'kpop-lestvice/{leto}-{mesec}-{dan}.html' 
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izlusci_podatke_pesmi(blok.group(0))


def izlusci_podatke_pesmi(blok):
    pesem = vzorec_pesmi1.search(blok)
    if not pesem:
        pesem = vzorec_pesmi2.search(blok)
    pesem = pesem.groupdict()
    link_in_sifra = vzorec_linka_in_sifre.search(blok)
    if link_in_sifra:
        link_in_sifra = link_in_sifra.groupdict()
        pesem['sifra_umetnika'] = int(link_in_sifra['sifra_umetnika'])
        pesem['link_umetnika'] = 'http://world.kbs.co.kr/service/' + link_in_sifra['link_umetnika'][1:]
    else:
        pesem['sifra_umetnika'] = None
        pesem['link_umetnika'] = None
    pesem['mesto'] = int(pesem['mesto'])
    pesem['ime_umetnika'] = pocisti_tekst(pesem['ime_umetnika'])
    pesem['naslov'] = pocisti_tekst(pesem['naslov'])
    return pesem

def poberi_in_izlusci_umetnika(ime, url):
    SOLO, SKUPINA = 'SO', 'SK'
    umetnik = {}
    datoteka = f'umetniki/{ime}.html' 
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)

    zalozbe = vzorec_zalozba.search(vsebina)
    if zalozbe:
        zalozbe_za_precistiti = zalozbe['zalozba'].split(', ')
        preciscene_zalozbe = []
        for zalozba in zalozbe_za_precistiti:
            zalozba = neumne_izjeme(zalozba)
            cista_zalozba = pocisti_tekst(zalozba)
            preciscene_zalozbe.append(cista_zalozba)
        umetnik['zalozbe'] = preciscene_zalozbe
        if ime == 'SHAUN':
            umetnik['zalozbe'] = ['Happy Robot Record']
    else:
        umetnik['zalozbe'] = None

    debut = vzorec_debut1.search(vsebina)
    if not debut:
        debut = vzorec_debut2.search(vsebina)
    if debut:
        debut = int(debut['debut'])
        if debut == 1808:
            debut = 2013
        umetnik['debut'] = debut
    else:
        umetnik['debut'] = None

    clani = vzorec_clani.search(vsebina)
    if ime == 'X1':
        clani = vzorec_clani_za_x1_ker_so_tako_posebni.search(vsebina)
    if clani:
        umetnik['clani'] = pocisti_tekst(clani['clani']).split(', ')
        umetnik['tip'] = SKUPINA
    else:
        umetnik['clani'] = None
        umetnik['tip'] = SOLO

    biografija = vzorec_biografija1.search(vsebina)
    if not biografija:
        biografija = vzorec_biografija2.search(vsebina)
    if not biografija:
        biografija = vzorec_biografija3.search(vsebina)
    if biografija:
        biografija = biografija['biografija']
        umetnik['biografija'] = pocisti_tekst(biografija)
    else:
        umetnik['biografija'] = None

    return umetnik

def neumne_izjeme(zalozba):
    if 'KakaoM' in zalozba:
        return 'KakaoM'
    if 'Y-WHO Enterprise' in zalozba:
        return 'Y-WHO Enterprise'
    if 'Woollim' in zalozba:
        return 'Woollim'
    return zalozba

def pocisti_tekst(tekst):
    tekst = tekst.replace(r'<br />', '')
    tekst = tekst.replace(r'<br />', '')
    tekst = tekst.replace(r'</div>', '')
    tekst = tekst.replace(r'</span>', '')
    tekst = tekst.replace('\n', ' ')
    tekst = tekst.replace('&nbsp;', ' ')
    tekst = tekst.replace('&amp;', ' ')
    tekst = tekst.strip()
    if 'Entertainment' == tekst[-13:]:
        tekst = tekst[:-13]
    return tekst


def zberi_podatke_umetnikov(pesmi):
    obdelani_umetniki = set()
    umetniki, clani_skupin, zalozbe = [], [], []

    for pesem in pesmi:
        ime_umetnika = pesem.pop('ime_umetnika')
        sifra_umetnika = pesem['sifra_umetnika']
        if sifra_umetnika in obdelani_umetniki:
            pesem.pop('link_umetnika')
        if sifra_umetnika not in obdelani_umetniki:
            link_umetnika = pesem.pop('link_umetnika')
            if link_umetnika is None:
                continue
            umetnik = poberi_in_izlusci_umetnika(ime_umetnika, link_umetnika)
            zalozbe_umetnika = umetnik['zalozbe']
            debut = umetnik['debut']
            biografija = umetnik['biografija']
            tip = umetnik['tip']
            clani = umetnik['clani']
            umetniki.append({'sifra_umetnika': sifra_umetnika, 'ime_umetnika': ime_umetnika,
                            'biografija': biografija, 'tip': tip, 'debut': debut})

            if zalozbe_umetnika:
                for zalozba in zalozbe_umetnika:
                    zalozbe.append({'sifra_umetnika': sifra_umetnika, 'zalozba': pocisti_tekst(zalozba)})

            if clani:
                for clan in clani:
                    clani_skupin.append({'sifra_umetnika': sifra_umetnika, 'clan': clan})

            obdelani_umetniki.add(sifra_umetnika)

    return umetniki, clani_skupin, zalozbe
        



trenutni_datum = ZACETNI_DATUM
pesmi = []
while trenutni_datum != KONCNI_DATUM:
    stevec = 0
    for pesem in poberi_tedensko_lestvico(trenutni_datum):
        pesem['datum'] = trenutni_datum.strftime('%Y-%m-%d')
        pesmi.append(pesem)
        stevec += 1
        if stevec == 10: break
    trenutni_datum += datetime.timedelta(days=7) 

pesmi.sort(key=lambda pesem: (pesem['datum'], pesem['mesto']))
umetniki, clani_skupin, zalozbe = zberi_podatke_umetnikov(pesmi)
orodja.zapisi_csv(
    pesmi,
    ['datum', 'mesto', 'naslov', 'sifra_umetnika'], 'obdelani-podatki/pesmi.csv'
)
orodja.zapisi_csv(umetniki, ['sifra_umetnika', 'ime_umetnika', 'biografija', 'debut', 'tip'], 'obdelani-podatki/umetniki.csv')
orodja.zapisi_csv(clani_skupin, ['sifra_umetnika', 'clan'], 'obdelani-podatki/clani_skupin.csv')
orodja.zapisi_csv(zalozbe, ['sifra_umetnika', 'zalozba'], 'obdelani-podatki/zalozbe.csv')


