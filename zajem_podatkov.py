import requests
import re
import orodja

server = 'http://www.metacritic.com/browse/albums/score/metascore/all/filtered?view=detailed&%3Bsort=desc&page=0'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def shrani_html(server):
    for stran in range(20):
        r = requests.get('http://www.metacritic.com/browse/albums/score/metascore/all/filtered?view=detailed&%3Bsort=desc&page={}'.format(stran),
                         headers=headers)
        ime = 'strani/{}.html'.format(stran)
        orodja.pripravi_imenik(ime)
        with open(ime, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')

regex_albuma = re.compile(r'"product_title"><a.*?>(?P<naslov>.+?)</a><.*?> - (?P<avtor>.*?)</span>'
                          r'</h3>.*?tive">(?P<ocena_kritikov>\d{2})</s'
                          r'pan>.*?data">.*?(?P<leto>\d{4})</span>.*?Genre.*?data">.*?(?P<zanr>\D.*?)</s'
                          r'pan>.*?<span class="data textscore.*?>(?P<ocena_ljudi>.*?)</span>',
                          flags=re.DOTALL)

imena_polj = ['naslov', 'avtor', 'ocena_kritikov', 'leto', 'zanr', 'ocena_ljudi']

def naredi_csv():
    sez = []
    for html in orodja.datoteke('strani/'):
        counter = 0 #s tem odstranim tezavo pri regexu na koncu vsakega htmlja
        for album in re.finditer(regex_albuma, orodja.vsebina_datoteke(html)):
            podatki = album.groupdict()
            counter += 1
            podatki['zanr'] = podatki['zanr'].split()
            for i in range(len(podatki['zanr'])):
                podatki['zanr'][i] = podatki['zanr'][i].replace(',','')
            podatki['leto'] = int(podatki['leto'])
            podatki['ocena_kritikov'] = int(podatki['ocena_kritikov'])
            podatki['ocena_ljudi'] = float(podatki['ocena_ljudi'])
            if counter >= 70:
                break
            sez.append(podatki)
    orodja.zapisi_tabelo(sez, imena_polj, 'tabela.csv')

#shrani_html(server)
#naredi_csv()





