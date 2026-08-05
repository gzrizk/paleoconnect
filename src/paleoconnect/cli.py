from __future__ import annotations

import argparse
from pathlib import Path

from .model import ConnectivityModel


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="paleoconnect",
        description="Palaeogeographic connectivity analysis",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run a connectivity analysis")
    run_parser.add_argument(
        "--rotations",
        required=True,
        nargs="+",
        type=Path,
        help="Rotation file(s) (.rot)",
    )
    run_parser.add_argument(
        "--topologies",
        required=True,
        nargs="+",
        type=Path,
        help="Topology file(s) (.gpml)",
    )
    run_parser.add_argument(
        "--proxies",
        required=True,
        nargs="+",
        type=int,
        help="Plate IDs representing each landmass in path order",
    )
    run_parser.add_argument(
        "--names",
        required=True,
        nargs="+",
        type=str,
        help="Landmass names in the same order as --proxies",
    )
    run_parser.add_argument(
        "--from",
        dest="start_time",
        required=True,
        type=float,
        help="Start time in Ma (older)",
    )
    run_parser.add_argument(
        "--to",
        dest="end_time",
        required=True,
        type=float,
        help="End time in Ma (younger)",
    )
    run_parser.add_argument(
        "--step",
        type=float,
        default=1.0,
        help="Time step in Myr (default: 1.0)",
    )
    run_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("connectivity.csv"),
        help="Output CSV path (default: connectivity.csv)",
    )

    args = parser.parse_args(argv)

    if args.command == "run":
        if len(args.proxies) != len(args.names):
            parser.error(
                f"--proxies ({len(args.proxies)}) and --names ({len(args.names)}) "
                "must have the same length"
            )
        model = ConnectivityModel(
            rotation_files=args.rotations,
            topology_files=args.topologies,
        )
        result = model.run_path(
            proxies=args.proxies,
            names=args.names,
            start_time=args.start_time,
            end_time=args.end_time,
            time_step=args.step,
        )
        result.to_csv(args.output)
        print(f"Results written to {args.output} ({len(result)} records)")


if __name__ == "__main__":
    main()
