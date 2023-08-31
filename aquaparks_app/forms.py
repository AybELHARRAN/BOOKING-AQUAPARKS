from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from . import constantes
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name','last_name','email','gender', 'user_type','password1', 'password2']
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Username'})
        self.fields['gender'].widget.attrs.update({'class':'form-control Select'})
        self.fields['first_name'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Prénom'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Nom'})
        self.fields['email'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Email'})
        self.fields['user_type'].widget.attrs.update({'class':'form-control Select'})
        self.fields['password1'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class':'form-control',
                                                    'placeholder':'Confirmer le mot de passe'})
    

#FORM AJOUTER AGENT/CONJOINTE/ENFANT    
class AjouterAgentForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['matricule'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le matricule'})
        self.fields['nom'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le nom'})
        self.fields['prenom'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le prenom'})
        self.fields['CIN'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer la CIN'})
        self.fields['telephone'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le numero de telephone'})
        self.fields['email'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer email'})
        self.fields['categorie'].widget.attrs.update({'class': 'form-control Select'})

        self.fields['sexe'].widget.attrs.update({'class': 'form-control Select',
                                                 })
        self.fields['adulte_enfant'].widget.attrs.update({'class': 'form-control Select',
                                                        })


    matricule = forms.CharField(required=True)
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    CIN = forms.CharField(required=False)
    categorie = forms.ChoiceField(required=True, choices=constantes.CATEGORIE)
    datenaissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd', 'class': 'form-control'}),
                                required=True)
    telephone = forms.CharField(required=True,max_length=30)
    email = forms.EmailField()
    sexe = forms.ChoiceField(required=True, 
                             choices=constantes.SEXE,
                             )
    adulte_enfant = forms.ChoiceField(choices=constantes.ADULTE_ENFANT,
                                       required=True,
                                       )

    class Meta:
        model = Agent   
        fields = ['matricule', 'nom', 'prenom', 'CIN','datenaissance','telephone','email', 'categorie','sexe','adulte_enfant'] 

class AjouterConjointeForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['nom'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le nom'})
        self.fields['prenom'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le prenom'})
        self.fields['CIN'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer la CIN'})
        #self.fields['datenaissance'].widget.attrs.update({'class':'form-control',})
        #self.fields['age'].widget.attrs.update({'class': 'form-control','disabled': 'disabled'})
        self.fields['sexe'].widget.attrs.update({'class': 'form-control Select',
                                                 })
        self.fields['adulte_enfant'].widget.attrs.update({'class': 'form-control Select',
                                                 })

    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    CIN = forms.CharField(required=False)
    datenaissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd', 'class': 'form-control'}),
                                required=True)

    #age = forms.DecimalField(max_digits=4,decimal_places=2,required=False)
    sexe = forms.ChoiceField(required=True, 
                             choices=constantes.SEXE,
                             )
    adulte_enfant = forms.ChoiceField(choices=constantes.ADULTE_ENFANT,
                                       required=True,
                                       )

    class Meta:
        model = Conjointe   
        fields = ['nom', 'prenom', 'CIN','datenaissance', 'sexe', 'adulte_enfant'] 

class AjouterEnfantForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['nom'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le nom'})
        self.fields['prenom'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le prenom'})
        self.fields['CIN'].widget.attrs.update({'class':'form-control',
                                                      'placeholder': 'Entrer le CIN'})
        #self.fields['datenaissance'].widget.attrs.update({'class':'form-control',})
        #self.fields['age'].widget.attrs.update({'class': 'form-control','disabled': 'disabled'})
        self.fields['sexe'].widget.attrs.update({'class': 'form-control Select',
                                               })
        self.fields['adulte_enfant'].widget.attrs.update({'class': 'form-control Select',
                                                })

    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    CIN = forms.CharField(required=False)
    datenaissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd', 'class': 'form-control'}),
                                required=True)
    #age = forms.DecimalField(max_digits=4,decimal_places=2,required=False)
    sexe = forms.ChoiceField(required=True, 
                             choices=constantes.SEXE,
                             )
    adulte_enfant = forms.ChoiceField(choices=constantes.ADULTE_ENFANT,
                                       required=True,
                                       )

    class Meta:
        model = Enfant   
        fields = ['nom', 'prenom', 'CIN','datenaissance','sexe', 'adulte_enfant'] 

class ChercherAgentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['matricule'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Entrer le matricule'
        })
    matricule = forms.CharField(required=True,)


class ReserverForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dinoland'].widget.attrs.update({'class': 'form-control Select',
                                                })
        self.fields['tamaris'].widget.attrs.update({'class': 'form-control Select',
                                                })
        self.fields['aquafun'].widget.attrs.update({'class': 'form-control Select',
                                                })
        self.fields['aquamirage'].widget.attrs.update({'class': 'form-control Select',
                                                })

    dinoland = forms.ChoiceField(required=True, choices=constantes.DINOLAND_CHOICES )
    tamaris = forms.ChoiceField(required=True, choices=constantes.TAMARIS_CHOICES )
    aquafun = forms.ChoiceField(required=True, choices=constantes.AQUAFUN_CHOICES)
    aquamirage = forms.ChoiceField(required=True, choices=constantes.AQUAMIRAGE_CHOICES)
    '''dinoland_e = forms.ChoiceField(required=True, choices=(('0','0')) )
    tamaris_e = forms.ChoiceField(required=True, choices=(('0','0')) )
    aquafun_e = forms.ChoiceField(required=True, choices=(('0','0')))
    aquamirage_e = forms.ChoiceField(required=True, choices=(('0','0')))'''

class VerifierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accord'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Entrer le matricule'})
    matricule = forms.CharField(required=True)
    class Meta:
        model = Agent
        fields = ['matricule']

class ExcelUploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['excel_file'].widget.attrs.update({
            'class': 'custom-file-input',
        })
    excel_file = forms.FileField(label="hahahah")