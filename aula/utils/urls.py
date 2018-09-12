from django.conf.urls import url
from aula.utils.views import carregaInicial, calendariDevelop, blanc, about, ajuda

urlpatterns = [
                       
    url(r'^carregaInicial/$', carregaInicial,
        name ="administracio__configuracio__carrega_inicial" )    ,
                       
    url(r'^about/$', about,
        name ="varis__about__about" )    ,
                       
    url(r'^calendariDevelop/$', calendariDevelop,
        name ="help__calendari__calendari" )    ,

    url(r'^opcionsSincro/$', blanc,
        name ="administracio__sincronitza__blanc" )    ,

    url(r'^ajuda/$', ajuda,
        name="varis__ajuda__ajuda")

]

