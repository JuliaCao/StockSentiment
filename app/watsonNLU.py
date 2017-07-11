import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features

natural_language_understanding = NaturalLanguageUnderstandingV1(
username="33ef4781-a0cc-4486-b186-28d5e78bdc06",
password="hN7h6o6sTnD4",
version="2017-07-11")

response = natural_language_understanding.analyze(
text = "IBM is an American multinational technology company headquartered \
    in Armonk, New York, United States, with operations in over 170 \
    countries.",
features=[
Features.Sentiment(
  # Emotion options
  targets=["IBM"]
    )
  ]
)

# print(json.dumps(response, indent=2))
print response["sentiment"]["document"]["score"]