from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS
import json
import os
import multiprocessing as mp
from multiprocessing import Process, Queue
import time 
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
    sanitise_document_qa(document, questions)
    return reply(document)

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
        answer = answerer.predict(document, question)
        print("Question: ", question, "- Answer: ", answer)
        answerQueue.put(answer)

def sanitise_document_qa(document, questions):
    start_time = time.time()
    questions = json.loads(questions)
    for question in questions["questions"]:
        questQueue.put(question)

    nu_of_cpus = mp.cpu_count()
    p = []
    for i in range(min(nu_of_cpus, len(questions["questions"]))):
        process = Process(target=worker, args=(document,))
        p.append(process)
        process.start()

    for process in p: 
        process.join()
    print("--- %s seconds ---" % (time.time() - start_time))

def reply(document):
    # replace
    sanitised_document = document
    highlighted_document = document
    while not answerQueue.empty():
        answer = answerQueue.get()
        sanitised_document = sanitised_document.replace(answer, "[Sensitive Information]")
        highlighted_document = highlighted_document.replace(answer, "<span style=\"background-color: #FFFF00\">" + answer + "</span>")
    
    return jsonify(sanitisedDocument = sanitised_document, highlightedDocument=highlighted_document)

if __name__ == '__main__':
    app.run()
