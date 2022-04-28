from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt

"""------------------------------------------------------------------------------------------------------------------"""

stop = stopwords.words('english')


# Questa classe prende in ingresso una stringa e crea un wordcloud sulla stessa
class Cloud:

    def __init__(self, testo):
        self.testo = testo

    # Questo metodo restituisce un testo un minimo ripulito
    def tokenize(self):
        tokens = nltk.word_tokenize(self.testo)
        token_words = [w for w in tokens if w.isalpha()]
        parole_significative = [w for w in token_words if not w in stop]
        joined_words = (" ".join(parole_significative))
        return joined_words

    # Partendo dal testo ripulito si utilizza la libreria wordcloud
    def nuvola(self):
        wordcloud = WordCloud(
            width=3000,
            height=2000,
            background_color='white').generate(self.tokenize())
        fig = plt.figure(
            figsize=(40, 30),
            facecolor='k',
            edgecolor='k')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.show()
        nome = str(input('\nInserire il nome del file: '))
        wordcloud.to_file(nome + '.png')


"""------------------------------------------------------------------------------------------------------------------"""


# Questa funzione verifica tramite un blocco try/except che l'oggetto sia un singolo articolo o l'intero file degli
# articoli mensili così da applicare le eventuali trasformazioni necessarie e infine creare l'istanza
def crea_cloud(file):
    mese = []
    try:
        isinstance(file, str)
        Mese = Cloud(file)
        Mese.nuvola()

    except ValueError:
        with open(file, encoding='utf8') as f:
            for line in f:
                mese.append(line)
        testo = ','.join(mese)
        Mese = Cloud(testo)
        Mese.nuvola()
