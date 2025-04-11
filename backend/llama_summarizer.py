# llama_summarizer.py

from transformers import pipeline

# Load the summarizer pipeline (only once)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_len=200, min_len=30):
    # HuggingFace pipelines handle chunking for long texts
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']
