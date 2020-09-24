"""Machine Learning Model for MedCab"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def searchfunc(user_input, num_results=5):
    """Flexible function that searches for cannabis strains.
    ### Request Body
    - user_input str : string of ailments to be trained on
    - num_results int : number of strains desired, default 5
    ### Response
    - `output`: a list of indices matching predicted strains
    """
    user_input = [user_input]
    tf = TfidfVectorizer(stop_words='english')
    print(df.head())
    dtm = tf.fit_transform(df['ailment_tokens'])
    dtm = pd.DataFrame(dtm.todense(), columns=tf.get_feature_names())
    nr = num_results
    nn = NearestNeighbors(n_neighbors=nr, algorithm='ball_tree')
    nn.fit(dtm)
    dtf = tf.transform(user_input)
    _, output = nn.kneighbors(dtf.todense())
    return output