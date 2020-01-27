if __name__ == "__main__":
    from argparse import ArgumentParser

    from tree_sitter import Language

    parser = ArgumentParser("Buid .so for tree-sitter")
    parser.add_argument(
        "--languages",
        required=True,
        nargs="+",
        help="Path to the git repositories of the languages to build.",
    )
    parser.add_argument(
        "--output", required=True, help="Path of the output .so to produce.",
    )

    args = parser.parse_args()

    Language.build_library(args.output, args.languages)
