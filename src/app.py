from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import json
import os

from allennlp_answerer import PythonPredictor

app = Flask(__name__)
cors = CORS(app)

answerer = PythonPredictor()

@app.route('/document', methods=['POST'])
def create_task():
    if not request.json or not "document" or not "questions" in request.json:
        abort(400)
    document = request.json["document"]
    questions = request.json["questions"]
    print("Document", document)
    print("Questions:", questions)
    return jsonify({'sanitisedDocument': sanitise_document(document, questions)})


def sanitise_document(document, questions):
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
