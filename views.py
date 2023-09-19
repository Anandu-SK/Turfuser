from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
import stripe
from django.conf import settings
import re
from django.http import HttpResponse

from Admin.models import *
from User.models import *
from Manager.models import *


def userregistration(request):

    if request.method == 'POST':

        uFname = request.POST['uFname']

        uLname = request.POST['uLname']

        uPhone = request.POST['uPhone']

        uEmail = request.POST['uEmail']

        uPassword = request.POST['uPassword']

        if Userregister.objects.filter(useremail = uEmail).exists() or Managerregister.objects.filter(manageremail = uEmail).exists():

            return render(request, 'userregistration.html', {'msg1': 'This Email address already exists'})
        
        else:

            Userregister.objects.create(userfirstname = uFname, userlastname = uLname, userphone = uPhone, useremail = uEmail, userpassword = uPassword)

            return redirect('login_for_all')
    
    return render(request, 'userregistration.html')


def districtdropdown(request):

    data = Districts.objects.all()

    carouselimages = Carouselimages.objects.all()

    return render(request, 'districtdropdown.html', {'data':data , 'carouselimages':carouselimages})


def userdashboard(request):

    carouselimages = Carouselimages.objects.all()

    return render(request, 'userdashboard.html', {'carouselimages':carouselimages})


def turflocationdropdown(request, locationId):

    locationinstance = Districts.objects.get(id=locationId)

    Turfs_under_location = Turflocation.objects.filter(turflocation = locationinstance)

    carouselimages = Carouselimages.objects.all()

    return render(request, 'Turfs_undera_district.html', {'Turfs_under_location':Turfs_under_location, 'carouselimages':carouselimages})




def bookturf(request, iTurfid):

    if 'u_id' in request.session:

        individual_turf = Turflocation.objects.filter(id=iTurfid)

        individual_turfaddress = Turflocation.objects.get(id=iTurfid).turfaddress

        request.session['uturfaddress'] = individual_turfaddress


        individual_turf_price = Turflocation.objects.get(id=iTurfid).placeprice
        
        request.session['individual_turf_price_amt'] = individual_turf_price


        turfcategory = Turfcategory.objects.all()

        timerange = TimeRange.objects.all()

        # timerange = request.session.get('filtered_times')

        # print("=======================================")

        # print(timerange)

        # print("=======================================")

        turfextraimages = Extraimages.objects.filter(location__id=iTurfid)

        bookedtime = Booknow.objects.all()

        context = {

            'individual_turf':individual_turf, 'timerange':timerange,

            'turfcategory':turfcategory, 'turfextraimages':turfextraimages,

            'bookedtime':bookedtime, 'iTurfid': iTurfid
        }

        return render(request, 'bookturf.html', context)
    
    else:

        next_url = reverse('bookturf', args=[iTurfid])

        login_url = next_url

        request.session['loginsession'] = login_url

        messages.warning(request,"Please login first before going any further")

        return redirect('login_for_all')
    
def get_price(request):

    basic_price = request.session.get('individual_turf_price_amt')

    category_id = request.GET['category_id']

    category_price = Turfcategory.objects.get(id = category_id).categoryprice

    final_amount = int(category_price) + int(basic_price)

    return render(request, 'getprice.html', locals())



def get_time(request):

    uTurfaddress = request.session.get('uturfaddress')

    turfid = Turflocation.objects.get(turfaddress = uTurfaddress).id

    ubookdates = request.GET['booking_id']
            
    all_time_ranges = TimeRange.objects.filter()

    list_of_not_booked_times = []

    booked_time_ranges_list = []

    if Booknow.objects.filter(ubookingaddress = turfid, ubookingdate = ubookdates).exists():

        all_time_list = []

        for all_time in all_time_ranges:

            all_time_list.append(all_time)


        booked_time_ranges = Booknow.objects.filter(ubookingaddress = turfid, ubookingdate = ubookdates)

        for booked_time in booked_time_ranges:

            booked_time_ranges_list.append(booked_time.ubookingtime)

        for all_time in all_time_list:

            if all_time in booked_time_ranges_list:

                pass

            else:

                list_of_not_booked_times.append(all_time.time)
    else:

        for all_time in all_time_ranges:

            list_of_not_booked_times.append(all_time.time)

    context = {

        'list_of_not_booked_times':list_of_not_booked_times
    }

    return render(request, 'gettime.html', context)

    

stripe.api_key = settings.STRIPE_SECRET_KEY

def booknow(request, Turfid):

        if request.method == 'POST':

            action_type = request.POST.get("actionType")

            userid = request.session.get('u_id')

            useridinstance = Userregister.objects.get(id = userid).id

            request.session['uidsession'] = useridinstance

            uName = request.POST['uName']

            request.session['unamesession'] = uName

            uEmailaddress = request.POST['uEmail']

            request.session['uemailsession'] = uEmailaddress

            uPhone = request.POST['uPhone']

            request.session['uphonesession'] = uPhone

            uTurfCategory = request.POST['uTurfCategory']

            uTurfCategoryvalue = Turfcategory.objects.get(id = uTurfCategory).category

            request.session['ucategorysession'] = uTurfCategoryvalue

            uPrice = request.POST['uPrice']

            request.session['upricesession'] = uPrice

            uTurfaddress = request.POST['uTurfaddress']

            uPricesplit = re.sub(r'\D', '' , uPrice)

            turfaddressinstance = Turflocation.objects.get(id = Turfid).turfaddress

            request.session['uaddresssession'] = turfaddressinstance

            uDate = request.POST['uDate']

            request.session['udatesession'] = uDate

            uTimeslotvalue = request.POST['uTimeslot']

            uTimeslot = TimeRange.objects.get(time = uTimeslotvalue).time

            request.session['utimesession'] = uTimeslot

            turf_details  = Turflocation.objects.get(id = Turfid)

            if action_type == "action1":

                session = stripe.checkout.Session.create(

                payment_method_types = ['card'],

                line_items=[{
                        'price_data':{
                            'currency': 'inr',
                            'product_data':{
                                'name': turf_details.tname,
                            },
                            'unit_amount': int(uPricesplit)*100,
                        
                        },
                        'quantity':1,
                }],
                mode='payment',
                success_url = "http://127.0.0.1:8000/paynowsuccesspage?session_id={CHECKOUT_SESSION_ID}",
                cancel_url = "http://127.0.0.1:8000/pay_cancel",
                client_reference_id=Turfid,
                )
                return redirect(session.url, code=303)
            
            elif action_type == 'action2':

                return redirect('paylatersuccesspage')
            
        return render(request, 'bookturf.html' )


def allturfs(request):

    carouselimages = Carouselimages.objects.all()

    allturfs = Turflocation.objects.all()

    context = {

        'carouselimages':carouselimages, 'allturfs':allturfs
    }

    return render(request, 'allturfs.html', context)


def bookinghistory(request):

    if 'u_id' in request.session:

        usersession = request.session.get('u_id')

        userbookings_list = []

        userbookings  = Booknow.objects.filter(userid = usersession)

        for i in userbookings:

            userbookings_list.append(i)
        
        userbookings_list_length = len(userbookings_list)

        return render(request, 'userbookingspage.html', {'userbookings':userbookings, 'userbookings_list_length':userbookings_list_length})
    else:
        return redirect('login_for_all')


def paynowsuccesspage(request):

    session = stripe.checkout.Session.retrieve(request.GET['session_id'])

    Turfid = session.client_reference_id

    usersessionid = request.session.get('u_id')

    userdetails = Userregister.objects.get(id = usersessionid)
    uName = request.session.get('unamesession')
    uEmailaddress = request.session.get('uemailsession')
    uPhone = request.session.get('uphonesession')
    uTurfCategoryvalue = request.session.get('ucategorysession')
    uPrice = request.session.get('upricesession')
    turfaddressinstance = request.session.get('uaddresssession')
    turfdetails = Turflocation.objects.get(turfaddress = turfaddressinstance)

    uDate = request.session.get('udatesession')
    uTimeslot = request.session.get('utimesession')

    timedetails = TimeRange.objects.get(time = uTimeslot)


    Booknow.objects.create(userid = userdetails, ubookingname = uName,ubookingemail = uEmailaddress, ubookingphone = uPhone, ubookingcategory = uTurfCategoryvalue, ubookingprice = uPrice, ubookingaddress = turfdetails,ubookingdate = uDate, ubookingtime = timedetails )

    data = Booknow.objects.filter(userid = userdetails, upaymentstatus = 'unpaid').order_by('-id')[:1]

    data1 = Booknow.objects.filter(userid = userdetails, upaymentstatus = 'unpaid').order_by('-id').first()


    if data1:

        data1.upaymentstatus = 'paid'

        data1.save()
    else:

        pass


    del request.session['individual_turf_price_amt']

    if 'uturfaddressinstance' in request.session:
        del request.session['uturfaddressinstance']
    if 'usersessionid' in request.session:
        del request.session['usersessionid']
    if 'uName' in request.session:
        del request.session['uName']
    if 'uPhone' in request.session:
        del request.session['uPhone']
    if 'uTurfCategoryvalue' in request.session:
        del request.session['uTurfCategoryvalue']
    if 'uPrice' in request.session:
        del request.session['uPrice']
    if 'uDate' in request.session:
        del request.session['uDate']
    if 'uTimeslot' in request.session:
        del request.session['uTimeslot']

    return render(request, 'successpage.html', {'data':data})


def paylatersuccesspage(request):

    usersessionid1 = request.session.get('u_id')
    userdetails = Userregister.objects.get(id = usersessionid1)
    uName1 = request.session.get('unamesession')
    uEmail1 = request.session.get('uemailsession')
    uPhone1 = request.session.get('uphonesession')
    uTurfCategoryvalue1 = request.session.get('ucategorysession')
    uPrice1 = request.session.get('upricesession')
    turfaddressinstance1 = request.session.get('uaddresssession')
    turfdetails = Turflocation.objects.get(turfaddress = turfaddressinstance1)
    turfid = turfdetails.id

    uDate1 = request.session.get('udatesession')
    uTimeslot1 = request.session.get('utimesession')

    timedetails = TimeRange.objects.get(time = uTimeslot1)

    if Booknow.objects.filter(ubookingdate = uDate1, ubookingtime = timedetails).exists():

         messages.warning(request,"This timeslot is already booked")

         return redirect(reverse('bookturf', args=[turfid]))

    else:

        Booknow.objects.create(userid = userdetails, ubookingname = uName1,ubookingemail = uEmail1, ubookingphone = uPhone1, ubookingcategory = uTurfCategoryvalue1, ubookingprice = uPrice1, ubookingaddress = turfdetails,ubookingdate = uDate1, ubookingtime = timedetails )

        data = Booknow.objects.filter(userid = userdetails, upaymentstatus = 'unpaid').order_by('-id')[:1]

    if 'uturfaddressinstance1' in request.session:
        del request.session['uturfaddressinstance1']
    if 'usersessionid1' in request.session:
        del request.session['usersessionid1']
    if 'uName1' in request.session:
        del request.session['uName1']
    # if 'uEmail1' in request.session:
    #     del request.session['uEmail1']
    if 'uPhone1' in request.session:
        del request.session['uPhone1']
    if 'uTurfCategoryvalue1' in request.session:
        del request.session['uTurfCategoryvalue1']
    if 'uPrice1' in request.session:
        del request.session['uPrice1']
    if 'uDate1' in request.session:
        del request.session['uDate1']
    if 'uTimeslot1' in request.session:
        del request.session['uTimeslot1']


    return render(request, 'successpage.html', {'data':data})


def userfeedback(request):

    if request.method == 'POST':

        uname = request.POST['name']
        uemail = request.POST['email']
        usubject = request.POST['subject']
        umessage = request.POST['message']


        Userfeedback.objects.create(username = uname, useremail = uemail, usersubject = usubject, usermessage = umessage)

        return redirect('index')
    
def preloader(request):

    return render(request, 'index.html')


  