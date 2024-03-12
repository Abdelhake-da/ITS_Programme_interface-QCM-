import random
from flask import Flask, render_template, request
from collections import defaultdict

from numpy import mean

app = Flask(__name__)


class ThompsonSampler:
    def __init__(self, arms):
        self.arms = arms
        self.num_arms = len(arms)
        self.successes = defaultdict(int)
        self.failures = defaultdict(int)
        self.times = defaultdict(list)

    def select_arm(self):
        probabilities = []
        for i in range(self.num_arms):
            alpha1 = self.failures[i] + 1
            beta1 = self.successes[i] + 1
            a = random.betavariate(alpha1, beta1)
            range_ = (
                max(self.times[i]) - min(self.times[i])
                if len(self.times[i]) >= 2
                else 1
            )
            alpha2 = self.times[i][-1] / range_ if len(self.times[i]) >= 2 else 1
            beta2 = mean(self.times[i]) / range_ if len(self.times[i]) >= 2 else 0.01
            b = random.betavariate(alpha2, abs(beta2))
            probabilities.append(a * 2 + b)
        return probabilities.index(max(probabilities))

    def update(self, arm, success, time_taken):
        if success:
            self.successes[arm] += 1
            self.times[arm].append(time_taken)
        else:
            self.failures[arm] += 1


questions = [
    {"question": "What is 2 x 2?", "correct_answer": 4},
    {"question": "What is 3 x 5?", "correct_answer": 15},
    {"question": "What is 7 x 8?", "correct_answer": 56},
    {"question": "What is 9 x 8?", "correct_answer": 72},
    {"question": "What is 8 x 8?", "correct_answer": 64},
    {"question": "What is 9 x 9?", "correct_answer": 81},
    {"question": "What is 10 x 10?", "correct_answer": 100},
    {"question": "What is 4 x 5?", "correct_answer": 20},
    {"question": "What is 5 x 5?", "correct_answer": 25},
    {"question": "What is 6 x 6?", "correct_answer": 36},
    {"question": "What is 7 x 7?", "correct_answer": 49},
]

sampler = ThompsonSampler(questions)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        time_taken = float(request.form["time"])
        answer = int(request.form["answer"])
        correct_answer = questions[int(request.form["arm"])]["correct_answer"]
        success = answer == correct_answer
        sampler.update(int(request.form["arm"]), success, time_taken)
        # print(answer, " - ", correct_answer, " - ", time_taken)
        arm = sampler.select_arm()
        question = questions[arm]["question"]
        feedback = (
            [0, "You answered correctly!"]
            if success
            else [
                1,
                "Oops, your answer was incorrect.the correct answer is: "
                + str(correct_answer),
            ]
        )
        results = []
        for i, q in enumerate(questions):
            incorrect = sampler.failures[i]
            correct = sampler.successes[i]
            # Calculate average time
            times = sampler.times[i]
            total_time = sum(times)
            avg_time = total_time / len(times) if times else 0

            results.append(
                {
                    "question": q["question"],
                    "correct": correct,
                    "incorrect": incorrect,
                    "max_time": max(times) if times else 0,
                    "min_time": min(times) if times else 0,
                    "average_time": avg_time,
                }
            )

        return render_template(
            "index.html",
            question=question,
            arm=arm,
            feedback=feedback,
            results=results,
        )
    else:
        arm = sampler.select_arm()
        question = questions[arm]["question"]

        return render_template(
            "index.html",
            question=question,
            arm=arm,
            feedback=[0, ""],
        )


if __name__ == "__main__":
    app.run(debug=True)
