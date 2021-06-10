from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime as dt
import csv


engine = create_engine('sqlite:///inventory.db', echo=False)
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
            f'product_name="{self.product_name}", ' + \
            f'product_quantity={self.product_quantity}, ' + \
            f'product_price={self.product_price}, ' + \
            f'date_updated="{self.date_updated}"'
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
    else:
        print('Database already initialized!')


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


def show_menu():
    prompt = '' + \
        '[V]iew a single product\'s inventory\n' + \
        '[A]dd a new product to the database\n' + \
        '[B]ackup the entire inventory\n' + \
        '[Q]uit the program\n'
    print(prompt)


def handle_user_input(option):
    menu_option = {
        'Q': quit_program,
        'V': view_product,
        'A': add_product,
        'B': backup_inventory
        }
    try:
        menu_option[option.upper()]()
    except KeyError:
        handle_invalid_input()


def handle_invalid_input():
    print('Invalid menu option\n')
    show_menu()


def quit_program():
    print('Goodbye!')
    quit()


def view_product():
    upper_limit = session.query(Product).count()
    product_id = input(f'Select a [Product ID] between 1 and {upper_limit}: ')
    if int(product_id) not in set(range(1,(upper_limit+1))):
        handle_invalid_input()
    else:
        product = session.query(Product).filter_by(product_id=int(product_id)).one()
        print(f'\n{product}\n')
        show_menu()



def add_product():
    pass


def backup_inventory():
    pass




if __name__ == '__main__':
    Base.metadata.create_all(engine)

    load_csv('inventory.csv')

    print('Welcome to the Product Inventory Database!\n')
    show_menu()

    while True:
        menu_option = input('Select an [OPTION]: ')
        handle_user_input(menu_option)