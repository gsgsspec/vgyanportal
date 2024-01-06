
import os
import secrets
import string
import razorpay
from vgyanportal import settings
from app_api.models import Registration, User_data, CourseRating, Course, Payment, CourseRegistration, Question, CourseMedia, \
    Assessment,CourseLesson , Notification ,CourseModule, Coupon
from datetime import datetime
from  .mailing import sendRegistrainMail
from vgyanportal.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET
from vgyanportal.metadata import getConfig


def addUserDB(dataObjs):
    try:

        razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))

        params_dict = {
            'razorpay_order_id': dataObjs['order_id'],
            'razorpay_payment_id': dataObjs['payment_id'],
            'razorpay_signature': dataObjs['signature']
		}
        
        verification =  razorpay_client.utility.verify_payment_signature(params_dict)

        if verification == True:

            payment_details = razorpay_client.payment.fetch(dataObjs['payment_id'])
            
            user_email = dataObjs['email']
            user_check = Registration.objects.filter(email=user_email)

            if user_check :

                registration = Registration.objects.get(email=user_email)
            else:
                
                random_password = generate_random_password()
                
                registration = Registration(
                    firstname = dataObjs['first_name'],
                    lastname = dataObjs['last_name'],
                    email = dataObjs['email'],
                    password = random_password,
                    profilepicurl = "user_profile/default.png",
                    dateregistered = datetime.now(),
                    status = 'A'
                )

                registration.save()

            course_payment = Payment(
                registrationid = registration.id,
                courseid = dataObjs["course_id"],
                amount = payment_details["amount"] / 100,
                paymod = payment_details["method"],
                paydate = datetime.now()
            )

            course_payment.save()
            
            
            if dataObjs["coupon_code"] != None:
                coupon_code = dataObjs["coupon_code"]
                coupon = Coupon.objects.filter(couponcode=coupon_code,status='A').last()

                if coupon:
                    if coupon.coupontype == 'C':
                        current_count = coupon.remainingcount
                        coupon.remainingcount = int(current_count) - 1
                        coupon.save()

            else :
                coupon_code = None
            

            course_registration = CourseRegistration(
                registrationid = registration.id,
                courseid = dataObjs["course_id"],
                status = "A",
                couponcode = coupon_code
            )

            course_registration.save()
            
            course_title = Course.objects.get(id=dataObjs["course_id"]).title
            web_domain = getConfig()['MEDIA']['web_domain']
            portal_domain = getConfig()['MEDIA']['domain']
            img_url = CourseMedia.objects.get(courseid=dataObjs["course_id"], type='T').mediaurl

            mail_data = {'email':user_email,'password':registration.password,'url':portal_domain,'name':registration.firstname,'course':course_title,'img_url':f"{web_domain}{img_url}"}

            sendRegistrainMail(mail_data)

    except Exception as e:
        print(str(e))
        raise


def generate_random_password(length=15):
    try:
        characters = string.ascii_letters + string.digits

        password = ''.join(secrets.choice(characters) for _ in range(length))

        return password
    
    except Exception as e:
        raise


def saveProfileDetailsDB(dataObjs, fileObjs):
    try:

        user_profile = Registration.objects.get(email=dataObjs['email'])
        user_profile.firstname = dataObjs['firstname']
        user_profile.lastname = dataObjs['lastname']
        user_profile.password = dataObjs['password']
        # user_profile.country = dataObjs['country']

        user_img = fileObjs.get('file')

        if user_img:

            img_file = os.path.splitext(user_img.name)
            img_extension = img_file[1]

            user_img_name = f"{user_profile.id}_{user_profile.firstname}{img_extension}"
            img_path = os.path.join(settings.MEDIA_ROOT,'user_profile',user_img_name)

            with open(img_path, 'wb+') as user_image:
                for chunk in user_img.chunks():
                    user_image.write(chunk)

            user_profile.profilepicurl = f"user_profile/{user_img_name}"
        
        user_profile.save()

        user_auth = User_data.objects.get(usr_email=dataObjs['email'])
        user_auth.usr_password = dataObjs['password']
        user_auth.save()

    except Exception as e:
        raise


def saveCourseRatingDB(dataObjs,user):
    try:

        user_id = Registration.objects.get(email=user).id
        instructor_id = Course.objects.get(id=dataObjs["course_id"]).instructorid

        try:
            course_rating = CourseRating.objects.get(courseid=dataObjs["course_id"],registrationid=user_id)
            course_rating.rating = dataObjs["rating"]
            course_rating.comments = dataObjs["comments"]
            course_rating.save()

        except:
            course_rating = CourseRating(
                courseid = dataObjs["course_id"],
                registrationid=user_id,
                rating = dataObjs["rating"],
                comments = dataObjs["comments"],
                instructorid  = instructor_id,
                dateofrating = datetime.now()
            )
            course_rating.save()

        return course_rating.rating
    
    except Exception as e:
        raise


def saveAskQuestionDb(dataObjs):
    try:
        lessonId = dataObjs['lessonId']['lesson_id']
        
        courseLessonDetails = CourseLesson.objects.filter(id = lessonId).last()

        getcourseid = courseLessonDetails.courseid
        courseModuleId =  courseLessonDetails.moduleid
        courseLessonId =  courseLessonDetails.id

        userEmail = dataObjs['userId']
        getUserRegisterId = Registration.objects.filter(email = userEmail).last()
        
        userid = getUserRegisterId.id

        getQuestion = dataObjs['question']
        vidCurrentTime = dataObjs['videotimecurr']
        
        saveQuestion = Question(
            registrationid = userid,
            courseid = getcourseid if getcourseid != "" else 0,
            moduleid = courseModuleId if courseModuleId != "" else 0,
            lessonid = courseLessonId if courseLessonId != "" else 0,
            question = getQuestion if getQuestion != '' else "",
            questionvideotime = vidCurrentTime,
            questiondate = datetime.now()
        )
        saveQuestion.save()

        notificationType = {
            "notifiType" : 'Q',
            "Action"     : 'newQuestion' ,
            "user_id"    : userid,  
            "courseid"   : getcourseid,
            "courseModule" : courseModuleId
        }

        saveNotificationData(notificationType)
        
    except Exception as e:
        raise



def saveAssessmentData(dataObjs,user):
    try:

        userid = Registration.objects.get(email=user).id

        Assessment(
            registrationid = userid,
            courseid = dataObjs["course_id"],
            moduleid = dataObjs["module_id"],
            assessmentdate = datetime.now(),
            status = 'P'
        ).save()

        notificationType = {
            "notifiType" : 'A' ,
            "Action"     : 'newAssessment' ,
            "user_id"    : userid, 
            "courseid"   : dataObjs["course_id"],
            "courseModule" : dataObjs["module_id"]
        }

        saveNotificationData(notificationType)

    except Exception as e:
        raise
        

def saveNotificationData(dataObjs):
    try:
        notifType   = dataObjs['notifiType']
        notifAction = dataObjs['Action']
        userId      = dataObjs['user_id']
        notifCourseId = dataObjs['courseid']
        notifModuleId = dataObjs['courseModule']

        notificationEventType = "N"
        notificationMessage   = 'all conditions Failed'
        messageType = 'I'

        getCourseName = Course.objects.filter(id = notifCourseId).last()
        getCourseModuleName = CourseModule.objects.filter(id = notifModuleId).last()
        courseName = getCourseName.title
        courseModuleName = getCourseModuleName.name

        if notifType:
            if notifType == "A":
                if notifAction == "newAssessment":
                    notificationEventType = "A"
                    notificationMessage = 'Your Assessment for '+str(courseModuleName)+' in pending'
                    messageType = "I"
        
            if notifType == "Q":
                if notifAction == "newQuestion":
                    notificationEventType = "Q"
                    notificationMessage = 'Your Question in '+str(courseModuleName)+ ' is Posted for answer'
                    messageType = "S"


        saveNotificationDb = Notification(
            notifydate     = datetime.now() ,
            registrationid = userId ,
            courseid       = notifCourseId ,
            moduleid       = notifModuleId,
            eventtype      = notificationEventType ,
            message        = notificationMessage ,
            type           = messageType ,
            status         = None
        )
        saveNotificationDb.save()
    
    except Exception as e:
        raise