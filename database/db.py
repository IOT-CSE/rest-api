from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1:5432/test'

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app


