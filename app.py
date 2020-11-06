from flask import Flask, url_for
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc, asc
from flask_restful import Api, Resource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# Database table creation
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=0,  nullable=False)
    address = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.name


class UserSchema(ma.Schema):
    class Meta:
        fields = ("name", "age", "points", "address")
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def index():
    rows = User.query.order_by(desc(User.points),asc(User.name))
    return render_template('index.html',
                            title='Leaderboard',
                            rows=rows)

@app.route('/adduser', methods=['POST'])
def add_user():
    new_user = User(
        name=request.form['name'].lower(),
        age=request.form['age'],
        address=request.form['address']
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/plus', methods=['POST'])
def plus():
    user = User.query.filter_by(id=request.form["plus"]).first_or_404()
    user.points += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/minus', methods=['POST'])
def minus():
    user = User.query.filter_by(id=request.form["minus"]).first_or_404()
    if user.points > 0:
        user.points -= 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    user = User.query.filter_by(id=request.form["delete"]).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    return render_template("user.html")



#REST API methods
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        new_user = User(
            name=request.json['name'].lower(),
            age=request.json['age'],
            # points=request.json['points'],
            address=request.json['address']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

api.add_resource(UserResource, '/users/<int:user_id>') 
api.add_resource(UserListResource, '/users') 



if __name__ == '__main__':
    app.run(debug=True)
