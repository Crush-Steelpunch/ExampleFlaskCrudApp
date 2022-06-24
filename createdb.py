from application import db
from application.models import Items, ItemAttributes
import pdb

db.drop_all()
db.create_all()
for i in [{'name': 'Item1','value':10,'bool':True},{'name': 'Item2','value':5,'bool':True},{'name': 'Item3','value':15,'bool':False}]:
    item = Items(item_name=i['name'],item_value=i['value'],item_boolean=i['bool'])
    db.session.add(item)

for idnum in range(1,4):
    for i in [{'name': 'ItemAttr1','value':10,'bool':True},{'name': 'ItemAttr2','value':5,'bool':True },{'name': 'ItemAttr3','value':15,'bool':False}]:
        item = ItemAttributes(itemAttr_name=i['name'],itemAttr_value=i['value'],itemAttr_boolean=i['bool'], item_id_ref=idnum)
        db.session.add(item)

db.session.commit()
# query using backref
# select on the many and join the one

for row in db.session.query(ItemAttributes).join(Items).all():
    print(row.itemAttr_backref.item_id, 
        row.itemAttr_backref.item_name, 
        row.itemAttr_backref.item_value, 
        row.itemAttr_backref.item_boolean, 
        row.itemAttr_id, 
        row.itemAttr_name, 
        row.itemAttr_value,
        row.itemAttr_boolean
    )

# query using db.relationship()
# select on the one and loop over relationship for the many

for row in db.session.query(Items).join(ItemAttributes).all():
    for attritem in row.itemattr:
        print(row.item_id,
            row.item_name,
            row.item_value,
            row.item_boolean,
            attritem.itemAttr_id,
            attritem.itemAttr_name,
            attritem.itemAttr_value,
            attritem.itemAttr_boolean
        )