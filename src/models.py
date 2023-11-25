from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database

url = URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='banco',
    host='postgres',
    database='bestfriend',
    port=5432
)

if not database_exists(url):
    create_database(url)

engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'user'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    email       = Column(String)
    password    = Column(String)
    


class Pets(Base):
    __tablename__= 'pets'
    
    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey('user.id'))
    name        = Column(String)
    years_old   = Column(String)
    weight      = Column(String)
    user        = relationship(User)


class Exams(Base):
    __tablename__ = 'exams'
    id        = Column(Integer, primary_key=True, autoincrement=True)
    pet_id    = Column(Integer, ForeignKey('pets.id'))
    place     = Column(String)
    name_exam = Column(String)
    date      = Column(String)
    pets      = relationship(Pets)


class MedicineVaccine(Base):
    __tablename__ = 'medicinevaccine'
    id      = Column(Integer, primary_key=True, autoincrement=True)
    pet_id  = Column(Integer, ForeignKey('pets.id'))
    type_of = Column(String)
    name    = Column(String)
    date    = Column(String)
    pets    = relationship(Pets)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)