from application import app,db
from application.models import Items,ItemAttributes
from flask import render_template, redirect, url_for, request
from application.forms import ManipItem, ManipItemAttributes

# function to query items table
def queryItem(itemid):
    return Items.query.filter_by(item_id=itemid).first()

#function to query item attributes table
def queryItemAttr(itemattid):
    return ItemAttributes.query.filter_by(itemAttr_id=itemattid).first()

@app.route('/', methods = ['GET', 'POST'])
def front():
    # associate form, as this is used in the POST and also the render it needs to happen up here
    route_add_item_form = ManipItem()
    
    # logic if we've added an item
    if request.method == 'POST':
        # slurp values from the form into the db object
        add_values_from_form = Items(item_name=route_add_item_form.form_item_name.data,
                        item_value=route_add_item_form.form_item_value.data,
                        item_boolean = route_add_item_form.form_item_boolean.data
                        )
        # add and commit
        db.session.add(add_values_from_form)
        db.session.commit()
        return redirect(url_for('front'))

    # query for items
    queried_items = db.session.query(Items).all()
    # the objects we will use in the template are inherited from the objects in this route
    return render_template('index.html',
                            template_items=queried_items, 
                            template_addItem_form = route_add_item_form
                            )



@app.route('/item/<int:id>', methods = ['GET','POST'])
def item(id):
    # Add the form so it can be referenced for render and submit
    route_add_itemAttributes_form = ManipItemAttributes()

    if request.method == 'POST':
        add_values_from_form = ItemAttributes(
            itemAttr_name = route_add_itemAttributes_form.form_itemAttr_name.data,
            itemAttr_value = route_add_itemAttributes_form.form_itemAttr_value.data,
            itemAttr_boolean = route_add_itemAttributes_form.form_itemAttr_boolean.data,
            item_id_ref = id
        )
        db.session.add(add_values_from_form)
        db.session.commit()
        # return the current page as a get and pass the initially passed id
        return redirect(url_for('item',id=id))

    # use id to query for attrs and the item
    queried_item_attrs = ItemAttributes.query.filter_by(item_id_ref=id).all()
    queried_item = queryItem(id)

    # pass to jinja and render
    return render_template(
        'item.html', 
        template_item=queried_item,
        template_item_attrs=queried_item_attrs,
        template_addItemAttr_form = route_add_itemAttributes_form
        )

@app.route('/item/edititem/<int:id>', methods = ['GET','POST','DELETE'])
def edititem(id):
    # need to set up the form AND the query as they're needed in for 
    # the update in the POST and also the render
    route_edit_item_form = ManipItem()
    queried_item = queryItem(id)
    # Have we changed something?
    if request.method == 'POST':
        # Are we editing or deleting?
        if route_edit_item_form.form_item_submit_edit.data:
            # We're editing, change the values we collected from the db
            queried_item.item_name = route_edit_item_form.form_item_name.data
            queried_item.item_value = route_edit_item_form.form_item_value.data
            queried_item.item_boolean = route_edit_item_form.form_item_boolean.data
            # tell the db and go back
            db.session.commit()
            return redirect(url_for('item',id=id))
        else:
            # We're deleting.
            db.session.delete(queried_item)
            db.session.commit()
            return redirect(url_for('front'))
    # These lines will populate the editing form with the queried data
    route_edit_item_form.form_item_name.data = queried_item.item_name
    route_edit_item_form.form_item_value.data = queried_item.item_value
    route_edit_item_form.form_item_boolean.data = queried_item.item_boolean
    # Render the template!
    return render_template('edit.html',template_editItem_form = route_edit_item_form, template_pass_id = id)
    

@app.route('/item/edititemattr/<int:attid>', methods = ['GET','POST'])
def editattr(attid):
    # need to set up the form and the query as they're needed in for 
    # the update in the POST and also the render
    route_edit_item_form = ManipItem()
    queried_itemAttr = queryItemAttr(attid)
    # Are we POSTING?
    if request.method == 'POST':
        # Did we click Submit or Delete?
        if route_edit_item_form.form_item_submit_edit.data:
            queried_itemAttr.itemAttr_name = route_edit_item_form.form_item_name.data
            queried_itemAttr.itemAttr_value = route_edit_item_form.form_item_value.data
            queried_itemAttr.itemAttr_boolean = route_edit_item_form.form_item_boolean.data
            db.session.commit()
            return redirect(url_for('item',id=queried_itemAttr.item_id_ref))
        else:
            # I'm going to be deleting this attribute but I want to return to the
            # parent item, better grab that id_ref so I can pass it back to the return!
            item_id = queried_itemAttr.item_id_ref
            # delete!
            db.session.delete(queried_itemAttr)
            db.session.commit()
            return redirect(url_for('item',id=item_id))

    # These lines will populate the editing form with the queried data
    route_edit_item_form.form_item_name.data = queried_itemAttr.itemAttr_name
    route_edit_item_form.form_item_value.data = queried_itemAttr.itemAttr_value
    route_edit_item_form.form_item_boolean.data = queried_itemAttr.itemAttr_boolean
    return render_template('edit.html',template_editItem_form = route_edit_item_form, template_pass_id = queried_itemAttr.item_id_ref)