from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate , login , logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
import pandas as pd
import io

# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse('chercher_page',args=['verification']))
        return redirect(reverse('chercher_page_worker',args=['verification']))
    return render(request,'aquaparks_app/login.html')

def do_login(request):
    if request.method != "POST":
        return render(request , 'common_templates/stop.html')
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request , username=username , password=password) 
    action = 'verification'
    if user is not None :
        login(request, user)
        messages.success(request, 'You have logged successfuly!')
        if user.user_type =='1':
            return redirect(reverse('chercher_page', args=[action]))
        return redirect(reverse('chercher_page_worker',args=['verification']))
    messages.warning(request, 'ERROR! Username or Password is invalid')
    return redirect('/')

def do_logout(request):
    if request.user is not None:
        logout(request)
        messages.info(request, 'You have logged out!')
    return redirect('login_page')

def profil(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    
    context = {
        'page_header_title' : 'profil',
        'active_sidebar' : 'profil',
    }
    return render(request, 'common_templates/profil.html', context)

def aquaparks(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login_page'))
    
    dino,tam,aquaf,aquam = 0,0,0,0
    for model in [Agent,Conjointe,Enfant]:
        for instance in model.objects.all():
            dino += int(instance.dinoland_reservations)
            tam += int(instance.tamaris_reservations)
            aquaf += int(instance.aquafun_reservations[0])
            aquam += int(instance.aquamirage_reservations[0])
    print(f"din={dino}__tam={tam}__aquaf={aquaf}__aquam={aquam}")
    context = {
        'page_header_title' : 'aquaparks',
        'active_sidebar' : 'aquaparks',
        'dino':dino, 'tam':tam, 'aquaf':aquaf, 'aquam':aquam,
    }
    return render(request, 'common_templates/aquaparks.html', context)

def export_agents_excel(aquapark):
    # Query the Agent model to get all agents
    agents = Agent.objects.all()

    # Create a Pandas DataFrame to store the data
    data = []
    if aquapark == 'dinoland':
        for agent in agents:
            adulte_r,enfant_r=0,0
            conjointes = Conjointe.objects.filter(agent=agent)
            enfants = Enfant.objects.filter(agent=agent)
            adulte_r += int(agent.dinoland_reservations)
            for conjointe in conjointes:
                adulte_r += int(conjointe.dinoland_reservations)
            for enfant in enfants:
                if enfant.age<12 and enfant.age>2:
                    enfant_r += int(enfant.dinoland_reservations)
                if enfant.age >= 12:
                    adulte_r += int(enfant.dinoland_reservations[0])
            row = {
                'Matricule': agent.matricule,
                'Nom': agent.nom,
                'Prénom': agent.prenom,
                'email':agent.email,
                'Téléphone':agent.telephone,
                'Ticket adulte': adulte_r,
                'Ticket enfant': enfant_r,
            }
            data.append(row)
        
    if aquapark == 'tamaris':
        for agent in agents:
            adulte_r,enfant_r=0,0
            conjointes = Conjointe.objects.filter(agent=agent)
            enfants = Enfant.objects.filter(agent=agent)
            adulte_r += int(agent.tamaris_reservations)
            for conjointe in conjointes:
                adulte_r += int(conjointe.tamaris_reservations)
            for enfant in enfants:
                if enfant.age<12 and enfant.age>2:
                    enfant_r += int(enfant.tamaris_reservations)
                if enfant.age >= 12:
                    adulte_r += int(enfant.tamaris_reservations[0])
            row = {
                'Matricule': agent.matricule,
                'Nom': agent.nom,
                'Prénom': agent.prenom,
                'email':agent.email,
                'Téléphone':agent.telephone,
                'Ticket adulte': adulte_r,
                'Ticket enfant': enfant_r,
            }
            data.append(row)
    if aquapark == 'aquafun':
        for agent in agents:
            adulte_r,enfant_r=0,0
            conjointes = Conjointe.objects.filter(agent=agent)
            enfants = Enfant.objects.filter(agent=agent)
            adulte_r += int(agent.aquafun_reservations[0])
            for conjointe in conjointes:
                adulte_r += int(conjointe.aquafun_reservations[0])
            for enfant in enfants:
                if enfant.age<12 and enfant.age>2:
                    enfant_r += int(enfant.aquafun_reservations[0])
                if enfant.age >= 12:
                    adulte_r += int(enfant.aquafun_reservations[0])
            row = {
                'Matricule': agent.matricule,
                'Nom': agent.nom,
                'Prénom': agent.prenom,
                'email':agent.email,
                'Téléphone':agent.telephone,
                'Ticket adulte': adulte_r,
                'Ticket enfant': enfant_r,
            }
            data.append(row)
    if aquapark == 'aquamirage':
        for agent in agents:
            adulte_r,enfant_r=0,0
            conjointes = Conjointe.objects.filter(agent=agent)
            enfants = Enfant.objects.filter(agent=agent)
            adulte_r += int(agent.aquamirage_reservations[0])
            for conjointe in conjointes:
                adulte_r += int(conjointe.aquamirage_reservations[0])
            for enfant in enfants:
                if enfant.age<12 and enfant.age>2:
                    enfant_r += int(enfant.aquamirage_reservations[0])
                if enfant.age >= 12:
                    adulte_r += int(enfant.aquamirage_reservations[0])
                
            row = {
                'Matricule': agent.matricule,
                'Nom': agent.nom,
                'Prénom': agent.prenom,
                'email':agent.email,
                'Téléphone':agent.telephone,
                'Ticket adulte': adulte_r,
                'Ticket enfant': enfant_r,
            }
            data.append(row)

    df = pd.DataFrame(data)

    # Create an in-memory Excel writer using BytesIO
    excel_file = io.BytesIO()
    excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    # Convert the DataFrame to an Excel sheet
    df.to_excel(excel_writer, sheet_name='Agents', index=False)

    # Get the xlsxwriter workbook and worksheet objects
    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Agents']

    # Add additional formatting if needed
    # ...

    # Close the Pandas Excel writer and output the Excel file
    excel_writer.save()

    # Seek to the beginning of the BytesIO stream
    excel_file.seek(0)

    return excel_file

# In your view function
def download_agents_excel(request,aquapark):
    excel_file = export_agents_excel(aquapark)

    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    response['Content-Disposition'] = f"attachment; filename=liste_{aquapark}.xlsx"
    return response