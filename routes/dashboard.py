from flask import Blueprint, render_template
from datetime import datetime, timedelta
from models import maintenance_plans

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def dashboard():
    today = datetime.today().date()
    upcoming_maintenance = []

    for plan in maintenance_plans:
        maintenance_date = datetime.strptime(plan.date, "%Y-%m-%d").date()
        overdue = maintenance_date < today
        upcoming = 0 <= (maintenance_date - today).days <= 7  # Innerhalb einer Woche

        upcoming_maintenance.append({
            "id": plan.id,
            "building_id": plan.building_id,
            "date": plan.date,
            "description": plan.description,
            "overdue": overdue,
            "upcoming": upcoming
        })

    return render_template('index.html', upcoming_maintenance=upcoming_maintenance)
