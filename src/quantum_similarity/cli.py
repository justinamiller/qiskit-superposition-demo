import argparse
import json
import sys
from typing import List

import numpy as np

from .encoding import vector_to_statevector
from .swap_test import swap_test_similarity
from .text_features import text_to_vector

def _parse_vector_arg(arg: str) -> List[float]:
    """
    Accept either a JSON list, a comma-separated list, or a path to a JSON file.
    """
    # File path?
    try:
        with open(arg, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [float(x) for x in data]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # JSON list inline?
    try:
        data = json.loads(arg)
        if isinstance(data, list):
            return [float(x) for x in data]
    except json.JSONDecodeError:
        pass

    # Comma-separated
    try:
        return [float(x.strip()) for x in arg.split(",")]
    except Exception as e:
        raise ValueError(f"Could not parse vector: {arg}") from e

def do_vectors(args: argparse.Namespace) -> int:
    v1 = _parse_vector_arg(args.vector1)
    v2 = _parse_vector_arg(args.vector2)

    s1, n1 = vector_to_statevector(v1)
    s2, n2 = vector_to_statevector(v2)
    if n1 != n2:
        # Padding should have equalized sizes; sanity check
        raise ValueError("Internal error: different qubit counts after encoding.")

    res = swap_test_similarity(s1, s2, shots=args.shots)
    print(json.dumps({
        "mode": "vectors",
        "n_qubits_per_register": int(np.log2(len(s1))),
        "shots": args.shots,
        **res
    }, indent=2))
    return 0

def do_text(args: argparse.Namespace) -> int:
    if args.text1_file:
        with open(args.text1_file, "r", encoding="utf-8") as f:
            t1 = f.read()
    else:
        t1 = args.text1

    if args.text2_file:
        with open(args.text2_file, "r", encoding="utf-8") as f:
            t2 = f.read()
    else:
        t2 = args.text2

    v1, v2 = text_to_vector(t1, t2, mode=args.feature_mode, max_features=args.max_features)

    s1, _ = vector_to_statevector(v1.tolist())
    s2, _ = vector_to_statevector(v2.tolist())

    res = swap_test_similarity(s1, s2, shots=args.shots)
    print(json.dumps({
        "mode": "text",
        "feature_mode": args.feature_mode,
        "max_features": args.max_features,
        "shots": args.shots,
        **res
    }, indent=2))
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Quantum superposition SWAP-test similarity (vectors & text)."
    )
    sub = parser.add_subparsers(dest="subcmd", required=True)

    # vectors subcommand
    p_vec = sub.add_parser("vectors", help="Compare two numeric vectors.")
    p_vec.add_argument("vector1", help="Vector A: JSON, CSV, or path to JSON file.")
    p_vec.add_argument("vector2", help="Vector B: JSON, CSV, or path to JSON file.")
    p_vec.add_argument("--shots", type=int, default=8192, help="Simulation shots.")
    p_vec.set_defaults(func=do_vectors)

    # text subcommand
    p_txt = sub.add_parser("text", help="Compare two texts (bag-of-words over shared vocab).")
    g1 = p_txt.add_mutually_exclusive_group(required=False)
    g1.add_argument("--text1", help="Text A (inline).")
    g1.add_argument("--text1-file", help="Path to text A file.")
    g2 = p_txt.add_mutually_exclusive_group(required=False)
    g2.add_argument("--text2", help="Text B (inline).")
    g2.add_argument("--text2-file", help="Path to text B file.")
    p_txt.add_argument("--feature-mode", choices=["tf", "bin"], default="tf",
                       help="Bag-of-words weighting (term-frequency or binary presence).")
    p_txt.add_argument("--max-features", type=int, default=1024,
                       help="Max vocabulary size (will be padded to power-of-two for encoding).")
    p_txt.add_argument("--shots", type=int, default=8192, help="Simulation shots.")
    p_txt.set_defaults(func=do_text)

    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
