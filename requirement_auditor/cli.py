"""Console script for requirement_auditor."""
import argparse
import sys

from pkg_resources import Requirement


def main():
    """Console script for requirement_auditor."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "requirement_auditor.cli.main")
    r = Requirement.parse('Django==3.2.8')
    print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
