from database import db 

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable = False)
    peso = db.Column(db.String(255), nullable = False)

    raza = db.Column(db.String(255), nullable = False)
    edad = db.Column(db.String(255), nullable= False)
    nivel_de_actividad = db.Column(db.String(255))
    entorno = db.Column(db.String(255))
