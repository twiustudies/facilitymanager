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

from flask import request, redirect, url_for, session
from translations import LANGUAGES

@bp.route('/set_language', methods=['POST'])
def set_language():
    """Speichert die vom Nutzer gewählte Sprache in der Session."""
    lang = request.form.get("language")
    if lang in LANGUAGES:
        session["language"] = lang
    return redirect(request.referrer or url_for('dashboard'))
