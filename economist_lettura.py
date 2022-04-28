import requests
from bs4 import BeautifulSoup
import urllib.parse
from crawler import Economist
from requests_html import HTMLSession
import pandas as pd

"""------------------------------------------------------------------------------------------------------------------"""


# questa classe serve per estrarre il contenuto di un articolo dall' Economist, gli attributi di istanza sono
# definiti in modo che sia possibile ciclare all'interno della lista di collegamenti fornita dal crawler
class Estrattore:
    def __init__(self, href=[]):
        self.href = href

    def __iter__(self):
        return self.href

    def __next__(self):
        self._indice += 1
        if self._indice >= len(self.href):
            self._indice = -1
            raise StopIteration
        else:
            return self.href[self._indice]

    i = 0

    # Questo metodo crea una url completa partendo dalla lista di url parziali generati dal crawler e gli applica
    # direttamente la funzione request
    def creazione_richieste(self):
        url_base = 'https://www.economist.com'
        try:
            print('selezionata pagina')
            url_completa = [urllib.parse.urljoin(url_base, articolo) for articolo in self.href[self.i]]
            for _ in url_completa:
                print(_)
            lista_url = [requests.get(x) for x in url_completa]
            print('creato URL per 12 articoli')
            return lista_url
        except Exception as e:
            return print(e)

    # Questo metodo prende una lista di richieste e permette di navigare nei contenuti della pagina tramite la
    # libreria beautiful soup per estrarre il testo vero e proprio che viene infine inserito come stringa in una
    # lista 'risultato'
    def creazione_soup(self, lista_url=[]):
        try:
            risultato = []
            for pagina in lista_url:
                for articolo in pagina:
                    soup = BeautifulSoup(articolo.content, 'html.parser')
                    if soup.find('div', class_="ds-layout-grid ds-layout-grid--edged layout-article-body"):
                        contenuto = soup.find('div', class_="ds-layout-grid ds-layout-grid--edged layout-article-body")
                        for a in contenuto.select('aside'):
                            a.decompose()
                        for b in contenuto.find(class_="layout-article-links layout-article-promo"):
                            b.decompose()
                        for c in contenuto.find_all('p', class_="article__footnote"):
                            c.decompose()
                        print('articolo estratto')
                        risultato.append(contenuto.text)

                    # Alcuni articoli fanno un utilizzo pesante dei javascript e sono difficilmente estraibili con
                    # Beautiful soup ho quindi creato una sessione su cronium
                    elif soup.select('div', class_='article-text ds-container svelte-o3pylb'):
                        try:
                            contenuto = []
                            temp_url = articolo.url
                            sessione = HTMLSession()
                            r = sessione.get(temp_url)
                            r.html.render(sleep=1, timeout=120)
                            for paragrafo in r.html.find('.article-text.ds-container'):
                                contenuto.append(paragrafo.text)
                            definitivo = ''.join(contenuto)
                            print('articolo estratto')
                            risultato.append(definitivo)
                        except Exception as e:
                            print(e)
                            continue
                    else:
                        print('formato html non riconosciuto')
            return risultato
        except Exception as e:
            return print(e)


# La classe restituisce infine una lista contenente tutti gli articoli estratti come una stringa


"""------------------------------------------------------------------------------------------------------------------"""
# la classe viene fatta iterare fra le diverse pagine della sezione europa del The Economist, si ricordi infatti che
# il crawler restituisce una lista di liste, così da inserire in un unica lista tutti i collegamenti degli articoli che
# devono essere passati al metodo di estrazione

lista_url_def = []

Economist = Estrattore(Economist.ciclo_pagine())

for lista in Economist.href:
    lista_url_def.append(Economist.creazione_richieste())
    Economist.i += 1

articoli_TE = Economist.creazione_soup(lista_url_def)

te_df = pd.DataFrame(articoli_TE)

# dopo aver estratto tutti gli articoli delle diverse pagine si inserisce tutto in un dataframe così da semplificare le
# successive manipolazioni
