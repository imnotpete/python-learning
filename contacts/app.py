from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask import Flask, request, jsonify
from dataclasses import dataclass
from flask_caching import Cache

################
# Initialization
################

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object('config.BaseConfig')
db.init_app(app)
cache = Cache(app)

# Model
@dataclass
class Contact(db.Model):
    __tablename__ = 'contacts'

    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name:str = db.Column(db.String(40), nullable=False)
    email:str = db.Column(db.String(40), nullable=False)
    phone:str = db.Column(db.String(10), nullable=False)

# for testing - create blank database with our table(s) if not already existing
with app.app_context():
    db.create_all()

################
# REST API
################

@app.get("/contacts")
@cache.cached(timeout=30, query_string=True)
def get_contacts():
    # optional
    search = request.args.get("search")

    statement = db.select(Contact)
    if search:
        search = f"%{search}%"
        statement = statement.filter(or_(
            Contact.name.ilike(search),
            Contact.email.ilike(search)))

    contacts = db.session.execute(
        statement
    ).scalars()

    if not contacts:
        return "No contacts found", 404

    print("db contacts")
    return jsonify(list(contacts))

@app.get("/contacts/<int:id>")
@cache.cached(timeout=30)
def get_contact(id):
    contact = db.get_or_404(Contact, id)

    if not contact:
        return "Contact not found", 404

    print("db contacts")
    return jsonify(contact)

@app.post("/contacts")
def create_contact():
    if request.is_json:
        contact = request.get_json()

        if "id" in contact:
            return "Cannot specify ID for new contact - did you mean to update with PUT?", 400

        contact = db.session.execute(
            db.insert(Contact).returning(Contact), 
            contact
        ).scalar()

        db.session.commit()

        return {"id": contact.id}, 201
    
    return "error", 500

@app.put("/contacts/<int:id>")
def update_contact(id):
    if request.is_json:
        contact = request.get_json()

        if contact["id"] != id:
            return "ID in URL and body do not match", 500
        
        db.session.execute(
            db.update(Contact), 
            contact)

        db.session.commit()

        return {}, 201
    
    return "error", 500

@app.delete("/contacts/<int:id>")
def delete_contact(id):
    contact = db.get_or_404(Contact, id)

    db.session.delete(contact)
    db.session.commit()

    return {}, 201