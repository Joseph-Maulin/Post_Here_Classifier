
import keras
from tensorflow.keras.preprocessing import sequence
import unicodecsv as csv
from io import BytesIO


class Model:

    def __init__(self, model_location="model/post_here_classifier.h5"):
        self.model = keras.models.load_model(model_location)

        with open("data/id_to_word.csv", "rb") as f:
            reader = csv.reader(f, encoding="utf-8")
            self.id_to_word = {}
            self.id_to_word = {int(rows[0]):rows[1] for rows in reader}

        with open("data/subreddit_mapper.csv", "rb") as f:
          reader = csv.reader(f, encoding="utf-8")
          self.subreddits = {}
          self.subreddits = {rows[0]:int(rows[1]) for rows in reader}

        self.id_to_word[0] = '<PAD>'
        self.word_to_id = {i:k for k,i in self.id_to_word.items()}


    def tokenize(self, words):
        token_ids = []
        for word in words.split(" "):
            if word in self.word_to_id.keys():
                token_ids.append(self.word_to_id[word])
            else:
                token_ids.append(1)

        return token_ids


    def prepare_post_prediction(self, post):

        post_data = post['title'] + " " + post['selftext']

        clean_post = ""
        for chr in str(title):
            if chr in '.!?\\-':
                clean_post += " "
            else:
                l = re.match('\w|\s', chr)
                if l:
                    clean_post += chr.lower()

        post_ids = self.tokenize(clean_post)
        self.post_ids_padded = sequence_pad_sequences(post_ids, maxlen=300)


    def make_prediction(self, post):
        self.prepare_post_prediction(post)
        self.prediction = self.model.predict(self.post_ids_padded)

        return self.get_subreddit_probas()

    def get_subreddit_probas(self):
        self.subreddit_probas = {}
        for i in range(len(self.prediction)):
            self.subreddit_probas[self.subreddits[i]] = self.prediction[i]

        return self.subreddit_probas



if __name__ == "__main__":
    pass
