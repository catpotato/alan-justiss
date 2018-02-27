import glob, csv
from models import table_texts
from sqlalchemy import create_engine, MetaData
from os.path import basename, splitext
import numpy as np
from collections import defaultdict

home_path = '/Users/clark/Library/Mobile Documents/com~apple~CloudDocs/projects/soph/aj/web'
in_dir = 'raw'
word_dir = 'words'
encode_dir = 'encoded'

def add_to_db(poems):

    engine = create_engine('sqlite:///database.db', echo=True)
    connection = engine.connect()
    metadata = MetaData()

    texts = table_texts(metadata)

    ins = texts.insert()

    result = connection.execute(ins, poems)



def make_poems(in_path, out_path):

    scan_paths = glob.glob(in_path + '/*.txt')

    poems = []

    for scan_path in scan_paths:

        scan_name = scan_path.split('/')[-1][:-4]

        month = scan_name[:3]
        year = int(scan_name[-4:])


        filename = make_csv(in_path, out_path, scan_name)

        poem = {
            'month': month,
            'year': year,
            'filename': filename
        }

        poems.append(poem)

    return poems


# returns filename, saves all words in file, as csv
def make_csv(in_path, out_path, scan_name):

    in_file = in_path + '/' + scan_name + '.txt'
    out_file = out_path + '/' + scan_name + '.csv'

    words = []

    with open(in_file, 'r') as f:

        for line in f.readlines():
            # separate out words in document
            words.append(line.split())

    with open(out_file, 'w') as f:
        writer = csv.writer(f)

        concat_list = [item for sublist in words for item in sublist]

        writer.writerow(concat_list)

    return out_file


def make_csvs():

    in_path = home_path + '/' + in_dir
    out_path = home_path + '/' + word_dir

    poems = make_poems(in_path, out_path)

    add_to_db(poems)


def separarte_into_sentences(poem):

    sentences = []
    sentences_begin = 0

    for i, word in enumerate(poem):
        if word[-1] == '.':
            sentences.append(word[sentences_begin:i])
            sentences_begin = i + 1

    return sentences




def encode_csvs(encoding_dictionary):

    in_path = home_path + '/' + word_dir
    out_path = home_path + '/' + encode_dir

    word_paths = glob.glob(in_path + '/*.csv')

    # read in csvs
    scans = {}
    for word_path in word_paths:
        with open(word_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            file_as_list = []

            for row in reader:
                file_as_list = file_as_list + row

            scans[splitext(basename(word_path))[0]] = file_as_list

    encoded_scans = []

    # go through each scan
    for scan_name, words in scans.items():
        # make numpy arr with len of words
        a = np.zeros(shape=(len(encoding_dictionary), len(words)))

        # iterate each word in each scan
        for i, word in enumerate(words):
            a[encoding_dictionary[word], i] = 1

        encoded_scans.append(a)

    print(encoded_scans[0])


def decide_encodings():

    # important! enocding must be a default dict so that it has a fallback value for you

    d = {}
    d = defaultdict(lambda: 0, d)

    # read in encodings file
    with open(home_path + '/' + 'encodings.txt', 'r') as f:

        # simple assign to the number it is in the file, we can change this later
        for i, line in enumerate(f.readlines()):
            d[line.lower] = i + 1

    return d

def main():

    make_csvs()

    encodings = decide_encodings()

    encode_csvs(encodings)







if __name__ == '__main__':
    main()
