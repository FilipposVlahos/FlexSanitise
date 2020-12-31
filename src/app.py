from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS

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
    print(document)
    print(questions)
    return jsonify({'sanitisedDocument': sanitise_document(document, questions)})


def sanitise_document(document, questions):
    answers = []
    original_text = document
    
    for question in questions:
        print(question, end='')
        # find answer to question
        answer = answerer.predict(original_text, question)
        print(answer["answer"])
        print()
        answers.append(answer["answer"])
    
    # replace
    sanitised_text = original_text
    for answer in answers:
        sanitised_text = sanitised_text.replace(answer, "[Sensitive Information]")

    return sanitised_text

if __name__ == '__main__':
    app.run()
