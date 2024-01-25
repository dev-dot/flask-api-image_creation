from flask import Flask, request, render_template_string, send_file, render_template
import os

from flask_cors import CORS
from selenium import webdriver

app = Flask(__name__)
CORS(app, resources={r"/static/images": {"origins": "*"},})

with open('template.html', 'r', encoding='utf-8') as file:
    HTML_TEMPLATE = file.read()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/create_image', methods=['POST'])
def create_image():
     # Variablen aus JSON-Daten extrahieren
    data = request.get_json()
    home_team = data.get('home_team', 'Heimmannschaft')
    away_team = data.get('away_team', 'Auswärtsmannschaft')
    score = data.get('score', '3:1')
    image_url = data.get('image_url', "static/images/DSCF0297.jpg")
    

    # Beispiel: Erstellen Sie die HTML-Seite mit Jinja2-Templating
    html_content = render_template_string(HTML_TEMPLATE, home_team=home_team, away_team=away_team, score=score, image_url= image_url)

    # Beispiel: Speichern Sie die HTML-Seite vorübergehend in einer Datei
    html_file_path = 'temp_template.html'
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)
    
    # Beispiel: Verwenden Sie imgkit, um die HTML-Seite in ein Bild umzuwandeln
   
    output_image_path = 'output.png'

    #Erstellen Sie einen Headless-Chrome-Browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.set_window_size(1080,1080)
    
    
        # Öffnen Sie die lokale HTML-Datei
    driver.get('https://api-image-creation.onrender.com/temp_template')

    # Screenshot erstellen
    driver.save_screenshot(output_image_path)

    # Browser schließen
    driver.quit()

    


    # Beispiel: Rückgabe des personalisierten Bildes
    return send_file(output_image_path, as_attachment=True)

@app.route('/temp_template')
def template():
    return render_template("temp_template.html")