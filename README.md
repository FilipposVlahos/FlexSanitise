# Document Sanitisation Tool

## To install dependencies:

Install dependencies from requirements.txt by running

```pip install -r requirements.txt ```

Then install the pre-trained transformers model from spaCy by running
```python -m spacy download en_core_web_trf```


## To run:

Go to src directory and run:

```flask run```

## endpoints: 
### POST Request: /document
```json:
{
    document: "",
    questions: "{"questions":[]}",
    regex: [],
    ner: []
}
```

### POST Request: /ner
```json:
{
    document: ""
}
```


## React web interface:
[Web Interface Repository](https://gitlab.cs.man.ac.uk/p72510fv/sanitisation-system-front-end)