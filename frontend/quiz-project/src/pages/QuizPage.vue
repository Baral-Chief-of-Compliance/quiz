<template>
    <q-page class="flex flex-center">
        <!-- {{ route.params.id }}

        {{  state.quiz }} -->

        <q-card class="my-card">
          <img src="https://cdn.quasar.dev/img/mountains.jpg">
          <q-card-section>
            <div class="text-h6">Our Changing Planet</div>
            <div class="text-subtitle2">by John Doe</div>
          </q-card-section>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit
          </q-card-section>
        </q-card>
    </q-page>
</template>


<script setup>
import axios from 'axios';
import { ref, onMounted, reactive } from 'vue';

//состояние страницы
const state = reactive({
  quiz : {}
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
    state.quiz = response.data
  })
}


onMounted(() => {
  getQuiz();
})

defineOptions({
  name: 'QuizPage'
});
</script>