from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt


engine = create_engine('sqlite:///inventory.db', echo=True)
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(DateTime)

    def __repr__(self):
        attributes = f'product_name={self.product_name}, '
        attributes += f'product_quantity={self.product_quantity}, '
        attributes += f'product_price={self.product_price}, '
        attributes += f'date_updated={self.date_updated}'
        return f'<Product({attributes})>'




if __name__ == '__main__':
    Base.metadata.create_all(engine)

    # load_csv('inventory.csv')