"""ner.py

Run spaCy NER over an input string and insert XML tags for each entity.

"""

import io
import spacy

nlp = spacy.load("en_core_web_sm")


class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_tokens(self) -> list:
        return [token.lemma_ for token in self.doc]

    def get_entities(self) -> str:
        entities = []
        for e in self.doc.ents:
            entities.append((e.start_char, e.end_char, e.label_, e.text))
        return entities

    def get_entities_with_markup(self) -> str:
        entities = self.doc.ents
        starts = {e.start_char: e.label_ for e in entities}
        ends = {e.end_char: True for e in entities}
        buffer = io.StringIO()
        for p, char in enumerate(self.text):
            if p in ends:
                buffer.write("</entity>")
            if p in starts:
                buffer.write('<entity class="%s">' % starts[p])
            buffer.write(char)
        markup = buffer.getvalue()
        return "<markup>%s</markup>" % markup

    def get_dep_parses(self) -> list:
        sentences = []
        for sent in self.doc.sents:
            deps = [sent]
            for tok in sent:
                deps.append((tok.head.text, tok.dep_, tok.text))
            sentences.append(deps)
        return sentences

    def get_deps_w_markup(self) -> str:
        dep_markup = "<p><b> Dependency Parses </b></p>"
        for sent in self.doc.sents:
            dep_markup += "<p>" + sent.text + "</p>"
            dep_markup += "<table><tbody>"
            for tok in sent:
                dep_markup += "<tr>"
                dep_markup += "<td>" + tok.head.text + "</td>"
                dep_markup += "<td>" + tok.dep_ + "</td>"
                dep_markup += "<td>" + tok.text + "</td>"
                dep_markup += "</tr>"
            dep_markup += "</tbody></table>"
        return dep_markup

    def get_ents_and_rels(self) -> list:
        ents_and_rels = []
        for e in self.doc.ents:
            ents_and_rels.append((e.text, e.root.dep_, e.root.head.text))
        return ents_and_rels


if __name__ == "__main__":

    example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week."
    )

    sdoc = SpacyDocument(example)
    entities = sdoc.doc.ents
    print(sdoc.get_ents_and_rels())
    print(sdoc.get_tokens())
    for entity in sdoc.get_entities():
        print(entity)
    print(sdoc.get_entities_with_markup())
    print(sdoc.get_dep_parses()[0][1:])
    # print(doc.get_deps_w_markup())
