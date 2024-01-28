from django.shortcuts import render
from .apps import QstsapiConfig

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .predict_mouna.code import CalculMoyenneFiliere
from datetime import datetime

class call_model(APIView):

    def post(self,request):
        if request.method == 'POST':
            optionalFields = ['FName','LName','Email','Major']
            optionalFields.reverse()
            majors = ['IID','GI','GE','IRIC','GPEE']
            majCuts = {
                'IID':'Informatique et Ingenierie des Donnees (IID)',
                'GI':'Genie Informatique (GI)',
                'GE':'Genie Electrique (GE)',
                'IRIC':'Ingenierie des Reseaux Intelligent et Cybersecurite (IRIC)',
                'GPEE':'Genie des Procedes et des Energies Renouvelables (GPEE)',
            }
            #texts to describe each major :
            texts={
                'IID':"Are you hungry for Data ?",
                'GI':"Time to build the next Facebook!",
                'GE':"Autodriving cars said hello!",
                "IRIC":"Watch out, the internet is a dangerous place!",
                "GPEE":"Process, process, and more process!"
            }
            params =  request.POST
            #Preprocessing
            x = list(params.values())
            x.insert(0,datetime.now().date())
            if(len(x)<25):
                for optF in optionalFields:
                    if optF not in params.keys():
                        x.insert(1,'')
            #predection
            rsp = QstsapiConfig.model.Evaluate(x)
            #Empty majors:
            for major in majors :
                if major not in rsp.keys():
                    rsp[major] = 0.0
            #detect max major:
            max=0
            maxmajor= 'IID'
            for maj in majors:
                if rsp[maj]>max:
                    max = rsp[maj]
                    maxmajor = maj
            rsp['maxmajor']=maxmajor
            rsp['maxmajorName']=majCuts[maxmajor]
            rsp['text']=texts[maxmajor]
            return render(request, 'qstsFormResults.html', rsp)

        
from django.template import loader
def qstsapi(request):
  template = loader.get_template('qstsForm.html')
  return HttpResponse(template.render())

def acceuil(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

#Afaf & Mohamed :


# from predict_mouna import CalculMoyenneFiliere

# Cette vue sera responsable de la communication entre l'API et votre modèle de chatbot.

from django.views.decorators.csrf import csrf_exempt
from .chat_med.chatbot import predict


@csrf_exempt
def chatbot_api_view(request):
    if request.method == 'POST':
        data = request.POST.get('msg')  # Récupérer le message envoyé par le chatbot
        # Traiter le message et préparer la réponse
        #app_config = apps.get_app_config('myapii') 
        #chatbot = app_config.chatbot
        print(f"data={data}")
        response = {
            'ques': data,  # Echo the chatbot's question
            'res': predict(chatbot_=QstsapiConfig.chatbot_model,sentence=data),  # Replace with your chatbot's actual response
            #'res': 'Hey, this is a simple test !',  # Replace with your chatbot's actual response
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
        }
        return JsonResponse(response)



# CalculMoy
class calcul_moyenne(APIView):
    def post(self,request):
        if request.method == 'POST':
            notes = {}
            if len(list(request.POST.values()))==24:
                for key in request.POST.keys():
                    notes[key]=float(request.POST[key])
                
                # Création de l'instance du modèle
                calcul_moyenne = CalculMoyenneFiliere()
                # Appel des méthodes pour calculer les moyennes
                moyennes = calcul_moyenne.calculer_moyennes(notes)
                maxMoyMaj = ''
                maxMoy = 0
                for maj in moyennes.keys():
                    if moyennes[maj]>maxMoy:
                        maxMoy = moyennes[maj]
                        maxMoyMaj = maj
                moyennes['maxMaj']= maxMoyMaj
                texts={
                'IID':"Are you hungry for Data ?",
                'GI':"Time to build the next Facebook!",
                'GE':"Autodriving cars said hello!",
                "IRIC":"Watch out, the internet is a dangerous place!",
                "GPEE":"Process, process, and more process!"
                }
                majCuts = {
                'IID':'Informatique et Ingenierie des Donnees (IID)',
                'GI':'Genie Informatique (GI)',
                'GE':'Genie Electrique (GE)',
                'IRIC':'Ingenierie des Reseaux Intelligent et Cybersecurite (IRIC)',
                'GPEE':'Genie des Procedes et des Energies Renouvelables (GPEE)',
                }
                moyennes['maxMajName']=majCuts[maxMoyMaj]
                moyennes['text']=texts[maxMoyMaj]

                return render(request, 'gradesFormResults.html', moyennes)


def gradesapi(request):
    # index c'est le nom de la page html dans le dossier views
    template = loader.get_template('gradesForm.html')
    return HttpResponse(template.render({}, request))

