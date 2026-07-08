"""Simple Indonesian/English lexicon sentiment for news/RSS titles and scraped text."""
import json
import re
from pathlib import Path
import pandas as pd
from config import ROOT, DATA_PROCESSED
from utils import now_stamp

LEXICON_PATH = ROOT / "config" / "indonesian_sentiment_lexicon.json"
DEFAULT_LEXICON = {
    "positive": ["naik", "menguat", "untung", "profit", "positif", "pulih", "tumbuh", "rekor", "surplus", "stabil", "bullish", "optimis", "meningkat"],
    "negative": ["turun", "melemah", "rugi", "negatif", "krisis", "anjlok", "defisit", "inflasi", "mahal", "bearish", "pesimis", "gagal", "risiko"]
}


def load_lexicon():
    if LEXICON_PATH.exists():
        return json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
    LEXICON_PATH.write_text(json.dumps(DEFAULT_LEXICON, indent=2, ensure_ascii=False), encoding="utf-8")
    return DEFAULT_LEXICON


def score_text(text, lexicon=None):
    lexicon = lexicon or load_lexicon()
    words = re.findall(r"[a-zA-ZÀ-ÿ]+", str(text).lower())
    pos = sum(1 for w in words if w in set(lexicon.get("positive", [])))
    neg = sum(1 for w in words if w in set(lexicon.get("negative", [])))
    score = pos - neg
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return {"sentiment_score": score, "sentiment_label": label, "positive_hits": pos, "negative_hits": neg}


def analyze_observation_text(df, text_col="item"):
    if df is None or df.empty:
        return pd.DataFrame()
    lexicon = load_lexicon()
    out = df.copy()
    scores = out[text_col].apply(lambda x: score_text(x, lexicon))
    score_df = pd.DataFrame(scores.tolist())
    out = pd.concat([out.reset_index(drop=True), score_df], axis=1)
    return out


def export_sentiment(df, basename="sentiment"):
    out = analyze_observation_text(df)
    path = DATA_PROCESSED / f"{now_stamp()}_{basename}.csv"
    out.to_csv(path, index=False)
    return out, path
