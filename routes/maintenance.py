from flask import Blueprint, render_template, request, redirect, url_for, Response, jsonify
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from models import maintenance_plans, MaintenancePlan
from datetime import datetime, timedelta

bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@bp.route('/')
def maintenance_list():
    today = datetime.today().date()
    recent_days = timedelta(days=7)

    for plan in maintenance_plans:
        maintenance_date = datetime.strptime(plan.date, "%Y-%m-%d").date()
        plan.overdue = maintenance_date < today
        plan.recently_completed = today - maintenance_date <= recent_days

        # Berechnung der Priorität
        calculate_priority(plan)

    # Sortierung nach Priorität (höchste zuerst)
    sorted_plans = sorted(maintenance_plans, key=lambda p: p.priority, reverse=True)

    return render_template('maintenance.html', maintenance_plans=sorted_plans)

@bp.route('/history')
def maintenance_history():
    """Anzeige der Wartungshistorie mit Filteroptionen"""
    filter_type = request.args.get('type', '')
    filter_date = request.args.get('date', '')

    history = [
        plan for plan in maintenance_plans 
        if (filter_type in plan.category or filter_type == '') 
        and (filter_date in plan.date or filter_date == '')
    ]
    
    return render_template('history.html', maintenance_history=history)

@bp.route('/history/export/csv')
def export_history_csv():
    """Exportiert die Wartungshistorie als CSV"""
    def generate():
        data = [["ID", "Gebäude-ID", "Datum", "Auftrag", "Kategorie"]]
        for plan in maintenance_plans:
            data.append([plan.id, plan.building_id, plan.date, plan.description, plan.category])

        output = BytesIO()
        writer = csv.writer(output)
        writer.writerows(data)
        output.seek(0)
        return output.getvalue()

    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=maintenance_history.csv"})

@bp.route('/history/export/pdf')
def export_history_pdf():
    """Exportiert die Wartungshistorie als PDF"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "Wartungshistorie Bericht")

    y_position = 730
    for plan in maintenance_plans:
        pdf.drawString(100, y_position, f"ID: {plan.id}, Gebäude-ID: {plan.building_id}, Datum: {plan.date}, Kategorie: {plan.category}, Auftrag: {plan.description}")
        y_position -= 20

    pdf.save()
    buffer.seek(0)

    return Response(buffer, mimetype="application/pdf", headers={"Content-Disposition": "attachment;filename=maintenance_history.pdf"})

@bp.route('/search', methods=['GET'])
def search_maintenance():
    query = request.args.get('q', '').lower()
    results = []

    for plan in maintenance_plans:
        if (query in str(plan.building_id).lower() or
            query in plan.date.lower() or
            query in plan.description.lower()):
            results.append({
                "id": plan.id,
                "building_id": plan.building_id,
                "date": plan.date,
                "description": plan.description
            })

    return jsonify(results)

@bp.route('/add', methods=['GET', 'POST'])
def add_maintenance():
    if request.method == 'POST':
        new_id = len(maintenance_plans) + 1
        building_id = int(request.form['building_id'])
        date = request.form['date']
        description = request.form['description']
        category = request.form['category']
        plan = MaintenancePlan(new_id, building_id, date, description, category)
        maintenance_plans.append(plan)
        return redirect(url_for('maintenance.maintenance_list'))
    return render_template('add_maintenance.html')

@bp.route('/edit/<int:plan_id>', methods=['GET', 'POST'])
def edit_maintenance(plan_id):
    plan = next((m for m in maintenance_plans if m.id == plan_id), None)
    if request.method == 'POST':
        plan.date = request.form['date']
        plan.description = request.form['description']
        plan.category = request.form['category']
        return redirect(url_for('maintenance.maintenance_list'))
    return render_template('edit_maintenance.html', plan=plan)

@bp.route('/delete/<int:plan_id>', methods=['POST'])
def delete_maintenance(plan_id):
    global maintenance_plans
    maintenance_plans[:] = [m for m in maintenance_plans if m.id != plan_id]
    return redirect(url_for('maintenance.maintenance_list'))

# Export als CSV
@bp.route('/export/csv')
def export_csv():
    def generate():
        data = [["ID", "Building ID", "Date", "Description"]]
        for plan in maintenance_plans:
            data.append([plan.id, plan.building_id, plan.date, plan.description])

        output = BytesIO()
        writer = csv.writer(output)
        writer.writerows(data)
        output.seek(0)
        return output.getvalue()

    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=maintenance_report.csv"})

# Export als PDF
@bp.route('/export/pdf')
def export_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "Maintenance Report")

    y_position = 730
    for plan in maintenance_plans:
        pdf.drawString(100, y_position, f"ID: {plan.id}, Building ID: {plan.building_id}, Date: {plan.date}, Description: {plan.description}")
        y_position -= 20

    pdf.save()
    buffer.seek(0)

    return Response(buffer, mimetype="application/pdf", headers={"Content-Disposition": "attachment;filename=maintenance_report.pdf"})

# NEUE ROUTE: Datum ändern durch Drag-and-Drop
@bp.route('/update_date/<int:plan_id>', methods=['POST'])
def update_maintenance_date(plan_id):
    """Aktualisiert das Datum eines Wartungseintrags nach Drag-and-Drop."""
    new_date = request.json.get("date")
    
    plan = next((m for m in maintenance_plans if m.id == plan_id), None)
    if plan:
        plan.date = new_date
        return jsonify({"status": "success", "message": "Datum aktualisiert"}), 200
    return jsonify({"status": "error", "message": "Eintrag nicht gefunden"}), 404

# NEUE ROUTE: Wartungsanweisungen als PDF exportieren
@bp.route('/export/instruction_pdf/<int:plan_id>')
def export_instruction_pdf(plan_id):
    """Generiert eine detaillierte Wartungsanweisung als PDF mit Checklisten und Bildern."""
    plan = next((m for m in maintenance_plans if m.id == plan_id), None)
    if not plan:
        return jsonify({"status": "error", "message": "Wartungseintrag nicht gefunden"}), 404

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # PDF Kopf
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Wartungsanweisung")

    # Wartungsdetails
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"Gebäude-ID: {plan.building_id}")
    pdf.drawString(100, 710, f"Datum: {plan.date}")
    pdf.drawString(100, 690, f"Beschreibung: {plan.description}")
    pdf.drawString(100, 670, f"Kategorie: {plan.category}")

    # Checkliste
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 640, "Checkliste:")
    pdf.setFont("Helvetica", 12)
    checklist = [
        "✔ Werkzeuge bereitstellen",
        "✔ Sicherheitsvorkehrungen prüfen",
        "✔ Wartungsbereich absichern",
        "✔ Bauteile inspizieren",
        "✔ Funktionsprüfung durchführen"
    ]
    
    y_position = 620
    for item in checklist:
        pdf.drawString(120, y_position, item)
        y_position -= 20

    # Bild einfügen (Beispielbild)
    try:
        img_path = "static/images/maintenance_example.png"
        image = ImageReader(img_path)
        pdf.drawImage(image, 100, 400, width=200, height=150)
    except Exception as e:
        pdf.drawString(100, 380, "⚠️ Bild konnte nicht geladen werden.")

    pdf.save()
    buffer.seek(0)

    return Response(buffer, mimetype="application/pdf",
                    headers={"Content-Disposition": f"attachment;filename=maintenance_instruction_{plan_id}.pdf"})
@bp.route('/update', methods=['POST'])
def update_maintenance():
    """ Aktualisiert einen Wartungseintrag basierend auf dem Feld """
    data = request.json
    maintenance_id = int(data.get("id"))
    field = data.get("field")
    value = data.get("value")

    # Sicherheitsüberprüfung: Nur autorisierte Benutzer dürfen bearbeiten (Dummy-Check)
    if not request.headers.get("Authorization"):
        return jsonify({"status": "error", "message": "Nicht autorisiert"}), 403

    plan = next((m for m in maintenance_plans if m.id == maintenance_id), None)
    if not plan:
        return jsonify({"status": "error", "message": "Wartungseintrag nicht gefunden"}), 404

    if field == "date":
        plan.date = value
    elif field == "description":
        plan.description = value
    else:
        return jsonify({"status": "error", "message": "Ungültiges Feld"}), 400

    return jsonify({"status": "success", "message": "Änderung gespeichert"})

# Prioritätsstufen definieren
PRIORITY_LEVELS = {
    "low": 3,
    "medium": 2,
    "high": 1
}

def calculate_priority(plan):
    """ Berechnet die Priorität eines Wartungsplans basierend auf Deadline und Kritikalität """
    today = datetime.today().date()
    maintenance_date = datetime.strptime(plan.date, "%Y-%m-%d").date()
    
    # Dringlichkeit basierend auf der Nähe der Deadline
    days_until_due = (maintenance_date - today).days
    urgency_score = max(0, 10 - days_until_due)  # Höhere Werte für nähere Deadlines
    
    # Kritikalität basierend auf der Kategorie oder weiteren Faktoren
    criticality_score = PRIORITY_LEVELS.get(plan.criticality, 3)  # Default: low
    
    # Gesamtprioritätsbewertung (höhere Werte = höhere Priorität)
    plan.priority = urgency_score + (5 * criticality_score)
    
    # Prioritätsanzeige für UI
    if plan.priority > 20:
        plan.priority_indicator = "🔴 High Priority"
    elif plan.priority > 10:
        plan.priority_indicator = "🟠 Medium Priority"
    else:
        plan.priority_indicator = "🟢 Low Priority"

@bp.route('/priority-settings', methods=['POST'])
def update_priority_settings():
    """ Ermöglicht Nutzern die Anpassung der Priorisierungslogik """
    data = request.get_json()
    if "priority_weights" in data:
        global PRIORITY_LEVELS
        PRIORITY_LEVELS.update(data["priority_weights"])
    return jsonify({"message": "Priority settings updated"}), 200
from flask import request, jsonify
from models import comments, Comment
from datetime import datetime

@bp.route('/maintenance/<int:maintenance_id>/comments', methods=['GET'])
def get_comments(maintenance_id):
    """ Gibt alle Kommentare für einen Wartungseintrag zurück """
    entry_comments = [c for c in comments if c.maintenance_id == maintenance_id]
    return jsonify([{"user": c.user, "text": c.text, "timestamp": c.timestamp} for c in entry_comments])

@bp.route('/maintenance/<int:maintenance_id>/comments', methods=['POST'])
def add_comment(maintenance_id):
    """ Fügt einen neuen Kommentar zu einem Wartungseintrag hinzu """
    data = request.get_json()
    if "user" not in data or "text" not in data:
        return jsonify({"error": "Missing user or text"}), 400
    
    new_comment = Comment(
        maintenance_id=maintenance_id,
        user=data["user"],
        text=data["text"],
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    comments.append(new_comment)
    return jsonify({"message": "Comment added successfully"}), 201
