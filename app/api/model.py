"""Machine Learning Model for MedCab"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def searchfunc(user_input):
    """Flexible function that searches for cannabis strains.
    ### Request Body
    - user_input str : string of ailments to be trained on
    ### Response
    - `output`: a list of indices matching predicted strains
    """
    user_input = [user_input]
    tf = TfidfVectorizer(stop_words='english')
    print(df.head())
    dtm = tf.fit_transform(df['ailment_tokens'])
    dtm = pd.DataFrame(dtm.todense(), columns=tf.get_feature_names())
    nn = NearestNeighbors(n_neighbors=1, algorithm='ball_tree')
    nn.fit(dtm)
    dtf = tf.transform(user_input)
    _, output = nn.kneighbors(dtf.todense())
    return output