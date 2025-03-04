from flask import Blueprint, render_template, request, redirect, url_for
from models import maintenance_plans, MaintenancePlan

bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@bp.route('/')
def maintenance_list():
    return render_template('maintenance.html', maintenance_plans=maintenance_plans)

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
    if not plan:
        return "Wartungsplan nicht gefunden", 404
    if request.method == 'POST':
        plan.building_id = int(request.form['building_id'])
        plan.date = request.form['date']
        plan.description = request.form['description']
        return redirect(url_for('maintenance.maintenance_list'))
    return render_template('edit_maintenance.html', plan=plan)

@bp.route('/delete/<int:plan_id>', methods=['POST'])
def delete_maintenance(plan_id):
    global maintenance_plans
    maintenance_plans[:] = [m for m in maintenance_plans if m.id != plan_id]
    return redirect(url_for('maintenance.maintenance_list'))
