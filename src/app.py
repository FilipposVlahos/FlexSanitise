from common_components import DocumentRetrieval
from allennlp_answerer import PythonPredictor

import os

document_retriever = DocumentRetrieval()
answerer = PythonPredictor()

def main():
    answers = []
    original_text = document_retriever.get_document()
    with open("data_set/QuestionsForSanitisation.txt") as questions:
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

    f = open("results/sanitised_documet.txt", "w")
    f.write(sanitised_text)
    f.close()

main()
