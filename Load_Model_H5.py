
import keras
from tensorflow.keras.preprocessing import sequence
import csv


class Model:

    def __init__(self, model_location="model/post_here_classifier.h5"):
        self.model = keras.models.load_model(model_location)

        with open("data/word_to_id.csv", "r") as file:
            reader = csv.reader(file)
            self.word_to_id = {rows[0]:rows[1] for rows in reader}

        with open("subreddit_mapper.csv", "r") as file:
          reader = csv.reader(file)
          subreddit_mapper = {rows[0]:rows[1] for rows in reader}
          self.subreddit_mapper = {v:k for k,v in subreddit_mapper.items()}


    def tokenize(words, word_to_id):
        token_ids = []
        for word in words.split(" "):
            if word in word_to_id.keys():
                token_ids.append(word_to_id[word])
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

        post_ids = self.tokenize(clean_post, self.word_to_id)
        self.post_ids_padded = sequence_pad_sequences(post_ids, maxlen=300)


    def make_prediction(self, post):
        self.prepare_post_prediction(post)
        self.prediction = self.model.predict(self.post_ids_padded)

        return self.get_subreddit_probas()

    def get_subreddit_probas(self):
        self.subreddit_probas = {}
        for i in range(len(self.prediction)):
            self.subreddit_probas[self.subreddit_mapper[i]] = self.prediction[i]

        return self.subreddit_probas



if __name__ == "__main__":
    pass
