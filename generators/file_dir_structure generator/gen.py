import os
import sys
import json
import argparse
import shutil


# reading functions
def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir\
(path)]
    else:
        d['type'] = "file"
    return d
def directoryToJson(path, scheme):
    data = path_to_dict(path)
    with open("schemes/"+scheme, 'w') as f:
        json.dump(data, f)


# writing functions
def writeDirsAndFiles(scheme_data, path):
    if type(scheme_data) == type([]):
        for sub_scheme_data in scheme_data:
            writeDirsAndFiles(sub_scheme_data, path)
    else:
        if scheme_data["type"] == "directory":
            path = os.path.join(path, scheme_data["name"])
            if path != "./":
                os.mkdir(path)
                if scheme_data["children"]:
                    writeDirsAndFiles(scheme_data["children"], path)
        else:
            os.close(os.open(path+"/"+scheme_data["name"], os.O_CREAT))

def setFileContents(scheme_data, path):
    if "file_contents" in scheme_data:
        data = scheme_data["file_contents"]
        for entry in data:
            shutil.copyfile(entry["save_location"],os.path.join(path, entry["scheme_path"]))


# Handling CLI
def exitWithError(text):
    print("Something went wrong!")
    print(text)
    print("exiting, see --help for more info")
    sys.exit()

parser = argparse.ArgumentParser(
    description='''
        directory/file structure generator

        example usage (path can be relative or absolute):

        READING:
        python generator.py --operation read --scheme test --path /path/you/want/to/make/scheme/of

        WRITING:
        python generator.py --operation write --scheme test --path /path/where/you/want/to/create/directory/
    ''',
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('-o','--operation', help="Operation an be read or R (reads given directory and converts it to JSON scheme) or write or W (creates directory/file structure in given path based on given scheme name)")
parser.add_argument('-p','--path', help="Path to directory you want to read, or to directory you want to write to. If this argument is empty, script will refer to directory in which this script was called at.")
parser.add_argument('-s','--scheme', help="Scheme name which will be used (when --operation write) or created (when when --operation read). Scheme name refers to file living in schemes/ directory.")
parser.add_argument('-i','--ignore', help="Ignores if given scheme already exist. Use this option carefully, not to overwrite something important. Values can be yes or no, and it's no by default", choices=['yes', 'no'], default='no')

args = parser.parse_args()

operation = args.operation
path = args.path
scheme = args.scheme
ignore = args.ignore

if not operation:
    exitWithError("--operation is required!")
if not scheme:
    exitWithError("--scheme is required!")
else:
    scheme+=".json"

if operation == "read" or operation == "R":
    if ignore and ignore == "yes":
        directoryToJson(path, scheme)
    else:
        schemes = os.listdir("schemes/")
        if scheme in schemes:
            exitWithError("Scheme with that name already exist! Delete/rename existing scheme, or use --ignore yes to overwrite")
        else:
            directoryToJson(path, scheme)

elif operation == "write" or operation == "W":
    scheme_data = json.load(open('schemes/'+scheme))
    schemes = os.listdir(path)
    if scheme_data['name'] in schemes:
        exitWithError("That directory already exist in given path! Delete/rename existing directory, or use --ignore yes to overwrite")
    else:
        writeDirsAndFiles(scheme_data, path)
        setFileContents(scheme_data, path)

else:
    wrongParamsError('--operation provided, but with unknown parameter. Known parameters are: "read", "R", "write", "W" ')

