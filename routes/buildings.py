from flask import Blueprint, render_template, request, redirect, url_for
from models import buildings, Building

bp = Blueprint('buildings', __name__, url_prefix='/buildings')

@bp.route('/')
def building_list():
    return render_template('buildings.html', buildings=buildings)

@bp.route('/add', methods=['GET', 'POST'])
def add_building():
    if request.method == 'POST':
        new_id = len(buildings) + 1
        name = request.form['name']
        address = request.form['address']
        building = Building(new_id, name, address)
        buildings.append(building)
        return redirect(url_for('buildings.building_list'))
    return render_template('add_building.html')

@bp.route('/edit/<int:building_id>', methods=['GET', 'POST'])
def edit_building(building_id):
    building = next((b for b in buildings if b.id == building_id), None)
    if not building:
        return "Gebäude nicht gefunden", 404
    if request.method == 'POST':
        building.name = request.form['name']
        building.address = request.form['address']
        return redirect(url_for('buildings.building_list'))
    return render_template('edit_building.html', building=building)

@bp.route('/delete/<int:building_id>', methods=['POST'])
def delete_building(building_id):
    global buildings
    buildings[:] = [b for b in buildings if b.id != building_id]
    return redirect(url_for('buildings.building_list'))
