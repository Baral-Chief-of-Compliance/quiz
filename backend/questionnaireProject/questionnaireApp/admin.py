from django.contrib import admin
import questionnaireApp.models as models


#регистрируем в админ панели отображение сущности Quiz(опрос)
@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("quiz_title", "quiz_title_status", "quiz_title_date_create",)
    list_filter = ("quiz_title_status",)
    search_fields  = ("quiz_title",)
    save_on_top = True
    save_as = True


#регистрируем в админ панели отображение сущности Question(вопрос)
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("q_title",)
    list_filter = ("q_one_answer",)
    search_fields = ("q_title",)
    save_on_top = True
    save_as = True


#регистрируем в админ панели отображение сущности Choise(вариант ответа)
@admin.register(models.Choise)
class ChoiseAdmin(admin.ModelAdmin):
    list_display = ("ch_title",)
    list_filter = ("ch_points",)
    search_fields = ("ch_title",)
    save_on_top = True
    save_as = True


#регистрируем в админ панели отображение сущности Answer(ответ польлзователя)
@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("quiz", "question", "user_token", "created",)
    list_filter = ("question", "quiz")
    search_fields = ("question", "user_token", "quiz")
    save_on_top = True
    save_as = True