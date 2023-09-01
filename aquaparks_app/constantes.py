CATEGORIE = (('hc', 'HC'), ('tam' , 'TAM'), ('oe', 'OE'),
             ('gm', 'GM'),('gc', 'GC'),('pm', 'PM'),
              ('pc', 'PC'),)
CATEGORIE_D = dict(CATEGORIE)

ADULTE_ENFANT = (('adulte','Adulte') , ('enfant', 'Enfant'))
ADULTE_ENFANT_D = dict(ADULTE_ENFANT)

ACCORD = (('oui', 'OUI') , ('non', 'NON'))
ACCORD_D = dict(ACCORD)

BENEFICIER = (('oui', 'OUI') , ('non', 'NON'))
BENEFICIER_D = dict(BENEFICIER)

SEXE = (('m', 'Masculin'), ('f', 'Féminin'))
SEXE_D = dict(SEXE)

DINOLAND_CHOICES = ( (str(i),str(i)) for i in range(3) )
TAMARIS_CHOICES = ( (str(i),str(i)) for i in range(3) )
AQUAMIRAGE_CHOICES =(('0', '0'), ('1S', '1S'), ('1D', '1D'), ('2S', '2S'), ('2D', '2D'))
AQUAFUN_CHOICES = (('0', '0'), ('1S', '1S'), ('1D', '1D'), ('2S', '2S'), ('2D', '2D'))

DINOLAND_PRIX = {'adulte':30 , 'enfant':25}
TAMARIS_PRIX = {'adulte':40 , 'enfant':30}
AQUAFUN_PRIX = {
    'avec' : {'adulte':50 , 'enfant':40}
    ,'sans' : {'adulte':40 , 'enfant':30}
}
AQUAMIRAGE_PRIX = {
    'avec' : {'adulte':50 , 'enfant':40}
    ,'sans' : {'adulte':40 , 'enfant':30}
}







'''{% if form_c.nom.errors %}
                    <div class="alert alert-danger">
                        {{ form_c.nom.errors|join:", " }}
                    </div>
                {% endif %}     '''
