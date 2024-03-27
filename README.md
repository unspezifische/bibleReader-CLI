# bibleReader-CLI
A Python-based tool for reading the Bible from the CLI

The `read.py` script accepts up to 3 arguemtns: first is the 3 letter abbreviation for the desired book, second is the chapter number, and third is what version to use. The versions should be stored in a `Versions` directory at the root of the project, with versions stored in sub-directories. The script will try to match the requested version to one of those sub-directories, so use consistent naming conventions. Saving the USX files to a sub-directory called `King James Version` but requesting a passage in `KJV` won't work.

Dependencies:
This script requires the `rich` library in order to provide nicer formatting in the Command Line environment.

Future Features:
Eventually I'd like to adjust the script so that it can also print out an entire book of the Bible if there is no specified chapter from the user.
