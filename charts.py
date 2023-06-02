import os
import pandas as pd
from speakleash import Speakleash
#from datetime import datetime


def prepare_data(date_string):

  #Dummy datetime input string to reset cache daily. Different string triggers cache refresh

  base_dir = os.path.join(os.path.dirname(__file__))
  replicate_to = os.path.join(base_dir, "datasets")
  sl = Speakleash(replicate_to)

  datasets = []
  size = []
  name = []
  category = []
  avg_doc_length = []
  avg_words_in_sentence = []
  avg_sents_in_docs = []
  avg_text_dynamics = []
  avg_nouns_to_verbs = []
  avg_stopwords_to_words = []
  avg_punctuation_to_words = []
  total_documents = 0
  total_characters = 0
  total_words = 0
  total_sentences = 0
  total_verbs = 0
  total_nouns = 0
#   total_adverbs = 0
#   total_adjectives = 0
  total_punctuations = 0
  total_symbols = 0
  total_stopwords = 0
#   total_oovs = 0
  total_size_mb = 0

  for d in sl.datasets:
      punctuations = getattr(d, 'punctuations', 0)
      symbols = getattr(d, 'symbols', 0)
    #   oovs = getattr(d, 'oovs', 0)
      size_mb = round(d.characters/1024/1024)
      datasets.append("Dataset: {0}, size: {1} MB, characters: {2}, documents: {3}".format(d.name, size_mb, d.characters, d.documents))
      size.append(size_mb)
      name.append(d.name)
      category.append(d.category)
      total_size_mb += size_mb
      total_documents += getattr(d, 'documents', 0)
      total_characters += getattr(d, 'characters', 0)
      total_sentences += getattr(d, 'sentences', 0)
      total_words += getattr(d, 'words', 0)
      total_verbs += getattr(d, 'verbs', 0)
      total_nouns += getattr(d, 'nouns', 0)
    #   total_adverbs += getattr(d, 'adverbs', 0)
    #   total_adjectives += getattr(d, 'adjectives', 0)

      if isinstance(punctuations, list):
        total_punctuations += len(punctuations)
      else:
        total_punctuations += punctuations
      if isinstance(symbols, list):
        total_symbols += len(symbols)
      else:
        total_symbols += symbols
    #   if isinstance(oovs, list):
    #     total_oovs += len(oovs)
    #   else:
    #     total_oovs += oovs
      
      total_stopwords += getattr(d, 'stopwords', 0)

      try:
        avg_doc_length.append(d.words/d.documents)
      except:
        avg_doc_length.append(0)
      try:
        avg_words_in_sentence.append(d.words/d.sentences)
      except:
        avg_words_in_sentence.append(0)
      try:
        avg_sents_in_docs.append(d.sentences/d.documents)
      except:
        avg_sents_in_docs.append(0)
      try: 
        avg_text_dynamics.append(d.verbs/d.words)
      except:
        avg_text_dynamics.append(0)
      try: 
        avg_nouns_to_verbs.append(d.nouns/d.verbs)
      except:
        avg_nouns_to_verbs.append(0)
      try: 
        avg_stopwords_to_words.append(d.stopwords/d.words)
      except:
        avg_stopwords_to_words.append(0)
      try:
          avg_punctuation_to_words.append(d.punctuations/d.words)
      except:
          avg_punctuation_to_words.append(0)


  data = {
    "name": name,
    "category": category,
    "size": size,
    "avg doc length": avg_doc_length,
    "avg sentence length" : avg_words_in_sentence,
    "avg sentences in doc": avg_sents_in_docs,
    "avg text dynamics" : avg_text_dynamics,
    "avg nouns to verbs" : avg_nouns_to_verbs,
    "avg stopwords to words": avg_stopwords_to_words,
    "avg punctuation to words": avg_punctuation_to_words
  }

  #Using name as indexer for easier navigation
  df = pd.DataFrame(data).set_index('name')

  return sl, datasets, df, total_size_mb, total_documents, total_characters, total_sentences, total_words, total_verbs, total_nouns, total_punctuations, total_symbols, total_stopwords,


# if __name__ == '__main__':
#     prepare_data(datetime.today())[2].to_csv("data.csv")
