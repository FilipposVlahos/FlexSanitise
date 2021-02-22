from multiprocessing import Process, Queue
import multiprocessing as mp
import time
import json

from allennlp_answerer import PythonPredictor

class QASanitiser:
    def __init__(self):
        self.questQueue = Queue()
        self.answerQueue = Queue()
        self.answerer = PythonPredictor()

    
    def sanitise_qa(self, documents, questions):
        sanitised_document = documents["docToSanitise"]
        highlighted_document = documents["docToHighlight"]
        self.schedule_qa(sanitised_document, questions)
        
        while not self.answerQueue.empty():
            answer = self.answerQueue.get()
            sanitised_document = sanitised_document.replace(answer, "[Sensitive Information]")
            highlighted_document = highlighted_document.replace(answer, "<span style=\"background-color: yellow\">" + answer + "</span>")
        return {"sanitisedDocument":sanitised_document, "highlightedDocument":highlighted_document}

    def schedule_qa(self, document, questions):
        start_time = time.time()
        questions = json.loads(questions)
        for question in questions["questions"]:
            self.questQueue.put(question)

        nu_of_cpus = mp.cpu_count()
        p = []
        for i in range(min(nu_of_cpus, len(questions["questions"]))):
            process = Process(target=self.answer, args=(document,))
            p.append(process)
            process.start()

        for process in p:
            process.join()
        print("--- %s seconds ---" % (time.time() - start_time))
        
    def answer(self, document):
        while not self.questQueue.empty():
            question = self.questQueue.get()
            answer = self.answerer.predict(document, question)
            print("Question: ", question, "- Answer: ", answer)
            self.answerQueue.put(answer)
