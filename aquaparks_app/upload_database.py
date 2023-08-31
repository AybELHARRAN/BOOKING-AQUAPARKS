from .models import *
import pandas as pd
# Replace 'your_file.csv' with the actual file path
excel_file_path = ''
df=pd.read_excel(excel_file_path)
for index, row in df.iterrows():
    # Create Agent
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
