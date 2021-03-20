# Document Sanitisation Tool

## To run:

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