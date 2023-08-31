from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from .forms import *

def verification(request, matricule):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '2':
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
    return render(request, 'worker_templates/verification.html',context)

def reservation(request, matricule):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '2':
        return HttpResponseForbidden()
    
    agent = Agent.objects.get(matricule=matricule)
    conjointes = Conjointe.objects.filter(agent=agent)
    enfants = Enfant.objects.filter(agent=agent)
    form_a = ReserverForm(request.POST or None,prefix='a')
    forms_c = [ReserverForm(request.POST or None,prefix=f'c{n}') for n in range(len(conjointes))]
    forms_e = [ReserverForm(request.POST or None,prefix=f'e{n}') for n in range(len(enfants))]
    print(matricule)
    print([conjointe for conjointe in conjointes])
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
    context = {
        'page_header_title' : 'reservation',
        'active_sidebar' : 'reservation',
        'agent':agent,'conjointes':conjointes,'enfants':enfants,'form_a':form_a,
        'forms_c':forms_c,'forms_e':forms_e,
    }
    return render(request, 'worker_templates/reservation.html', context)

def chercher(request,action):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    if request.user.user_type != '2':
        return HttpResponseForbidden()
    
    form = ChercherAgentForm(request.POST or None)
    if action == 'reservation':
        if request.method == 'POST':
            if form.is_valid():
                matricule = form.cleaned_data.get('matricule')
                try:
                    Agent.objects.get(matricule=matricule)
                    return redirect(reverse('worker_reservation_page',args=[matricule]))
                except Agent.DoesNotExist:
                    messages.warning(request, 'Matricule invalide')
    if action == 'verification':
        if request.method == 'POST':
            if form.is_valid():
                matricule = form.cleaned_data.get('matricule')
                try:
                    Agent.objects.get(matricule=matricule)
                    return redirect(reverse('worker_verification_page',args=[matricule]))
                except Agent.DoesNotExist:
                    messages.warning(request, 'Matricule invalide')
    context = {
        'page_header_title' : action,
        'active_sidebar' : action,
        'form':form,
    }
    return render(request, 'worker_templates/chercher.html', context)