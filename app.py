from flask import Flask, render_template,redirect,url_for, request, jsonify
from forms.mascota_form import mascotaForm, preguntaForm
from database import db 
from models.mascotas import Mascota
from database import create_db
import openai


app = Flask(__name__)


openai.api_key = "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"


app.config.from_object('config.Config')

create_db(app)

# FUNCION DE PROMPT A CHATGPT
def send_prompt_chatgpt(prompt) : 
    model = 'gpt-3.5-turbo'
    response = openai.Completion.create(
        engine = "text-davinci-003", 
        prompt = prompt,
        max_tokens = 1200,
        n = 1, 
        stop = None,
        temperature = 0
    )
    answer = response.choices[0].text.strip()
    return answer 


# LISTA DE MASCOTAS
@app.route("/mascotas")
def mascotas():
    mascotas = Mascota.query.all()

    return render_template("mascotas.html",mascotas=mascotas)


# INICIO

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("Pantalla-1.html")

# ABOUT US 
@app.route("/about_us")
def about_us():
    return render_template("Pantalla-2.html")

# ESPECIE
@app.route("/especie")
def especie():
    return render_template("Pantalla-3.html")

# MEET
@app.route("/meet")
def meet():
    return render_template("Pantalla-4.html")

# FORM
@app.route("/form", methods=["GET","POST"])
def form():
    form = mascotaForm()
    return render_template("Pantalla-5.html",form=form)

# MENU
@app.route("/menu")
def menu():
    return render_template("Pantalla-6.html")

# PROFILE
@app.route("/lista")
def profile():
    mascotas = Mascota.query.all()
    return render_template("mascotas.html",mascotas=mascotas)

# CHAT
@app.route("/chat")
def chat():
    return render_template("Pantalla-8.html")

# HOME

# @app.route("/home")
# def home():
    
#     return render_template("home.html")









# REGISTRAR GATO
@app.route("/registrar_gato", methods=["GET","POST"])
def registrar_gato():
    form = mascotaForm()

    if form.validate_on_submit():
        mascota = Mascota(nombre=form.nombre.data, raza=form.raza.data,peso=form.peso.data, edad=form.edad.data,nivel_de_actividad=form.nivel_de_actividad.data , entorno=form.entorno.data)
        db.session.add(mascota)
        db.session.commit()
        return redirect(url_for('registro'))
    return render_template("registrar_gato.html",form=form)




# REGISTRO DE GATO CON LISTA DE GATOS
@app.route('/registro', methods=['GET','POST' ])
def registro():
    form = mascotaForm()
    if form.validate_on_submit():
        mascota = Mascota(nombre=form.nombre.data, raza=form.raza.data,peso=form.peso.data, edad=form.edad.data,nivel_de_actividad=form.nivel_de_actividad.data , entorno=form.entorno.data)
        db.session.add(mascota)
        db.session.commit()
        redirect(url_for('registro'))
    mascotas = Mascota.query.all()
    return render_template('registro.html', mascotas=mascotas, form=form)









# EDITAR REGISTRO
@app.route('/edit/<id>', methods=['GET','POST' ])
def edit(id):
    mascota = Mascota.query.get_or_404(id)
    form = mascotaForm(obj=mascota)
    if form.validate_on_submit():
        mascota.nombre = form.nombre.data
        mascota.raza = form.raza.data
        mascota.edad = form.edad.data
        mascota.nivel_de_actividad = form.nivel_de_actividad.data
        mascota.entorno = form.entorno.data
        mascota.peso = form.peso.data
        db.session.commit()
        return redirect(url_for('registro'))
    return render_template('edit.html', form=form, mascota=mascota)



# ELIMINAR REGISTRO
@app.route("/delete/<id>")
def delete(id):

    mascota = Mascota.query.get_or_404(id)
    db.session.delete(mascota)
    db.session.commit()
    return redirect(url_for('registro'))



# CHAT MASCOTA
@app.route("/chatasinc/<id>")
def chatasinc(id):
    mascota = Mascota.query.get_or_404(id)
    nombre = mascota.nombre
    return render_template("chatearAjax.html",id=id,nombre=nombre)








# RESPUESTA DEL CHAT CON AJAX


@app.route('/send_message/<id>', methods=['POST'])
def send_message(id):
    pregunta = request.form.get('message')
    # Aquí puedes procesar el mensaje o realizar cualquier otra acción que desees
    mascota = Mascota.query.get_or_404(id)
    nombre = mascota.nombre
    raza = mascota.raza
    edad = mascota.edad
    peso = mascota.peso
    nivel_de_actividad = mascota.nivel_de_actividad
    entorno = mascota.entorno
    part1 = "Eres un asistente veterinario que brinda información sobre alimentación adecuada y cuidado para diferentes animales. Como asistente, proporcionas instrucciones claras sobre qué tipo de alimento puede y no puede comer un animal, las cantidades correctas para alimentarlo y pautas generales para ayudar a las personas a mantener a sus mascotas en óptimas condiciones de salud. Tu objetivo final es proporcionar instrucciones y pautas claras para seguir en relación con un tipo específico de animal. Te proporcionaré contexto sobre el animal específico en cada consulta. "
    # part2 = "CONTEXTO: Fluffy es un perro, específicamente un border collie de dos años de edad que pesa 30 kg. La cantidad adecuada de alimento diario para Fluffy, un border collie de dos años de edad que pesa 30 kg, es aproximadamente de 600 a 900 gramos al día, lo que equivale al 2-3% de su peso corporal. Consulta con un veterinario para obtener pautas precisas basadas en las necesidades individuales de Fluffy. "
    part3 = f"Pregunta: {pregunta}, un gato de raza {raza} de {edad} de edad que pesa {peso} kg, que tiene un nivel de actividad fisica {nivel_de_actividad}, que normalmente habita en {entorno}? brinda consejos para esa pregunta en menos de 50 palabras, teniendo en cuenta los datos proporcionados."
    promt = part1 + part3
    answer = send_prompt_chatgpt(promt)
    # Devuelve una respuesta, puedes usar jsonify para enviar datos JSON
    print(f"pregunta: {pregunta}")
    print(promt)
    return jsonify({'status': 'OK','message':f'{answer}'})





# CHAT
@app.route("/chatear/<id>", methods=['GET','POST' ])
def chatear(id):
    id_gato= id
    pregunta = preguntaForm()
    if pregunta.validate_on_submit():
        mascota = Mascota.query.get_or_404(id_gato)
        nombre = mascota.nombre
        raza = mascota.raza
        edad = mascota.edad
        peso = mascota.peso
        nivel_de_actividad = mascota.nivel_de_actividad
        entorno = mascota.entorno
        part1 = "Eres un asistente veterinario que brinda información sobre alimentación adecuada y cuidado para diferentes animales. Como asistente, proporcionas instrucciones claras sobre qué tipo de alimento puede y no puede comer un animal, las cantidades correctas para alimentarlo y pautas generales para ayudar a las personas a mantener a sus mascotas en óptimas condiciones de salud. Tu objetivo final es proporcionar instrucciones y pautas claras para seguir en relación con un tipo específico de animal. Te proporcionaré contexto sobre el animal específico en cada consulta. "
        part2 = "CONTEXTO: Fluffy es un perro, específicamente un border collie de dos años de edad que pesa 30 kg. La cantidad adecuada de alimento diario para Fluffy, un border collie de dos años de edad que pesa 30 kg, es aproximadamente de 600 a 900 gramos al día, lo que equivale al 2-3% de su peso corporal. Consulta con un veterinario para obtener pautas precisas basadas en las necesidades individuales de Fluffy. "
        part3 = f"Pregunta: {pregunta.pregunta.data} para un gato de nombre{nombre}, un {raza} de {edad} de edad que pesa {peso} kg, que tiene un nivel de actividad fisica {nivel_de_actividad}, que normalmente habita {entorno}? Responde en menos de 50 palabras, teniendo en cuenta los datos proporcionados."
        promt = part1 + part2 + part3
        answer = send_prompt_chatgpt(promt)
        print(f"Pregunta: {part3}, RESPUESTA: {answer}")
        # return render_template('resultado.html', answer = answer)
        return render_template("chatear.html",answer=answer,id=id_gato,nombre=nombre,pregunta=pregunta)




    return render_template("chatear.html",id=id_gato,pregunta=pregunta)

if __name__ == "__main__":
    app.run(debug=True)