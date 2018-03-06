# alan-justiss

# structure

1. take each file, turn into csv of word `make_csvs()`, located in `/words`
2. decide on what encodings each word will get `decide_encodings()`, currently stored as one hot vectors with an alphabetical encoding
3. turn csvs into arrays of numbers `encode_csvs()`, located in `/encoded`
2. make database that separates csvs by month and year `make_into_database()`, located in `database.db`
