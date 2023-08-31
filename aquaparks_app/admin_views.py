from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import *
from . import constantes
import pandas as pd

#import numpy as np

def verification(request,matricule):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    agent = Agent.objects.get(matricule=matricule)
    conjointes = Conjointe.objects.filter(agent=agent)
    enfants = Enfant.objects.filter(agent=agent)
    dino_p,tam_p,aquaf_p,aquam_p=0,0,0,0
    for personnes in [agent,conjointes,enfants]:
        if personnes == agent:
            dino_p += int(personnes.dinoland_reservations)*constantes.DINOLAND_PRIX['adulte']
            tam_p += int(personnes.tamaris_reservations)*constantes.TAMARIS_PRIX['adulte']
            if len(personnes.aquafun_reservations)==2:
                aquaf_p += int(personnes.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['avec']['adulte']
            else:
                aquaf_p += int(personnes.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['sans']['adulte']
            if len(personnes.aquamirage_reservations)==2:
                aquam_p += int(personnes.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['avec']['adulte']
            else:
                aquam_p += int(personnes.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['sans']['adulte']
        else:
            for per in personnes:
                if isinstance(per,Conjointe) or per.age>21:
                    dino_p += int(per.dinoland_reservations)*constantes.DINOLAND_PRIX['adulte']
                    tam_p += int(per.tamaris_reservations)*constantes.TAMARIS_PRIX['adulte']
                    if len(per.aquafun_reservations)==2:
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['avec']['adulte']
                    else:
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['sans']['adulte']
                    if len(per.aquamirage_reservations)==2:
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['avec']['adulte']
                    else:
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['sans']['adulte']
                elif isinstance(per,Enfant) and per.age<2:
                    dino_p += 0
                    tam_p += 0
                    aquaf_p += 0
                    aquam_p += 0
                else:
                    dino_p += int(per.dinoland_reservations)*constantes.DINOLAND_PRIX['enfant']
                    tam_p += int(per.tamaris_reservations)*constantes.TAMARIS_PRIX['enfant']
                    if len(per.aquafun_reservations)==2:
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['avec']['enfant']
                    else:
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['sans']['enfant']
                    if len(per.aquamirage_reservations)==2:
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['avec']['enfant']
                    else:
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['sans']['enfant']
    context = {
        'page_header_title' : 'verification',
        'active_sidebar' : 'verification',
        'agent':agent,'conjointes':conjointes,'enfants':enfants,
        'dino_p':dino_p,'tam_p':tam_p,'aquaf_p':aquaf_p,'aquam_p':aquam_p,
        'prix_total':sum((dino_p,tam_p,aquaf_p,aquam_p))  
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
    forms_c = [ReserverForm(request.POST or None,prefix=f'c{n}') for n in range(len(conjointes))]
    forms_e = [ReserverForm(request.POST or None,prefix=f'e{n}') for n in range(len(enfants))]
    if agent.dinoland_reservations != '0' or agent.tamaris_reservations != '0' or agent.aquafun_reservations != '0' or agent.aquamirage_reservations != '0':
        messages.warning(request,'Reservation déjà faite!')
    else:
        if request.method == 'POST':
            if form_a.is_valid():
                agent.dinoland_reservations = form_a.cleaned_data.get('dinoland')
                agent.tamaris_reservations = form_a.cleaned_data.get('tamaris')
                agent.aquafun_reservations = form_a.cleaned_data.get('aquafun')
                agent.aquamirage_reservations = form_a.cleaned_data.get('aquamirage')
                agent.save()
            for n,form_c in enumerate(forms_c):
                if form_c.is_valid():
                    conjointe = conjointes[n]
                    conjointe.dinoland_reservations = form_c.cleaned_data.get('dinoland')
                    conjointe.tamaris_reservations = form_c.cleaned_data.get('tamaris')
                    conjointe.aquafun_reservations = form_c.cleaned_data.get('aquafun')
                    conjointe.aquamirage_reservations = form_c.cleaned_data.get('aquamirage')
                    conjointe.save()
            for n,form_e in enumerate(forms_e):
                if form_e.is_valid():
                    enfant = enfants[n]
                    enfant.dinoland_reservations = form_e.cleaned_data.get('dinoland')
                    enfant.tamaris_reservations = form_e.cleaned_data.get('tamaris')
                    enfant.aquafun_reservations = form_e.cleaned_data.get('aquafun')
                    enfant.aquamirage_reservations = form_e.cleaned_data.get('aquamirage')
                    enfant.save()
            messages.success(request, 'La réservation est faite avec succès')
        else:
            form = ReserverForm()
        ###
    dino_p,tam_p,aquaf_p,aquam_p=0,0,0,0
    for personnes in [agent,conjointes,enfants]:
        if personnes == agent:
            dino_p += int(personnes.dinoland_reservations)*constantes.DINOLAND_PRIX['adulte']
            tam_p += int(personnes.tamaris_reservations)*constantes.TAMARIS_PRIX['adulte']
            if personnes.aquafun_reservations[-1]=='D':
                aquaf_p += int(personnes.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['avec']['adulte']
            else:
                aquaf_p += int(personnes.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['sans']['adulte']
            if personnes.aquamirage_reservations[-1]=='D':
                aquam_p += int(personnes.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['avec']['adulte']
            else:
                aquam_p += int(personnes.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['sans']['adulte']
        else:
            for per in personnes:
                if isinstance(per,Conjointe) or per.age>12:
                    dino_p += int(per.dinoland_reservations)*constantes.DINOLAND_PRIX['adulte']
                    tam_p += int(per.tamaris_reservations)*constantes.TAMARIS_PRIX['adulte']
                    if per.aquafun_reservations[-1]=='D':
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['avec']['adulte']
                    else:
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['sans']['adulte']
                    if per.aquamirage_reservations[-1]=='D':
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['avec']['adulte']
                    else:
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['sans']['adulte']
                elif isinstance(per,Enfant) and per.age<2:
                    dino_p += 0
                    tam_p += 0
                    aquaf_p += 0
                    aquam_p += 0
                else:
                    dino_p += int(per.dinoland_reservations)*constantes.DINOLAND_PRIX['enfant']
                    tam_p += int(per.tamaris_reservations)*constantes.TAMARIS_PRIX['enfant']
                    if per.aquafun_reservations[-1]=='D':
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['avec']['enfant']
                    else:
                        aquaf_p += int(per.aquafun_reservations[0])*constantes.AQUAFUN_PRIX['sans']['enfant']
                    if per.aquamirage_reservations[-1]=='D':
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['avec']['enfant']
                    else:
                        aquam_p += int(per.aquamirage_reservations[0])*constantes.AQUAMIRAGE_PRIX['sans']['enfant']

    context = {
        'page_header_title' : 'reservation',
        'active_sidebar' : 'reservation',
        'agent':agent,'conjointes':conjointes,'enfants':enfants,'form_a':form_a,
        'forms_c':forms_c,'forms_e':forms_e,
        'dino_p':dino_p,'tam_p':tam_p,'aquaf_p':aquaf_p,'aquam_p':aquam_p,
        'prix_total':sum((dino_p,tam_p,aquaf_p,aquam_p)) 
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


def add_user(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Staff creé avec succès!")
        
    else:
        form = CustomUserCreationForm()
    context = {
        'page_header_title' : 'Ajouter Staff',
        'active_sidebar' : 'Ajouter Staff',
        'form':form,
    }
    return render(request,'admin_templates/add_user.html',context)


def upload_base(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '1':
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            
            df = pd.read_excel(excel_file)
            #drop the unamed columns
            df=df.loc[:, ~df.columns.str.startswith('Unnamed')]
            for index, row in df.iterrows():
                # Create Agent
                #if row['Matricule'] existe
                if not pd.isna(row['Matricule']):
                    agent = Agent(
                        matricule=row['Matricule'],
                        nom=row['Nom'],
                        prenom=row['Prénom'],
                        datenaissance=row['date_ naissance'].date(),
                        CIN=row['cin'],
                        categorie=row['categorie'],
                        sexe=row['code_ sexe'].lower(),
                        ent_affect=row['Ent_affect'],
                        dateembauche=row['date_ embauche'].date(),     
                    )
                    agent.save()

                    # Create Conjointes
                    for i in range(1, 3):  # Assuming you have two conjointes
                        conjointe_name = row[f'Nom et prénom Conjointe {i}']
                        conjointe_datenaissance = row[f'Date naissance Conjointe {i}']
                        if not pd.isna(conjointe_name) and not pd.isna(conjointe_datenaissance):
                            conjointe = Conjointe(
                                agent=agent,  # Associate with the Agent
                                datenaissance=conjointe_datenaissance.date(),
                                nom=' '.join(conjointe_name.split(' ')[:-1]),
                                prenom=conjointe_name.split(' ')[-1],
                            )
                            conjointe.save()
                        elif pd.isna(conjointe_name) and not pd.isna(conjointe_datenaissance):
                            conjointe = Conjointe(
                                agent=agent,  # Associate with the Agent
                                prenom='',
                                nom='',
                                datenaissance=conjointe_datenaissance.date(),
                            )
                            conjointe.save()
                        else:
                            pass

                    # Create Enfants
                    for i in range(1, 8):  # Assuming you have up to 7 enfants
                        enfant_name = row[f'Enfant {i}']
                        enfant_datenaissance=row[f"Date de naissance {i}"]
                        enfant_sexe=row[f"sexe \nenf {i}"]
                        if not pd.isna(enfant_name)  and not pd.isna(enfant_datenaissance) and not pd.isna(enfant_sexe):
                            enfant = Enfant(
                                agent=agent,  # Associate with the Agent
                                prenom=enfant_name.split(' ')[-1],
                                nom=' '.join(enfant_name.split(' ')[:-1]),
                                datenaissance=enfant_datenaissance.date(),
                                sexe=enfant_sexe.lower(),
                            )
                            enfant.save()
                        elif pd.isna(enfant_name) and pd.isna(enfant_datenaissance) and pd.isna(enfant_sexe):
                            pass
                        else:
                            try:
                                nomm=' '.join(enfant_name.split(' ')[:-1]),
                                prenomm=enfant_name.split(' ')[-1],
                            except:
                                nomm=''
                                prenomm=''
                            try:
                                sexee=enfant_sexe.lower(),
                            except:
                                sexee='m'
                            enfant = Enfant(
                                agent=agent,  # Associate with the Agent
                                prenom=prenomm,
                                nom=nomm,
                                datenaissance=enfant_datenaissance.date(),
                                sexe=sexee,
                            )
                            enfant.save()
            excel_table = df.to_html(classes='table table-bordered', index=False)
            #print(df.head())
            messages.success(request,'Votre fichier est uploadé avec succès!')
            context = {'form': form, 'excel_table': excel_table,
                       'page_header_title' : 'Upload Base',
                        'active_sidebar' : 'Upload Base',}
            return render(request, 'admin_templates/upload_base.html', context)
    else:
        form = ExcelUploadForm()
    context={
        'page_header_title' : 'Upload Base',
        'active_sidebar' : 'Upload Base',
        'form':form,
        #'excel_table':excel_table,
    }
    return render(request,'admin_templates/upload_base.html',context)

