from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import Quiz, Question, Choise, Answer


def index(request):
    return HttpResponse('Hello world')


#получить тест по его id
def getQuiz(request, quiz_url: str) -> JsonResponse:

    try:
        quiz = Quiz.objects.get(quiz_title_url=quiz_url)
    except:
        HttpResponseNotFound("There is no such survey")

    questions =  quiz.questions.all()

    questions_info = []

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

    return JsonResponse({
        "quiz_id": quiz.id,
        "quiz_title": quiz.quiz_title,
        "quiz_questions_quantity": len(questions),
        "quiz_questions": questions_info
    })
