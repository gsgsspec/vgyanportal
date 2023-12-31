from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User_data(AbstractUser):
    id = models.AutoField(primary_key=True)
    usr_email = models.CharField(max_length=120)
    usr_password = models.CharField(max_length=60)

    class Meta:
        db_table = 'user_data'

@receiver(post_save, sender=User_data)
def create_auth_token_for_customer(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    imageurl = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=1, null=True) # A - Active, I - Inactive

    class Meta:
        db_table = 'subject'


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    about = models.CharField(max_length=500,null=True)
    experience = models.IntegerField(null=True)
    status = models.CharField(max_length=1, null=True) # A - Active, I - Inactive

    class Meta:
        db_table = 'instructor'


class CourseModule(models.Model):
    id = models.AutoField(primary_key=True)
    sequence = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    courseid = models.IntegerField(null=True)
    assesment = models.CharField(max_length=1,null=True) # Y - Needed,  N - Not Needed
    duration = models.IntegerField(null=True) # in hours
    status = models.CharField(max_length=1, null=True) # A - Active, I - Inactive

    class Meta:
        db_table = 'coursemodule'


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True)
    subjectid = models.IntegerField(null=True)
    about = models.CharField(max_length=500, null=True)
    outcomes = models.CharField(max_length=500, null=True)
    level = models.CharField(max_length=1,null=True) # B-  Beginners ,I - Intermediate ,A - Advanced
    instructorid = models.IntegerField(null=True)
    agegroup = models.CharField(max_length=1, null=True)
    language = models.CharField(max_length=1, null=True) # E - English, T - Telugu, H - Hindi
    duration = models.DecimalField(max_digits=10,decimal_places=2)
    timeframe = models.IntegerField(null=True) # in months
    certificate = models.CharField(max_length=1, null=True) # 'Y - Certificate will be issued\nN - No Certificate'
    price = models.DecimalField(max_digits=13,decimal_places=2)
    objectives = models.CharField(max_length=500, null=True)
    eligibility = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=1, null=True) # A - Active, I - Inactive

    class Meta:
        db_table = 'course'


class CourseMedia(models.Model):
    id = models.AutoField(primary_key=True)
    courseid = models.IntegerField(null=True)
    moduleid = models.IntegerField(null=True)
    lessonid = models.IntegerField(null=True)
    libraryid = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=1, null=True) # T - Thumbnail Pic, B - Banner Pic, P - Poster Pic
    mediaurl = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'coursemedia'


class CourseLesson(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True)
    courseid = models.IntegerField(null=True)
    type = models.CharField(max_length=1, null=True) # V - Video, I - Image, P - PDF, A - Audio
    medialurl = models.CharField(max_length=100, null=True)
    moduleid = models.IntegerField(null=True)
    sequence = models.IntegerField(null=True)
    duration = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=1, null=True) # A - Active, I - Inactive

    class Meta:
        db_table = 'courselesson'


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=2, null=True)
    agegroup = models.IntegerField(null=True)
    profilepicurl = models.CharField(max_length=100, null=True)
    dateregistered = models.DateTimeField(null=True)
    status = models.CharField(max_length=1, null=True) # A - Active, E - Expired

    class Meta:
        db_table = 'registration'


class CourseRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    registrationid = models.IntegerField(null=True)
    courseid = models.IntegerField(null=True)
    status = models.CharField(max_length=1, null=True) # A - Active, E - Expired
    dateofpurchase = models.DateTimeField(null=True)
    couponcode = models.CharField(max_length=20,null=True)

    class Meta:
        db_table = 'courseregistration'


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    registrationid = models.IntegerField(null=True)
    courseid = models.IntegerField(null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    reference = models.CharField(max_length=100, null=True)
    paymod = models.CharField(max_length=20, null=True)
    paydate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'payment'


class CourseRating(models.Model):
    id = models.AutoField(primary_key=True)
    registrationid = models.IntegerField(null=True)
    courseid = models.IntegerField(null=True)
    comments = models.CharField(max_length=500, null=True)
    rating = models.IntegerField(null=True)
    dateofrating = models.DateTimeField(null=True)
    instructorid = models.IntegerField(null=True)

    class Meta:
        db_table = 'courserating'


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    registrationid = models.IntegerField(null=True)
    courseid = models.IntegerField(null=True)
    question = models.CharField(max_length=100, null=True)
    questiondate = models.DateTimeField(null=True)
    answer = models.CharField(max_length=256, null=True)
    lessonid = models.IntegerField(null=True)
    moduleid = models.IntegerField(null=True)
    questionvideotime = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    status = models.CharField(max_length=1, null=True) # Y - Display, N - Not to Display
    answertype = models.CharField(max_length=1, null=True) # A - Answer, R - Refered Answer
    referquestionid = models.IntegerField(null=True)

    class Meta:
        db_table = 'question'


class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    registrationid = models.IntegerField(null=True)
    courseid = models.IntegerField(null=True)
    moduleid = models.IntegerField(null=True)
    assessmentdate = models.DateTimeField(null=True)
    remarks = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=1, null=True) # P - Pending, R - Reassessment, C - Cleared

    class Meta:
        db_table = 'assessment'


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    registrationid = models.IntegerField(null=True)
    courseid = models.IntegerField(null=True)
    moduleid = models.IntegerField(null=True)
    lessonid = models.IntegerField(null=True)
    activity = models.CharField(max_length=1, null=True)  # V - Video Play , D - Document Download, Q - Question, W - Last Watched video Id
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True)  # In seconds
    status = models.CharField(max_length=1, null=True) # C - Completed 

    class Meta:
        db_table = 'activity'


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    notifydate = models.DateTimeField(null=True)
    registrationid = models.IntegerField(null=True)
    courseid = models.IntegerField(null=True)
    moduleid = models.IntegerField(null=True)
    eventtype = models.CharField(max_length=1, null=True) # "Q" Questions , "A" Assessment
    message = models.CharField(max_length=512, null=True)
    type = models.CharField(max_length=1, null=True) #      "I" Information , "S" success, "W" Warning , "C" Critical
    status = models.CharField(max_length=1, null=True) #   "C" Clear from Board , "D" Deleted
    read = models.CharField(max_length=1, null=True) 

    class Meta:
        db_table = 'notification'


class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    couponfor = models.CharField(max_length=100, null=True) 
    couponcode = models.CharField(max_length=15, null=True)
    discount = models.IntegerField(null=True) 
    coupontype = models.CharField(max_length=1, null=True)  # D - By Date , C - By count
    validitydate = models.DateField(null=True)
    couponcount = models.IntegerField(null=True)
    remainingcount = models.IntegerField(null=True)
    datecreated = models.DateTimeField(null=True)  
    status =  models.CharField(max_length = 1 ,null=True)
     
    class Meta:
        db_table = 'coupon'
