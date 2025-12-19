<script setup>
import { ref } from 'vue'

defineProps({
  question: {
    type: String,
    required: true
  },
  answer: {
    type: String,
    required: true
  }
})

const isFlipped = ref(false)

function flipCard() {
  isFlipped.value = !isFlipped.value
}
</script>

<template>
  <div class="flashcard-scene" @click="flipCard">
    <div class="flashcard-card" :class="{ 'is-flipped': isFlipped }">
      <div class="card-face card-face--front">
        <span class="card-title">Pertanyaan:</span>
        <p>{{ question }}</p>
      </div>
      <div class="card-face card-face--back">
        <span class="card-title">Jawaban:</span>
        <p>{{ answer }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.flashcard-scene {
  width: 400px;
  height: 250px;
  perspective: 800px;
  cursor: pointer;
  border-radius: 12px;
}
.flashcard-card {
  width: 100%;
  height: 100%;
  position: relative;
  transition: transform 0.6s;
  transform-style: preserve-3d;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-radius: 12px;
}
.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
  border-radius: 12px;
  background-color: white;
  border: 1px solid #e0e0e0;
}
.card-title {
  font-weight: bold;
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 10px;
}
.card-face--back {
  transform: rotateY(180deg);
  background-color: #f9f9f9;
}
.flashcard-card.is-flipped {
  transform: rotateY(180deg);
}
</style>