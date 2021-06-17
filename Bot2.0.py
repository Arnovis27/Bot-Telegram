from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction
import requests, urllib
import csv
import os
#from Credential import TOKENKEY


INPUT_TEXT=0
TOKENKEY= os.getenv("TOKENKEY")#Esta linea es para heroku, comentala y decomenta la de arriba

def start(update, context):
    update.message.reply_text("Hola,Bienvendio\n\nEsta es la linea de comandos que manejo hasta ahora\n/pokemon Buscar datos de un pokemon")

def pokemon_Command_Handler(update,context):
    update.message.reply_text("Enviame el nombre del pokemon a encontrar")
    return INPUT_TEXT

def informacion_Command_Handler(update,context):
    update.message.reply_text("https://github.com/Arnovis27/Bot-Telegram")
    return ConversationHandler.END

def send_imag(text,update,context):
    url='http://pokeapi.co/api/v2/pokemon/'
    pokename= text.lower()

    url2= url + pokename
    response= requests.get(url2)

    if response.status_code == 200:
        response2= requests.get(url2)
        payload2= response2.json()
        sprites= payload2.get('sprites', [])
        front_sprite=''

        update.message.reply_text(pokename.upper())
        if sprites:
            #Descargando Imagen
            if sprites:
                other= sprites["other"]
                if other:
                    officialartwork= other["official-artwork"]
                    if officialartwork:
                        front_sprite= officialartwork["front_default"]
            
            imagen= open("./Sprite/Sprite.png", 'wb')
            imagen.write(urllib.request.urlopen(front_sprite).read())
            imagen.close()
        
        imagen2= "./Sprite/Sprite.png"
        chat= update.message.chat
        chat.send_action(
        	action=ChatAction.UPLOAD_PHOTO,
        	timeout=None
    	)
        
        chat.send_photo(
        	photo=open(imagen2, 'rb')
    	)
        
        get_pokemons(text,update,context)

    else:
        update.message.reply_text("Desconozco ese nombre, te recomiendo estos segun lo que escribiste.")
        
        csvFile = open("./DB/data.csv", "r")
        csvReader = csv.reader(csvFile, delimiter=",")
        res = [[str(n) for n in line] for line in csvReader]
        csvFile.close()

        lista=[]

        #Agregando a una lista simple
        for lista1 in res:
            for numero in lista1:
                lista.append(numero)

        #Busqueda dentro de la lista
        ocurrenciatotal=[0 for i in range(len(lista))]
        empieza= pokename[0]
        inicial=0

        for z in range(len(lista)):
            aux2= z
            contador=0
            for c in pokename:
                inicial= lista[aux2]
                inicial= inicial[0]
                if(inicial==empieza):
                    if(len(lista[aux2]) <= len(pokename)+1):
                        ocurrencia= lista[aux2].count(c)    
                        contador= contador+ ocurrencia
            ocurrenciatotal[z]= contador
        
        nuevalista=[]
        maximo= max(ocurrenciatotal)
        for i in range(len(lista)):
            if (ocurrenciatotal[i]>= len(pokename)-2 and ocurrenciatotal[i]<= maximo):
                nuevalista.append(lista[i])
        
        f = open ('./DB/Sugerencia.txt','w')
        for i in range(len(nuevalista)):
            f.write(nuevalista[i]+"\n")
        f.close()

        chat= update.message.chat
        chat.send_action(
        	action=ChatAction.UPLOAD_DOCUMENT,
        	timeout=None
    	)
        
        chat.send_document(
        	document=open('./DB/Sugerencia.txt', 'rb')
    	)

        update.message.reply_text("Digita nuevamente /pokemon")
    

def get_pokemons(text,update,context):
    url='http://pokeapi.co/api/v2/pokemon/'
    pokename= text.lower()
    

    url2= url + pokename
    response= requests.get(url2)
    vacio1=[]
    vacio2=[]
    vacio3=[]



    if response.status_code == 200:
        response2= requests.get(url2)
        payload2= response2.json()
        types= payload2.get('types', [])
        abilities= payload2.get('abilities', [])
        stats= payload2.get('stats', [])
        especies= payload2.get('species', [])
        tipo1=0
        habilidad=0
        stabs=0
        valor=0
        descripcion=0

        if especies:
            espo= especies["url"]
        
        response3= requests.get(espo)
        payload3= response3.json()
        flavor= payload3.get('flavor_text_entries', [])
        aux=0

        if flavor:
            for aux in flavor:
                valor2= aux["language"]
                if(valor2["name"]=="es"):
                    descripcion= aux["flavor_text"]
                    break
        update.message.reply_text("POKEDEX: "+descripcion)

        if types:
            for tipos in types:
                tipo1= tipos['type']
                vacio1.append(tipo1['name'])

        if abilities:
            for hiden in abilities:
                habilidad= hiden['ability']
                vacio2.append(habilidad['name'])

        if stats:
            for base in stats:
                valor= base['base_stat']
                stabs= base['stat']
                vacio3.append(stabs['name'])
                vacio3.append(valor)    

    
        update.message.reply_text("---Tipo---\n"+' - '.join(vacio1)+"\n---Habilidades---\n"+'  '.join(vacio2)+"\n---Stab Base---\n"+'  '.join(map(str,vacio3)))
        

def informacion(text,update,context):
    update.message.reply_text("https://github.com/Arnovis27/Bot-Telegram")

def input_text(update, context):
    text= update.message.text
    send_imag(text,update,context)
    return ConversationHandler.END



if __name__ == '__main__':

    updater= Updater(token=TOKENKEY, use_context=True)
    
    dp= updater.dispatcher

    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('pokemon',pokemon_Command_Handler),
            CommandHandler('info',informacion_Command_Handler)
        ],
        states={
            INPUT_TEXT:[MessageHandler(Filters.text, input_text)],
        },
        fallbacks=[]
    ))

    updater.start_polling()
    print("Bot Running")
    updater.idle()