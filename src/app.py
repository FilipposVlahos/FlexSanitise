from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import json
import os
import multiprocessing as mp
from multiprocessing import Process, Queue

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

questQueue = Queue()
answerQueue = Queue()

def worker(document):
    while not questQueue.empty():
        question = questQueue.get()
        print("Question ", "question")
        answerQueue.put(answerer.predict(document, question))

def sanitise_document_qa(document, questions):
    questions = json.loads(questions)
    for question in questions["questions"]:
        questQueue.put(question)

    nu_of_cpus = mp.cpu_count()
    p = []
    for i in range(nu_of_cpus):
        process = Process(target=worker, args=(document,))
        p.append(process)
        process.start()

    for process in p: 
        process.join()

    # replace
    sanitised_text = document
    while not answerQueue.empty():
        sanitised_text = sanitised_text.replace(answerQueue.get(), "[Sensitive Information]")

    return sanitised_text

if __name__ == '__main__':
    app.run()
