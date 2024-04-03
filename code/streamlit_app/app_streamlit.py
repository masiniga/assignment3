from collections import Counter

import streamlit as st
import pandas as pd
import altair as alt
import graphviz
import ner

example = (
    "When Sebastian Thrun started working on self-driving cars at "
    "Google in 2007, few people outside of the company took him "
    "seriously. “I can tell you very senior CEOs of major American "
    "car companies would shake my hand and turn away because I wasn’t "
    "worth talking to,” said Thrun, in an interview with Recode earlier "
    "this week."
)


# st.set_page_config(layout='wide')
st.markdown("## spaCy Named Entity Recognition")


parse = st.sidebar.radio("Select view", ["entities", "dependencies"])

text = st.text_area("Text to process", value=example, height=100)

doc = ner.SpacyDocument(text)

entities = doc.get_entities()
tokens = doc.get_tokens()
counter = Counter(tokens)
words = list(sorted(counter.most_common(30)))
deps = doc.get_dep_parses()

if parse == "entities":
    # https://pandas.pydata.org
    chart = pd.DataFrame(
        {"frequency": [w[1] for w in words], "word": [w[0] for w in words]}
    )

    # https://pypi.org/project/altair/
    bar_chart = alt.Chart(chart).mark_bar().encode(x="word", y="frequency")

    st.markdown(
        f"Total number of tokens: {len(tokens)}<br/>"
        f"Total number of types: {len(counter)}",
        unsafe_allow_html=True,
    )

    # https://docs.streamlit.io/library/api-reference/data/st.table
    st.table(entities)

    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
    st.altair_chart(bar_chart)
else:
    # dep_chart = df = pd.DataFrame(tuple, columns=['parent', 'label', 'child'])
    table_tab, graph_tab = st.tabs(["table", "graph"])
    with table_tab:
        for sent in deps:
            st.markdown(sent[0])
            st.table(sent[1:])

    with graph_tab:
        for sent in deps:
            st.markdown(sent[0])
            graph = graphviz.Digraph()
            for word in sent[1:]:
                graph.edge(word[0], word[2], label=word[1])
            st.graphviz_chart(graph)
