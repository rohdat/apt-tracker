import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
#from database_setup import Base, Restaurant, Menu
import datetime
Base = declarative_base()

## CODE HERE

class Apt(Base):
	__tablename__ = 'apts'
	link = Column(String(250), nullable = False)
	rent = Column(Integer)
	addr = Column(String(250))
	emailaddr = Column(String(250))
	desc = Column(String(250))
	id = Column(Integer, primary_key=True)
	tel = Column(String(10))
	posted = Column(DateTime)
	updated = Column(DateTime)

	def __repr__(self):
		return "Apartment at %s with rent $%d"%(self.addr,self.rent)
	@property
	def serialize(self):
		return {
				'id':self.id,
				'link':self.link,
				'rent': self.rent,
				'addr':self.addr,
				'desc':self.desc,
		}
## END OF FILE

engine = create_engine('sqlite:///apts.db')

Base.metadata.create_all(engine)