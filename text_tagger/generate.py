from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential

from collections import defaultdict

import numpy as np

class Generate():
    def __init__(self):
        pass

    def get_random_seed(self, docs, seed_size=100):
        """
        gera um texto com carracteristicas de sua classe.
        """
        return "Abra Cadabra"

    def create_model(self, total_words, max_sequence_len):
        """
        Args: 
            total_words:
            max_sequence_len:
        """
        self.model = Sequential()
        self.model.add(Embedding(total_words, 256, input_length=max_sequence_len))
        self.model.add(Bidirectional(LSTM(128)))
        self.model.add(Dense(total_words, activation='softmax'))

    def train_model(self, sequences, max_sequence_len, total_words):
        """
        Args: 
            sequences:
        """
        sequences = pad_sequences(sequences, maxlen=max_sequence_len+1, padding='pre')
        X = sequences[:, :-1]
        y = to_categorical(sequences[:, -1], num_classes=total_words)
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.9)

        self.model.fit(X_train, y_train, epochs=50, batch_size=4096, 
                    validation_data=(X_valid, y_valid))

    def sequence_generate(self, docs):
        """
        Args: 
            docs:
        """
        sequences = []
        for line in docs:
            token_list = Tokenizer.texts_to_sequences([line])[0]
            for i in range(2, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                sequences.append(n_gram_sequence)
                        
        sequences = pad_sequences(sequences, maxlen=max_sequence_len+1, padding='pre')
        return sequences
    
    def generate_lerolero(self, seed_text, next_words = 100, T = 0.9):
        """
        Args: 
            seed_text:
            next_words:
            T:
        """

        index_to_word = {index: word for word, index in tokenizer.word_index.items()}

        for _ in range(next_words):
            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')

            probas = model.predict(token_list, verbose=0)
            probas = np.array(probas[0][1:])
            probas = probas ** (1.0 / T)
            probas /= np.sum(probas)
            predicted = np.random.choice(range(1,total_words), p=probas)
            # predicted = model.predict_classes(token_list, verbose=0)[0]
            
            seed_text += " " + (index_to_word[predicted] if predicted != 0 else '')

        return seed_text

    def run(self, database, tag=None, seed_text=None):
        """
        Start the generate component
        Args: 
            tag:  
            repo:
            seed_text:
        """
    
        # Filtra os dados rederentes a tag escolhida
        docs = database.df[database.df[database.tags_columns[0]]== tag]

        #lista de documentos do texto original
        docs = list(docs[f"orig_{database.text_column}"])

        print(docs[0:5])

        if(seed_text is None):
            seed_text = self.get_random_seed(docs)
            
        docs = docs[database.text_column]
        print(docs)
        
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(docs)

#        sequence = self.sequence_generate(docs)
        

        #self.create_model()
        #self.train_model()
        #generate_lerolero(seed_text)
