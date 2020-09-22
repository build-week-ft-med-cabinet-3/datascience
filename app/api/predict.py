import logging
import random
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator


log = logging.getLogger(__name__)  # Jeremy might be able to explain
router = APIRouter()  # this establishes what router we are using (i.e FLASK)
df = pd.read_csv("data/cannabis_final.csv")


# def searchfunc():  # this is the function steve and jeremy will give me, used in ML training
#     """
#         Flexible function that searches for cannabis strains.
#         ### Request Body
#         - user_input str
#         - num_results int: default 10
#         ### Response
#         - `strain_recommendation`: dictionary of strain recommendations
#         """


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    symptoms: str = Field(..., example='insomia')  # this takes any symptom as a string
    # can also put a field for 'effects', 'flavors', 'strain', (if they do not concatnate the strings for us)

    def to_df(self):  # this will take our symptoms and takes it as a dictionary and makes it a dataframe for the model
                      # to use
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

    # @validator('x1')
    # def x1_must_be_positive(cls, value):
    #     """Validate that x1 is a positive number."""
    #     assert value > 0, f'x1 == {value}, must be > 0'
    #     return value


@router.post('/predict')
async def predict(item: Item):
    """
    # Make random baseline predictions for classification problem 🔮
    #
    # ### Request Body
    # - `x1`: positive float
    # - `x2`: integer
    # - `x3`: string
    #
    # ### Response
    # - `prediction`: boolean, at random
    # - `predict_proba`: float between 0.5 and 1.0,
    # representing the predicted class's probability
    #
    # Replace the placeholder docstring and fake predictions with your own model.
    # """

    X_new = item.to_df()
    log.info(X_new)
    # y_pred = random.choice([True, False])
    # y_pred_proba = random.random() / 2 + 0.5
    return {
        'recommendations': {
         "strain_recommendations": [
      {
        "name": "Hawaiian Thunder Fuck",
        "type": "hybrid",
        "flavors": "Sweet, Berry, Pungent",
        "positive_effects": "Relaxed, Euphoric, Happy, Talkative",
        "negative_effects": "Dry Mouth, Paranoid",
        "ailment": "Depression, Insomnia, Pain, Stress, Nausea, Headache",
        "search": "Hawaiian Thunder Fuck,Relaxed, Euphoric, Happy, Talkative,Sweet, Berry, Pungent,Depression, "
                  "Insomnia, Pain, Stress, Nausea, Headache"
      }
    ]}}
    # this is going to be the name of the prediction function, it will change
    # 'probability': y_pred_proba
