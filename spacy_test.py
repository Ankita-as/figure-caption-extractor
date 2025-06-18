import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp("Apple Inc. is looking at buying a startup in the U.K. for $1 billion.")

print([(ent.text, ent.label_) for ent in doc.ents])
