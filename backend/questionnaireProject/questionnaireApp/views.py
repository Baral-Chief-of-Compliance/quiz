from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseNotAllowed
from .models import Quiz, Question, Choise, Answer
from django.views.decorators.csrf import csrf_exempt
import secrets
import json


def index(request):
    return HttpResponse('Hello world')


#получить тест по его id
@csrf_exempt
def getQuiz(request, quiz_url: str) -> JsonResponse:


    # при методе гет происходит получение всей информации об опросе
    if request.method == 'GET':

        try:
            quiz = Quiz.objects.get(quiz_title_url=quiz_url)
        except:
            HttpResponseNotFound("There is no such survey")

        questions =  quiz.questions.all()

        questions_info = []

        user_questions = []

        for index, q in enumerate(questions):
        
            choises_info = []

            choises = q.q_choises.all()

            for c in choises:
                choises_info.append({
                    "ch_id": c.id,
                    "ch_title": c.ch_title,
                    "ch_points": c.ch_points
                })
                
            questions_info.append({
                "q_id": q.id,
                "q_index": index + 1,
                "q_title": q.q_title,
                "q_choises": choises_info
            }) 

            user_questions.append({
                "q_id": q.id,
                "user_choise": 1
            })

        return JsonResponse({
            "quiz_id": quiz.id,
            "quiz_title": quiz.quiz_title,
            "quiz_questions_quantity": len(questions),
            "quiz_questions": questions_info,
            "user_token": secrets.token_hex(32),
            "user_questions": user_questions
        })
    

    #при методе пост по данному запросу, добавляются ответы пользователя на этот тест
    elif request.method == 'POST':
        try:
            quiz = Quiz.objects.get(quiz_title_url=quiz_url)
        except:
            HttpResponseNotFound("There is no such survey")

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        #ответы пользователя
        user_questions =  body["user_questions"]

        #токен пользователя
        user_token = body["user_token"]

        #добавление ответов пользователя в базу данных для статистики
        for u_q in user_questions:

            Answer.objects.create(
                user_token=user_token,
                quiz= quiz,
                question = Question.objects.get(id=u_q["q_id"]),
                choise = Choise.objects.get(id=u_q["user_choise"])  
            )

        return JsonResponse({
            "user_token": user_token,
            "user_questions": user_questions,
            "quiz_id": quiz.id
        })
    
    #ну это если метод будет отличаться от POST или GET
    else:
        return JsonResponse({
            "no": "method"
        })
    

#статистика опроса по его id
def statisticQuiz(request, quiz_url: str):
    if request.method == 'GET':
        try:
            quiz = Quiz.objects.get(quiz_title_url=quiz_url)
        except:
            HttpResponseNotFound("There is no such survey")

        
        questions = quiz.questions.all()

        questions_info = []

        # количество людей прошедших опрос
        quiz_count_user_pass = 0

        for q in questions:

            #получение всех вариантов ответа по данному вопросу
            choises_info = []

            choises = q.q_choises.all()

            # количестов людей прошедших вопрос
            q_count_user_pass = 0
            for c in choises:
                answers = Answer.objects.filter(quiz=quiz) & Answer.objects.filter(question=q) & Answer.objects.filter(choise=c)

                q_count_user_pass += len(answers)

                choises_info.append({
                    "ch_id": c.id,
                    "ch_title": c.ch_title,
                    "ch_points": c.ch_points,
                    "answer_quanty": len(answers)
                })

            
            if q_count_user_pass > quiz_count_user_pass:
                quiz_count_user_pass = q_count_user_pass

            questions_info.append({
                "q_id": q.id,
                "q_title": q.q_title,
                "q_count_user_pass": q_count_user_pass,
                "q_choises": choises_info,

            })

        return JsonResponse({
            "quiz_id": quiz.id,
            "quiz_title": quiz.quiz_title,
            "quiz_questions_quantity": len(questions),
            "quiz_title_subtitle": quiz.quiz_title_subtitle,
            "quiz_count_user_pass": quiz_count_user_pass,
            "quiz_questions": questions_info,
        })

    else:
        return HttpResponseNotAllowed()
