#!/usr/bin/env python3

'''
This script will apply patches from bromite to a chromium/src checkout
It wll also configure the output directory with the specified args
'''

import os
import argparse
import subprocess
import shutil

CURRENT_FOLDER = os.path.dirname(__file__)
DEFAULT_BROMITE = os.path.join(CURRENT_FOLDER, '../bromite')
DEFAULT_CHROMIUM = os.path.join(CURRENT_FOLDER, '../chromium/src')

# Parse args
parser = argparse.ArgumentParser(
    description='Configure chromium directory with bromite checkout and patches'
)
parser.add_argument(
    '--bromite',
    default=DEFAULT_BROMITE,
    help="The checkout of bromite to use for patches"
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
bromite = args.bromite
build_name = args.build_name

build_path = "out/" + build_name

bromite_build_folder = os.path.join(bromite, 'build')
# Checkout version from RELEASE (or RELEASE_COMMIT?), with `--hard`
release_file_name = os.path.join(bromite_build_folder, 'RELEASE')

with open(release_file_name, 'r', encoding='utf8') as release_file:
    checkout_value = release_file.read()
    to_exec = "git checkout --hard " + checkout_value
    subprocess.run(to_exec, cwd=chromium, shell=True, check=True)

# Copy build/bromite.gn_args to out/Default/args.gn (configurable?) (check if exists?)
source_gn_args = os.path.join(bromite_build_folder, 'bromite.gn_args')
destination_gn_args = os.path.join(chromium, build_path, 'args.gn')
shutil.copyfile(source_gn_args, destination_gn_args)
# Clean the build folder
subprocess.run(f'gn clean {build_path}', cwd=args.chromium, shell=True, check=True)
# Apply gclient sync
subprocess.run('gclient sync -D', cwd=args.chromium, shell=True, check=True)
# Get `bromite/build/bromite_patches_list.txt` and read each line
patch_list_file_name = os.path.join(bromite_build_folder, 'bromite_patches_list.txt')
with open(patch_list_file_name, 'r', encoding='utf8') as patch_list:
    for patch_name in patch_list:
        patch_path = os.path.join(bromite_build_folder, 'patches', patch_name.strip())
        # Use `git am` to apply patches one by one from `bromite/build/patches/`
        subprocess.run(f"git am {patch_path}", cwd=chromium, shell=True, check=True)

print("Done!")
