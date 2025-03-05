from flask import Blueprint, render_template, request, jsonify
from models import buildings, Building

bp = Blueprint('buildings', __name__, url_prefix='/buildings')

@bp.route('/')
def building_list():
    return render_template('buildings.html', buildings=buildings)

####
# FM-US-1 added
@bp.route('/facilities')
def get_facilities():
    """API endpoint to fetch facility list as JSON"""
    facility_data = [{"id": b.id, "name": b.name} for b in buildings]
    return jsonify(facility_data)
####

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

import qrcode
from flask import send_file
from io import BytesIO

@bp.route('/buildings/<int:building_id>/qr', methods=['GET'])
def generate_qr(building_id):
    """Generiert einen QR-Code für eine Gebäudeseite."""
    facility_url = f"{request.url_root}buildings/{building_id}"
    qr = qrcode.make(facility_url)

    img_io = BytesIO()
    qr.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name=f"facility_{building_id}_qr.png")
