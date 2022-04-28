import requests
from bs4 import BeautifulSoup

"""------------------------------------------------------------------------------------------------------------------"""
# La classe crawler serve per esplorare la sezione europa sia del Financial Times sia del The Economist per poter
# estrarre gli href dei singoli articoli

visitate = set()


class Crawler:

    def __init__(self, giornale):
        self._url = ''
        self.giornale = giornale
        self.pagina_ini = int(input(f'\nInserire la pagina di partenza per il {self.giornale}: '))
        self.pagina_fin = int(input(f'\nInserire la pagina finale per il {self.giornale}: '))

    # Definire una proprietà dell'attributo permette di modificare automaticamente l' URL di partenza in accordo alla
    # pagina dalla quale si decide di iniziare l'estrazione
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, indirizzo):
        self._url = indirizzo+str(self.pagina_ini)

    def ottieni_html(self):
        try:
            if self.url not in visitate:
                visitate.add(self.url)
                print('richiesta ok')
                return requests.get(self.url).content
        except Exception as e:
            return print(e)

    # Il crawler è comune a entrambe le testate, dopo aver verificato per l'estrazione di quale testata è stato lanciato
    # si individuano i selettori CSS all'inteno dei quali sono contenuti i link per i diversi articoli
    def estrai_link(self):
        try:
            if self.url.find('https://www.economist.com') != -1:
                soup = BeautifulSoup(self.ottieni_html(), 'html.parser')
                pagina = soup.find(class_='layout-section-collection ds-layout-grid')
                titoli = pagina.find_all('a', class_="headline-link")
                temp_href_economist = [titolo.get('href') for titolo in titoli if titolo.get('href') not in visitate]
                print('estrazione ok')
                return temp_href_economist
            elif self.url.find('https://www.ft.com') != -1:
                soup = BeautifulSoup(self.ottieni_html(), 'html.parser')
                pagina = soup.find_all(class_='o-teaser__heading')
                lst_pagina = list(pagina)
                lst_stringhe = [str(lista) for lista in lst_pagina]
                temp_href_financial = []
                for _ in lst_stringhe:
                    content_split = _.split('"')
                    for item in content_split:
                        if item.startswith('/content'):
                            temp_href_financial.append(item)
                print('estrazione ok')
                return temp_href_financial
            else:
                print('URL non riconosciuta')
        except Exception as e:
            return print(e)

    # per poter ciclare fra le diverse pagine per le quali si vuole esplorare i collegamenti è necessario aggiornare
    # l'URL così che si aggiorni il numero della pagina
    def ciclo_pagine(self):
        try:
            href = []
            while self.pagina_ini <= self.pagina_fin:
                print(f"selezionata pagina: {self.pagina_ini}")
                href.append(self.estrai_link())
                self.pagina_ini += 1
                print(self.url)
                if self.url.find('https://www.economist.com') != -1:
                    self.url = self.url.replace(str(self.pagina_ini - 1), str(self.pagina_ini))
                elif self.url.find('https://www.ft.com') != -1:
                    self.url = self.url.replace(str(self.pagina_ini - 1), str(self.pagina_ini))
            return href
        except Exception as e:
            return print(e)
    # il crawler restituisce infine una lista che contiene altre liste corrispondenti alle diverse pagine che a loro
    # volta contengono tutti i collegamenti agli articoli che verranno successivamente estratti


"""------------------------------------------------------------------------------------------------------------------"""


# Creazione istanze
FinancialTimes = Crawler('Financial Times')
FinancialTimes.url = "https://www.ft.com/world/europe?page="
Economist = Crawler('The Economist')
Economist.url = "https://www.economist.com/europe?page="

# L38452NMbu7cL2C2Sypv
