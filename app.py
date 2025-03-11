from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description_text = db.Column(db.Text, nullable=True)
    image_scr = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template("index.html", items=items)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        description_text = request.form['description_text']
        image_scr = request.form['image_scr']
        item = Item(title=title, price=price, description_text=description_text, image_scr=image_scr)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Выпола ошибка"
    else:
        return render_template("create.html")



@app.route('/about')
def about():
    return render_template("about.html")



if __name__ == '__main__':
    app.run(debug=True)
