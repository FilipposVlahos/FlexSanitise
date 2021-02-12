from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import json
import os

from allennlp_answerer import PythonPredictor
from regex_sanitizations import RegexSanitization

app = Flask(__name__)
cors = CORS(app)

answerer = PythonPredictor()
regex_sanitiser = RegexSanitization()

@app.route('/document', methods=['POST'])
def create_task():
    if not request.json or not "document" or not "questions" or not "regex" in request.json:
        abort(400)
    document = request.json["document"]
    questions = request.json["questions"]
    regex = request.json["regex"]
    print("Document:", document)
    print("Questions:", questions)
    print("Regex:", regex)
    document = sanitise_document_regex(document, regex)
    return jsonify({'sanitisedDocument': sanitise_document_qa(document, questions)})

def sanitise_document_regex(document, regex):
    result = document
    if ("dates" in regex):
        result = regex_sanitiser.sanitise_dates(result)
    if ("days" in regex):
        result = regex_sanitiser.sanitise_days(result)
    if ("months" in regex):
        result = regex_sanitiser.sanitise_months(result)
    if ("emails" in regex):
        result = regex_sanitiser.sanitise_email_addresses(result)
    return result

def sanitise_document_qa(document, questions):
    answers = []
    questions = json.loads(questions)

    for question in questions["questions"]:
        print("Question", ": ", question)
        # find answer to question
        answer = answerer.predict(document, question)
        print("Answer ", ": ", answer["answer"])
        print()
        answers.append(answer["answer"])
    
    # replace
    sanitised_text = document
    for answer in answers:
        sanitised_text = sanitised_text.replace(answer, "[Sensitive Information]")

    return sanitised_text

if __name__ == '__main__':
    app.run()
