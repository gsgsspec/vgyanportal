from rest_framework.authtoken.models import Token
from vgyanportal.metadata import getConfig
from .database import addUserDB, saveProfileDetailsDB
from app_api.models import Registration, User_data , CourseRegistration, Course, CourseRating, CourseLesson, CourseModule, CourseMedia


def authentication_service(dataObjs):
    try:
        user = Registration.objects.get(email=dataObjs['email'],password=dataObjs['password'],status='A')
    except:
        return (None,)
    
    try:
        if user:
            check1 = User_data.objects.filter(usr_email=user.email, usr_password=user.password)
            if not check1:
                User_data(username=user.email, usr_email=user.email, usr_password=user.password, is_staff=True).save()
            token_obj = Token.objects.filter(user__usr_email=user.email).order_by('-created').first()
            user_data = User_data.objects.get(usr_email=user.email, usr_password=user.password)
            user_data.is_staff = True 
            user_data.save()
            if token_obj:
                return token_obj.key
            else:
                check = User_data.objects.filter(usr_email=user.email).first()
                token_obj, token_flag = Token.objects.get_or_create(user=check)
                return token_obj.key
    except Exception as e:
        print(str(e))
        raise


def addUserService(dataObjs):
    try:

        addUserDB(dataObjs)

    except Exception as e:
        raise


def getMyCourses(userId):
    courseList = []
    getCourse = CourseRegistration.objects.filter(registrationid = userId).values()
    for getcourse in getCourse:
        if getcourse['status'] == "A":
            courseId = getcourse['courseid']
            if courseId:
                getCourseDetails = Course.objects.filter(id = courseId).last()

                courseDetails = {
                    "id"           : getCourseDetails.id,
                    "title"        : getCourseDetails.title,
                    "subjectid"    : getCourseDetails.subjectid,
                    "about"        : getCourseDetails.about,
                    "outcomes"     : getCourseDetails.outcomes,
                    "level"        : getCourseDetails.level,
                    "instructorid" : getCourseDetails.instructorid,
                    "agegroup"     : getCourseDetails.agegroup,
                    "language"     : getCourseDetails.language,
                    "duration"     : getCourseDetails.duration,
                    "timeframe"    : getCourseDetails.timeframe,
                    "certificate"  : getCourseDetails.certificate,
                    "price"        : getCourseDetails.price,
                    "objectives"   : getCourseDetails.objectives,
                    "eligibility"  : getCourseDetails.eligibility,
                    "status"       : getCourseDetails.status,
                }
                
                courseList.append(courseDetails)
    return courseList


def getUserProfile(user_email):
    try:

        user = Registration.objects.get(email=user_email)
        media_domain = getConfig()['MEDIA']['media_domain']

        user_data = {
            'first_name': user.firstname,
            'last_name':user.lastname,
            'email':user.email,
            'password':user.password,
            'country':user.country if user.country else "",
            'profile_img': f"{media_domain}{user.profilepicurl}"
        }

        return user_data

    except Exception as e:
        raise


def saveProfileDetails(dataObjs, fileObjs):
    try:
        saveProfileDetailsDB(dataObjs, fileObjs)
    except Exception as e:
        raise


def getCourseDetails(cid):
    try:

        course = Course.objects.get(id=cid)

        course_details = {
            'courseid':course.id,
            'title':course.title,
            'module': None,
            # 'instructor_details':None,
        }

        c_module = CourseModule.objects.filter(courseid=cid,status='A').order_by('sequence')

        module_details = []

        for module in c_module:

            c_lesson = CourseLesson.objects.filter(courseid=cid,moduleid=module.id,status='A').order_by('sequence')

            lesson_title = []

            for lesson in c_lesson:
                lesson_title.append({
                    'title':lesson.title
                })

            module_details.append({
                'module_name':module.name,
                'lesson_title': lesson_title
            })


        # instructor = Instructor.objects.get(id=course.instructorid,status='A')
        # instructor_rating = CourseRating.objects.filter(instructorid=instructor.id).aggregate(avg_rating=Avg('rating'))
        # instructor_courses = Course.objects.filter(instructorid=instructor.id).count()

        # instructor_details = {
        #     'name': instructor.name,
        #     'rating':instructor_rating['avg_rating'],
        #     'courses': instructor_courses,
        #     'about':instructor.about,
        #     'experience':instructor.experience
        # }

        course_details["module"] = module_details
        # course_details["instructor_details"] = instructor_details

        return course_details


    except Exception as e:
        raise