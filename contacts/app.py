from dataclasses import dataclass
from flask import Flask, request, jsonify

app = Flask(__name__)

@dataclass
class Contact:
    id: int
    name: str
    email: str
    phone: str

contacts = {
    1: Contact(1, "John", "john email", "john phone"),
    2: Contact(2, "Sue", "Sue email", "Sue phone"),
    3: Contact(3, "Steve", "Steve email", "Steve phone"),
}

def _find_next_id():
    return max(contact.id for contact in contacts) + 1

@app.get("/contacts")
def get_contacts():
    return jsonify(contacts.values)

@app.get("/contacts/<id>")
def get_contact(id):
    print(type(id))
    return jsonify(contacts[int(id)])

@app.post("/contacts")
def create_contact():
    if request.is_json:
        contact = request.get_json()
        id = _find_next_id()
        contact["id"] = id
        contact = Contact(**contact)
        contacts[id] = contact
        return {"id": id}, 201
    
    return "error", 500