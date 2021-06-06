from database.db import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


def find(filter=None):
    categories = Category.query.filter_by(**filter)

    return [c.serialize for c in categories]


def insert(category):

    insertedCategory = Category(**category)
    db.session.add(insertedCategory)
    db.session.commit()

    return insertedCategory.serialize


def update(id, category):
    Category.query.filter_by(id=id).update(category)

    db.session.commit()

    return find({"id": id})[0]


def delete(id):
    Category.query.filter_by(id=id).delete()

    db.session.commit()
