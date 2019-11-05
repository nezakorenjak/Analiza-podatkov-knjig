import re
import orodja


vzorec_bloka = re.compile(
    r'<td width="100%" valign="top">\s*<a class="bookTitle".*?'
    r'</td>',
    flags=re.DOTALL
)

vzorec_knjige = re.compile(
    r"<span itemprop='name' role='heading' aria-level='4'>(?P<naslov>.*?)</span>.*?"
    r"<div class='authorName.*?<span itemprop=.name.>(?P<avtor>.*?)</span>.*?"
    r"</span> (?P<povprecna_ocena>\d\.\d{2}) avg rating &mdash; (?P<stevilo_ocen>\d*,?\d+) ratings</span>.*?"
    ,
    flags=re.DOTALL
)



def izloci_podatke_knjige(blok):
    knjiga = vzorec_knjige.search(blok)
    if knjiga is None:
        pass
    else: 
        knjiga = knjiga.groupdict()
        knjiga['povprecna_ocena'] = float(knjiga['povprecna_ocena'])
        knjiga['stevilo_ocen'] = int(knjiga['stevilo_ocen'].replace(',', ''))
        knjiga['naslov'] = knjiga['naslov'].replace('&amp;', '&').replace('"','')
        return knjiga


def knjige_na_strani(st_strani):
    url = (
        f'https://www.goodreads.com/list/show/133723.Goodreads_Choice_Awards_2019_eligible_for_write_in_only_?page={st_strani}'
    )
    ime_datoteke = 'knjige-na-strani-{}.html'.format(st_strani)
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_knjige(blok.group(0))


knjige = []
for st_strani in range(1, 13):
    for knjiga in knjige_na_strani(st_strani):
        knjige.append(knjiga)
orodja.zapisi_json(knjige, 'knjige.json')
orodja.zapisi_csv(knjige, ['naslov', 'avtor', 'povprecna_ocena', 'stevilo_ocen'], 'knjige.csv')