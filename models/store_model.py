from typing import Dict, List, Union

from db import db
from models.item_model import ItemJSON

# Type hinting
StoreJSON = Dict[str, Union[str, int, List[ItemJSON]]]


class StoreModel(db.Model):
	__tablename__ = 'stores'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)

	items = db.relationship('ItemModel', lazy='dynamic')

	def __init__(self, name: str):
		self.name = name

	def json(self) -> Dict:
		return {
			'id': self.id,
			'name': self.name,
			'items': [x.json() for x in self.items]
		}

	@classmethod
	def find_by_name(cls, name: str) -> "StoreModel":
		return cls.query.filter_by(name=name).first()

	@classmethod
	def find_all(cls) -> List["StoreModel"]:
		return cls.query.all()

	def save_to_db(self) -> None:
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self) -> None:
		db.session.delete(self)
		db.session.commit()
