
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import tensorflow
import tensorflow.keras as keras
from tensorflow.keras.preprocessing import sequence
import unicodecsv as csv
from io import BytesIO
import re
import numpy as np
import pandas as pd
from collections import Counter

# https://console.cloud.google.com/appengine/start/deploy?language=python&environment=standard&project=post-here-classi-1612563081759&folder&organizationId
# https://github.com/llSourcell/how_to_deploy_a_keras_model_to_production/blob/master/instructions.ipynb

class Model:

    def __init__(self, model_location="reddit/model/model/post_here_classifier.h5", url_read = False):

        if(url_read):
            drive.mount('/content/gdrive')
            url = "/content/gdrive/My Drive/post_here_classifier"
            self.model = keras.models.load_model(url)

        else:
            self.model = keras.models.load_model(model_location)


        with open("reddit/model/model/id_to_word.csv", "rb") as f:
            reader = csv.reader(f, encoding="utf-8")
            id_to_word = {}
            id_to_word = {int(rows[0]):rows[1] for rows in reader}

        with open("reddit/model/model/subreddit_mapper.csv", "rb") as f:
          reader = csv.reader(f, encoding="utf-8")
          self.subreddits = {}
          self.subreddits = {rows[0]:int(rows[1]) for rows in reader}

        self.subreddit_mapper = {i:k for k,i in self.subreddits.items()}

        id_to_word[0] = '<PAD>'
        self.word_to_id = {i:k for k,i in id_to_word.items()}


        # this fixes a '\n' issue I have with this model. A new model with PHC.py can be trained on reddit_posts_4M
        keys_to_add = {}
        for key in self.word_to_id.keys():
            if "<NEWLINEMARKER>" in key:
                keys_to_add[re.sub("<NEWLINEMARKER>", "\n", key)] = [self.word_to_id[key], key]

        for i,k in keys_to_add.items():
            self.word_to_id[i] = k[0]
            del self.word_to_id[k[1]]



    def tokenize(self, words):
        token_ids = []
        for word in words.split(" "):
            if word in self.word_to_id.keys():
                token_ids.append(self.word_to_id[word])
            else:
                token_ids.append(1)

        return token_ids


    def prepare_post_prediction(self, post):
        """
        pass dictionary with {"post_title":"dalsfkjds", "post_text":"ldkfjasdlkfjd fsdljf slkfj asdkjf lsdkf"}
        """
        post_data = str(post['post_title']) + " " + str(post['post_text'])

        clean_post = ""
        for chr in str(post_data):
            if chr in '.!?\\-':
                clean_post += " "
            else:
                l = re.match('\w|\s', chr)
                if l:
                    clean_post += chr.lower()

        post_ids = self.tokenize(clean_post)
        self.post_ids_padded = sequence.pad_sequences([post_ids], maxlen=300)


    def make_prediction(self, post):
        self.prepare_post_prediction(post)
        self.prediction = self.model.predict(self.post_ids_padded)


        return self.get_subreddit_probas()

    def get_subreddit_probas(self):

        probas = {}

        for i in range(len(self.prediction[0])):
            probas[self.subreddit_mapper[i]] = self.prediction[0][i]

        max_features = 5

        k = Counter(probas)

        top_5 = k.most_common(max_features)

        pred_class = np.argmax(self.prediction, axis=1)

        return top_5
        # print(self.subreddit_mapper[pred_class[0]])
        # print(top_5)

model = Model()

def get_model():
    global model
    return model




if __name__ == "__main__":
    m = Model()

    post = {"post_title": "Only in 1989",
            "post_text" : "I'm absolutely losing my mind that credit scores weren't established in the US until 1989. We really are teh guinea pig generations for all the bad boomer ideas"}

    print(m.make_prediction(post))


    # df = pd.read_csv("data/test_reddit_frame.csv")
    # for i in range(20):
    #     title = df["title"][i]
    #     text = df["selftext"][i]
    #
    #     post = {"post_title": title,
    #             "post_text": text}
    #
    #     m.make_prediction(post)
    #     print("\n")
