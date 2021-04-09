import spacy
import en_core_web_trf

class NamedEntityRecogniser:
    def __init__(self):
        self.nlp = en_core_web_trf.load(exclude=["lemmatizer", "token"])

    def getNamedEntities(self, document):
        doc = self.nlp(document)
        name_entities = []
        uniqueEntities = set()
        for X in doc.ents:
            if X.text not in uniqueEntities:
                name_entities.append([X.text, X.label_])
                uniqueEntities.add(X.text)
        return ({
            "ner": name_entities
        })

    def sanitiseNer(self, documents, ner):
        document_without_ne = documents["sanitisedDocument"]
        highlighted_document = documents["highlightedDocument"]
        for named_entity, label in ner:
            document_without_ne = document_without_ne.replace(named_entity, "[" + label + "]")
            highlighted_document = highlighted_document.replace(named_entity,  "<span style=\"background-color:lightgreen\">" + named_entity + "</span>")
        return ({"sanitisedDocument": document_without_ne, "highlightedDocument": highlighted_document})
