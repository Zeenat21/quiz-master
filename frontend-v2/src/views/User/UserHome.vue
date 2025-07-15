<template>
  <div class="container py-4">
    <h3 class="fw-bold text-dark mb-4">Welcome, {{ userName }}!</h3>

    <div class="card shadow">
      <div class="card-header bg-primary text-white fw-bold">
        Upcoming Quizzes
      </div>
      <div class="card-body p-2">
        <table class="table table-hover table-bordered text-center">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Quiz Title</th>
              <th>Chapter</th>
              <th>Subject</th>
              <th>Questions</th>
              <th>Scheduled Date</th>
              <th>Duration</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in quizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.title }}</td>
              <td>{{ quiz.chapter }}</td>
              <td>{{ quiz.subject }}</td>
              <td>{{ quiz.question_count }}</td>
              <td>{{ quiz.date_of_quiz }}</td>
              <td>{{ quiz.time_duration }}</td>
              <td>
                <button
                  class="btn btn-sm"
                  :class="isTodayOrPast(quiz.date_of_quiz) ? 'btn-success' : 'btn-secondary'"
                  :disabled="!isTodayOrPast(quiz.date_of_quiz)"
                  @click="isTodayOrPast(quiz.date_of_quiz) && startQuiz(quiz.id)"
                >
                  Start Quiz
                </button>
              </td>
            </tr>
            <tr v-if="quizzes.length === 0">
              <td colspan="8" class="text-muted">No upcoming quizzes available.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/axios';

export default {
  data() {
    return {
      quizzes: [],
      userName: localStorage.getItem('full_name') || 'User',
    };
  },
  methods: {
    async fetchQuizzes() {
      try {
        const res = await api.get('/user/upcoming-quizzes');
        this.quizzes = res.data;
      } catch (err) {
        console.error('Failed to load quizzes:', err);
      }
    },
    isTodayOrPast(dateStr) {
      const today = new Date().toISOString().split('T')[0];
      return dateStr <= today;
    },

    startQuiz(quizId) {
      if (confirm("Ready to begin the quiz? Once you start, you can't go back. If you do all the progress will be lost.")) {
        this.$router.push(`user/quiz-attempt/${quizId}`);
      }
    }
  },
  mounted() {
    this.fetchQuizzes();
  }
};
</script>

<style scoped>
.card-header {
  background-color: #6a1b9a !important;
}
</style>
