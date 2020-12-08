# Post_Here_Classifier


# Introduction
This is a program to train a nueral network to classify which subreddit an inputed post title and text would fit best. Due to github file size restraints, a couple additional file(s) will have to be loaded into this structure. See "Functionality" below..

# What is Here?
  ## PHC.py 
PHC.py is a class to train the .csv for the collected Reddit post data using tensorflow. A trained tensorflow model is saved in the model subfolder in ".h5" format. Pertinant data for loading and translating model results are saved in the data subdirectory: a "subreddit_mapper.csv" to translate the subreddit name to the model node, and an id to word hash table for the corpus of words most common in the training data. 

## Load_Model_H5.py 
Load_Model_H5.py is a class to open the trained post_here_classifier.h5 model and used to make prediction calls. The model is loaded from the ".h5" save foramt with keras.load_model(). The "subreddit_mapper.csv" and "id_to_word.csv" saved with the model train are used to translate model predictions into a human readable format and encode input posts into word vectors. The make_prediction(self, post) call of this class takes an inputed jsonified post ex. 

{"post_title": "this is my post title.", 
 "post_text": "this is my post text."}

The posts are tokenized into word vectors and the loaded model is called to make a prediction. The prediction is the subreddit node(s) that is classified to fit best. The node(s) id is translated to english via the subreddit_mapper hash table and returned.

## test files
These are simple Flask test files. The test_request.py requests' json parameter can be changed to test various post titles and texts.

# Functionality
  ## Load_Model_H5.py
  Load Saved H5 Model and used class to hold a model to call predict

  ## PHC.py
  Create a clean data, create a pandas.DataFrame, fit model to subreddit targets, and save model files to be loaded.



# Additional Files to download for Post_Here_Classifier due to file size constraints
  ## Data used to run model in PHC.py (reddit_posts_4M.csv)
  Place in /data subdirectory -------> https://drive.google.com/file/d/1xSlIorTFBQC-wJ2lHBZNtyqTJ1Iy9-bl/view?usp=sharing

  ## Saved model for loading in Load_Model_H5.py (post_here_classifier.h5)
  Place in /model subdirectory ------> https://drive.google.com/file/d/1hGkHbrTXhsYSiO4du5uRtHybwPCCsrne/view?usp=sharing
