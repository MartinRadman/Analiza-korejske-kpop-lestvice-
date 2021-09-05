import re

with open('IU.html', encoding='utf8') as d:
    vsebina = d.read()

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


count = 0
for zadetek in vzorec_biografija.finditer(vsebina):
    print(zadetek.groupdict())
    count += 1
print(count)