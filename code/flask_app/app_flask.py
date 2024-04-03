"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

import ner


app = Flask(__name__)

app.config["SECRET_KEY"] = "fc3bb2a43ff1103895a4ee315ee27740"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class NER(db.Model):
    """This class manages the NER database."""
    entity = db.Column(db.String(100), nullable=False, primary_key=True)
    head = db.Column(db.String(100), nullable=False, primary_key=True)
    relation = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"('{self.entity}', '{self.relation}', '{self.head}')"

    @classmethod
    def add(cls, ent, rel, head):
        try:
            doc = NER(entity=ent, relation=rel, head=head)
            print(doc)
            db.session.add(doc)
            db.session.commit()
            return str(doc)
        except IntegrityError as e:
            db.session.rollback()
            return e


with app.app_context():
    db.create_all()


# For the website we use the regular Flask functionality and serve up HTML pages.
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("form.html", input=open("input.txt").read())
    else:
        text = request.form["text"]
        doc = ner.SpacyDocument(text)
        markup = doc.get_entities_with_markup()
        markup_paragraphed = ""
        for line in markup.split("\n"):
            if line.strip() == "":
                markup_paragraphed += "<p/>\n"
            else:
                markup_paragraphed += line
        # add entities and relation and their heads to database
        for ent, rel, head in doc.get_ents_and_rels():
            NER.add(ent, rel, head)
        markup_paragraphed += doc.get_deps_w_markup()
        return render_template("result.html", markup=markup_paragraphed)


# alternative where we use two resources


@app.get("/db")
def db_index():
    ents = NER.query.all()
    return render_template("form_db.html", ents=ents)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
    # app.run(debug=True)
