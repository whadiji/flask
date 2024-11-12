from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Team, Task
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/teams', methods=['GET', 'POST'])
def manage_teams():
    if request.method == 'POST':
        data = request.json
        new_team = Team(name=data['name'])
        db.session.add(new_team)
        db.session.commit()
        return jsonify({'id': new_team.id, 'name': new_team.name}), 201
    
    teams = Team.query.all()
    return jsonify([{'id': team.id, 'name': team.name} for team in teams])

@app.route('/teams/<int:team_id>/tasks', methods=['GET', 'POST'])
def manage_tasks(team_id):
    if request.method == 'POST':
        data = request.json
        new_task = Task(title=data['title'], description=data['description'], team_id=team_id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description}), 201
    
    tasks = Task.query.filter_by(team_id=team_id).all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks])

# Définir le endpoint pour ajouter une équipe
@app.route('/teams/add', methods=['POST'])
def add_team():
    data = request.json
    new_team = Team(name=data['name'])
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'id': new_team.id, 'name': new_team.name}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Créer les tables si elles n'existent pas
    app.run(debug=True)
