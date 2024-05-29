<template>
    <q-page class="flex flex-center">
        <!-- {{ route.params.id }}

        {{  state.quiz }} -->


          <!-- правая колонна -->
          <!-- <div class="col"></div> -->

          <!-- Средняя колонна в которой и будет основной контент -->

          <!-- карточка с названием опроса -->
          <div class="q-pa-md example-row-equal-width">
            <div class="row justify-center">
              <q-card v-if="!state.quiz_start" :class="[(width > 1200)  ? 'my-card col-5': (width > 900) ? 'my-card col-8': 'my-card col']">
                <q-card-section>
                  <div :class="[(width > 500)  ? 'q-mb-xl text-h3 text-center' : 'q-mb-md text-h5 text-center']">Опрос</div>
                  <div :class="[(width > 500)  ? 'text-h4 text-center' : 'text-h6 text-center']">{{ state.quiz.quiz_title }}</div>
                  <div class="q-mt-md text-subtitle text-center">Количество вопросов: {{ state.quiz.quiz_questions_quantity }}</div>
                </q-card-section>
                <q-card-section>
                  <div class="column">
                    <q-btn color="primary" label="ПРОЙТИ ОПРОС" @click="state.quiz_start=true"  size="xl"/>
                  </div>
                </q-card-section>
              </q-card>

              <!-- карточка с информацией о вопросе из опроса -->
              <q-card v-if="state.quiz_start  && !state.quiz_finish" :class="[(width > 1200)  ? 'my-card col-5': (width > 900) ? 'my-card col-8': 'my-card col']">
                <!-- <img src="https://cdn.quasar.dev/img/mountains.jpg"> -->
                <q-card-section>
                  <div :class="[(width > 1200) ? 'q-mb-sm text-h6 text-center': (width > 900) ? 'mid-text' : 'small-text']">{{ state.quiz.quiz_title }}</div>
                  <div :class="[(width > 1200) ? 'text-h5 text-center' : (width > 900) ? 'mid-title' : 'small-title']"><b>{{ state.current_question_info.q_index }}. {{ state.current_question_info.q_title }}</b></div>
                </q-card-section>
                <q-card-section>
                  <div class="column justify-center">
                      <q-radio class="q-mb-xs text-h6" v-model="state.user_choise"  v-for="(choise) in  state.current_question_info.q_choises" :key="choise.ch_id" :val="choise.ch_id">
                      <div :class="[(width > 1200) ? '': (width > 900) ? 'mid-quiz' : 'small-quiz']">{{ choise.ch_title }}</div>
                    </q-radio  >
                  </div>


                  <!-- кнопка следующего вопроса -->
                  <div v-if="state.user_choise !='' &&  ((state.current_question + 1) < state.quiz.quiz_questions_quantity)" class="q-mt-xs column">
                    <q-btn  size="lg" color="primary" label="следующий вопрос" @click="nextQestion()" />
                  </div>

                  <div v-if="state.user_choise !='' && state.current_question + 1 ==  state.quiz.quiz_questions_quantity" class="q-mt-xl column">
                    <q-btn size="lg" color="primary" label="Отправить резульатты" @click="sendAnswers()" />
                  </div>
                
                </q-card-section>
              </q-card>


              <!-- карточка с информацией о том, что опрос пройден -->
              <q-card v-if="state.quiz_finish" :class="[(width > 1200)  ? 'my-card col-5': (width > 900) ? 'my-card col-8': 'my-card col']">
                <q-card-section>
                  <div class="text-h3 text-center">Спасибо за участие в опросе!</div>
                  <div class="q-pa-md text-center col">
                    <q-icon color="green" name="check" size="10em"/>
                  </div>
                </q-card-section>
                <!-- <q-card-section>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit
                </q-card-section> -->
              </q-card>
            </div>
          </div>

          
          <!-- левая колонна -->
          <!-- <div class="col"></div> -->


    </q-page>
</template>


<script setup>
import axios from 'axios';
import { ref, onMounted, reactive } from 'vue';
import { useWindowSize  } from '@vueuse/core';

const { width, height } = useWindowSize()

//состояние страницы
const state = reactive({
  current_question : 0,
  quiz_start: false,
  current_question_info: {},
  quiz : {},
  user_choise: "",
  quiz_finish: false,
  user_token: "",
  user_questions : []
})


//импортирем для получения параметры с роута
import { useRoute } from 'vue-router';


//роут
const route = useRoute()



//функция для получения опроса, его вопросов от бекенда
function getQuiz() {
  axios.get(`http://localhost/api/v1/questionnaires/quiz/${route.params.id}`)
  .then(function(response){
    console.log(response);
    state.quiz = response.data;
    state.user_token = state.quiz.user_token;
    state.user_questions = state.quiz.user_questions;
    state.current_question_info = state.quiz.quiz_questions[0];
  })
}

// функция для перехода к следующему вопросу
function nextQestion(){
  state.user_questions[state.current_question].user_choise = state.user_choise 
  state.user_choise = '';
  state.current_question ++;
  state.current_question_info = state.quiz.quiz_questions[state.current_question];
}


// функция для окончания опроса и для отправкки результата
function sendAnswers(){
  state.user_questions[state.current_question].user_choise = state.user_choise 
  state.quiz_finish = true

  //отправка результатов
  axios.post(
    `http://localhost/api/v1/questionnaires/quiz/${route.params.id}/`,
    {
      "user_token": state.user_token,
      "user_questions": state.user_questions
    }
  ).then(function(response){
      console.log(response.data);
    
    })
    .catch(function(error){
      console.log(error);
    })
}

onMounted(() => {
  getQuiz();
})

defineOptions({
  name: 'QuizPage'
});
</script>

<style>



.mid-title{
  font-size: 24px;
  text-align: center;
}

.mid-text{
  font-size: 18px;
  text-align: center;
}

.small-title{
  font-size: 20px;
  text-align: center;
}

.small-text{
  font-size: 16px;
  text-align: center;
}

.mid-quiz{
  font-size: 20px;
  text-align: center;
}

.small-quiz{
  font-size: 14px;
  text-align: center;
}


</style>