from django.urls import path,include
from . import views ,admin_views, worker_views

urlpatterns = [
    #COMMON TEMPLATES
    path('',views.login_page,name='login_page'),
    path('do_login/', views.do_login,name='do_login'),
    path('do_logout/',views.do_logout,name='do_logout'),
    path('profil/',views.profil,name='profil_page'),
    path('aquaparks/',views.aquaparks,name='aquaparks_page'),
    path('download-agents-excel/<str:aquapark>', views.download_agents_excel, name='download_agents_excel'),


    #ADMIN
    path('administration/verification/<str:matricule>',admin_views.verification,name='verification_page'),
    path('administration/reservation/<str:action>',admin_views.chercher,name='chercher_page'),
    path('administration/reservation2/<str:matricule>',admin_views.reservation2,name='reservation2_page'),
    path('administration/ajouter_agent',admin_views.ajouter_agent,name='ajouter_agent_page'),
    path('administration/modifier_agent',admin_views.modifier_agent,name='modifier_agent_page'),
    path('administration/supprimer/<int:idd>/<str:type>',admin_views.supprimer,name='supprimer_page'),
    path('administration/ajouter_personne/<str:type>/<int:idd>',admin_views.ajouter_personne,name="ajouter_personne_page"),
    path('administration/modifier_personne/<str:type>/<int:idd>',admin_views.modifier_personne,name="modifier_personne_page"),
    path('administration/add_user',admin_views.add_user,name='add_user'),
    path('administration/upload_base',admin_views.upload_base,name='upload_base'),
    

    #WORKER
    path('worker/reservation/<str:matricule>',worker_views.reservation,name='worker_reservation_page'),
    path('worker/verification/<str:matricule>',worker_views.verification,name='worker_verification_page'),
    path('worker/chercher/<str:action>',worker_views.chercher,name='chercher_page_worker'),
    

]  
