"""
FastAPI interface to spaCy NER

$ curl http:/127.0.0.1:8000
$ curl -X POST -H 'accept: application/json' -H 'Content-Type: application/json' -d@input.json http:/127.0.0.1:8000

"""

import json
from fastapi import FastAPI, Response
from pydantic import BaseModel
import ner

app = FastAPI()


class Item(BaseModel):
    text: str = ""


@app.get("/")
def index(pretty: bool = False):
    content = "Content-Type: application/json"
    url = "http://127.0.0.1:8000/"
    answer = {
        "description": "Interface to the spaCy entity extractor",
        "usage": 'curl -H "%s" -d@input.json %s' % (content, url),
    }
    if pretty:
        answer = prettify(answer)
    return answer


@app.post("/ner")
def process(item: Item, pretty: bool = False):
    doc = ner.SpacyDocument(item.text)
    answer = {"input": item.text, "output": doc.get_entities()}
    if pretty:
        answer = prettify(answer)
    return answer


@app.post("/dep")
def process2(item: Item, pretty: bool = False):
    doc = ner.SpacyDocument(item.text)
    answer = {"input": item.text, "output": [sent[1:] for sent in doc.get_dep_parses()]}
    if pretty:
        answer = prettify(answer)
    return answer


def prettify(result: dict):
    json_str = json.dumps(result, indent=2)
    return Response(content=json_str, media_type="application/json")
