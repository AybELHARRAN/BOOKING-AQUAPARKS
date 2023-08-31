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

#try to combine the modifier_agent and supprimer functions
'''def modifier_agent_updated(request,action='r',type=None,idd=None):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    if action == 'r':
        form = ChercherAgentForm(request.POST or None)
        agent = None
        conjointes = []
        enfants = []
        if request.method == 'POST':
            if form.is_valid():
                matricule = form.cleaned_data.get('matricule')
                try:
                    agent = Agent.objects.get(matricule=matricule)
                    conjointes = Conjointe.objects.filter(agent=agent)
                    enfants = Enfant.objects.filter(agent=agent)
                except Agent.DoesNotExist :
                    messages.warning(request,'Matricule invalide')

        context = {
            'page_header_title' : 'modifier agent',
            'active_sidebar' : 'modifier',
            'code' : "agent",
            'form': form,
            'agent' : agent,'conjointes':conjointes , 'enfants':enfants,
        }
    elif action == 's':
        if type == 'a':
            agent = get_object_or_404(Agent, id=idd)
            agent.delete()
            messages.success(request, "Agent supprimé avec succès!")
        elif type == 'c':
            conjointe = get_object_or_404(Conjointe, id=idd)
            conjointe.delete()
            messages.success(request, "Conjoint(e) supprimé(e) avec succès!")
        else:
            enfant = get_object_or_404(Enfant, id=idd)
            enfant.delete()
            messages.success(request, "Enfant supprimé avec succès!")
            return redirect(reverse('modifier_agent_page_updated'))
    return render(request, 'admin_templates/modifier_agent.html', context)
'''