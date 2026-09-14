# Rolevia — AI-Powered Resume Screening & Candidate Ranking

Rolevia is a recruiter-style Streamlit dashboard that ranks PDF resumes by their **textual similarity** to a supplied job description. It is a B.Tech CSE/Data Science project demonstrating an understandable, traditional NLP pipeline—no LLMs, APIs, or transformer models are used.

## Objective

Compare multiple resumes against a job description using PDF text extraction, text preprocessing, TF-IDF representation, cosine similarity, and descending ranking.

## Features

- Multiple PDF resume upload with per-file error handling
- Text extraction from every PDF page via PyMuPDF
- Lightweight normalization: lowercase, punctuation/noise removal, whitespace normalization
- One shared `TfidfVectorizer` fit over the job description and all valid resumes
- Cosine-similarity match score, category, ranking cards, table, and chart
- Candidate-level inspection of source text and calculation details
- Theme-aware light and dark executive dashboard

## How it works

```
Job Description + PDF Resumes
        ↓
Text extraction and preprocessing
        ↓
Shared TF-IDF vector space
        ↓
Cosine similarity for each resume
        ↓
Percentage score and ranked results
```

### TF-IDF and cosine similarity

TF-IDF assigns a weight to terms based on how important they are in a document relative to the supplied document set. Rolevia fits one vectorizer across the job description and all valid resumes, ensuring each comparison is made in the same feature space. Cosine similarity measures the angle between the job vector and each resume vector; its 0–1 output is displayed as a 0–100% textual match score.

## Ranking methodology

Candidates are sorted by descending cosine similarity. Presentation categories are `Strong Match` (80–100), `Good Match` (60–79), `Moderate Match` (40–59), and `Low Match` (below 40). These labels are descriptive UI groupings, not assessments of candidate quality, suitability, or hiring probability.

## Project structure

```
AI-resume-screening/
├── app.py
├── resume_parser.py
├── nlp_utils.py
├── ui/
│   ├── styles.py
│   └── components.py
├── requirements.txt
└── .gitignore
```

## Installation and running

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Paste a job description, upload one or more text-based PDF resumes, and select **Analyze & Rank Resumes**.

## Limitations and future improvements

- Scanned/image-only PDFs have no machine-readable text without OCR.
- Textual similarity cannot evaluate experience quality, context, fairness, or human fit.
- Future versions could add local OCR, configurable weighting, exportable reports, and bias/audit support.

## Disclaimer

Rolevia is an assistive educational tool, not an automated hiring decision-maker. Keep a qualified human reviewer in the loop and do not use the score as a sole decision criterion.

## Author

Built for the AI Resume Screening academic project.
