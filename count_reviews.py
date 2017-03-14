from glob import glob
import json

if __name__ == '__main__':
    json_filenames = glob('comments/*.json')
    c = 0
    for json_filename in json_filenames:
        with open(json_filename, 'r') as r:
            c += len(json.load(r))
    print(c)