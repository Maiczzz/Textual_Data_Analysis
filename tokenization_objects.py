import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
"""------------------------------------------------------------------------------------------------------------------"""


class PreProcessing(object):

    def __init__(self, text):
        self.text = text

# Pulisco il testo da tutti i segni di interpunzione attraverso una regex.
    def cleaner(self):
        text_cleaned = re.sub(rf"[^\w\s]", "", self.text)
        text_cleaned2 = re.sub(rf"[\d]", "", text_cleaned).lower()
        return text_cleaned2

# Divido il testo in una lista di parole, o anche dette token
    def tokenization(self):
        words = word_tokenize(self.cleaner())
        return words

# Elimino tutte le stopwords, ossia preposizioni, congiunzioni, etc, che servono per legare il discorso ma non possono
# dare un significato alla nostra analisi
    def remove_stopwords(self):
        stop_words = set(stopwords.words("english"))
        filtered_words = [word for word in self.tokenization() if word not in stop_words]
        return filtered_words

# Lo stemming mi permette di portare le parole alla radice; uso Porter perché è performante con la lingua inglese
    def stemming_words(self):
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in self.remove_stopwords()]
        return stemmed_words

# Il lemming permette di riportare la parola al suo lemma originario. E' preferibile allo stemming nel caso si voglia
# avere un po' più di interpretazione nell'analisi.
    def lemmatize_words(self):
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in self.remove_stopwords()]
        return lemmatized_words

# La classe Pre_Processing prende in ingresso del testo, lo pulisce, lo tokenizza, rimuove le stepwords.
# Si possono richiamare due metodi: Lo stemming o il Lemming. L'output sarà una lista di parole totalmene
# lemmizzate/stemmizzate
