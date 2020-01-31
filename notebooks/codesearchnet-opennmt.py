"""
CLI tool for converting CodeSearchNet dataset to OpenNMT format for
function name suggestion task.

Usage example:
    wget 'https://s3.amazonaws.com/code-search-net/CodeSearchNet/v2/java.zip'
    unzip java.zip
    python notebooks/codesearchnet-opennmt.py \
        --data_dir='java/final/jsonl/valid' \
        --newline='\\n'
"""
from argparse import ArgumentParser, Namespace
import logging
from pathlib import Path
from time import time
from typing import List, Tuple

import pandas as pd


logging.basicConfig(level=logging.INFO)


class CodeSearchNetRAM(object):
    """Stores one split of CodeSearchNet data in memory"""

    def __init__(self, split_path: Path, newline_repl: str):
        super().__init__()
        self.pd = pd
        self.newline_repl = newline_repl

        files = sorted(split_path.glob("**/*.gz"))
        logging.info(f"Total number of files: {len(files):,}")
        assert files, "could not find files under %s" % split_path

        columns_list = ["code", "func_name", "code_tokens"]

        start = time()
        self.pd = self._jsonl_list_to_dataframe(files, columns_list)
        logging.info(f"Loading took {time() - start:.2f}s for {len(self)} rows")

    @staticmethod
    def _jsonl_list_to_dataframe(
        file_list: List[Path], columns: List[str]
    ) -> pd.DataFrame:
        """Load a list of jsonl.gz files into a pandas DataFrame."""
        return pd.concat(
            [
                pd.read_json(f, orient="records", compression="gzip", lines=True)[
                    columns
                ]
                for f in file_list
            ],
            sort=False,
        )

    def __getitem__(self, idx: int) -> Tuple[str, str]:
        row = self.pd.iloc[idx]

        # drop class name
        fn_name = row["func_name"]
        fn_name = fn_name.split(".")[-1]  # drop the class name
        # fn_name_enc = self.enc.encode(fn_name)

        # drop fn signature
        code = row["code"]
        fn_body = (
            code[
                code.find("{", code.find(fn_name) + len(fn_name)) + 1 : code.rfind("}")
            ]
            .lstrip()
            .rstrip()
        )
        fn_body = fn_body.replace("\n", self.newline_repl)
        # fn_body_enc = self.enc.encode(fn_body)

        tokens = row["code_tokens"]
        body_tokens = tokens[tokens.index(fn_name) + 2 :]
        fn_body_tokens = body_tokens[body_tokens.index("{") + 1 : len(body_tokens) - 1]

        return (fn_name, fn_body, fn_body_tokens)

    def __len__(self) -> int:
        return len(self.pd)


def main(args: Namespace) -> None:
    dataset = CodeSearchNetRAM(Path(args.data_dir), args.newline)
    split_name = Path(args.data_dir).name
    with open(args.src_file % split_name, mode="w", encoding="utf8") as s, open(
        args.tgt_file % split_name, mode="w", encoding="utf8"
    ) as t:
        for fn_name, fn_body, fn_body_tokens in dataset:
            if not fn_name or not fn_body:
                continue
            src = " ".join(fn_body_tokens) if args.token_level_sources else fn_body
            tgt = fn_name if args.word_level_targets else " ".join(fn_name)
            if args.print:
                print(f"'{tgt[:40]:40}' - '{src[:40]:40}'")
            else:
                print(src, file=s)
                print(tgt, file=t)


if __name__ == "__main__":
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--data_dir",
        type=str,
        default="java/final/jsonl/test",
        help="Path to the unziped input data (CodeSearchNet)",
    )

    parser.add_argument(
        "--newline", type=str, default="\\n", help="Replace newline with this"
    )

    parser.add_argument(
        "--token-level-sources",
        action="store_true",
        help="Use language-specific token sources instead of word level ones",
    )

    parser.add_argument(
        "--word-level-targets",
        action="store_true",
        help="Use word level targets instead of char level ones",
    )

    parser.add_argument(
        "--src_file",
        type=str,
        default="src-%s.token",
        help="File with function bodies",
    )

    parser.add_argument(
        "--tgt_file", type=str, default="tgt-%s.token", help="File with function texts"
    )

    parser.add_argument(
        "--print", action="store_true", help="Print data preview to the STDOUT"
    )

    args = parser.parse_args()
    main(args)
