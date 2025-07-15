<template>
  <div class="container py-4">
    <h2 class="fw-bold text-dark mb-4">Your Quiz Summary</h2>

    <div class="row g-4">
      <div class="col-md-4">
      <div class="card shadow text-center p-3 mb-4">
        <h4 class="fw-bold text-violet">Total Quizzes Attempted</h4>
        <div class="display-4">{{ totalAttempts }}</div>
      </div>

      <div class="card shadow text-center p-3">
        <h4 class="fw-bold text-violet">Average Score</h4>
        <div class="display-4">{{ averageScore }}</div>
      </div>
    </div>
      

      <div class="col-md-8">
        <div class="card shadow p-3">
          <h5 class="fw-bold text-violet mb-3">Subject-wise Attempts</h5>
          <canvas id="subjectAttemptsChart"></canvas>
        </div>
      </div>

      <div class="col-12">
        <div class="card shadow p-3">
          <h5 class="fw-bold text-violet mb-3">Monthly Attempts Trend</h5>
          <canvas id="monthlyAttemptsChart"></canvas>
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
  name: 'UserSummaryPage',
  data() {
    return {
      totalAttempts: 0,
      averageScore: 0,
      subjectAttempts: [],
      monthlyAttempts: [],
      charts: {
        subjectAttemptsChart: null,
        monthlyAttemptsChart: null,
      },
    };
  },
  mounted() {
    this.fetchSummary();
  },
  methods: {
    async fetchSummary() {
      try {
        const [totalRes, avgRes,subjectRes, monthRes] = await Promise.all([
          api.get('/user/summary/total-attempts'),
          api.get('/user/summary/avg-score'),
          api.get('/user/summary/subject-attempts'),
          api.get('/user/summary/monthly-attempts'),
        ]);

        this.totalAttempts = totalRes.data.total_quizzes_attempted;
        this.averageScore = avgRes.data.average_score;
        this.subjectAttempts = subjectRes.data;
        this.monthlyAttempts = monthRes.data;

        this.renderSubjectAttemptsChart();
        this.renderMonthlyAttemptsChart();

      } catch (err) {
        console.error("Error fetching summary:", err);
      }
    },

    renderSubjectAttemptsChart() {
      const ctx = document.getElementById('subjectAttemptsChart');

      if (this.charts.subjectAttemptsChart) {
        this.charts.subjectAttemptsChart.destroy();
      }

      this.charts.subjectAttemptsChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: this.subjectAttempts.map(item => item.subject),
          datasets: [{
            label: 'Subject Attempts',
            data: this.subjectAttempts.map(item => item.attempts),
            backgroundColor: ['#4dc9f6', '#f67019', '#f53794', '#537bc4', '#acc236'],
          }],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'bottom' },
            tooltip: { enabled: true },
          },
        },
      });
    },

    renderMonthlyAttemptsChart() {
      const ctx = document.getElementById('monthlyAttemptsChart');

      if (this.charts.monthlyAttemptsChart) {
        this.charts.monthlyAttemptsChart.destroy();
      }

      this.charts.monthlyAttemptsChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.monthlyAttempts.map(item => item.month),
          datasets: [{
            label: 'Monthly Attempts',
            data: this.monthlyAttempts.map(item => item.attempts),
            backgroundColor: '#6a1b9a',
          }],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: { enabled: true },
          },
          scales: {
            x: { grid: { display: false } },
            y: { beginAtZero: true },
          },
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
