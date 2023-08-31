from django.db import models
from django.contrib.auth.models import AbstractUser, Group , Permission, UserManager
from django.contrib.auth.hashers import make_password
from . import constantes
from datetime import datetime


class CustomUserManager(UserManager):
    def create_user(self, email= None, password= None, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_user_permissions')
    USER_TYPE = (
        ('1', 'admin'),
        ('2', 'staff'),
        )
    GENDER = (('m', 'male'), ('f', 'female'))

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    user_type = models.CharField( default= '2', choices= USER_TYPE, max_length=1)
    gender = models.CharField( choices= GENDER, max_length=1 , default='male' )
    created_at = models.DateTimeField( auto_now_add= True)
    updated_at = models.DateTimeField( auto_now= True )
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=100,blank=True)

    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Agent(models.Model):
    SEXE = (('m', 'Masculin'), ('f' , 'Feminin'),  )
    #personal info
    matricule = models.CharField(max_length=20, unique=True)
    CIN = models.CharField(max_length=20, blank=True)
    categorie = models.CharField(max_length=5,choices=constantes.CATEGORIE,blank=True,null=True)
    age = models.IntegerField(null=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=50)
    datenaissance = models.DateField(blank=True,null=True)
    telephone = models.CharField(max_length=50,null=True)
    email = models.EmailField(max_length=254,blank=True)
    sexe = models.CharField(max_length=2, choices=constantes.SEXE,default='m')
    adulte_enfant = models.CharField(max_length=10, choices=constantes.ADULTE_ENFANT, default='adulte')
    accord = models.CharField(max_length=3, choices=constantes.ACCORD,default='oui')
    
    #database new fields
    ent_affect = models.CharField(max_length=20,null=True,blank=True)
    dateembauche = models.DateField(blank=True,null=True)

    #reservation info
    dinoland_reservations = models.CharField(max_length=2,default='0')
    tamaris_reservations = models.CharField(max_length=2,default='0')
    aquafun_reservations = models.CharField(max_length=2,default='0')
    aquamirage_reservations = models.CharField(max_length=2,default='0')

    def __str__(self):
        return self.nom.upper() + ' ' +self.prenom.capitalize()
    def save(self, *args, **kwargs):
        if self.datenaissance:
            age = (datetime.now().date() - self.datenaissance).days // 365
            self.age = int(age)
        super().save(*args, **kwargs)

class Conjointe(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    #personal info
    age = models.IntegerField(blank=True)
    CIN = models.CharField(max_length=20, blank=True,null=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=50)
    datenaissance = models.DateField()
    sexe = models.CharField(max_length=2, choices=constantes.SEXE, default='f')
    adulte_enfant = models.CharField(max_length=10, choices=constantes.ADULTE_ENFANT, default='adulte')
    accord = models.CharField(max_length=3, choices=constantes.ACCORD,default='oui')

    #reservation info
    dinoland_reservations = models.CharField(max_length=2,default='0')
    tamaris_reservations = models.CharField(max_length=2,default='0')
    aquafun_reservations = models.CharField(max_length=2,default='0')
    aquamirage_reservations = models.CharField(max_length=2,default='0')

    def save(self, *args, **kwargs):
        if self.datenaissance:
            age = (datetime.now().date() - self.datenaissance).days // 365
            self.age = int(age)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nom.upper() + ' ' +self.prenom.capitalize()

class Enfant(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    #personal info
    age = models.IntegerField(blank=True)
    CIN = models.CharField(max_length=20, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=50)
    datenaissance = models.DateField()
    sexe = models.CharField(max_length=2, choices=constantes.SEXE, default='f')
    adulte_enfant = models.CharField(max_length=10, choices=constantes.ADULTE_ENFANT, default='enfant')
    accord = models.CharField(max_length=3, choices=constantes.ACCORD,default='oui')
    droit_a_beneficier = models.CharField(max_length=3, choices=constantes.BENEFICIER, default='oui')
    
    #reservation info
    dinoland_reservations = models.CharField(max_length=2,default='0')
    tamaris_reservations = models.CharField(max_length=2,default='0')
    aquafun_reservations = models.CharField(max_length=2,default='0')
    aquamirage_reservations = models.CharField(max_length=2,default='0')
    
    def save(self, *args, **kwargs):
        if self.datenaissance:
            age = (datetime.now().date() - self.datenaissance).days // 365
            self.age = int(age)
            if age < 21:
                self.droit_a_beneficier = 'oui'
            else:
                self.droit_a_beneficier = 'non'
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nom.upper() + ' ' +self.prenom.capitalize()
