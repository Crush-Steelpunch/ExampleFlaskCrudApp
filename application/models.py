from application import db

# SQLAlchemy Docs
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html

class Items(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(30), nullable=False)
    item_value = db.Column(db.Float(), nullable=True)
    item_boolean = db.Column(db.Boolean(), nullable = True)
    itemattr = db.relationship('ItemAttributes', backref='itemAttr_backref')


class ItemAttributes(db.Model):
    __tablename__ = "itemattributes"
    itemAttr_id = db.Column(db.Integer, primary_key=True)
    itemAttr_name = db.Column(db.String(30), nullable=False)
    itemAttr_value = db.Column(db.Float(), nullable=True)
    itemAttr_boolean = db.Column(db.Boolean(), nullable = True)
    item_id_ref = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
