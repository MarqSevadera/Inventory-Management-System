from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return 'Product  ' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products', methods=['GET'])
def products():
    query = request.args.get('query')
    if query is None: 
        products = Product.query.order_by(Product.date_created).all()
    else:
        query = "%{}%".format(query)
        products = Product.query.filter(Product.name.like(query)).order_by(Product.date_created).all()
    return render_template("products.html",products=products)



@app.route('/products/add',methods=['GET','POST'])
def addProduct():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity'].replace(',','')
        price = request.form['price'].replace(',', '')
        desc = request.form['description']
        new_prod = Product(name=name, quantity=quantity,price=price, description=desc)
        db.session.add(new_prod)
        db.session.commit()
        return redirect('/products')
    else:
        return render_template('add.html')



@app.route('/products/<int:id>', methods=['GET','POST'])
def editProduct(id):
    old_prod = Product.query.get_or_404(id)
    if request.method == 'POST':
        old_prod.name = request.form['name']
        old_prod.quantity = request.form['quantity']
        old_prod.price = request.form['price']
        old_prod.description = request.form['description']
        db.session.commit()
        return redirect('/products')
    else:
        return render_template('edit.html',product=old_prod)



@app.route('/products/delete/<int:id>')
def deleteProduct(id):
    prod = Product.query.get_or_404(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect('/products')


@app.errorhandler(404)
def handle_bad_request(e):
    return render_template('404.html')
    



if (__name__ == "__main__"):
    app.run(debug=True)
