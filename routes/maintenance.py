from flask import Blueprint, render_template, request, redirect, url_for, Response, jsonify
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from models import maintenance_plans, MaintenancePlan

bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@bp.route('/')
def maintenance_list():
    return render_template('maintenance.html', maintenance_plans=maintenance_plans)

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
        plan = MaintenancePlan(new_id, building_id, date, description)
        maintenance_plans.append(plan)
        return redirect(url_for('maintenance.maintenance_list'))
    return render_template('add_maintenance.html')

@bp.route('/edit/<int:plan_id>', methods=['GET', 'POST'])
def edit_maintenance(plan_id):
    plan = next((m for m in maintenance_plans if m.id == plan_id), None)
    if request.method == 'POST':
        plan.date = request.form['date']
        plan.description = request.form['description']
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
