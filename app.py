from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime as dt
import csv


engine = create_engine('sqlite:///inventory.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(DateTime)

    def __repr__(self):
        attributes = '' + \
            f'product_name={self.product_name}, ' + \
            f'product_quantity={self.product_quantity}, ' + \
            f'product_price={self.product_price}, ' + \
            f'date_updated={self.date_updated}'
        return f'<Product({attributes})>'


def load_csv(file):
    if session.query(Product).count() == 0:
        products = []
        with open(file) as f:
            reader = csv.DictReader(f)
            for line in reader:
                product_params = clean_data(line)
                products.append(Product(**product_params))
        session.add_all(products)
        session.commit()
        print('Database initialized from inventory.csv')


def clean_data(params):
    params['product_name'] = clean_name(params['product_name'])
    params['product_price'] = int(float(params['product_price'][1:])*100)
    params['product_quantity'] = int(params['product_quantity'])
    params['date_updated'] = clean_date(params['date_updated'])
    return params


def clean_name(name_params):
    character_set = set(name_params)
    if '"' in character_set:
        name_params = name_params.replace('"', '')
    if ',' in character_set:
        name_params = name_params.replace(',', ', ')
    return name_params


def clean_date(date_params):
    month, day, year = map(lambda x: int(x), date_params.split('/'))
    return dt.date(year=year,  month=month, day=day)




if __name__ == '__main__':
    Base.metadata.create_all(engine)

    load_csv('inventory.csv')