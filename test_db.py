from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = automap_base()
engine = create_engine('postgresql:///vethaumiau')
Base.prepare(engine, reflect=True)
vets = Base.classes.vets
animals = Base.classes.animals
DBSession = sessionmaker(bind=engine)
session = DBSession()
for vet in session.query(vets).all():
    print "{} {} {}".format( 
	vet.first_name.encode('utf-8'),    
	vet.last_name.encode('utf-8'),    
	vet.login_name.encode('utf-8'))

for a in session.query(animals).all():

    sex = ''
    if a.sex is None:
       sex = 'x'
    else:
       sex = a.sex.encode('utf-8'),    
    print "id={} owner={} breed={} {} {} {} {} sex={} {}".format( 
	a.id,    
	a.owner_id,    
	a.breed_id,    
	a.name.encode('utf-8'),    
	a.birth,    
	a.death,    
	a.color.encode('utf-8'),    
	sex,
	a.note.encode('utf-8')    
	)
