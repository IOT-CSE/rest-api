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


def insertCategory(category):

    insertedCategory = Category(**category)
    db.session.add(insertedCategory)
    db.session.commit()

    return insertedCategory.serialize
