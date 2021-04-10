# FlexSanitise

FlexSanitise is a hybrid document sanitisation API developed as part of my 3rd year project for my BSc in Computer Science at the University of Manchester.

It sanitises/redact documents using one or more of the following techniques:
* Question Answering
* Regular Expressions
* Named Entity Recognition

The API's front-end can be found [here](https://github.com/FilipposVlahos/FlexSanitise-Front-End)

## Installing dependencies

Install dependencies from requirements.txt by running

```pip install -r requirements.txt ```

Then install the pre-trained transformer model from spaCy by running

```python -m spacy download en_core_web_trf```

## Run application

Go to src directory and run:

```flask run```

## Endpoints
### Sanitise Document
* **URL**
    /document
* **Method**
    `POST`
* **Body**
    * document: The document to be sanitised
    * questions: List of questions the answers of which will be sanitised from the document
    * regex: List containing one or more of the available regex labels e.g. ["dates", "emails"]
    * ner: List of lists of the form [named_entity, label]. Wherever named_entity appears in document replace it with label

* **Success Response:**
  * **Code:** 200 OK
  * **Content:** 
    * sanitisedDocument: the sanitised document
    * highlightedDocument: the original document with the sensitive information being highlighted with html

* **Body example**
```json:
{
    document: "Mary had arthritis on 30/03/21",
    questions: "{"questions":["What did Mary suffer from?"}",
    regex: ["dates"],
    ner: [["Mary", "Person"]]
}
```
* **Response Example**
```json:
{
    "highlightedDocument":"<span style=\"background-color:lightgreen\">Mary</span> had <span style=\"background-color: Cyan\">arthritis</span> on <span style=\"background-color: orange\"><span style=\"background-color: orange\"><span style=\"background-color: orange\"><span style=\"background-color: orange\">30</span>/<span style=\"background-color: orange\">03</span>/<span style=\"background-color: orange\">21</span></span></span></span>.\n",
    
    "sanitisedDocument":"<span style=\"background-color: yellow\">[PERSON]</span> had <span style=\"background-color: yellow\">[Sensitive Information]</span> on <span style=\"background-color: yellow\">[Date]</span>.\n"
}
```


### Extract Named Entities
* **URL**
    /ner
* **Method**
    `POST`
* **Body**
    * document: Document from which named entities will be extracted
* **Body example**
    ```json:
    {document: "Bob used to work for Apple"}
    ```
* **Response example**
    ```json:
    {"ner":[["Bob", "PERSON"],["Apple","ORG"]]}
    ```
    