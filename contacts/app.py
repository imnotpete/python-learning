from dataclasses import dataclass
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@dataclass
class Contact:
    id: int
    name: str
    email: str
    phone: str

# data source
contacts = {
    1: Contact(1, "John", "john email", "john phone"),
    2: Contact(2, "Sue", "Sue email", "Sue phone"),
    3: Contact(3, "Steve", "Steve email", "Steve phone"),
}

def _find_next_id():
    return max(contacts.keys()) + 1

@app.get("/contacts")
def get_contacts():
    return jsonify(list(contacts.values()))

@app.get("/contacts/<int:id>")
def get_contact(id):
    if id in contacts:
        return jsonify(contacts[id])

    return "Contact not found", 404

@app.post("/contacts")
def create_contact():
    if request.is_json:
        contact = request.get_json()

        if "id" in contact:
            return "Cannot specify ID for new contact - did you mean to update with PUT?", 400

        id = _find_next_id()

        contact = Contact(id, **contact)
        contacts[id] = contact

        return {"id": id}, 201
    
    return "error", 500

@app.put("/contacts/<int:id>")
def update_contact(id):
    if request.is_json:
        contact = request.get_json()
        contact = Contact(**contact)

        if contact.id != id:
            return "error", 500
        
        contacts[id] = contact
        return {}, 201
    
    return "error", 500

@app.delete("/contacts/<int:id>")
def delete_contact(id):
    contacts.pop(id)
    return {}, 201