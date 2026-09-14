"""Traditional NLP utilities for similarity-based resume screening."""

import re
from collections import Counter
from typing import Iterable

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text: str) -> str:
    """Normalize text while preserving useful technical tokens such as C++ and .NET."""
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def match_category(score: float) -> str:
    """Return a presentational category for a percentage similarity score."""
    if score >= 80:
        return "Strong Match"
    if score >= 60:
        return "Good Match"
    if score >= 40:
        return "Moderate Match"
    return "Low Match"


def keyword_analysis(job_description: str, resume_text: str) -> dict:
    """Return an explainable keyword-overlap summary for the candidate details view."""
    stop_words = {
        "and", "the", "with", "for", "from", "that", "this", "are", "has", "have", "will",
        "into", "your", "their", "they", "our", "you", "who", "can", "should", "about", "using",
        "include", "including", "ideal", "looking", "help", "work", "team", "plus", "related",
    }
    job_tokens = re.findall(r"[a-z][a-z0-9+#.]{2,}", preprocess_text(job_description))
    resume_tokens = set(re.findall(r"[a-z][a-z0-9+#.]{2,}", preprocess_text(resume_text)))
    required = [word for word, _ in Counter(job_tokens).most_common() if word not in stop_words][:18]
    matched = [word for word in required if word in resume_tokens]
    missing = [word for word in required if word not in resume_tokens]
    coverage = round((len(matched) / len(required)) * 100, 1) if required else 0.0
    return {"matched_keywords": matched, "missing_keywords": missing, "keyword_coverage": coverage}


def rank_resumes(job_description: str, resumes: Iterable[dict]) -> list[dict]:
    """Rank extracted resumes in one shared TF-IDF vector space.

    ``resumes`` must provide ``filename`` and ``extracted_text``. Empty source text is
    excluded rather than allowing a malformed file to affect valid candidates.
    """
    valid = [item.copy() for item in resumes if preprocess_text(item.get("extracted_text", ""))]
    if not valid:
        return []

    job_text = preprocess_text(job_description)
    if not job_text:
        return []

    corpus = [job_text] + [preprocess_text(item["extracted_text"]) for item in valid]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(corpus)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    results = []
    for resume, similarity in zip(valid, similarities):
        score = round(float(similarity) * 100, 1)
        results.append({
            **resume,
            "cosine_similarity": round(float(similarity), 4),
            "match_score": score,
            "match_category": match_category(score),
            "status": "Analyzed",
            **keyword_analysis(job_description, resume["extracted_text"]),
        })

    results.sort(key=lambda item: item["match_score"], reverse=True)
    for position, item in enumerate(results, start=1):
        item["rank"] = position
    return results


def results_dataframe(results: list[dict]) -> pd.DataFrame:
    """Build a compact display table without exposing the full extracted text."""
    return pd.DataFrame([
        {
            "Rank": f"#{item['rank']}",
            "Candidate": item["filename"],
            "Match Score": f"{item['match_score']:.1f}%",
            "Cosine Similarity": f"{item['cosine_similarity']:.4f}",
            "Category": item["match_category"],
        }
        for item in results
    ])
