from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(User.id))
    owner = relationship(
        User, backref=backref('shopping_carts', uselist=True)
    )
    products = relationship(
        'Product',
        secondary='shopping_cart_product_link'
    )
    def __repr__(self):
        return '( {0}:{1.owner.name}:{1.products!r} )'.format(ShoppingCart, self)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Using a Float is not the right way of modeling a currency value.
    # We will investigate that topic in a different article.
    price = Column(Float)
    shopping_carts = relationship(
        'ShoppingCart',
        secondary='shopping_cart_product_link'
    )
    def __repr__(self):
        return '( {0}:{1.id}:{1.name!r}:{1.price!r} )'.format(Product, self)


class ShoppingCartProductLink(Base):
    __tablename__ = 'shopping_cart_product_link'
    shopping_cart_id = Column(Integer, ForeignKey('shopping_cart.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)


from sqlalchemy import create_engine
engine = create_engine('sqlite:///', echo=True)

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.configure(bind=engine)
Base.metadata.create_all(engine)

session = DBSession()
cpu = Product(name='CPU', price=300.00)
motherboard = Product(name='Motherboard', price=150.00)
coffee_machine = Product(name='Coffee Machine', price=30.00)
john = User(name='John')
session.add(cpu)
session.add(motherboard)
session.add(coffee_machine)
session.add(john)
session.commit()

# cpu = session.query(Product).filter(Product.name == 'CPU').one()
# print(cpu)


session = DBSession()
cpu = session.query(Product).filter(Product.name == 'CPU').one()
motherboard = session.query(Product).filter(Product.name == 'Motherboard').one()
coffee_machine = session.query(Product).filter(Product.name == 'Coffee Machine').one()
john = session.query(User).filter(User.name == 'John').one()
john_shopping_cart_computer = ShoppingCart(owner=john)
john_shopping_cart_kitchen = ShoppingCart(owner=john)
john_shopping_cart_computer.products.append(cpu)
john_shopping_cart_computer.products.append(motherboard)
john_shopping_cart_kitchen.products.append(coffee_machine)
session.add(john_shopping_cart_computer)
session.add(john_shopping_cart_kitchen)
session.commit()


from sqlalchemy import select
product_higher_than_one_hundred = select([Product.id]).where(Product.price > 100.00)
# ret = session.query(Product).filter(Product.id.in_(product_higher_than_one_hundred)).all()
# print(ret)

shopping_carts_with_products_higher_than_one_hundred = select([ShoppingCart.id]).where(
    ShoppingCart.products.any(Product.id.in_(product_higher_than_one_hundred)))
ret = session.query(ShoppingCart).filter(ShoppingCart.id.in_(shopping_carts_with_products_higher_than_one_hundred)).one()

print(ret)