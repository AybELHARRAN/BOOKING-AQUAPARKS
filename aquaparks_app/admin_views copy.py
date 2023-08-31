from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .forms import *

def verification(request,matricule):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    agent = Agent.objects.get(matricule=matricule)
    conjointes = Conjointe.objects.filter(agent=agent)
    enfants = Enfant.objects.filter(agent=agent)
    form = AjouterAgentForm(request.POST or None)
    context = {
        'page_header_title' : 'verification',
        'active_sidebar' : 'verification',
        'agent':agent,'conjointes':conjointes,'enfants':enfants,
        'form':form,
    }
    return render(request, 'admin_templates/verification.html',context)

def chercher(request,action):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    form = ChercherAgentForm(request.POST or None)
    if action == 'reservation':
        if request.method == 'POST':
            if form.is_valid():
                matricule = form.cleaned_data.get('matricule')
                try:
                    Agent.objects.get(matricule=matricule)
                    return redirect(reverse('reservation2_page',args=[matricule]))
                except Agent.DoesNotExist:
                    messages.warning(request, 'Matricule invalide')
    if action == 'verification':
        if request.method == 'POST':
            if form.is_valid():
                matricule = form.cleaned_data.get('matricule')
                try:
                    Agent.objects.get(matricule=matricule)
                    return redirect(reverse('verification_page',args=[matricule]))
                except Agent.DoesNotExist:
                    messages.warning(request, 'Matricule invalide')
    context = {
        'page_header_title' : action,
        'active_sidebar' : action,
        'form':form,
    }
    return render(request, 'admin_templates/chercher.html', context)

def reservation2(request,matricule):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    agent = Agent.objects.get(matricule=matricule)
    conjointes = Conjointe.objects.filter(agent=agent)
    enfants = Enfant.objects.filter(agent=agent)
    form_a = ReserverForm(request.POST or None,prefix='a')
    form_c = ReserverForm(request.POST or None,prefix='c')
    form_e = ReserverForm(request.POST or None,prefix='e')
    print(matricule)
    print([conjointe for conjointe in conjointes])
    if request.method == 'POST':
        if form_a.is_valid():
            agent.dinoland_reservations = form_a.cleaned_data.get('dinoland')
            agent.tamaris_reservations = form_a.cleaned_data.get('tamaris')
            agent.aquafun_reservations = form_a.cleaned_data.get('aquafun')
            agent.aquamirage_reservations = form_a.cleaned_data.get('aquamirage')
            agent.save()
    
        if form_c.is_valid():
            for conjointe in conjointes :
                conjointe.dinoland_reservations = form_c.cleaned_data.get('dinoland')
                conjointe.tamaris_reservations = form_c.cleaned_data.get('tamaris')
                conjointe.aquafun_reservations = form_c.cleaned_data.get('aquafun')
                conjointe.aquamirage_reservations = form_c.cleaned_data.get('aquamirage')
                conjointe.save()
        if form_e.is_valid():
            for enfant in enfants :
                enfant.dinoland_reservations = form_e.cleaned_data.get('dinoland')
                enfant.tamaris_reservations = form_e.cleaned_data.get('tamaris')
                enfant.aquafun_reservations = form_e.cleaned_data.get('aquafun')
                enfant.aquamirage_reservations = form_e.cleaned_data.get('aquamirage')
                enfant.save()

        messages.success(request, 'La réservation est faite avec succès')
    else:
        form = ReserverForm()
    context = {
        'page_header_title' : 'reservation',
        'active_sidebar' : 'reservation',
        'agent':agent,'conjointes':conjointes,'enfants':enfants,'form_a':form_a,
        'form_c':form_c,'form_e':form_e,
    }
    return render(request,'admin_templates/reservation2.html',context)


































#it needs a slight update
def ajouter_agent(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    form_a = AjouterAgentForm(request.POST or None, prefix = 'a')
    form_c = AjouterConjointeForm(request.POST or None, prefix = 'c')
    form_e = AjouterEnfantForm(request.POST or None, prefix = 'e')
    if request.method == 'POST':
        if 'submit_a' in request.POST:
            # Handle AjouterAgentForm submission
            if form_a.is_valid():
                agent = form_a.save()
                messages.success(request, f"L'agent: {agent.nom} {agent.prenom} est ajouté avec succès")
            
        if 'submit_c' in request.POST:
            # Handle AjouterConjointeForm submission
            if form_c.is_valid():
                conjointe = form_c.save(commit=False)
                agent = Agent.objects.last()
                conjointe.agent = agent
                conjointe.save()
                messages.success(request, f"La Conjointe: {conjointe.nom.upper()} {conjointe.prenom.capitalize()} est ajoutée avec succès")
        
        if 'submit_e' in request.POST:
            # Handle AjouterEnfantForm submission
            if form_e.is_valid():
                enfant = form_e.save(commit=False)
                agent = Agent.objects.last()
                enfant.agent = agent
                enfant.save()
                messages.success(request, f"L'enfant: {enfant.nom.upper()} {enfant.prenom.capitalize()} est ajouté avec succès")
    context = {
        'page_header_title' : 'ajouter agent',
        'active_sidebar' : 'ajouter',
        'code' : "agent",
        'form_a' : form_a, 
        'form_c' : form_c, 
        'form_e' : form_e, 
    }
    return render(request, 'admin_templates/ajouter_agent.html', context)

def modifier_agent(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    matricule = request.GET.get('matricule')
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
    return render(request, 'admin_templates/modifier_agent.html', context)

def supprimer(request,idd,type):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    matricule = request.GET.get('matricule')
    print(matricule)
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
    return HttpResponseRedirect(reverse('modifier_agent_page') + f'?matricule={matricule}')

def ajouter_personne(request,type,idd):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    matricule = Agent.objects.get(id=idd).matricule
    if type == 'c':
        form_c = AjouterConjointeForm(request.POST or None)
        if request.method == 'POST':
            if form_c.is_valid():
                conjointe = form_c.save(commit=False)
                agent = Agent.objects.get(id=idd)
                conjointe.agent = agent
                conjointe.save()
                messages.success(request, f"La Conjointe: {conjointe.nom.upper()} {conjointe.prenom.capitalize()} est ajoutée avec succès")
                return redirect(reverse('modifier_agent_page') + f'?matricule={matricule}')
        context = {
            'page_header_title' : 'ajouter conjointe',
            'active_sidebar' : 'ajouter',
            'code' : "conjointe",
            'form_c' : form_c,
            'matricule': matricule
        }
        page = 'admin_templates/ajouter_conjointe.html'
    elif type == 'e':
        form_e = AjouterEnfantForm(request.POST or None)
        if request.method == 'POST':
            if form_e.is_valid():
                enfant = form_e.save(commit=False)
                agent = Agent.objects.get(id=idd)
                enfant.agent = agent
                enfant.save()
                messages.success(request, f"L'enfant: {enfant.nom.upper()} {enfant.prenom.capitalize()} est ajouté avec succès")
                return redirect(reverse('modifier_agent_page') + f'?matricule={matricule}')
        context = {
            'page_header_title' : 'ajouter enfant',
            'active_sidebar' : 'ajouter',
            'code' : "enfant",
            'form_e' : form_e,
            'matricule':matricule
        }
        page = 'admin_templates/ajouter_enfant.html'
    return render(request, page, context)

def modifier_personne(request,type,idd):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    if type == 'c':
        conjointe = get_object_or_404(Conjointe, id=idd)
        form_c = AjouterConjointeForm(request.POST or None , instance=conjointe)
        if request.method == 'POST':
            if form_c.is_valid():
                conjointe = form_c.save()
                messages.success(request, f"La Conjointe: {conjointe.nom.upper()} {conjointe.prenom.capitalize()} est modifiée avec succès")
                return redirect(reverse('modifier_agent_page') + f'?matricule={conjointe.agent.matricule}')
        context = {
            'page_header_title' : 'modifier conjointe',
            'active_sidebar' : 'modifier',
            'code' : "conjointe",
            'form_c' : form_c,
            'matricule':conjointe.agent.matricule,
            'action':'modifier'
        }
        page = 'admin_templates/ajouter_conjointe.html'
    elif type == 'e':
        enfant = get_object_or_404(Enfant, id=idd)
        form_e = AjouterEnfantForm(request.POST or None , instance=enfant)
        if request.method == 'POST':
            if form_e.is_valid():
                enfant = form_e.save()
                messages.success(request, f"L'enfant: {enfant.nom.upper()} {enfant.prenom.capitalize()} est modifié avec succès")
                return redirect(reverse('modifier_agent_page') + f'?matricule={enfant.agent.matricule}')
        context = {
            'page_header_title' : 'modifier enfant',
            'active_sidebar' : 'modifier',
            'code' : "enfant",
            'form_e' : form_e,
            'matricule':enfant.agent.matricule,
            'action':'modifier'
        }
        page = 'admin_templates/ajouter_enfant.html'
    else:
        agent = get_object_or_404(Agent,id=idd)
        form_a = AjouterAgentForm(request.POST or None , instance=agent)
        if request.method == 'POST':
            if form_a.is_valid():
                agent = form_a.save()
                messages.success(request, f"L'agent: {agent.nom.upper()} {agent.prenom.capitalize()} est modifié avec succès")
                return redirect(reverse('modifier_agent_page') + f'?matricule={agent.matricule}')
        context = {
            'page_header_title' : 'modifier agent',
            'active_sidebar' : 'modifier',
            'code' : "agent",
            'form_a' : form_a,
            'matricule':agent.matricule,
        }
        page = 'admin_templates/ajouter_agent_seul.html'  
    return render(request, page, context)