from flask import Flask,render_template, request, redirect, flash, url_for
from flask_admin import Admin
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
import os


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'password'
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Page_info(db.Model):
    __tablename__ = 'page_info'

    id = db.Column(db.Integer, primary_key=True)
    home_page = db.Column(db.String(100), nullable=False)
    about_page= db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    company_description_text = db.Column(db.Text, nullable=True)
    company_about = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return self.company_name


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.email


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description_text = db.Column(db.Text, nullable=True)
    file = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


admin = Admin(app, name='Админка', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session, name="Пользователь"))
admin.add_view(ModelView(Item, db.session, name="Товар"))
admin.add_view(ModelView(Page_info, db.session, name="Информация о сайте"))


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    page_info = Page_info.query.all()
    return render_template("index.html", items=items, page_info=page_info)





@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        file = request.files['file']
        title = request.form['title']
        price = request.form['price']
        filename = secure_filename(file.filename)
        description_text = request.form['description_text']
        if request.form["url_text"] == '':
            files = str(UPLOAD_FOLDER + "/" + filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            files = request.form["url_text"]

        item = Item(title=title, price=price, description_text=description_text, file=files)
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
    page_info = Page_info.query.all()
    return render_template("about.html",  page_info=page_info)

@app.route('/buy/<int:id>')
def item_buy(id):
    return str(id)

if __name__ == '__main__':
    app.run(debug=True)
