import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
db_user = os.getenv('POSTGRES_USER', 'user')
db_password = os.getenv('POSTGRES_PASSWORD', 'super-secret-password')
db_host = os.getenv('POSTGRES_HOST', 'db')
db_port = os.getenv('POSTGRES_PORT', '5432')
db_name = os.getenv('POSTGRES_DB', 'test')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
db = SQLAlchemy(app)

class Moment(db.Model):
    __tablename__ = 'moments'
    mid = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<Moment {self.name} parent_id:{self.parent_id}>'

Moment.parent_id = db.Column(db.Integer, db.ForeignKey(Moment.mid))
Moment.parent = relationship(Moment, backref='children', remote_side=Moment.mid)

@app.route('/')
def index():
    mid = request.args.get('id', default=1)
    return str(db.session.get(Moment, mid))

@app.route('/moments/<int:mid>/descendants')
def descendants(mid):
    parent = db.session.get(Moment, mid)
    return format_descendants(parent)

def format_descendants(moment, indent=0):
    if moment is None:
        return ""
    descendants_list = [f"{' ' * indent}{moment.name}\n"]
    for child in moment.children:
        descendants_list.append(format_descendants(child, indent + 4))
    return ''.join(descendants_list)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
