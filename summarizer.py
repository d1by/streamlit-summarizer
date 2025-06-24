import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def summarize_text(text, threshold_factor=1.2):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqs = {}
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        freqs[word] = freqs.get(word, 0) + 1

    sentences = sent_tokenize(text)
    sentenceValue = {}
    for sentence in sentences:
        for word, freq in freqs.items():
            if word in sentence.lower():
                sentenceValue[sentence] = sentenceValue.get(sentence, 0) + freq

    average = sum(sentenceValue.values()) / len(sentenceValue)

    summary = ''
    for sentence in sentences:
        if sentence in sentenceValue and sentenceValue[sentence] > (threshold_factor * average):  # use slider value
            summary += " " + sentence

    return summary.strip()

st.title("Text Summarizer (Extractive)")

text = st.text_area("Enter text:", height=300)

threshold = st.slider("Summary threshold", min_value=0.5, max_value=2.0, value=1.2, step=0.1)
    
if st.button("Summarize"):
    result = summarize_text(text, threshold)
    if result:
        st.subheader("Summary:")
        st.write(result)

        original_word_count = len(text.split())
        summary_word_count = len(result.split())

        st.markdown(f"**Original Word Count:** {original_word_count}")
        st.markdown(f"**Summary Word Count:** {summary_word_count}")
                    
    else:
        st.warning("No summary could be generated. ")