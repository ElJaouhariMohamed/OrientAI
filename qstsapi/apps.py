from django.apps import AppConfig
from .qmdl.QModel import QModel
from .chat_med.chatbot import chatbot,predict

class QstsapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qstsapi'
    model = QModel('./qstsapi/qmdl/formData.csv')
    import nltk
    nltk.download('wordnet')
    chatbot_model=chatbot()
    chatbot_model.launch()