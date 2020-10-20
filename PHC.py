import pandas as pd
import re
from collections import Counter
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing import sequence
# from tensorflow.keras.callbacks import EarlyStopping
# from tensorflow.keras.layers import Dropout, Dense, Embedding, LSTM
# from tensorflow.keras.models import Sequential
# from keras.optimizers import Adam
# import tensorflow
import os
import datetime
import csv


class Post_Here_Classifier:

    def __init__(self, file="data/reddit_posts_4M.csv"):

        # load csv into pandas.DataFrame
        self.df = pd.read_csv(file)
        self.df = self.df.sample(1000)

        if file != "data/test_reddit_frame.csv":
            self.df.to_csv("data/test_reddit_frame.csv")

        if file != "data/prepared_reddit_frame.csv":

            # clean and join "title" and "selftext"
            self.prepare_data()
            print(self.df.head())

            # get corpus of posts
            self.get_corpus()
            print(len(self.corpus))

            # limit corpus to most popular words
            self.get_max_words()
            print(len(self.word_to_id))
            # tokenize
            self.tokenize_words()

            # set subbreddit ids
            self.set_subreddit_ids()
            print(self.df.head())

            # save clean_df to csv
            self.save_df()

            # split_and_pad_train_test
            self.split_and_pad_train_test()

            # save csv_data
            self.save_csv_data()

        else:
            with open("data/word_to_id.csv", "r") as file:
                reader = csv.reader(file)
                self.word_to_id = {rows[0]:rows[1] for rows in reader}

            with open("subreddit_mapper.csv", "r") as file:
              reader = csv.reader(file)
              subreddit_mapper = {rows[0]:rows[1] for rows in reader}
              self.subreddit_mapper = {v:k for k,v in subreddit_mapper.items()}



    def save_df(self):
        self.df.to_csv("data/prepared_reddit_frame.csv", index=False)


    def clean(self, text):
        clean = ""
        for chr in str(text):
            if chr in '.!?\\-':
                clean += " "
            else:
                l = re.match('\w|\s', chr)
                if l:
                    clean += chr.lower()

        return clean


    def prepare_data(self):
        # clean
        self.df['clean_title'] = self.df['title'].apply(self.clean)
        self.df['clean_selftext'] = self.df['selftext'].apply(self.clean)

        # clean_text_total
        self.df['clean_text_total'] = self.df['clean_title'] + " " + self.df['clean_selftext']


    def get_corpus(self):
        self.corpus = {}

        for i in range(len(self.df)):
            words = (self.df['clean_title'][i] + " " + self.df['clean_selftext'][i]).split(" ")

            for word in words:
                if word == 'nan':
                    continue
                if word not in self.corpus.keys():
                    self.corpus[word] = 1
                else:
                    self.corpus[word] += 1

        del self.corpus['']

    def get_max_words(self, max_features=100000):

        # collect max_features number of top words from corpus
        k = Counter(self.corpus)
        highest = k.most_common(max_features)

        # create id to word for words
        self.id_to_word = {}
        self.id_to_word[0] = '<PAD>'
        self.id_to_word[1] = '<UNK>'

        for i in range(2, len(highest)+2):
            self.id_to_word[i] = highest[i-2][0]

        # create word to id for words
        self.word_to_id = {v:k for k,v in self.id_to_word.items()}


    def tokenize(self, words):
        token_ids = []
        for word in words.split(" "):
            if word in self.word_to_id.keys():
                token_ids.append(self.word_to_id[word])
            else:
                token_ids.append(1)

        return token_ids


    def tokenize_words(self):
        self.df['clean_text_tokens'] = self.df['clean_text_total'].apply(self.tokenize)


    def set_subreddit_ids(self):
        self.subreddits = {k:v for v,k in enumerate(self.df['subreddit_name'].unique())}
        self.df['subreddit_name_id_simple'] = self.df['subreddit_name'].map(self.subreddits)


    def split_and_pad_train_test(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.df['clean_text_tokens'], self.df['subreddit_name_id_simple'], test_size=0.2, random_state=5)
        self.X_train_sequenced = sequence.pad_sequences(self.X_train, maxlen=300)
        self.X_test_sequenced = sequence.pad_sequences(self.X_test, maxlen=300)


    def create_model(self):
        max_features = len(self.id_to_word) + 1

        self.model = Sequential()

        self.model.add(Embedding(max_features, 128))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(len(self.subreddits), activation='softmax'))

        # opt = Adam(learning_rate=0.01)

        self.model.compile(loss='sparse_categorical_crossentropy',
                           optimizer='nadam',
                           metrics=['sparse_categorical_accuracy'])


    def fit_model(self):
        stop = EarlyStopping(monitor='val_sparse_categorical_accuracy', min_delta=0.005, patience=3)

        self.model.fit(self.X_train_sequenced, self.y_train,
                batch_size=32,
                epochs=100,
                validation_data=(self.X_test_sequenced, self.y_test),
                callbacks=[stop],
                verbose=1)

        self.model.save("model/post_here_classifier", save_format="h5")

        self.save_csv_data()


    def save_csv_data(self):

        with open("data/subreddit_mapper.csv", "w") as f:
            for key in self.subreddits.keys():
                f.write("%s,%s\n"%(key, self.subreddits[key]))

        with open('data/word_to_id.csv', 'w') as f:
            for key in self.word_to_id.keys():
                f.write("%s,%s\n"%(key, self.word_to_id[key]))


if __name__ == "__main__":
    phc = Post_Here_Classifier(file="data/test_reddit_frame.csv")
    # phc = Post_Here_Classifier(file="data/prepared_reddit_frame.csv")
    phc.create_model()
