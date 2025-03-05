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

# Changed for FM-US-2
class MaintenancePlan:
    def __init__(self, id, building_id, date, description, reminder_enabled=False):
        self.id = id
        self.building_id = building_id
        self.date = date
        self.description = description
        self.reminder_enabled = reminder_enabled  # Neues Attribut für Erinnerungen

# Sample Users List
users = [
    User(1, "admin", "admin@example.com"),
    User(2, "john_doe", "john.doe@example.com"),
    User(3, "jane_smith", "jane.smith@example.com")
]

# Sample Buildings List
buildings = [
    Building(1, "Main Facility", "123 Main St"),
    Building(2, "Engineering Hub", "456 Tech Rd"),
    Building(3, "Research Center", "789 Innovation Ave"),
    Building(4, "Data Center München", "101 Cloud St"),
    Building(5, "Zentrale Köln", "102 Rheinstr."),
]

<<<<<<< HEAD
# Sample Maintenance Plans List (Previously Missing!) now added new in this version
=======
# Sample Maintenance Plans List (Previously Missing!) now added new
>>>>>>> 68db010 (changes)
maintenance_plans = [
    MaintenancePlan(1, 1, "2024-03-10", "HVAC inspection"),
    MaintenancePlan(2, 2, "2024-04-15", "Elevator maintenance"),
    MaintenancePlan(3, 3, "2024-05-20", "Fire safety check"),
]
