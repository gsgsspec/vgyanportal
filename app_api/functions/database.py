
import os
import secrets
import string
import razorpay
from vgyanportal import settings
from app_api.models import Registration, User_data, CourseRating, Course, Payment, CourseRegistration
from datetime import datetime
from  .mailing import sendRegistrainMail
from vgyanportal.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET


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

            course_registration = CourseRegistration(
                registrationid = registration.id,
                courseid = dataObjs["course_id"],
                status = "A"
            )

            course_registration.save()
            
            sendRegistrainMail()

    except Exception as e:
        print(str(e))
        raise


def generate_random_password(length=15):
    try:
        characters = string.ascii_letters + string.digits + string.punctuation

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
        user_profile.country = dataObjs['country']

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