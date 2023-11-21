from rest_framework.authtoken.models import Token
from vgyanportal.metadata import getConfig
from .database import addUserDB, saveProfileDetailsDB, saveCourseRatingDB, saveAskQuestionDb
from app_api.models import Registration, User_data , CourseRegistration, Course, CourseRating, CourseLesson, CourseModule, CourseMedia , question


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


def getCourseDetails(request,cid):
    try:

        course = Course.objects.get(id=cid)
        user_id = Registration.objects.get(email=request.user).id

        course_details = {
            'courseid':course.id,
            'title':course.title,
            'module': None,
            'rating':None,
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
                'assesment':module.assesment,
                'lesson_title': lesson_title
            })

        course_details["module"] = module_details

        try:
            course_rating = CourseRating.objects.get(registrationid=user_id,courseid=cid).rating
            course_details["rating"] = course_rating
        except:
            course_details["rating"] = None

        return course_details


    except Exception as e:
        raise


def getModuleLessonService(dataObjs):
    try:
        getCourseId = dataObjs['courseId']
        getModuleId = dataObjs['moduleId']
        getLessonId = dataObjs['lessionId']

        moduleAndLessonsData = {}

        modulesList = [] 
        lessonsList = []

        getCourseIdDb = Course.objects.filter(id  = getCourseId).last()
        
        if getCourseIdDb.id:
            
            getCourseModuleIdDb = CourseModule.objects.filter(courseid = getCourseIdDb.id)

            for module in getCourseModuleIdDb:

                default = "NO"

                if int(getModuleId) == module.id:

                    default = "YES"

                modulesData = {
                    'selected' : default,
                    'moduleId' : module.id,
                    'moduleName' : module.name,
                    'moduleSequence' : module.sequence
                }

                modulesList.append(modulesData)
            
            getModeulesDetails = getCourseModuleIdDb.first()

            courseId = getModeulesDetails.courseid
            moduleId = getModeulesDetails.id

            getModulesLesson = CourseLesson.objects.filter(courseid = courseId, moduleid = getModuleId)
            
            for lesson in getModulesLesson:
                
                defaultLesson = 'NO'

                if lesson.id == getLessonId:

                    defaultLesson = 'YES'
                
                lessonData = {
                    'defaultLesson' : defaultLesson,
                    'lessonid' : lesson.id,
                    'title'    : lesson.title,
                }

                lessonsList.append(lessonData)

        
            moduleAndLessonsData['Modules'] = modulesList
            moduleAndLessonsData['lesson']  = lessonsList

        return moduleAndLessonsData
    
    except Exception as e:
        raise
            


def saveCourseRating(dataObjs,user):
    try:
        course_rating =  saveCourseRatingDB(dataObjs,user)
        return course_rating
    except Exception as e:
        raise


def saveAskQuestion(dataObjs):
    try:
        saveAskQuestionDb(dataObjs)
    except Exception as e:
        raise


def getAskQuestion(dataObjs):
    try:
        questionList = []
        unansweredQuestion = []
        sendQuestions = {}
        userCourseId = int(dataObjs['getQuestionData']['courseId'])
        registeredUerId   = int(dataObjs['getQuestionData']['userId'])

        userCourseDetails = CourseRegistration.objects.filter(courseid = userCourseId ,registrationid = registeredUerId).last()

        getcourseid = userCourseDetails.courseid

        getQuestions = question.objects.filter(registrationid = userCourseDetails.registrationid,courseid = getcourseid)

        for ques in getQuestions:
            if ques.answer:
                questions = {
                    'id'   : ques.id,
                    'ques' : ques.question,
                    'ans'  : ques.answer
                }

                questionList.append(questions)

            else:
                unquestions = {
                    'id'   : ques.id,
                    'ques' : ques.question 
                }
                unansweredQuestion.append(unquestions
                )
        
        sendQuestions['questionList'] = questionList
        sendQuestions['unansweredQuestion'] = unansweredQuestion

        return sendQuestions

    except Exception as e:
        raise