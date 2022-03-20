#!/usr/bin/env python3

'''
This script will trigger a new build of the browser
'''

import os
import argparse
import subprocess

CURRENT_FOLDER = os.path.dirname(__file__)
DEFAULT_BROMITE = os.path.join(CURRENT_FOLDER, '../bromite')
DEFAULT_CHROMIUM = os.path.join(CURRENT_FOLDER, '../chromium/src')

# Parse args
parser = argparse.ArgumentParser(
    description='Build the browser'
)
parser.add_argument(
    '--chromium',
    default=DEFAULT_CHROMIUM,
    help="The chromium/src folder to apply patches to"
)
parser.add_argument(
    '--build_name',
    default="Default",
    help="The name within the chromium/src/out folder to use for the build"
)

args = parser.parse_args()

chromium = args.chromium
build_name = args.build_name

build_path = "out/" + build_name

print(f"Building {build_name}")
to_run = f'autoninja -C {build_path} chrome_public_apk'
subprocess.run(to_run, cwd=args.chromium, shell=True, check=True)

print("Done!")
