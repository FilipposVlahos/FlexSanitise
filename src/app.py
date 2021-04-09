from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import re

from regex_sanitisations import RegexSanitisation
from qa_sanitiser import QASanitiser
from ner import NamedEntityRecogniser

app = Flask(__name__)
cors = CORS(app)

regex_sanitiser = RegexSanitisation()
qa_sanitiser = QASanitiser()
named_entity_recogniser = NamedEntityRecogniser()

@app.route('/document', methods=['POST'])
def sanitise():
    '''
        Takes a document and returns a sanitised document and a highlighted document
            document: The document to be sanitised
            questions: List of questions the answers of which will be sanitised from the document
            regex: List containing types of structured data to be sanitised. For more info look in regex_sanitisations.py
            ner: List of lists containing of the form [named_entity, label]. Wherever named_entity appears in document replace it with label
    '''
    if not request.json or not "document" or not "questions" or not "regex" or not "ner" in request.json:
        abort(400)
    document, questions, regex, ner = request.json["document"], request.json["questions"], request.json["regex"], request.json["ner"]
    print("Document:", document, "\n" "Questions:", questions, "\n", "Regex:", regex)
    docs = {"sanitisedDocument": document, "highlightedDocument": document}
    docs = qa_sanitiser.sanitise_qa(docs, questions)
    docs = regex_sanitiser.sanitise_document_regex(docs, regex)
    docs = named_entity_recogniser.sanitiseNer(docs, ner)
    docs = highlight_sanitised_document(docs)
    return jsonify(docs)

@app.route('/ner', methods=['POST'])
def ner():
    '''
        Takes a document and returns list of lists of the form [named_entity, label]
            document: Document from which named entities will be recognised
    '''
    if not request.json or not "document" in request.json:
        abort(400)
    document = request.json["document"]
    name_entities = named_entity_recogniser.getNamedEntities(document)
    return (jsonify(name_entities))

def highlight_sanitised_document(docs):
    '''
        Highlights text in brackets within the sanitisedDocument 
    '''
    sanitised_doc = docs["sanitisedDocument"]
    sanitisedDocument = re.sub(
        r'(\[.*?\])', r'<span style="background-color: yellow">\1</span>', sanitised_doc)
    docs["sanitisedDocument"] = sanitisedDocument
    return docs

if __name__ == '__main__':
    app.run()
