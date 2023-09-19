from django.db import models

from Admin.models import *


class Userregister(models.Model):

    userfirstname = models.CharField(max_length=50)

    userlastname = models.CharField(max_length=50)

    userphone = models.CharField(max_length=50)

    useremail = models.EmailField(max_length=50)

    userpassword = models.CharField(max_length=50)

    designation = models.CharField(default='User', max_length=50)


class Carouselimages(models.Model):

    Image  = models.ImageField(upload_to= 'carousel', default='null.jpg')

class TimeRange(models.Model):

    time = models.CharField(max_length=50, null = True)

    def __str__(self):

        return self.time



    
class Booknow(models.Model):

    userid = models.ForeignKey(Userregister, on_delete=models.CASCADE, null=True)

    ubookingname = models.CharField(max_length=50, null=True)

    ubookingemail = models.EmailField(max_length=50, null=True)

    ubookingphone = models.CharField(max_length=50, null=True)

    ubookingcategory = models.CharField(max_length=50, null=True)

    ubookingprice = models.CharField(max_length=50, null=True)

    ubookingaddress = models.ForeignKey(Turflocation, on_delete= models.CASCADE, null=True)

    ubookingdate = models.DateField(max_length=50, null=True)

    ubookingtime = models.ForeignKey(TimeRange ,max_length=50, null=True, on_delete=models.DO_NOTHING)

    ubookingstatus = models.CharField(max_length=50, default=0, null=True)

    upaymentstatus = models.CharField(default='unpaid', max_length=50)



class Userfeedback(models.Model):

    username = models.CharField(max_length=50, null=True)

    useremail = models.CharField(max_length=50, null=True)

    usersubject = models.CharField(max_length=50, null=True)

    usermessage = models.TextField(max_length=50, null=True)


class Availabletimeslots(models.Model):

    availabletime = models.CharField(max_length=50, null=True)

    def __str__(self):

        return self.availabletime