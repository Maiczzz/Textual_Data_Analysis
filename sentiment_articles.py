import pandas as pd
from creazione_df import temp
from topic_modeling_objects import ProcessText
import sentiment_mod_objects as s
import matplotlib.pyplot as plt
import numpy as np
"""------------------------------------------------------------------------------------------------------------------"""


class SentimentAnalysis:
    def __init__(self, lista):
        self.lista = lista
        self.articoli = []
        self.articoli_puliti = []
        self.articoli_sentiment = []

    positivi = pd.DataFrame({'% positivi': []})
    negativi = pd.DataFrame({'% negativi': []})

    # Questo metodo agisce sugli articoli così come sono stati estratti e li ripulisce con i metodi elencati nelle
    # funzioni richiamate
    def pulizia_articoli(self):
        self.articoli_puliti = ProcessText(self.articoli).text_cleaner()

    # Questo metodo agisce sulla lista di articoli ripuliti, per ogni articolo crea una tupla che ha come primo elemento
    # l'articolo e come secondo elemento una tupla (richiamata dal modulo 'sentiment_mod_objects' e a cui viene passato
    # ogni articolo) che ha come primo elemento il sentiment dell'articolo e come secondo l'accuratezza del sentiment.
    def sentiment(self):
        for art in self.articoli_puliti:
            self.articoli_sentiment.append((art, s.sentiment(art)))

    # Questo metodo prende in ingresso la lista di tuple creata con il metodo precedente, inizializza due
    # contatori, itera all'interno della tupla andando a ricercare il risultato del sentiment per ogni articolo. A
    # questo punto se l'articolo risulta positivo, aumenta il counter dei positivi, viceversa dei negativi. Infine li
    # restituisce.
    def counter_pos_neg(self):
        neg_count = 0
        pos_count = 0
        for art, sent in self.articoli_sentiment:
            if sent[0] == 'pos':
                pos_count += 1
            elif sent[0] == 'neg':
                neg_count += 1
        return pos_count, neg_count

    # Questo è il metodo principale che verrà richiamato nel main, richiama una lista di che contiene il nome dei file
    # dove sono stati salvati gli articoli, ogni file corrisponde a un mese nel nostro caso, per ogni file viene quindi
    # inseriti gli articoli in una lista che è poi la base su cui lavorano i metodi precedenti
    def esegui_sentiment(self):
        for elemento in self.lista:
            print(f'Sto lavorando su {elemento}')
            with open(elemento, encoding='utf8') as f:
                for line in f:
                    self.articoli.append(line)
                self.pulizia_articoli()
                self.sentiment()
                risultato = self.counter_pos_neg()
                perc_pos = round(np.divide(risultato[0], risultato[0] + risultato[1]) * 100)
                perc_neg = round(np.divide(risultato[1], risultato[0] + risultato[1]) * 100)
                # dopo aver eseguito le operazioni della sentiment vera e propria tramite i metodi precedenti si mostra
                # un grafico a barre sui risultati (che si può decidere di salvare) e si procede a inserire i valori
                # mensili nelle corrispondenti righe del dataframe tramite gli attributi di classe "positivi" "negativi"
                plt.bar('positive', perc_pos, label=f'positive:  {perc_pos}%')
                plt.bar('negative', perc_neg, label=f'negative: {perc_neg}%')
                plt.title(f'Sentiment per il file {elemento}')
                plt.xlabel('Sentiment')
                plt.ylabel('% of Articles')
                plt.legend(loc='upper right')
                plt.show()
                self.positivi.loc[len(self.positivi.index)] = perc_pos
                self.negativi.loc[len(self.negativi.index)] = perc_neg
        df_finale = pd.concat([temp, self.positivi, self.negativi], axis=1)
        df_finale.to_csv('DataFrame_progetto.csv')


"""------------------------------------------------------------------------------------------------------------------"""

mesi = ['6. Marzo_22.md',
        '5. Febbraio_22.md',
        '4. Gennaio_22.md',
        '3. Dicembre_21.md',
        '2. Novembre_21.md',
        '1. Ottobre_21.md']

Sentiment = SentimentAnalysis(mesi)
