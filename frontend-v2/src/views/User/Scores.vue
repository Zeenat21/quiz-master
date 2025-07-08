<template>
  <div class="container py-4">
    <h3 class="mb-4 fw-bold text-dark">My Quiz Scores</h3>

    <div v-if="scores.length === 0" class="alert alert-info text-center">
      No scores available yet.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-hover table-bordered align-middle text-center">
        <thead class="table-light">
          <tr>
            <th>Quiz ID</th>
            <th>Title</th>
            <th>Date of Attempt</th>
            <th>Total Questions</th>
            <th>Correct Answers</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="score in scores" :key="score.id">
            <td>{{ score.quiz.id }}</td>
            <td>{{ score.quiz.title }}</td>
            <td>{{ formatDate(score.timestamp) }}</td>
            <td>{{ score.total_questions }}</td>
            <td>{{ score.correct_answers }}</td>
            <td>
              <span
                class="badge"
                :class="getScoreClass(score.percentage)"
                >
                {{ score.total_score }}/{{ score.total_questions * score.total_score / score.correct_answers || score.total_score }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '@/axios';

export default {
  data() {
    return {
      scores: [],
    };
  },
  methods: {
    async fetchScores() {
      try {
        const res = await api.get('/user/scores');
        this.scores = res.data;
      } catch (err) {
        console.error('Failed to load scores:', err);
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    },
    getScoreClass(percentage) {
      if (percentage >= 80) return 'bg-success';
      if (percentage >= 50) return 'bg-warning text-dark';
      return 'bg-danger';
    }
  },
  mounted() {
    this.fetchScores();
  }
};
</script>

<style scoped>
.badge {
  font-size: 0.9rem;
  padding: 8px 12px;
  border-radius: 12px;
}
</style>

