from argparse import ArgumentParser
import logging
from pathlib import Path
from time import time
from typing import List

import pandas as pd


logging.basicConfig(level=logging.INFO)


class CodeSearchNetRAM(object):
    """Stores one split of CodeSearchNet data in memory

    Usage example:
        wget 'https://s3.amazonaws.com/code-search-net/CodeSearchNet/v2/java.zip'
        unzip java.zip
        python notebooks/codesearchnet-opennmt.py \
            --data_dir='java/final/jsonl/valid' \
            --newline='\\n'
    """

    def __init__(self, split_path: Path, newline_repl: str):
        super().__init__()
        self.pd = pd

        files = sorted(split_path.glob("**/*.gz"))
        logging.info(f"Total number of files: {len(files):,}")
        assert files, "could not find files under %s" % split_path

        columns_list = ["code", "func_name"]

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

    def __getitem__(self, idx: int):
        row = self.pd.iloc[idx]

        # drop class name
        fn_name = row["func_name"]
        fn_name = fn_name.split(".")[-1]  # drop the class name
        # fn_name_enc = self.enc.encode(fn_name)

        # drop fn signature
        code = row["code"]
        fn_body = code[code.find("{") + 1 : code.rfind("}")].lstrip().rstrip()
        fn_body = fn_body.replace("\n", "\\n")
        # fn_body_enc = self.enc.encode(fn_body)
        return (fn_name, fn_body)

    def __len__(self):
        return len(self.pd)


def main(args):
    dataset = CodeSearchNetRAM(Path(args.data_dir), args.newline)
    split_name = Path(args.data_dir).name
    with open(args.src_file % split_name, mode="w", encoding="utf8") as s, open(
        args.tgt_file % split_name, mode="w", encoding="utf8"
    ) as t:
        for fn_name, fn_body in dataset:
            if not fn_name or not fn_body:
                continue
            print(fn_body, file=s)
            print(fn_name if args.word_level_targets else " ".join(fn_name), file=t)


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
        "--word-level-targets",
        action="store_true",
        help="Use word level targets instead of char level ones",
    )

    parser.add_argument(
        "--src_file", type=str, default="src-%s.txt", help="File with function bodies",
    )

    parser.add_argument(
        "--tgt_file", type=str, default="tgt-%s.txt", help="File with function texts"
    )

    args = parser.parse_args()
    main(args)
