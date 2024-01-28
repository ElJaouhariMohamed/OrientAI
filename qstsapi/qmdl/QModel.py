'''
 --->  DOCUMENTATION <---
 This class is made to instentiate and use a semi-supervised Machine Learning model, conceptualized and developped by Ilyas El Amrani,
 as part of the AI Assissted Orientation project made by the Team : Afaf Matouk, Ilyas El Amrani, Mohamed El Jaouhari, Mouna Guerrab.
To understand better the functionnality of this model please visit the notebook 'Form Based Classifier : DEMO'
This code is under the MIT Licence. Anyone can work with this code for research and business projects, with giving credit to its original creator:
Ilyas El Amrani.

2022-2023
'''

#IMPORTS :
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from os.path import isfile,abspath

#Defautls : 
defaultMajors = {'IID':1,'GI':2,'GE':3,'GPEE':4,'IRIC':5}
defaultQ_answers = {'I love it':2,'I like it':1,'I am not sure':0,'Yes':1,'No':-1,
             'I haven\'t tried it yet':0,'I am very familiar with them':2,'I know the basics':1,
             'I have limited experience':0,'I have no experience with them':0,'I have little to no experience':0}


class QModel:
    #Init
    def __init__(self,dataFile='./formData.csv',apiDataFile='./apiData.csv'
                 ,majorsEncoding=defaultMajors,Q_ansEcoding=defaultQ_answers,KNNmodelFile="KNNSupModel.pickle",loadKNNOnStart = False):
        '''
        dataFile : File regrouping data to use for model training.
        majorsEncoding : Dictionary to encode the majors.
        Q_ansEncoding : Dictionary to use for question answers encoding.
        KNNmodelFile : The file where to load and save the KNN (supervised) model
        LoadKNNOnStart : Tru to load the KNN model on the initialisation
        
        '''
        self.dataFile = dataFile
        self.apiDataFile = apiDataFile
        self.majors = majorsEncoding
        #Creating the reverse of dictionary, keys are the numbers and values are the encoded name of the major.
        self.majorsR = {v:k for v,k in enumerate(self.majors.keys(),1)}
        self.Q_ansEncoding = Q_ansEcoding
        #Load the data
        self.loadData()
        
        #Loading the KNN model if specified, else configure it not created yet, nor loaded, finaly consider the data not clustered yet
        self.KNNmFile = KNNmodelFile
        self.KNNCreated = False
        self.KNNLoaded = self.LoadKNN() if loadKNNOnStart else False
        self.clustered = False
        self.APIDataLoaded = False

    #Fonctions de chargements des donnees :
    def loadData(self):
        self.data = pd.read_csv(self.dataFile)
        self.pData = self.preproc(self.data.values)
        self.X = self.pData.drop('Major',axis=1)
        self.y = self.pData.Major
        #Charger les données récupérés via l'application web
        self.loadAPIDataset(self.apiDataFile)
        #Si ses données existent, nous allons ajouter au données d'entrainement les enregistrement dont la filière est différente de "Aucune"
        if(self.apiData.values.shape[0]!=0):
            xad = self.preproc(self.apiData[self.apiData['Major']!='Aucune'].values)
            self.X = pd.concat([self.X,xad.drop('Major',axis=1)],axis=0)
            self.y = pd.concat([self.y,xad['Major']],axis=0)
        return True
        

    #Preprocessing Function
    def preproc(self,x):
        if(type(x)==list):
            x=np.array(x)
        assert(x.size==25 or x.shape[1]==25)
        if(len(x.shape)==1):
            x=np.array([x])
        inData = pd.DataFrame(x[:,4:],columns=[ 'Major']+[f'Q{i}' for i in range(1,21)])
        inData.replace(self.majors,inplace=True)
        inData.replace(self.Q_ansEncoding,inplace=True)
        return inData
    
    #Creer et trainer le model supervisé 
    def CreateSupKNN(self):
        self.KNNmodel = KNeighborsClassifier()
        self.KNNmodel.fit(self.X,self.y)
        pickle.dump(self.KNNmodel, open(self.KNNmFile, "wb"))
        self.KNNCreated=True
        return True

    #Charger le model s'il exist 
    def LoadKNN(self):
        if(isfile(abspath(self.KNNmFile))):
            try:
                self.KNNmodel = pickle.load(open(self.KNNmFile, "rb"))
                self.KNNLoaded=True
                return True
            except:
                pass
        return False
    
    #Creer et trainer le model non supervisé 
    def CreateKMeans(self):
        KMmodel = KMeans(5,random_state=1)
        y_clusts = KMmodel.fit_predict(self.X)
        self.clustered = True
        return y_clusts

    #Evaluer la classe d'un étudiant
    def Evaluate(self,x):
        orgx = x.copy()
        x=  self.preproc(x)
        self.X.add(x)
        y_clusts = self.CreateKMeans()
        y_clusts = pd.Series(y_clusts)
        y_clusts.value_counts()
        maj = self.getMajors(y_clusts,self.y,self.X)
        if(orgx[3]!='' and orgx[4]!='Aucune'):
            self.updateDataSet(orgx,self.apiDataFile)
        return maj

    #Récuperer la filière en fct des réponses de l'utilisatuer et en utilisant le modèle
    def getMajors(self,y,y_org,X):
        clusterMajors = {}
        for clust in y.unique():
            clustEtds = y[y==clust]
            clustEtdsReel = y_org.iloc[clustEtds.index].value_counts()
            max = clustEtdsReel.max()
            #Nombre des classes dominantes 
            nbCs = len(clustEtdsReel[clustEtdsReel==max].to_list())
            #On assume que la classe sera celle de la majorite
            if nbCs == 1:
                #Retourner les probabilites 
                clss = clustEtdsReel.to_dict()
                total = sum(list(clss.values()))
                probas = {}
                for clse in clss.keys() :
                    if(round(clss[clse]*100,3)!=0):
                        probas[self.majorsR[clse]] = round((clss[clse]/total)*100,3)
                clusterMajors[clust] = probas
            #Si la majorite n'est pas determinee, on utilise le model supervise
            else : 
                if(not self.KNNLoaded):
                   if(not self.LoadKNN()):
                       self.CreateSupKNN()
                Xm = X.iloc[-1,:].values.reshape(1,-1)
                probas = {}
                prbs = self.KNNmodel.predict_proba(Xm)[0,:]
                for proba in range(0,len(prbs)):
                    if(round(prbs[proba]*100,3)!=0):
                        probas[self.majorsR[proba+1]] = prbs[proba]*100
                clusterMajors[clust] = probas
        return clusterMajors[clustEtds.iloc[-1]]
    
    #Créer le dataset pour récuillir les réponses des utilisateurs
    def createAPIDataset(self,path='./apiData.csv'):
        apiData= pd.DataFrame(data={},columns=self.data.columns)
        apiData.to_csv(path)

    #Charger ce dataset
    def loadAPIDataset(self,path='./apiData.csv'):
        if(not isfile(path)):
            self.createAPIDataset(path)
        self.apiData = pd.read_csv(path,index_col='Unnamed: 0')
        self.APIDataLoaded=True

    #Sauvgarder les modifications effectués sur le dataset
    def saveAPIDataset(self,path='./apiData.csv'):
        if(self.APIDataLoaded):
            self.apiData.to_csv(path)
    #Mettre à jours le dataset
    def updateDataSet(self,x,path):
        if(not self.APIDataLoaded):
            self.loadAPIDataset(path)
        X = pd.DataFrame([x],columns=self.apiData.columns)
        if self.apiData.values.shape[0]!=0:
            if X.iloc[0,4] not in self.apiData.iloc[:,4]: #Si l'email n'est pas sur la base de donnée, ajouté l'étudiant
                self.apiData=pd.concat([self.apiData,X],axis=0)
            else :#S'il est, modifier l'enregistrement de l'étudiant ( le supprimer et le r'inserer)
                id = self.apiData[self.apiData['email']==X.iloc[0,4]].index[0]
                self.apiData.drop([id],inplace=True)
                self.apiData = pd.concat([self.apiData,X],axis=0)
        else :
            self.apiData = X
        print(self.apiData)
        self.saveAPIDataset(path)