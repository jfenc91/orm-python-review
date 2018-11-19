from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Index

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    # back reference
    parent = relationship("Parent", back_populates="children")




from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///:memory:', echo=True)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.flush()
session.add(Parent(id = 1))
session.flush()
