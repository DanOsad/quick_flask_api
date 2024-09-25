from extensions import db

#### DB TABLE MODEL ####
class Model(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text, default = None)
    date = db.Column(db.DateTime, default = None)

    @property
    def as_dict(self):
        return { column.name: getattr(self, column.name) for column in self.__table__.columns }

    @property
    def serialize(self):
        return { attr: getattr(self, attr) for attr in self.columns }
    
    @property
    def columns(self):
        return [ column.name for column in self.__table__.columns ]