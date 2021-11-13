#!/usr/bin/python3

import argparse
import subprocess
import os


def main():
    DEFAULT_RESOLUTION = 150
    # if we can't run directly on the path then we shouldn't do this at all.
    # PDF_TO_PPM_PATH = os.path.abspath("/usr/bin/pdftoppm")

    set_resolution = DEFAULT_RESOLUTION

    parser = argparse.ArgumentParser(
        description="convert a pdf into a new folder contianing a series of pngs. Can specify optional dpi (resolution), otherwise set at 150")
    parser.add_argument("inputFile", type=str, help="path to a pdf file")
    parser.add_argument("outputFileName", type=str,
                        help="prefix name of png files to generate as well as generated folder name")
    parser.add_argument("-r", "--resolution", default=150,
                        help="the dpi that the page is rendered at, default=150")

    args = parser.parse_args()

    set_resolution = args.resolution

    if os.path.exists(args.inputFile) and os.path.splitext(args.inputFile)[1] == '.pdf':
        path_to_infile = os.path.abspath(args.inputFile)
    else:
        parser.error("couldn't parse infile")
        exit()

    if os.path.exists(args.outputFileName):
        path_to_outdirectory = os.path.abspath(args.outputFileName)
    else:
        os.makedirs(args.outputFileName)
        path_to_outdirectory = os.path.abspath(args.outputFileName)

    # New and improved, make the new directory our working directory and then
    # pop out once we're done
    os.chdir(path_to_outdirectory)

    # build up the dang run statement
    try:
        runArgs = ['pdftoppm', '-png', '-r',
                   str(set_resolution), path_to_infile, args.outputFileName]
        subprocess.run(runArgs)
    except OSError as e:
        print("execution failed:", e)
    except subprocess.CalledProcessError as e:
        print(e.output)
        print("exiting process with error...")
        exit()

    # back to our old directory
    os.chdir('..')


if __name__ == "__main__":
    main()
