from app import db
db.Model.metadata.reflect(db.engine)

class Vets(db.Model):
    __table__ = db.Model.metadata.tables['vets']

    def __repr__(self):
        return '<Vet {}>'.format(self.last_name.encode('utf-8'))

class Users(db.Model):
    __table__ = db.Model.metadata.tables['users']

    def __repr__(self):
        user = self.user_name.encode('utf-8')
        role = self.role.encode('utf-8')
        return '<User {}({})>'.format(user, role)

class Breeds(db.Model):
    __table__ = db.Model.metadata.tables['breeds']

    def __repr__(self):
        breed = self.name.encode('utf-8')
        breed_id = self.id
        species_id = self.species_id
        return '<Breed({}) {}({})>'.format(species_id, breed, breed_id)

class Species(db.Model):
    __table__ = db.Model.metadata.tables['species']

    def __repr__(self):
	species = self.name.encode('utf-8')
	species_id = self.id
	return '<Species({}) {}>'.format(species_id, species)


class Animals(db.Model):
    __table__ = db.Model.metadata.tables['animals']

    @classmethod
    def get_animal_by_id(self, animal):
        return Animals.query.filter_by(id=animal)\
                            .join(Breeds, Species, Owners)\
                            .add_entity(Breeds)\
                            .add_entity(Species)\
                            .add_entity(Owners)\
                            .order_by(Animals.id)\
                            .first_or_404()

    def __repr__(self):
        animal_id = self.id
        breed_id = self.breed_id
        return '<Animal({}) {}({})>'.format(breed_id, self.name.encode('utf-8'), animal_id)
    

class Owners(db.Model):
    __table__ = db.Model.metadata.tables['owners']

    @classmethod
    def get_owner_by_id(self, owner):
        return Owners.query.filter_by(id=owner)\
                            .order_by(Owners.id)\
                            .first_or_404()

    def __repr__(self):
        owner_id = self.id
        first_name = self.first_name
        last_name = self.last_name
        return '<Owner({}) {} {}>'.format(owner_id, first_name.encode('utf-8'), last_name.encode('utf-8'))
    
class Visits(db.Model):
    __table__ = db.Model.metadata.tables['visits']

    def __repr__(self):
        return '<Visit({}) {} ({})>'.format(
            self.id,
            self.date,
            self.animal_id
        )

    @classmethod
    def get_visits_by_animal(self, animal):
        return Visits.query.filter_by(animal_id=animal)\
                           .join(Vets)\
                           .add_entity(Vets)\
                           .order_by(Visits.date)\
                           .all()


def get_all_animals():
        return Animals.query.join(Breeds, Species, Owners)\
                            .add_entity(Breeds)\
                            .add_entity(Species)\
                            .add_entity(Owners)\
                            .order_by(Animals.name)

def get_all_breeds():
        return Breeds.query.join(Species)\
                           .add_entity(Species)\
                           .order_by(Species.name, Breeds.name)

def get_all_species():
        return Species.query.order_by(Species.name)

def get_all_owners():
        return Owners.query.order_by(Owners.last_name, Owners.first_name)

def get_all_vets():
        return Vets.query.order_by(Vets.last_name, Vets.first_name)

def get_all_users():
        return Users.query.order_by(Users.user_name)
