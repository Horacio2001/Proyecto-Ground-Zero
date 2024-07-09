from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import path, include 
from .views import *
from rest_framework import routers
from . import views



#Api
router = routers.DefaultRouter()
router.register('empleados', EmpleadoViewSet)
router.register('tipoempleados', TipoEmpleadoViewSet)
router.register('genero', GeneroViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login , name='login'),
    path('gestion/', gestion, name='gestion'),
    path('autor/', agregar_autor, name='autor'),
    path('contacto/', contacto, name='contacto'),
    path('modificar/<id_obra>/', modificar_obra, name='modificar'),
    path('eliminar/<id_obra>/', eliminar_obra, name='eliminar'),
    path('detalle/<id_obra>/', detalle, name='detalle'),
    path('register/', register, name='register'), 
    path('suscripcion/', suscripcion, name='suscripcion'),
    path('bloqueo/', bloqueo_view, name='bloqueo'),
    path('guardar_pago/', views.guardar_pago, name='guardar_pago'),
    path('historial/', historial, name='historial'),
    path('voucher/', voucher, name='voucher'),
    path('generar-pdf/<int:pago_id>/', views.generar_pdf, name='generar_pdf'),
    

    # Reset password URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #API
    path('api/', include(router.urls)),
    path('obrasapi/', empleadosapi, name='obrasapi'), 
    path('monedaapi/', dineroapi, name='monedaapi'), 

    #captcha
    path('captcha/', include('captcha.urls')),
]

    
