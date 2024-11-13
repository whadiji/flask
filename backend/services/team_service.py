from models.models import db, Team

class TeamService:
    @staticmethod
    def create_team(name):
        new_team = Team(name=name)
        db.session.add(new_team)
        db.session.commit()
        return new_team

    @staticmethod
    def get_all_teams():
        return Team.query.all()
    
    @staticmethod
    def get_team_by_id(team_id: int):
        # Récupérer une équipe par son ID
        team = Team.query.get(team_id)  # Recherche l'équipe par son ID dans la base
        if team is None:
            raise Exception(f"Team with id {team_id} not found.")  # Gestion d'erreur si l'équipe n'existe pas
        return team  # Retourne l'objet Team trouvé