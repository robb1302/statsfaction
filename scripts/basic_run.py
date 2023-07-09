import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

print('pleeeease')

from transformers import pipeline

classifier = pipeline('sentiment-analysis')
sentence = "Henni likes the Medis!!!"
print("\nLabel:", sentence)
result = classifier("Henni likes the Medis!!!")
print(result)

sentence = "Robert does not unterstand the Medis!!!"
print("\nLabel:", sentence)
result = classifier(sentence)
print(result)

print("\nDONE")