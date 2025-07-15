<template>
  <div class="container py-4">
    <h2 class="fw-bold text-dark mb-4">Admin Summary Dashboard</h2>

    <div class="row g-4">
      <div class="col-md-6">
        <div class="card shadow p-3">
          <h5 class="fw-bold text-violet mb-3">Subject Wise Quiz Attempts</h5>
          <canvas id="subjectAttemptsChart"></canvas>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow p-3">
          <h5 class="fw-bold text-violet mb-3">Top Scores Per Subject</h5>
          <canvas id="topScoresChart"></canvas>
        </div>
      </div>

      <div class="col-12">
        <div class="card shadow p-3">
          <h5 class="fw-bold text-violet mb-3">User Activity Summary</h5>
          <canvas id="userActivityChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import api from '@/axios';

Chart.register(...registerables);

export default {
  name: 'AdminSummaryPage',
  mounted() {
    this.loadCharts();
  },
  methods: {
    async loadCharts() {
      const [subjectData, topScoresData, userActivityData] = await Promise.all([
        api.get('/admin-summary/subject-quiz-attempts'),
        api.get('/admin-summary/top-scores-per-subject'),
        api.get('/admin-summary/user-activity'),
      ]);

      this.renderSubjectAttemptsChart(subjectData.data);
      this.renderTopScoresChart(topScoresData.data);
      this.renderUserActivityChart(userActivityData.data);
    },

    renderSubjectAttemptsChart(data) {
      const ctx = document.getElementById('subjectAttemptsChart');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: data.map(d => d.subject),
          datasets: [{
            label: 'Quiz Attempts',
            data: data.map(d => d.total_attempts),
            backgroundColor: ['#4dc9f6', '#f67019', '#f53794', '#537bc4', '#acc236'],
          }],
        },
      });
    },

    renderTopScoresChart(data) {
      const ctx = document.getElementById('topScoresChart');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map(d => d.subject),
          datasets: [{
            label: 'Top Score',
            data: data.map(d => d.max_score),
            backgroundColor: '#36a2eb',
          }],
        },
      });
    },

    renderUserActivityChart(data) {
      const ctx = document.getElementById('userActivityChart');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map(d => d.user),
          datasets: [{
            label: 'Total Attempts',
            data: data.map(d => d.total_attempts),
            backgroundColor: '#ff6384',
          }],
        },
      });
    },
  },
};
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: 300px !important;
}

.card {
  border-radius: 0.75rem;
  border: 1px solid #ddd;
  background: #fff;
  margin-bottom: 1rem;
}

h5 {
  margin-bottom: 1rem;
}

.container {
  padding-top: 2rem;
}

.text-violet {
  color: #6a1b9a;
}
</style>
