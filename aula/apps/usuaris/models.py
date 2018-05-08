# This Python file uses the following encoding: utf-8

from django.db import models
#from django.db.models import get_model
from django.contrib.auth.models import User, Group
from aula.apps.usuaris.abstract_usuaris import AbstractDepartament,\
    AbstractAccio, AbstractLoginUsuari, AbstractOneTimePasswd

#-------------------------------------------------------------

class Departament(AbstractDepartament):
    pass
#-------------------------------------------------------------

class AlumneUserManager(models.Manager):
    def get_queryset(self):
        grupAlumnes, _ = Group.objects.get_or_create( name = 'alumne' )
        return super(AlumneUserManager, self).get_queryset().filter( groups = grupAlumnes   )


class AlumneUser(User):
    objects = AlumneUserManager()
    class Meta:
        proxy = True
        ordering = ['last_name','first_name','username']

    def getUser(self):
        return User.objects.get( pk = self.pk )

    def getAlumne(self):
        alumne = None
        try:
            alumne = self.alumne
        except:
            pass
        return alumne
                        
    def __unicode__(self):
        return unicode( self.getAlumne() )

class PortalUser(User):
    objects = AlumneUserManager()
    class Meta:
        proxy = True
        ordering = ['last_name','first_name','username']

    def getUser(self):
        return User.objects.get( pk = self.pk )

class PortalTokenUser(User):
    usuari_del_token = models.OneToOneField( User,
                                related_name = "portal_token_user_set",
                                related_query_name = "portal_token_user",  )
    data_creacio = models.DateField( auto_now_add=True )
    clau = models.CharField(max_length=120, blank=False )

class AlumnePortalUser(User):
    PARE = 'PARE'
    MARE = 'MARE'
    APP = 'APP'
    ALTRES = 'ALTRES'
    RELACIO_TUTOR_CHOICES = (
        (PARE,"Pare",),
        (MARE,"Mare",),
        (ALTRES,"Altres",),
        (APP,"Usuari APP",),
    )
    alumne_relacionat = models.ForeignKey("alumnes.Alumne")
    usuari_relacionat = models.ForeignKey( PortalUser,
                                related_name = "alumne_portal_user_set",
                                related_query_name = "alumne_portal_user",  )
    data_creacio = models.DateField( auto_now_add=True )
    relacio_amb_l_alumne = models.CharField(choices=RELACIO_TUTOR_CHOICES,
                                            max_length=7, blank=True)
    
# ----------------------------------------------------------------------------------------------

class ProfessorManager(models.Manager):
    def get_queryset(self):
        #grupProfessors, _ = Group.objects.get_or_create(name='professors')
        #return super(ProfessorManager, self).get_queryset().filter(groups=grupProfessors)

        grupProfessors = 'professors'
        return super(ProfessorManager, self).get_queryset().filter(groups__name=grupProfessors)


class Professor(User):
    objects = ProfessorManager()

    class Meta:
        proxy = True
        ordering = ['last_name', 'first_name', 'username']

    def getUser(self):
        return User.objects.get(pk=self.pk)

    def nMissatgesNoLlegits(self):
        self.destinatari_set.filter(moment_lectura__isnull=True).count()

    def __unicode__(self):
        nom = self.first_name + u' ' + self.last_name if self.last_name else self.username
        return nom.title()

def User2Professor(user):
    professor = None
    try:
        professor = Professor.objects.get(pk=user.pk)
    except:
        pass
    return professor

# ----------------  ------------------------------------------------------------------------------

class ProfessorConsergeManager(models.Manager):
    def get_queryset(self):
        #grupProfessors, _ = Group.objects.get_or_create(name='professors')
        #grupConsergeria, _ = Group.objects.get_or_create(name='consergeria')
        grupProfessors = 'professors'
        grupConsergeria = 'consergeria'
        return super(ProfessorConsergeManager, self).get_queryset().filter(groups__name__in=[grupProfessors, grupConsergeria]).distinct()

class ProfessorConserge(User):
    objects = ProfessorConsergeManager()

    class Meta:
        proxy = True
        ordering = ['last_name', 'first_name', 'username']

    def getUser(self):
        return User.objects.get(pk=self.pk)

    def nMissatgesNoLlegits(self):
        self.destinatari_set.filter(moment_lectura__isnull=True).count()

    def __unicode__(self):
        nom = u"{} {}".format( self.first_name, self.last_name ) if self.last_name else self.username
        rol = u" (consergeria)" if self.groups.filter(name="consergeria").exists() else u" (professorat)"
        nom += rol
        return nom

def User2ProfessorConserge(user):
    professor = None
    try:
        professor = ProfessorConserge.objects.get(pk=user.pk)
    except:
        pass
    return professor


#----------------------------------------------------------------------------------------------

class ProfessionalManager(models.Manager):
    def get_queryset(self):
        grupProfessional, _ = Group.objects.get_or_create( name = 'professional' )
        return super(ProfessionalManager, self).get_queryset().filter( groups = grupProfessional   )

class Professional(User):
    objects = ProfessionalManager()
    class Meta:
        proxy = True
        ordering = ['last_name','first_name','username']

    def getUser(self):
        return User.objects.get( pk = self.pk )
                    
    def __unicode__(self):
        nom = self.first_name + u' ' + self.last_name if self.last_name else self.username 
        return nom.title() 

def User2Professional( user ):
    professional = None
    try:
        professional = Professional.objects.get( pk = user.pk )
    except:
        pass
    return professional

#----------------------------------------------------------------------------------------------

class Accio(AbstractAccio):
    pass
    
#----------------------------------------------------------------------------------------------

class LoginUsuari(AbstractLoginUsuari):
    pass   

class OneTimePasswd(AbstractOneTimePasswd):
    pass

