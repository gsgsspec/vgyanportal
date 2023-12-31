import re
from rest_framework.authtoken.models import Token
from vgyanportal.metadata import getConfig, change_timeformat
from .database import addUserDB, saveProfileDetailsDB, saveCourseRatingDB, saveAskQuestionDb, saveAssessmentData,saveNotificationData
from app_api.models import Registration, User_data , CourseRegistration, Course, CourseRating, CourseLesson, CourseModule, CourseMedia , Question , \
        Assessment, Activity , Notification
from django.utils import timezone
from django.utils.timesince import timesince


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
            getCourseDetails = Course.objects.filter(id = courseId,status='A').last()

            if getCourseDetails:
                couerseId = getCourseDetails.id
                getAssessmentCount = CourseModule.objects.filter( courseid = couerseId ,assesment = "Y").count()
                assessmentCount = Assessment.objects.filter(registrationid = userId, courseid = couerseId , status = 'C').count()

                if assessmentCount:
                    completedAssessments = assessmentCount
                else:
                    completedAssessments = 0
                
                courseDuration = Activity.objects.filter(registrationid = getcourse['registrationid'],courseid = getcourse['courseid'],activity = 'V').values()
                
                watchingTime = 0
                if courseDuration:

                    for coursedur in courseDuration:
                        cousDur = coursedur['duration']
                        watchingTime += int(cousDur)

                courseLessonDetails = CourseLesson.objects.filter(courseid = courseId).values()

                courseTotalDuration = 0
                for courseLessonDuration in courseLessonDetails:
                    
                    if courseLessonDuration['duration'] != None:

                        if int(courseLessonDuration['duration']):
                            courseTotalDuration += int(courseLessonDuration['duration']) 

                totalPrograss = 0
                if watchingTime:
                    totalPrograss = round(( watchingTime / courseTotalDuration) * 100)

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
                    'totalPrograss': totalPrograss,
                }
                
                courseList.append(courseDetails)

                courseDetails['assessments'] = { 'completedAssessmentsCount' : completedAssessments, 'totalAssessments' : getAssessmentCount}      
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
            'locked_modules':None,
            'current_lessonid':None,
        }

        try:
            current_lesson_id = Activity.objects.get(registrationid=user_id,courseid=course.id,activity='W').lessonid
            course_details["current_lessonid"] = current_lesson_id
        except:
            current_lesson_id = None



        c_module = CourseModule.objects.filter(courseid=cid,status='A').order_by('sequence')

        module_details = []
        locked_modules = []

        # Unlocked Modules list

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

                try:
                    lesson_activity = Activity.objects.get(registrationid=user_id,lessonid=lesson.id,activity='V').status
                    if lesson_activity != None:
                        lesson_status = lesson_activity
                    else:
                        lesson_status = 'N'
                except:
                    lesson_status = 'N'


                lesson_duration = ''
                module_duration = ''
                if lesson.duration != None:
                    lesson_duration = change_timeformat(lesson.duration,'L')
                elif module_duration != None:
                    module_duration = change_timeformat(module.duration,'M')

                lesson_title.append({
                    'title':lesson.title,
                    'id':lesson.id,
                    'lesson_type':lesson.type,
                    'lesson_duration':lesson_duration,
                    'lesson_status':lesson_status
                })

            module_details.append({
                    'module_id': module.id,
                    'module_name':module.name,
                    'assesment':module.assesment,
                    'mail_check': mail_check,
                    'lesson_title': lesson_title,
                    'lessons_count':c_lesson.count(),
                    'module_duration':module_duration,     
                })
            if module.assesment == 'Y' and (assessment_status == 'P' or assessment_status == 'R') :
                break
        
        # Locked Modules List
        
        for lck_module in c_module[len(module_details):]:

            c_lesson = CourseLesson.objects.filter(courseid=cid,moduleid=lck_module.id,status='A').order_by('sequence')
            mail_check=''

            try:
                assessment_status = Assessment.objects.get(registrationid=user_id,courseid=cid,moduleid=lck_module.id).status
                mail_check = 'S'
            except:
                assessment_status = 'P'
                mail_check = 'N'

            lesson_title = []

            for lesson in c_lesson:

                lesson_duration = change_timeformat(lesson.duration,'L')
                module_duration = change_timeformat(module.duration,'M')

                lesson_title.append({
                    'title':lesson.title,
                    'id':lesson.id,
                    'lesson_type':lesson.type,
                    'lesson_duration':lesson_duration,
                })

            locked_modules.append({
                    'module_id': lck_module.id,
                    'module_name':lck_module.name,
                    'assesment':lck_module.assesment,
                    'mail_check': mail_check,
                    'lesson_title': lesson_title,
                    'lessons_count':c_lesson.count(),
                    'module_duration':module_duration,         
                })

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

        getQuestions = Question.objects.filter(courseid = getcourseid ,moduleid = getModuleId, lessonid = getLessonId)

        for allQuestion in getQuestions:
            
            questionId     = allQuestion.id
            question       = allQuestion.question 
            questionAnswer = allQuestion.answer
            userRegisterId = allQuestion.registrationid
            quesDate       = allQuestion.questiondate
            
            formateQuestionDate = quesDate.strftime("%d-%m-%Y")
            formateQuestionTime = quesDate.strftime("%H : %M")

            if userRegisterId == registeredUerId:

                questions = {
                    'id'   : questionId,
                    'userId' : userRegisterId,
                    'ques' : question,
                    'ans'  : "N" if questionAnswer == None else questionAnswer,
                    'queDate' : formateQuestionDate,
                    'queTime' : formateQuestionTime,
                }
                questionList.append(questions)

            allQuestionsData = {
                    'id'   : questionId,
                    'userId' : userRegisterId,
                    'ques' : question,
                    'ans'  : "N" if questionAnswer == None else questionAnswer,
                    'queDate'  : formateQuestionDate,
                    'queTime' : formateQuestionTime,
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



def getlessonVideoService(dataObjs,user):
    try:
        user_id = Registration.objects.get(email = user).id
        course_video = CourseMedia.objects.get(lessonid=dataObjs['lesson_id'])

        try:
            user_activity = Activity.objects.get(registrationid=user_id,lessonid= dataObjs["lesson_id"],activity='V')
            video_duration = user_activity.duration
        except:
            video_duration = 0

        video_id = course_video.mediaurl
        library_id = course_video.libraryid
        video_time = video_duration

        return video_id,library_id,video_time

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

        notificationType = {
            "notifiType" : 'A' ,
            "Action"     : 'UpdateAssessment' ,
            "user_id"    : registration_id, 
            "courseid"   : course_id,
            "courseModule" : module_id
        }

        saveNotificationData(notificationType)

    except Exception as e:
        raise



def saveVideoActivityService(dataObjs,user):
    try:
        user_id = Registration.objects.get(email=user).id
        lesson = CourseLesson.objects.get(id=dataObjs["lesson_id"])
        
        try:
            user_activity = Activity.objects.get(registrationid=user_id,lessonid=lesson.id,activity='V')
            user_activity.duration = int(dataObjs['time_duration'])
            user_activity.save()

        except:
            user_activity = Activity(
                registrationid = user_id,
                lessonid=lesson.id,
                activity='V',
                duration = int(dataObjs['time_duration']),
                courseid = lesson.courseid,
                moduleid = lesson.moduleid
            )
            user_activity.save()

        try:
            watched_video = Activity.objects.get(registrationid=user_id,courseid=lesson.courseid,activity='W')
            watched_video.lessonid = dataObjs["current_video_id"]
            watched_video.save()

        except:

            watched_video = Activity(
                registrationid = user_id,
                courseid = lesson.courseid,
                activity='W',
                lessonid = dataObjs["current_video_id"]
            )
            watched_video.save()


    except Exception as e:
        raise


def courseModuleNameService(courseId,moduleId):
    try:
        courseDetails = CourseModule.objects.filter(id = moduleId).last()
        coursModuleName = courseDetails.name

        courseName = Course.objects.filter(id = courseDetails.courseid).last()
        coursName = courseName.title

        courseAndModulename = {
            'coursename' :  coursName,
            'coursemodname' : coursModuleName
        }

        return courseAndModulename

    except Exception as e:
        raise


def assessmentListService(dataObjs,user):
    try:
        userDetails = Registration.objects.filter(email = str(user)).last()
        assessmentsList = []

        if userDetails:
            userID = userDetails.id

            assessmentDetails = Assessment.objects.filter(registrationid = userID).values()
            assessmentData = {}

            for details in assessmentDetails:

                assessmentCourseId = details['courseid']
                if assessmentCourseId:
                    courseDetails = Course.objects.filter(id = assessmentCourseId).last()
                    courseName = courseDetails.title
                
                assessmentModuleId = details['moduleid']
                if assessmentModuleId:
                    courseModule = CourseModule.objects.filter(id = assessmentModuleId).last()
                    courseModuleName = courseModule.name

                assessmentDate    = details['assessmentdate']
                asseessmentStatus = details['status']

                assessmentData = {
                    'coursetitle'      : courseName,
                    'coursemoduletitle': courseModuleName,
                    'assessmentstatus' : asseessmentStatus,
                    'assessmentdate'   : assessmentDate
                }

                assessmentsList.append(assessmentData)

    except Exception as e:
        raise


def allNotificationsList(dataObjs,user):
    try:
        userDetails = Registration.objects.filter(email = str(user)).last()
        userNotificationsList = []

        if userDetails:
            userID = userDetails.id

            if  dataObjs['notificationFor'] == "HomePage":
                notificationData = Notification.objects.filter(registrationid = userID,status = None,).values()

            notificationDetails = {}

            counter = len(notificationData)

            if counter >= 5:
                if counter > 5:
                    showMoreNotification = "Y"
                else:
                    showMoreNotification = "N"
            
            else:
                showMoreNotification = "N"

            if notificationData:
                for notifi in range(0,counter):

                    notificationCourseId = notificationData[notifi]['courseid']
                    courseName = ''
                    if notificationCourseId:
                        courseDetails = Course.objects.filter(id = notificationCourseId).last()
                        courseName = courseDetails.title
                    
                    notificationCourseModule = notificationData[notifi]['moduleid']
                    courseModuleName = ''
                    if notificationCourseModule:
                        courseModule = CourseModule.objects.filter(id = notificationCourseModule).last()
                        courseModuleName = courseModule.name

                    notificationTimeSince = timesince(notificationData[notifi]['notifydate'], timezone.now())

                    customizedNotificationTimeSince = notificationTimeSince.replace("minutes", "min").replace("hour", "hr").replace("hours", "hrs")
   
                    notificationDate = str(customizedNotificationTimeSince) + ' ago'

                    notificationDetails = {
                        'identity'         : notificationData[notifi]['id'],
                        'coursetitle'      : courseName,
                        'coursemoduletitle': courseModuleName,
                        'notificationDate' : notificationDate,
                        'notificationEventType' : notificationData[notifi]['eventtype'],
                        'notificationMessage'   : notificationData[notifi]['message'],
                        'notificationDataType'  : notificationData[notifi]['type'],
                        'notificationStatus'    : notificationData[notifi]['status']
                    }

                    userNotificationsList.append(notificationDetails)

                userNotificationsList.reverse()
            else:
                userNotificationsList = 'EMPTY'

            return userNotificationsList , showMoreNotification
        
    except Exception as e:
        raise


def removeNotificationService(dataObjs,user):
    try:

        userDetails = Registration.objects.filter(email = str(user)).last()

        if userDetails:
            userID = userDetails.id

        notificationId = dataObjs['notificationsId']
        notificationStatus = dataObjs['status']

        if notificationId:
            if notificationStatus == "C":
                updateNotification = Notification.objects.filter(id = notificationId).last()
                updateNotification.status = "C"
                updateNotification.save()

    except Exception as e:
        raise


def markAsReadNotificationService(dataObjs,user):
    try:

        userDetails = Registration.objects.filter(email = str(user)).last()

        if userDetails:
            userID = userDetails.id

        notificationId = dataObjs['notificationsIdList']

        if notificationId != []:

            for notifiId in notificationId:

                updateNotification = Notification.objects.filter(id = notifiId , registrationid = userID).last()

                if updateNotification:
                    if updateNotification.read != 'Y':

                        updateNotification.read = 'Y'
                        updateNotification.save()

    except Exception as e:
        raise


def checkLatestNotificationsService(dataObjs,user):
    try:

        userDetails = Registration.objects.filter(email = str(user)).last()

        if userDetails:
            userID = userDetails.id

            notificationId = dataObjs['notificationCheck']

            notificationCount = {'count' : 0 }

            if notificationId == "check":
                notificationsCountDetails = Notification.objects.filter(registrationid = userID , read = None).count()

                notificationCount = {
                    'count' : notificationsCountDetails
                }
        
            return notificationCount

    except Exception as e:
        raise

