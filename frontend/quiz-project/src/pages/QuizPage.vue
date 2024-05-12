<template>
    <q-page class="flex flex-center">
        Опрос
        {{ $route.params.id }}
    </q-page>
</template>


<script setup>

defineOptions({
  name: 'QuizPage'
});
</script>