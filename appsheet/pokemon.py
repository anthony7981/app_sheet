import os

import requests
import pandas as pd
import gspread
from decouple import config
from progress.bar import ChargingBar
from googletrans import Translator
from oauth2client.service_account import ServiceAccountCredentials



if os.name == 'nt':
    clean_screen = 'cls'
else:
    clean_screen = "clear"

os.system(clean_screen)

# En primer lugar, establecemos en listas vacías las columnas que usaremos más
# adelante para nuestro dataframe con pandas. Luego, obtenemos el listado de 
# todos los pokemones desde la API y guardamos la información que nos interesa.

names = []
abilities = []
hp = []
attack = []
defense = []
special_attack = []
special_defense = []
speed = []
location = []
types = []
articles = []
images = []


print('Go grab a coffee\nThis may take a few minutes...')

main_api = requests.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1154')

main_response = main_api.json()['results']

api_bar = ChargingBar('Downloading information |', max=len(main_response))

for pokemon in main_response:
    names.append(pokemon['name'].capitalize())
    ind_request = requests.get(pokemon['url']).json()

    str_abilities = ''
    str_location = ''
    str_type = ''


    for a in ind_request['abilities']:
        str_abilities += a['ability']['name'] + '\n'
    abilities.append(str_abilities[:-2])



    for stat in ind_request['stats']:
        if stat['stat']['name'] == 'hp':
            hp.append(stat['base_stat'])

        elif stat['stat']['name'] == 'attack':
            attack.append(stat['base_stat'])

        elif stat['stat']['name'] == 'defense':
            defense.append(stat['base_stat'])

        elif stat['stat']['name'] == 'special-attack':
            special_attack.append(stat['base_stat'])

        elif stat['stat']['name'] == 'special-defense':
            special_defense.append(stat['base_stat'])
        
        else:
            speed.append(stat['base_stat'])



    location_area_url = requests.get(ind_request['location_area_encounters']).json()
    if location_area_url == []:
        location.append('Unknown')
    else:
        for l in location_area_url:
            for x in l['location_area']['name'].split('-'):
                str_location += x.capitalize() + ' '

            location.append(str_location[:-1])
            break

    
    photo = ind_request['sprites']['other']['official-artwork']['front_default']
    if photo is not None:
        images.append(photo)
    else:
        # En caso de que el campo esté vacío, pasamos la url
        # de una imagen con el símbolo '?' para indicar que
        # la apariencia del pokemon es desconocida.
        images.append("https://www.clipartmax.com/png/middle/105-1054330_question-mark-png-transparent-background-question-mark.png")



    # Aquí extraemos los tipos de pokemon para realizar
    # la traducción de las palabras y más adelante 
    # compararlas con el Código Penal.
    for t in ind_request['types']:
        str_type += t['type']['name'] + '-'
    types.append(str_type[:-1])
        
    api_bar.next()
api_bar.finish()




# Obtenemos el dataframe del cual sacaremos los artículos
# del Código Penal. Luego traducimos las palabras en la lista
# 'types', comparamos cuáles de ellas se relacionan con los
# artículos y creamos la asociación con la lista 'articles'.
print('Getting the legislation...')

legislation = pd.read_csv(config('LAW'))
legislation = legislation.loc[legislation['titulo_completo'].str.contains('CPN')]

print('The "Código Penal de la Nación Argentina" legislation was obtained successfully!')

law_bar = ChargingBar('Finding potential crimes |', max=len(main_response))

for field in types:
    str_articles = ''
    for f in field.split('-'):
        translator = Translator()
        translated_word = translator.translate(f, dest='es').text
        table = legislation.loc[legislation['delito_descripcion'].str.contains(translated_word) == True, ['delito_artículo']]
        if len(table.index) > 0:
            for i in table.index.tolist():
                str_articles += table.loc[i, 'delito_artículo'] + '\n'
        else:
            str_articles += ''

    articles.append(str_articles[:-2])

    law_bar.next()
law_bar.finish()



# Creamos un DataFrame con pandas y pasamos las columnas 
# con los datos correspondientes.

df = pd.DataFrame()        

df["Names"] = names
df["Abilities"] = abilities
df["HP"] = hp
df["Attack"] = attack
df["Special attack"] = special_attack
df["Defense"] = defense
df["Special defense"] = special_defense
df["Location"] = location
df["Types"] = types
df["CPN articles"] = articles
df["Images"] = images


df["CPN articles"].replace({'': 'None'}, inplace=True)



# Empezamos a trabajar con Google Sheets.
# Establecemos el alcance que queremos en 'scope'
# (las apis a las que queremos acceder), nos
# autenticamos, compartimos el acceso a nuestro
# correo personal y pasamos el dataframe como
# sheet.



print("Creating google sheet...")

scopes = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(config('SHEETS'), scopes=scopes)

auth = gspread.authorize(credentials=credentials)
db_name = 'pokemondb'

sheet = auth.create(db_name)
sheet.share(
    email_address=config('PERSONAL_EMAIL'),
    perm_type='user',
    role='writer',
    notify=True,
    email_message='Please start the AppSheet with this database.'
    )

post_sheet = auth.open(db_name).sheet1.update([df.columns.values.tolist()] + df.values.tolist())

print('Congratulations!\nThe google sheet has been created.\nI hope you are enjoying that coffee c:')