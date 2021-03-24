Project on google cloud: 
  https://post-here-classi-1612563081759.uc.r.appspot.com/
  
Note : I am no longer paying Google Cloud to host the project. You can host it locally with instructions below:

Local Environment Setup
  a. The repository will need to be downloaded into the file of your choice. The link is here: “https://github.com/Joseph-Maulin/Post_Here_Classifier.git”. You will need to enable git for your terminal or command line. The documentation for setting up git for your command or terminal can be found here: “https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html”.
  
  b. Once git is installed you will run this command to download the repository to your local environment.
    i. git clone https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html

  c. You will need to get the model for the application.
    i.   Download the model here: “https://drive.google.com/file/d/1hGkHbrTXhsYSiO4du5uRtHybwPCCsrne/view?usp=sharing” 
    ii.  Save the model as “post_here_classifier.h5”
    iii. Place the “post_here_classifier.h5” in the “src/reddit/model/model/” subdirectory.

  d. Next set up a virtual environment for the application.
    i.  In the command line cd into the project directory.
    ii. Create a new virtual environment and install the requirements
      1. If you do not have Python installed, download it here: “https://www.python.org/downloads/” 
      2. Use the command “pip install virtualenv” in the terminal or command line. 
      3. Windows command line operations
        a. python -m venv environment
        b. environment\Scripts\activate
        c. pip install -r requirements.txt
      4. Mac or Linux
        a. virtualenv environment
        b. source venv/bin/activate
        c. pip install -r requirements.txt
    iii. Once you have the virtual environment setup and activated, we can start the application. 
      1. cd one level down into /src
      2. Run the command “python manage.py runserver”
        a. On initial setup you may have to run the following:
          i. “python manage.py migrate”
          ii. “python mange.py makemigrations”
      3. This should start a local instance of the server on your machine at 127.0.0.1:8000. This can be accessed by typing the   IP in a browser (127.0.0.1:8000). 


# Reddit Classifier

It uses an LSTM nueral network to train on reddit post data to predict to which subreddit a post would best fit. This will build over time as new post data will be trained for the model. It will also contain user post data to track recent user activity and post metrics.

# Post_Here_Classifier


# Introduction
This is a program to train a neural network to classify which subreddit an inputed post title and text would fit best. Due to github file size restraints, a couple additional file(s) will have to be loaded into this structure. See "Functionality" below..

# What is Here?

## src
Django app files are here.

## reddit
This is the file contains the web application and supporting files.
  
  ### reddit/model
  Contains the LSTM model, PHC(trainer), Load_Model_H5(loader), and model data.
  
  #### reddit/model/PHC.py 
PHC.py is a class to train the .csv for the collected Reddit post data using tensorflow. A trained tensorflow model is saved in the model subfolder in ".h5" format. Pertinant data for loading and translating model results are saved in the data subdirectory: a "subreddit_mapper.csv" to translate the subreddit name to the model node, and an id to word hash table for the corpus of words most common in the training data. 

  #### reddit/model/Load_Model_H5.py 
Load_Model_H5.py is a class to open the trained post_here_classifier.h5 model and used to make prediction calls. The model is loaded from the ".h5" save foramt with keras.load_model(). The "subreddit_mapper.csv" and "id_to_word.csv" saved with the model train are used to translate model predictions into a human readable format and encode input posts into word vectors. The make_prediction(self, post) call of this class takes an inputed jsonified post ex. 

{"post_title": "this is my post title.", 
 "post_text": "this is my post text."}

The posts are tokenized into word vectors and the loaded model is called to make a prediction. The prediction is the subreddit node(s) that is classified to fit best. The node(s) id is translated to english via the subreddit_mapper hash table and returned.

  ### reddit/templates
  Holds the templates and graph html files for web application.
  
  ## reddit/Reddit_API.py
  This class controls the Reddit API (praw) to pull data from Reddit to support application.
  
  ## reddit/views.py
  Controls web application routing


# Functionality
  ## Load_Model_H5.py
  Load Saved H5 Model and used class to hold a model to call predict

  ## PHC.py
  Create a clean data, create a pandas.DataFrame, fit model to subreddit targets, and save model files to be loaded.



# Additional Files to download for Post_Here_Classifier due to file size constraints
  ## Data used to train the model in PHC.py (reddit_posts_4M.csv)
                      -------> https://drive.google.com/file/d/1xSlIorTFBQC-wJ2lHBZNtyqTJ1Iy9-bl/view?usp=sharing

  ## Saved model for loading in Load_Model_H5.py (post_here_classifier.h5)
  Place in “src/reddit/model/model/” subdirectory 
  ##
                      -------> https://drive.google.com/file/d/1hGkHbrTXhsYSiO4du5uRtHybwPCCsrne/view?usp=sharing
