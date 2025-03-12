from app import app, db

def new_base():
    app.app_context().push()
    db.create_all()


if __name__ == '__main__':
    new_base()