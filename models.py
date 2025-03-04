# models.py

class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

class Building:
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

class MaintenancePlan:
    def __init__(self, id, building_id, date, description):
        self.id = id
        self.building_id = building_id
        self.date = date
        self.description = description

# Simulierter Speicher (in-memory)
users = []
buildings = []
maintenance_plans = []
