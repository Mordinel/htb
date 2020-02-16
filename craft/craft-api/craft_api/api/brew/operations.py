from craft_api.database.models import Brew
from craft_api.database import db

def create_brew(data):
    name = data.get('name')
    brewer = data.get('brewer')
    style = data.get('style')
    abv = data.get('abv')
    brew = Brew(brewer, name, style, abv)
    db.session.add(brew)
    db.session.commit()


def update_brew(brew_id, data):
    brew = Brew.query.filter(Brew.id == brew_id).one()
    brew.name = data.get('name')
    brew.brewer = data.get('brewer')
    brew.style = data.get('style')
    brew.abv = data.get('abv')
    db.session.add(brew)
    db.session.commit()


def delete_brew(brew_id):
    brew = Brew.query.filter(Brew.id == brew_id).one()
    db.session.delete(brew)
    db.session.commit()
