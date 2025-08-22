#!/usr/bin/env python

import argparse
import csv
import fileinput
import re
import sys
from datetime import datetime


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Apache's (Combined Log Format) access.log to csv",
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=48),
    )
    required = parser.add_argument_group("required")
    optional = parser.add_argument_group("optional")
    required.add_argument(
        "-i",
        "--input",
        type=str,
        nargs="+",
        metavar="<PATH>",
        help="path to access.log file(s)",
        required=True,
    )
    required.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="<PATH>",
        help="path to output file",
        required=True,
    )
    optional.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    try:
        with (
            fileinput.input(files=args.input) as input,
            open(args.output, "w", encoding="utf-8", newline="") as output,
        ):
            # fmt: off
            pattern = re.compile(r"^(?P<Host>(?:(?:\d{1,3}\.){3}\d{1,3}|([0-9a-fA-F]{0,4}\:?){2,8}))\s(?P<Clientid>[\S]+)\s(?P<Userid>[\S]+)\s\[(?P<Timestamp>\d{2}\/[A-Za-z]{3}\/\d{4}:\d{2}\:\d{2}\:\d{2}\s[+-]\d{4})\]\s\"(?P<Method>[A-Z]{3,7})\s(?P<Resource>[\S]+)\s(?P<Protocol>HTTP\/\d(?:\.\d)?)\"\s(?P<Status>\d{3})\s(?P<Size>\-|\d+)\s\"(?P<Referer>[^\"]*)\"\s\"(?P<Useragent>[^\"]*)\"$")
            # fmt: on
            writer = csv.DictWriter(
                output,
                lineterminator="\r\n" if sys.platform == "win32" else "\n",
                fieldnames=[
                    "Host",
                    "Clientid",
                    "Userid",
                    "Timestamp",
                    "Method",
                    "Resource",
                    "Protocol",
                    "Status",
                    "Size",
                    "Referer",
                    "Useragent",
                ],
            )
            writer.writeheader()

            for line in input:
                try:
                    match = pattern.match(line).groupdict()
                except AttributeError:
                    print(
                        f"Error: malformed structure in {input.filename()} at line {input.filelineno()}",
                        file=sys.stderr,
                    )
                    continue

                if match["Size"] == "-":
                    match["Size"] = 0

                match["Timestamp"] = datetime.strptime(
                    match["Timestamp"], "%d/%b/%Y:%H:%M:%S %z"
                ).isoformat()

                writer.writerow(match)
    except (FileNotFoundError, IOError) as err:
        print(err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
