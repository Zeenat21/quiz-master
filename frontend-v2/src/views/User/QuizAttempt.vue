<template>
  <div class="quiz-attempt-page bg-light d-flex flex-column vh-100">
    <div class="quiz-top-bar d-flex justify-content-between align-items-center p-3 shadow-sm bg-white">
      <div class="quiz-title fw-bold">{{ quizTitle }}</div>
      <div class="timer d-flex align-items-center">
        <i class="fa fa-clock-o text-violet me-2"></i>
        <span class="fw-medium">{{ formattedTime }}</span>
      </div>
    </div>

    <div class="quiz-body flex-grow-1 overflow-auto p-4">
      <form @submit.prevent="submitQuiz(false)">
        <div v-for="(question, index) in questions" :key="question.id" class="question-block mb-4">
          <div class="fw-bold mb-2">{{ index + 1 }}. {{ question.question_statement }}</div>
          <div class="options-list">
            <div v-for="option in [1, 2, 3, 4]" :key="option" class="form-check mb-2">
              <input
                class="form-check-input"
                type="radio"
                :name="'question_' + question.id"
                :id="'q' + question.id + '_opt' + option"
                :checked="isSelected(question.id, option)"
                @change="selectOption(question.id, option)"
              />
              <label class="form-check-label" :for="'q' + question.id + '_opt' + option">
                {{ question['option' + option] }}
              </label>
            </div>
          </div>
        </div>

        <div class="text-center mt-4">
          <button class="btn btn-lg btn-success" type="submit">Submit Quiz</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/axios";

export default {
  data() {
    return {
      quizId: null,
      quizTitle: "",
      questions: [],
      answers: [],
      durationMinutes: 0,
      timeLeftSeconds: 0,
      timer: null,
      isSubmittingManually: false,
      isSubmittingAutomatically: false,
    };
  },
  computed: {
    formattedTime() {
      const min = Math.floor(this.timeLeftSeconds / 60);
      const sec = this.timeLeftSeconds % 60;
      return `${min.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
    },
  },
  methods: {
    async loadQuiz() {
      try {
        const res = await api.get(`/user/quiz/${this.quizId}/questions`);
        this.questions = res.data.questions;
        this.quizTitle = res.data.title;
        this.durationMinutes = res.data.duration_minutes;
        this.timeLeftSeconds = this.durationMinutes * 60;
        this.answers = this.questions.map((q) => ({ question_id: q.id, selected_option: null }));

        this.startTimer();
      } catch (err) {
        console.error(err);
        alert("Error loading quiz!");
        this.$router.push("/user");
      }
    },

    startTimer() {
      if (this.timer) clearInterval(this.timer);
      this.timer = setInterval(() => {
        if (this.timeLeftSeconds > 0) {
          this.timeLeftSeconds--;
        } else {
          clearInterval(this.timer);
          this.submitQuiz(true);
        }
      }, 1000);
    },

    selectOption(questionId, option) {
      const answer = this.answers.find((a) => a.question_id === questionId);
      if (answer) answer.selected_option = option;
    },

    isSelected(questionId, option) {
      const answer = this.answers.find((a) => a.question_id === questionId);
      return answer?.selected_option === option;
    },

    async submitQuiz(autoSubmit = false) {
      if (this.isSubmittingManually || this.isSubmittingAutomatically) return;

      const unansweredCount = this.answers.filter((a) => a.selected_option === null).length;

      if (autoSubmit) {
        if (this.timeLeftSeconds > 0) {
          return; // Prevent accidental auto-submit before timer is actually zero.
        }

        this.isSubmittingAutomatically = true;
        clearInterval(this.timer);

        try {
          await api.post(`/user/quiz/${this.quizId}/submit`, { answers: this.answers });
          alert("Time is up! Quiz submitted automatically.");
          this.$router.push("/user/scores");
        } catch (err) {
          console.error(err);
          alert("Failed to auto-submit quiz.");
        }
        return;
      }

      // Manual submission flow
      if (unansweredCount > 0) {
        alert("You have to attempt all questions.");
        return;
      }

      if (this.timeLeftSeconds > 0) {
        const confirmed = confirm("Are you sure you want to submit? Time still remains.");
        if (!confirmed) return;
      }

      this.isSubmittingManually = true;
      clearInterval(this.timer);

      try {
        await api.post(`/user/quiz/${this.quizId}/submit`, { answers: this.answers });
        alert("Quiz submitted successfully!");
        this.$router.push("/user/scores");
      } catch (err) {
        console.error(err);
        alert("Failed to submit quiz.");
      }
    },

    confirmNavigation(e) {
      e.preventDefault();
      e.returnValue = "";
    },
  },

  beforeRouteEnter(to, from, next) {
    if (confirm("Ready to begin the quiz? Once you start, you can't go back. If you do all progress will be lost.")) {
      next();
    } else {
      next(false);
    }
  },

  mounted() {
    this.quizId = this.$route.params.quizId;
    this.loadQuiz();
    window.addEventListener("beforeunload", this.confirmNavigation);
  },

  beforeUnmount() {
    clearInterval(this.timer);
    window.removeEventListener("beforeunload", this.confirmNavigation);
  },
};
</script>

<style scoped>
.quiz-attempt-page {
  background: #f8f9fa;
}

.quiz-top-bar {
  height: 60px;
}

.quiz-title {
  font-size: 1.2rem;
  color: #6a1b9a;
  font-weight: bold;
}

.text-violet {
  color: #6a1b9a !important;
}

.timer i {
  margin-right: 8px;
}

.question-block {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.options-list {
  margin-top: 10px;
  /* display: flex;
  flex-direction: column;
  align-items: flex-start; */
}

/* .form-check {
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0;
} */

.form-check-input {
  cursor: pointer;
  border: 2px solid #6a1b9a;
  /* margin-right: 8px; */
}

.form-check-label {
  cursor: pointer;
  /* flex-grow: 1; */
}

.btn-lg {
  min-width: 200px;
}

.question-block .fw-bold {
  color: black;
  font-weight: bold;
}
</style>
