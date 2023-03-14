from lib.tui import display_live_events
import argparse
import sys, os

def main(args):
    display_live_events(tour=args.tour, level=args.level)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Say hello')
    parser.add_argument(
        '-t',
        '--tour',
        type=str,
        required=False,
        choices=['wta', 'atp']
    )
    parser.add_argument(
        '-l',
        '--level',
        type=str,
        required=False,
        choices=['gs', '1000', '500', '250', 'ch']
    )
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)