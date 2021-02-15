import os
import pandas as pd
import re
from collections import Counter
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing import sequence
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout, Dense, Embedding, LSTM
from tensorflow.keras.models import Sequential
from keras.optimizers import Adam
import tensorflow
import datetime
import unicodecsv as csv
from io import BytesIO



# this is for model training. Use Load_Model_H5.py for loading model.



class Post_Here_Classifier:

    def __init__(self, file="data/reddit_posts_4M.csv", mode="prod"):

        # load csv into pandas.DataFrame
        self.df = pd.read_csv(file)
        if mode == "test" and file == "data/reddit_posts_4M.csv":
            self.df = self.df.sample(20000)
            self.df = self.df.reset_index()

        if file != "data/test_reddit_frame.csv":
            self.df.to_csv("data/test_reddit_frame.csv")

        if file != "data/prepared_reddit_frame.csv":

            # clean and join "title" and "selftext"
            print("...preparing")
            self.prepare_data()

            # get corpus of posts
            print("...gathering corpus")
            self.get_corpus()

            # limit corpus to most popular words
            print("...getting max_words")
            self.get_max_words()

            # tokenize
            print("...tokenizing posts")
            self.tokenize_words()

            # set subreddit ids
            print("...subreddit ids")
            self.set_subreddit_ids()

            # save clean_df to csv
            print("...saving prepared df")
            self.save_df()

            # # split_and_pad_train_test
            print("...train test split")
            self.split_and_pad_train_test()

            # save csv_data
            print("...saving csv_data")
            self.save_csv_data()

        else:
            with open("data/id_to_word.csv", "rb") as f:
                reader = csv.reader(f, encoding="utf-8")
                self.id_to_word = {}
                self.id_to_word = {int(rows[0]):rows[1] for rows in reader}

            with open("data/subreddit_mapper.csv", "rb") as f:
              reader = csv.reader(f, encoding="utf-8")
              self.subreddits = {}
              self.subreddits = {rows[0]:int(rows[1]) for rows in reader}

            self.split_and_pad_train_test()

            self.id_to_word[0] = '<PAD>'
            self.word_to_id = {i:k for k,i in self.id_to_word.items()}


            print(len(self.id_to_word), len(self.word_to_id), len(self.subreddits))



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
                word = re.sub("\n+|\s+", "", word)
                if word == 'nan':
                    continue
                if word not in self.corpus.keys():
                    self.corpus[word] = 1
                else:
                    self.corpus[word] += 1

        del self.corpus['']

    def get_max_words(self, max_features=200000):

        # collect max_features number of top words from corpus
        k = Counter(self.corpus)
        highest = k.most_common(max_features)

        # print(len(highest))
        # print(highest[:5])

        # word_cache = []
        # for x in highest:
        #     if x[0] not in word_cache:
        #         word_cache.append(x[0])
        #     else:
        #         print(x[0])

        # create id to word for words
        self.word_to_id = {}
        self.word_to_id['<PAD>'] = 0
        self.word_to_id['<UNK>'] = 1

        for i in range(2, len(highest)+2):
            # self.word_to_id[re.sub("\n+|\s+", "", highest[i-2][0])] = i
            self.word_to_id[highest[i-2][0]] = i

        # create word to id for words
        self.id_to_word = {k:v for v,k in self.word_to_id.items()}

        # print(len(self.id_to_word), len(self.word_to_id))



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

        print(self.model.summary())


    def fit_model(self):
        stop = EarlyStopping(monitor='val_sparse_categorical_accuracy', min_delta=0.005, patience=3)

        # print(self.X_train_sequenced[0])
        # print(type(self.y_train[0]))

        self.model.fit(self.X_train_sequenced, self.y_train, batch_size=32, epochs=100, validation_data=(self.X_test_sequenced, self.y_test), callbacks=[stop])

        self.model.save("model/post_here_classifier", save_format="h5")


    def save_csv_data(self):

        # print(self.subreddits)
        # print(len(self.id_to_word), len(self.word_to_id), len(self.subreddits))
        # for i in range(11994):
        #     try:
        #         self.id_to_word[i]
        #     except:
        #         print(i)

        with open("data/subreddit_mapper.csv", "wb") as f:
            writer = csv.writer(f, encoding="utf-8")
            for key in self.subreddits.keys():
                writer.writerow([key,self.subreddits[key]])

        with open("data/id_to_word.csv", "wb") as f:
            writer = csv.writer(f, encoding="utf-8")
            for key in self.id_to_word.keys():
                writer.writerow([key,self.id_to_word[key]])

        # # testing saving and loading parity
        # with open("data/id_to_word.csv", "rb") as f:
        #     reader = csv.reader(f, encoding="utf-8")
        #     self.id_to_word_r = {}
        #     for row in reader:
        #         self.id_to_word_r = {int(rows[0]):rows[1] for rows in reader}
        #
        # problem_keys = []
        # for n in self.id_to_word.keys():
        #     try:
        #         if self.id_to_word_r[n] != self.id_to_word[n]:
        #             problem_keys.append(n)
        #
        #     except:
        #         print(n)
        #
        # print(problem_keys)

if __name__ == "__main__":
    phc = Post_Here_Classifier(mode="test")
    # phc = Post_Here_Classifier(file="data/test_reddit_frame.csv")
    # phc = Post_Here_Classifier(file="data/prepared_reddit_frame.csv")
    phc.create_model()
    phc.fit_model()
