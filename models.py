from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, DateTime

def table_texts(metadata):

    texts =  Table('texts', metadata,
        Column('id', Integer(), primary_key=True),
        Column('year', Integer()),
        Column('month', Integer()),
        Column('filename', String(511)),
    )

    return texts

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///database.db', echo=True)
    metadata = MetaData()

    table_texts(metadata)

    metadata.create_all(engine)
