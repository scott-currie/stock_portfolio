from . import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Company(db.Model):
    __tablename__ == 'companies'
