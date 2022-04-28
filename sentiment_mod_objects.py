import nltk
import random
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from sklearn.model_selection import train_test_split
from tokenization_objects import PreProcessing
"""------------------------------------------------------------------------------------------------------------------"""

# Apertura dei file base con cui verrà successivamente addestrato il modello.
short_positive_raw = open('positive.txt', 'r').read()
short_negative_raw = open('negative.txt', 'r').read()

# Pulizia dei due file richiamando il metodo cleaner
short_positive_cleaned = PreProcessing(short_positive_raw).cleaner()
short_negative_cleaned = PreProcessing(short_negative_raw).cleaner()

# creazione di due liste
documents = []
all_words = []

# lista dei 'tag' delle parole che saranno estratte dai documenti. 'J':Aggettivi, 'V': Verbi, 'N': Sostantivi
allowed_word_types = ['J', 'V', 'N']

# Questa funzione cicla nel documento delle recensioni positive, inserisce nella lista 'documenti' una tupla in cui il
# primo valore è l'articolo e il secondo è la classificazione. Parallelamente le recensioni vengono tokenizzate, rimosse
# le stopwords e lemmizzate e inserite nella varaibile 'words'. Successivemente viene chiamata la funzione 'pos_tag'
# dalla libreria nltk e gli viene passata la variabile 'words'. La funzione restituisce il tag per ogni parola.
# Infine si cicla nei tag e se il tag corrisponde ai tag consentiti (dichiarati precedentemente nella variabile
# 'allowed_word_types'), la parola viene inserita nella lista 'all_words', anch'essa inizializzata in precedenza.
for p in short_positive_cleaned.split('\n'):
    documents.append((p, 'pos'))
    words = PreProcessing(p).lemmatize_words()
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0])

# Qui succede la stessa cosa ma con il file delle recensioni negative.
for p in short_negative_cleaned.split('\n'):
    documents.append((p, 'neg'))
    words = PreProcessing(p).lemmatize_words()
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0])


# La lista 'all words' viene passata alla funzione FreqDist della libreria nltk, che genera la frequenza di ogni parola
# all'interno della lista. Può essere chiamato il metodo 'most_common', che restituisce in ordine decrescente
# una lista di tuple in cui il primo elemento è la parola e il secondo la frequenza della parola (quante volte la
# parola appare nella lista).
all_words_fd = nltk.FreqDist(all_words)
# print(all_words_fd.most_common(10))
# print(all_words_fd['stupid'])


# Dentro questa variabile viene inserita la lista di tutte le parole prese una sola volta.
word_feature = list(all_words_fd.keys())
"""------------------------------------------------------------------------------------------------------------------"""


# Questa funzione prende in ingresso un documento, viene pulito e vengono lemmatizzate le parole. Successivamente viene
# inizializzato un dizionario in cui vengono inserite
def find_features(document):
    wordz = PreProcessing(document)
    wordz_def = wordz.lemmatize_words()
    features = {}
    for word in word_feature:
        features[word] = (word in wordz_def)
    return features


featuresets = [(find_features(article), tag) for (article, tag) in documents]
random.shuffle(featuresets)
#print(len(featuresets))


### SUBSET ###
# Ci sono vari approcci al setting del set dei dati per l'addestramento de per il testaggio dei modelli.
# In questo caso ho utilizzato direttamente l'approccio del training e del validation set, in cui viene diviso il
# dataset secondo una certa percentuale definita dall'analista. In questo caso scelgo 50/50 in quanto andremo ad
# utilizzare i modelli per classificare dei dati che non sono recensioni, ma tweet e articoli; se utilizzassimo
# un training set troppo grande rischieremmo un overfitting, ossia che il modello sia molto performante con i dati che
# gli abbiamo dato noi, ma poi se ne dovessimo passare altri nuovi sarebbe molto scarso.

# TRAINING-TEST set approach
# training_set = featuresets[:6000]
# test_set = featuresets[6000:]

# Validation set approach
training, validation = train_test_split(featuresets, test_size=0.4, random_state=5)


############ MODELLI ############
# Abbiamo utilizzato diversi modelli per la classificazione e le prestazioni di questi ultimi si aggirano tutte
# intorno al 75%. A questo punto abbiamo deciso di prediligere i modelli di Regressione Logistica e il Naive-Bayes,
# in quanto sono il miglior compromesso tra precisione e potenza computazionale.

print("Addestramento modello in corso")

### Naive Bayes ###
NBclassifier = nltk.NaiveBayesClassifier.train(training)
print('Original_Naive_Bayes_accuracy:', (nltk.classify.accuracy(NBclassifier, validation))*100)
NBclassifier.show_most_informative_features(20)


# #-------------------------------
# print("Addestramento modello in corso")
### Classificatore Multinomial Naive Bayes ###
# MNB_classifier = SklearnClassifier(MultinomialNB())
# MNB_classifier.train(training_set)
# print('MultinomialNB_classifier_accuracy:', (nltk.classify.accuracy(MNB_classifier, test_set))*100)


# -------------------------------

#print("Addestramento modello in corso")
### Classificatore Bernoulli Naive_Bayes ###
# BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
# BernoulliNB_classifier.train(training_set)
# print('BernoulliNB_classifier_accuracy:', (nltk.classify.accuracy(BernoulliNB_classifier, test_set))*100)


# -------------------------------
# print("Addestramento modello in corso")
### Regressione Logistica ###
# LogisticRegression = SklearnClassifier(LogisticRegression())
# LogisticRegression.train(training)
# print('LogisticRegression_classifier_accuracy:', (nltk.classify.accuracy(LogisticRegression, validation))*100)


# -------------------------------
# print("Addestramento modello in corso")
### Classificatore SGDClassifier ###
# SGDClassifier = SklearnClassifier(SGDClassifier())
# SGDClassifier.train(training_set)
# print('SGDClassifier_classifier_accuracy:', (nltk.classify.accuracy(SGDClassifier, test_set))*100)


# -------------------------------
# print("Addestramento modello in corso")
### SVM  ###
# SVC_classifier = SklearnClassifier(SVC())
# SVC_classifier.train(training_set)
# print('SVC_classifier_accuracy:', (nltk.classify.accuracy(SVC_classifier, test_set))*100)


#-------------------------------
# print("Addestramento modello in corso")
### SVM lineare ###
# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(training)
# print('LinearSVC_classifier_accuracy:', (nltk.classify.accuracy(LinearSVC_classifier, validation))*100)


# -------------------------------
# print("Addestramento modello in corso")
### Nu SVM ###
# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training)
# print('NuSVC_classifier_accuracy:', (nltk.classify.accuracy(NuSVC_classifier, validation))*100)


# Questa classe serve per 'votare' quale sia il responso della sentiment (se positivo o negativo).
# Prende in ingresso da 1 a n modelli/classificatori, e il metodo classify ritorna il sentiment, mentre il metodo
# confidece ritorna la sicurezza/accuratezza della decisione
"""------------------------------------------------------------------------------------------------------------------"""


class VoteClassifier(ClassifierI):

    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


# Qui viene richiamata la funzione che 'vota' se un determinato articolo/tweet debba essere positivo o negativo.
# Può prendere in output uno o più classificatori. Nel caso siano di più ritorna la moda della classificazione, dunque
# la classe più frequente. Anche qui il fatto di utilizzare più di un classificatore è una scelta dell'analista: Per
# avere una maggiore interpretabilità è sempre meglio utilizzare un solo modello alla volta. Nel caso in cui interessi
# una maggiore precisione nella classificazione, gli altri modelli medieranno l'errore di un classificatore.
print('Sentiment in corso...')
voted_classifier = VoteClassifier(NBclassifier)
# print('Vote classifier accuracy percent:', (nltk.classify.accuracy(voted_classifier, validation))*100)

"""------------------------------------------------------------------------------------------------------------------"""


# Questa funzione è ciò che verrà chiamato nel momento in cui si importa questo file. Alla funzione verrà passato
# Del testo (che può essere un articolo o un tweet), e ci restituisce la sentiment del testo (quindi se è positivo
# o negativo); ma anche la sicurezza con cui il modello decreta la scelta.
def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)