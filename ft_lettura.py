import requests
from bs4 import BeautifulSoup
import urllib.parse
from crawler import FinancialTimes
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd

"""------------------------------------------------------------------------------------------------------------------"""


# questa classe serve per estrarre il contenuto di un articolo del Financial Times, gli attributi d' istanza sono
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

    # IMPORTANTE: molti degli articoli del FT richiedono una sottoscrizione e non è possibile estrarli con bs4
    # per far funzionare questo programma è quindi necessario scaricare geckodriver e copiarlo nella cartella di python
    # dopodiché bisognerà caricare il profilo personale di firefox, si noti che il path scritto qua andrà sostituito con
    # quello della macchina dove sta girando il programma, il motivo è che si suppone che nel profilo siano salvate le
    # credenziali di accesso e si sia installata l'estensione "i don't care about cookies" che rimuove automaticamente
    # i pop-up per l'accettazione dei cookies, in linea puramente teorica in assenza di credenziali si potrebbero
    # visionare gli articoli anche installando l'estensione "Bypass Paywalls Clean"
    profile_path = r'C:\Users\utente\AppData\Roaming\Mozilla\Firefox\Profiles\nt4lo6kh.default-release'
    ffOptions = Options()
    ffOptions.add_argument("-profile")
    ffOptions.add_argument(profile_path)
    driver = webdriver.Firefox(options=ffOptions)

    # Questo metodo crea una url completa partendo dalla lista di url parziali generati dal crawler e gli applica
    # direttamente la funzione request
    def creazione_richieste(self):
        url_base = 'https://www.ft.com'
        try:
            print('\nselezionata pagina')
            url_completa = [urllib.parse.urljoin(url_base, articolo) for articolo in self.href[self.i]]
            for item in url_completa:
                print(item)
            lista_url = [requests.get(x) for x in url_completa]
            print('\ncreato URL per 26 articoli')
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
                    if soup.find('div', class_="article__content-body n-content-body js-article__content-body"):
                        print("\nutilizzo beautiful soup")
                        contenuto = []
                        tmp = soup.find('div', class_="article__content-body n-content-body js-article__content-body")
                        tmp = tmp.find_all('p')
                        for _ in tmp[1:]:
                            contenuto.append(_.text)
                        definitivo = ''.join(contenuto)
                        print(definitivo)
                        risultato.append([definitivo])

                    # gli articoli non estraibili con bs4 sono aperti direttamente su firefox ed estratti tramite XPATH
                    # posto che si siano rispettati i requisiti elencati sopra
                    elif soup.select('div', class_="article__content-body n-content-body js-article__content-body"):
                        try:
                            print("\nutilizzo selenium")
                            contenuto = []
                            url = articolo.url
                            self.driver.get(url)
                            gate = True
                            self.driver.set_page_load_timeout(10)
                            self.driver.implicitly_wait(10)
                            while gate:
                                # necessario refresh per assicurarsi che parta l'estensione per accettare
                                # automaticamente i cookies
                                self.driver.refresh()
                                # faccio scorrere la pagina così da assicurarsi che venga caricato tutto
                                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                                           "lenOfPage=document.body.scrollHeight;return lenOfPage;")
                                corpo = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]'
                                                                           '/article/div[3]/div[3]')
                                paragrafo = corpo.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div['
                                                                          '2]/article/div[3]/div[3]/div/p')
                                for item in paragrafo:
                                    contenuto.append(item.text.strip('\n'))
                                definitivo = ''.join(contenuto)
                                print(definitivo)
                                risultato.append([definitivo])
                                gate = False
                        except NoSuchElementException:
                            print('\nnon ho trovato il contenuto')
                            continue
                        except TimeoutException:
                            print('\ntroppo lento')
                            continue
                    else:
                        print('\nformato html non riconosciuto')
            print(len(risultato))
            return risultato
        except Exception as e:
            return print(e)


# La classe restituisce infine una lista contenente tutti gli articoli estratti come una stringa


"""------------------------------------------------------------------------------------------------------------------"""
# la classe viene fatta iterare fra le diverse pagine della sezione europa del Financial Times, si ricordi infatti che
# il crawler restituisce una lista di liste, così da inserire in un unica lista tutti i collegamenti degli articoli
# che devono essere passati al metodo di estrazione


FT = Estrattore(FinancialTimes.ciclo_pagine())

lista_url_def = []

for lista in FT.href:
    lista_url_def.append(FT.creazione_richieste())
    FT.i += 1

articoli_FT = FT.creazione_soup(lista_url_def)

ft_df = pd.DataFrame(articoli_FT)

# dopo aver estratto tutti gli articoli delle diverse pagine si inserisce tutto in un dataframe così da semplificare le
# successive manipolazioni
