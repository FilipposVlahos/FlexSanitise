from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import os

from regex_sanitizations import RegexSanitization
from qa_sanitiser import QASanitiser

app = Flask(__name__)
cors = CORS(app)

regex_sanitiser = RegexSanitization()
qa_sanitiser = QASanitiser()

@app.route('/document', methods=['POST'])
def sanitise():
    if not request.json or not "document" or not "questions" or not "regex" in request.json:
        abort(400)
    document, questions, regex = request.json["document"], request.json["questions"], request.json["regex"]
    print("Document:", document, "\n" "Questions:", questions, "\n", "Regex:", regex)
    docs = {"docToSanitise": document, "docToHighlight": document}
    docs = qa_sanitiser.sanitise_qa(docs, questions)
    docs = regex_sanitiser.sanitise_document_regex(docs, regex)
    return jsonify(docs)

if __name__ == '__main__':
    app.run()
