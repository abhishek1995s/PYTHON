
from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker
from temp import Base, Restaurant,MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession =sessionmaker (bind=engine)
session=DBsession()
app=Flask(__name__)
@app.route('/')
@app.route('/hello')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def resjason(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in menu])
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def comjason(restaurant_id,menu_id):
    menuitem=session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuitem.serialize)
@app.route('/restaurants/<int:restaurant_id>/')
def helloworld(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html',restaurant=restaurant,items=menu)
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        menuitem=MenuItem(name= request.form['name'],restaurant_id=restaurant_id)
        session.add(menuitem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('helloworld',restaurant_id=restaurant_id))
    else:
        return render_template('newmenu.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    edititem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method =='POST':
        edititem.name=request.form['name']
        session.add(edititem)
        session.commit()
        return  redirect(url_for('helloworld',restaurant_id=restaurant_id))
    else:
        return render_template('editmenu.html',restaurant_id=restaurant_id,menu_id=menu_id,i=edititem)




# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"
if __name__=='__main__':
    app.secret_key='super_secret_key'
    app.debug=True
    app.run(host='0.0.0.0',port=5000)