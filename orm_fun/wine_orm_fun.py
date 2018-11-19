import sqlalchemy
from sqlalchemy import create_engine, Index
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric

engine = create_engine('sqlite:///:memory:', echo=True)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#,country,
# description,designation,points,price,province,region_1,region_2,taster_name,
# taster_twitter_handle,title,variety,winery


class Taster(Base):
    __tablename__ = 'taster'
    name = Column(String, primary_key=True)
    twitter_handle = Column(String)

    def __str__(self):
        return '<Taster(name={}, twitter_handle={})>'.format(self.name, self.twitter_handle)


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    points = Column(Integer)
    taster_name = Column(String, ForeignKey('taster.name'))
    wine = Column(String, ForeignKey('wine.title'))

    def __str__(self):
        return '<Taster(wine={}, points={}, taster={}, description={})>'.format(self.wine, self.points, self.taster_name, self.description)

class Wine(Base):
    __tablename__ = 'wine'
    title = Column(String, primary_key=True)
    variety = Column(String)
    winery = Column(String)
    designation = Column(String)
    price = Column(Numeric)
    province = Column(String)
    region_1 = Column(String)
    region_2 = Column(String)


Base.metadata.create_all(engine)




from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


import json
with open("../wine-reviews/winemag-data-130k-v2.json") as f:
    data = json.loads(f.read())

i = 0
for entry in data:
    i += 1
    try:
        session.add(Wine(title = entry['title'],
             variety = entry['variety'],
             winery = entry['winery'],
             designation = entry['designation'],
             price = entry['price'],
             province = entry['province'],
             region_1 = entry['region_1'],
             region_2 = entry['region_2']))
        session.flush()
    except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.InvalidRequestError as e:
        print("Added dup wine", e)
        session.rollback()
    try:
        session.add(Taster(name = entry['taster_name'], twitter_handle = entry['taster_twitter_handle']))
        session.flush()
    except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.InvalidRequestError as e:
        print("Added dup taster {}", e)
        session.rollback()
    session.add(Review(id = i,
                       description = entry['description'],
                       points = entry['points'],
                       taster_name = entry['taster_name'],
                       wine = entry['title']))
    session.flush()




my_tasting = Taster(name="Jeff Fenchel", twitter_handle="@jfenc91")
session.add(my_tasting)
# session.commit()


found_taster = session.query(Taster).filter_by(name="Jeff Fenchel").first()
print('Found taster {}'.format(str(found_taster)))

found_taster = session.query(Review).all()
print('Found taster {}'.format(str([str(i) for i in found_taster])))
