from flask import Flask, render_template
from routes import users, buildings, maintenance

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(users.bp)
app.register_blueprint(buildings.bp)
app.register_blueprint(maintenance.bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
