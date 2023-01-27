from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from dataclasses import dataclass
import psycopg2


db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432'
db.init_app(app)

@dataclass
class Contact(db.Model):
    __tablename__ = 'contacts'

    id:int = db.Column(db.Integer, primary_key=True)
    name:str = db.Column(db.String(40), nullable=False)
    email:str = db.Column(db.String(40), nullable=False)
    phone:str = db.Column(db.String(10), nullable=False)

@app.get("/contacts")
def get_contacts():
    # contacts = Contact.query.all()
    contacts = db.session.execute(db.select(Contact)).scalars()
    # contacts = [contact for contact in contacts]

    if not contacts:
        return "No contacts found", 404

    return jsonify(list(contacts))

# @app.get("/contacts/<int:id>")
# def get_contact(id):
#     cur = conn.cursor()
#     # cur.execute('SELECT * FROM contacts where id=%s', (id,))
#     cur.execute('SELECT * FROM contacts where id=%(id)s', {"id": id})
#     contact = cur.fetchone()

#     if contact:
#         return jsonify(contact)

#     return "Contact not found", 404

# @app.post("/contacts")
# def create_contact():
#     if request.is_json:
#         contact = request.get_json()

#         if "id" in contact:
#             return "Cannot specify ID for new contact - did you mean to update with PUT?", 400

#         id = _find_next_id()

#         contact = Contact(id, **contact)
#         contacts[id] = contact

#         return {"id": id}, 201
    
#     return "error", 500

# @app.put("/contacts/<int:id>")
# def update_contact(id):
#     if request.is_json:
#         contact = request.get_json()
#         contact = Contact(**contact)

#         if contact.id != id:
#             return "error", 500
        
#         contacts[id] = contact
#         return {}, 201
    
#     return "error", 500

# @app.delete("/contacts/<int:id>")
# def delete_contact(id):
#     contacts.pop(id)
#     return {}, 201