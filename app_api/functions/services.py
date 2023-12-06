import re
from rest_framework.authtoken.models import Token
from vgyanportal.metadata import getConfig
from .database import addUserDB, saveProfileDetailsDB, saveCourseRatingDB, saveAskQuestionDb, saveAssessmentData
from app_api.models import Registration, User_data , CourseRegistration, Course, CourseRating, CourseLesson, CourseModule, CourseMedia , Question , \
        Assessment

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
    courseDetails = {}
    
    getCourse = CourseRegistration.objects.filter(registrationid = userId).values()
    for getcourse in getCourse:
        if getcourse['status'] == "A":
            courseId = getcourse['courseid']
            if courseId:
                getCourseDetails = Course.objects.filter(id = courseId).last()
                couerseId = getCourseDetails.id

                getAssessmentCount = CourseModule.objects.filter( courseid = couerseId ,assesment = "Y").count()

                img_url = CourseMedia.objects.get(courseid=courseId, type='T').mediaurl
                web_domain = getConfig()['MEDIA']['web_domain']

                courseDetails = {
                    "id"           : couerseId,
                    "title"        : getCourseDetails.title,
                    "subjectid"    : getCourseDetails.subjectid,
                    "about"        : getCourseDetails.about,
                    "outcomes"     : getCourseDetails.outcomes,
                    "level"        : getCourseDetails.level,
                    "instructorid" : getCourseDetails.instructorid,
                    "agegroup"     : getCourseDetails.agegroup,
                    "language"     : getCourseDetails.language,
                    "timeframe"    : getCourseDetails.timeframe,
                    "certificate"  : getCourseDetails.certificate,
                    "price"        : getCourseDetails.price,
                    "objectives"   : getCourseDetails.objectives,
                    "eligibility"  : getCourseDetails.eligibility,
                    "status"       : getCourseDetails.status,
                    'course_img'   : f"{web_domain}{img_url}",
                }
                
                courseList.append(courseDetails)

                courseDetails['assessments'] = { 'pendding' : 0, 'totalAssessments' : getAssessmentCount}      
                courseDetails['duration'] = { 'totalduration' : getCourseDetails.duration}        
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
            'locked_modules':None
        }

        c_module = CourseModule.objects.filter(courseid=cid,status='A').order_by('sequence')

        module_details = []
        locked_modules = []

        for module in c_module:

            c_lesson = CourseLesson.objects.filter(courseid=cid,moduleid=module.id,status='A').order_by('sequence')
            mail_check=''

            try:
                assessment_status = Assessment.objects.get(registrationid=user_id,courseid=cid,moduleid=module.id).status
                mail_check = 'S'
            except:
                assessment_status = 'P'
                mail_check = 'N'

            lesson_title = []

            for lesson in c_lesson:
                lesson_title.append({
                    'title':lesson.title,
                    'id':lesson.id
                })

            if module.assesment == 'N' or (module.assesment == 'Y' and assessment_status == 'C') :

                module_details.append({
                    'module_id': module.id,
                    'module_name':module.name,
                    'assesment':module.assesment,
                    'mail_check': mail_check,
                    'lesson_title': lesson_title,
                    
                })

            if module.assesment == 'Y' and assessment_status in ['P', 'R']:
                locked_modules.append({
                    'module_id': module.id,
                    'module_name':module.name,
                    'assesment':module.assesment,
                    'mail_check': mail_check,
                    'lesson_title': lesson_title,
                    
                })

        if locked_modules:
            module_details.append(locked_modules[0])
            locked_modules.remove(locked_modules[0])

        course_details["module"] = module_details
        course_details["locked_modules"] = locked_modules

        try:
            course_rating = CourseRating.objects.get(registrationid=user_id,courseid=cid).rating
            course_details["rating"] = course_rating
        except:
            course_details["rating"] = None

        return course_details


    except Exception as e:
        raise


# def getModuleLessonService(dataObjs):
#     try:
#         getCourseId = dataObjs['courseId']
#         getModuleId   = dataObjs['moduleId']
#         moduleAndLessonsData = {}

#         modulesList = [] 
#         lessonsList = []

#         getCourseIdDb = Course.objects.filter(id  = getCourseId).last()
        
#         if getCourseIdDb.id:
            
#             getCourseModuleIdDb = CourseModule.objects.filter(courseid = getCourseIdDb.id)

#             if getCourseModuleIdDb:
#                 for module in getCourseModuleIdDb:

#                     default = "NO"

#                     if module.id == int(getModuleId):

#                         default = "YES"

#                     modulesData = {
#                         'selected' : default,
#                         'moduleId' : module.id,
#                         'moduleName' : module.name,
#                         'moduleSequence' : module.sequence
#                     }

#                     modulesList.append(modulesData)
                
#                 getModeulesDetails = getCourseModuleIdDb.first()

#                 courseLessonId = getModeulesDetails.courseid
#                 moduleId = getModeulesDetails.id

#                 if module.id:
#                     getModulesLesson = CourseLesson.objects.filter(courseid = courseLessonId,moduleid = moduleId if getModuleId == 0 else getModuleId)

#                     if getModulesLesson:
                    
#                         for lesson in getModulesLesson:
                            
#                             defaultLesson = 'NO'

#                             if lesson.id:

#                                 defaultLesson = 'YES'
                            
#                             lessonData = {
#                                 'defaultLesson' : defaultLesson,
#                                 'lessonid' : lesson.id,
#                                 'title'    : lesson.title,
#                             }

#                             lessonsList.append(lessonData)
            
#             moduleAndLessonsData['Modules'] = modulesList
#             moduleAndLessonsData['lesson']  = lessonsList
        
        
#         return moduleAndLessonsData
    
#     except Exception as e:
#         raise


def getModuleLessonService(dataObjs):
    try:
        getCourseId   = 1
        getModuleId   = 1
        getLessionId  = 1
        moduleAndLessonsData = {}

        getCourseIdDetails = Course.objects.filter(id  = getCourseId).last()
        getCourseModuleDetails = CourseModule.objects.filter(id = getModuleId , courseid = getCourseId).last()
        getCourseModuleLessonDetails = CourseLesson.objects.filter(id = getLessionId , moduleid = getModuleId , courseid = getCourseId).last()

        getCourseTitle = ''
        if getCourseIdDetails:
            getCourseTitle = getCourseIdDetails.title
        
        getCourseModuleName = ''
        if getCourseModuleDetails:
            getCourseModuleName = getCourseModuleDetails.name
        
        getCourseLessonName = ''
        if getCourseModuleLessonDetails:
            getCourseLessonName = getCourseModuleLessonDetails.title


        moduleAndLessonsData['courseName'] = getCourseTitle
        moduleAndLessonsData['courseModuleName'] = getCourseModuleName
        moduleAndLessonsData['courseLessonName']  = getCourseLessonName
        
        
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


def getAskQuestion(dataObjs,userId):
    try:
        questionList     = []
        overAllQuestions = []
        sendUserId       = []

        sendQuestions    = {}
        userCourseId     = dataObjs['getQuestionData']['lesson_id']
        registeredUerId  = userId
        

        getUserId = Registration.objects.filter(email = registeredUerId).last()
        userCourseDetails = CourseLesson.objects.filter(id = userCourseId ).last()

        registeredUerId = getUserId.id
        getcourseid = userCourseDetails.courseid
        getModuleId = userCourseDetails.moduleid
        getLessonId = userCourseDetails.id

        courseName = Course.objects.filter(id = getcourseid).last()
        courseModule = CourseModule.objects.filter(id = getModuleId).last()

        courseGetName    = courseName.title
        courseModuleName = courseModule.name
        courseLessonName = userCourseDetails.title

        getQuestions = Question.objects.filter(courseid = getcourseid ,moduleid = getModuleId, lessonid = getLessonId ,registrationid = registeredUerId)

        for allQuestion in getQuestions:
            
            questionId     = allQuestion.id
            question       = allQuestion.question 
            questionAnswer = allQuestion.answer
            userRegisterId = allQuestion.registrationid

            if userRegisterId == registeredUerId:
                questions = {
                    'id'   : questionId,
                    'userId' : userRegisterId,
                    'ques' : question,
                    'ans'  : "N" if questionAnswer == None else questionAnswer
                }
                questionList.append(questions)

            allQuestionsData = {
                    'id'   : questionId,
                    'userId' : userRegisterId,
                    'ques' : question,
                    'ans'  : "N" if questionAnswer == None else questionAnswer
                }
            overAllQuestions.append(allQuestionsData)

        questionList.reverse()
        overAllQuestions.reverse()
        
        sendQuestions['sendUserId']   = registeredUerId
        sendQuestions['questionList'] = questionList
        sendQuestions['overAllQuestions'] = overAllQuestions

        sendQuestions['courseDetails'] = {'courseGetName':courseGetName,'courseModuleName':courseModuleName,'courseLessonName':courseLessonName}

        return sendQuestions

    except Exception as e:
        raise



def assessmentDetailsService(dataObjs,user):

    try:
        
        course_assessment = {
            
        }


    except Exception as e:
        raise



def getlessonVideoService(dataObjs):
    try:

        course_video = CourseMedia.objects.get(lessonid=dataObjs['lesson_id'])
        video_id = course_video.mediaurl
        library_id = course_video.libraryid

        return video_id,library_id

    except Exception as e:
        raise

    
def saveAssessmentService(dataObjs,user):
    try:

        saveAssessmentData(dataObjs,user)

    except Exception as e:
        raise



def updateAssessmentService(dataObjs):

    try:

        paper_name = dataObjs['paper_name']
        user_email = dataObjs['user_email']

        paper_data = re.sub('[a-zA-Z()\s-]','',paper_name)

        course_id = int(paper_data.split(',')[0])
        module_id = int(paper_data.split(',')[1])

        registration_id = Registration.objects.get(email=user_email).id

        assessment = Assessment.objects.get(registrationid=registration_id,courseid=course_id,moduleid=module_id)
        assessment.status = 'C'
        assessment.save()


    except Exception as e:
        raise
