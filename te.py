from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker
from temp import Base, Restaurant,MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession =sessionmaker (bind=engine)
session=DBsession()
m=Restaurant(name="asdf")
session.add(m)
session.commit()
mr=MenuItem(name="asdfa",description="asdfas",price="asdf",course="asdf",restaurant=m)
session.add(mr)
session.commit()
#firstresult=session.query(Restaurant).first()
#print(firstresult.id)
items=session.query(MenuItem).all()
for item in items:
    print(item.name)