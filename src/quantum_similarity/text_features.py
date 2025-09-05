from typing import List, Tuple, Dict
import re
import math
import numpy as np

TOKEN_RE = re.compile(r"[A-Za-z0-9']+")

def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]

def build_vocab(a_tokens: List[str], b_tokens: List[str], max_features: int = 1024) -> List[str]:
    # Simple DF counts
    df: Dict[str, int] = {}
    for tok in set(a_tokens):
        df[tok] = df.get(tok, 0) + 1
    for tok in set(b_tokens):
        df[tok] = df.get(tok, 0) + 1
    # Sort by document frequency desc, then alpha
    vocab = sorted(df.items(), key=lambda kv: (-kv[1], kv[0]))
    vocab = [w for w, _ in vocab][:max_features]
    return vocab

def vectorize(tokens: List[str], vocab: List[str], mode: str = "tf") -> np.ndarray:
    """
    Convert tokens into a vector over vocab.
    mode:
      - "tf": term frequency
      - "bin": binary presence
    """
    idx = {w: i for i, w in enumerate(vocab)}
    vec = np.zeros(len(vocab), dtype=float)
    for t in tokens:
        j = idx.get(t)
        if j is not None:
            if mode == "bin":
                vec[j] = 1.0
            else:
                vec[j] += 1.0
    if mode == "tf" and vec.sum() > 0:
        vec = vec / vec.sum()
    return vec

def text_to_vector(a_text: str, b_text: str, mode: str = "tf", max_features: int = 1024) -> Tuple[np.ndarray, np.ndarray]:
    a_toks = tokenize(a_text)
    b_toks = tokenize(b_text)
    vocab = build_vocab(a_toks, b_toks, max_features=max_features)
    va = vectorize(a_toks, vocab, mode=mode)
    vb = vectorize(b_toks, vocab, mode=mode)
    return va, vb
