from flask import Blueprint, render_template, request, redirect, url_for
from models import users, User

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def user_list():
    return render_template('users.html', users=users)

@bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_id = len(users) + 1
        username = request.form['username']
        email = request.form['email']
        user = User(new_id, username, email)
        users.append(user)
        return redirect(url_for('users.user_list'))
    return render_template('add_user.html')

@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        return "Benutzer nicht gefunden", 404
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        return redirect(url_for('users.user_list'))
    return render_template('edit_user.html', user=user)

@bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    global users
    users[:] = [u for u in users if u.id != user_id]
    return redirect(url_for('users.user_list'))
