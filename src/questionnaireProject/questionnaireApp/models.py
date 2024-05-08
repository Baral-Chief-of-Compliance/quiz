from django.db import models
from datetime import date
import secrets


#сущность варианта ответа в вопросе в опроснике
class Choise(models.Model):
    ch_title = models.TextField(verbose_name="Содержание выбора ответа")
    ch_points = models.IntegerField(verbose_name="Баллы за ответ, если опрос для статистики, то балл 0", default=0)

    def __str__(self) -> str:
        return self.ch_title
    
    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"


#сущность вопросов, из которых состоит опрос
class Question(models.Model):
    q_title = models.TextField(verbose_name="Текст вопроса")
    q_one_answer = models.BooleanField(verbose_name="Один ответ", default=True)
    q_choises = models.ManyToManyField(Choise, verbose_name="Варианты ответов", blank=True)

    def __str__(self) -> str:
        return self.q_title
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


#сущность тестов, которые будут хранить названия, а также вопросы
class Quiz(models.Model):
    quiz_title = models.TextField(verbose_name="Название опроса")
    quiz_title_subtitle = models.TextField(verbose_name="Дополнительная информация об опросе", blank=True, null=True)
    quiz_title_date_create = models.DateField(verbose_name="Дата создания опроса", default=date.today)
    quiz_title_status = models.BooleanField(verbose_name="Статус опроса: (Завершён/Незавршён)", default=True)
    quiz_title_url = models.TextField(verbose_name="url идентификатор по кторому доступен тест", default="Не сгенерирован")
    questions = models.ManyToManyField(Question, verbose_name="Вопросы опроса", blank=True)

    def __str__(self) -> str:
        return self.quiz_title
    

    def save(self, *args, **kwargs):
        if self.quiz_title_url == "Не сгенерирован":
            self.quiz_title_url = secrets.token_hex(16)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"



#сущность ответов на вопрос
class Answer(models.Model):
    user_token = models.TextField(verbose_name="Токен пользователя")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Опрос в котором участвует пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос на который отвечает пользователь")
    choise = models.ForeignKey(Choise, on_delete=models.CASCADE, verbose_name="Выбранный вариант ответа")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"пользователь {self.user_token} - {self.choise.ch_title}"
    
    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"