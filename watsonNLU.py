import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features

natural_language_understanding = NaturalLanguageUnderstandingV1(
username="33ef4781-a0cc-4486-b186-28d5e78bdc06",
password="hN7h6o6sTnD4",
version="2017-07-11")

response = natural_language_understanding.analyze(
html=" \
<html> \
  <head><title>Fruits</title></head> \
  <body> \
    <h1>Apples and Oranges</h1> \
    <p>I love apples! I don't like oranges.</p> \
  </body> \
</html>",
features=[
Features.Emotion(
  # Emotion options
  targets=["apples","oranges"]
    )
  ]
)

print(json.dumps(response, indent=2))