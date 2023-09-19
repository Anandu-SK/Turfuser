from django.urls import path
from User.views import *


urlpatterns = [

    path('userregistration/', userregistration, name='userregistration'),
    path('userdashboard/',userdashboard, name='userdashboard'),
    path('districtdropdown', districtdropdown, name='districtdropdown'),
    path('turflocationdropdown/<int:locationId>/', turflocationdropdown, name='turflocationdropdown'),
    path('bookturf/<int:iTurfid>/', bookturf, name='bookturf'),
    path('get-price/', get_price, name='get_price' ),
    path('get-time/', get_time, name='get_time'),
    path('booknow/<int:Turfid>/', booknow, name='booknow'),
    # path('index/#intro', index, name='index'),
    path('allturfs/', allturfs, name='allturfs'),
    path('bookinghistory/', bookinghistory, name='bookinghistory'),
    path('paynowsuccesspage', paynowsuccesspage, name = 'paynowsuccesspage'),
    path('paylatersuccesspage/', paylatersuccesspage, name='paylatersuccesspage'),
    path('userfeedback/', userfeedback, name='userfeedback'),
    path('preloader/', preloader, name = 'preloader'),
]