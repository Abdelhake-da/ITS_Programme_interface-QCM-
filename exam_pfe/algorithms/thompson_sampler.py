from statistics import mean
from algorithms.methods import is_correct
import heapq
import random
from app.models import Question
from student.models import StudentQuestions


class ThompsonSampler:
    def __init__(self, arms, rewards, nb_questions):
        self.arms = arms
        self.probabilities = rewards
        self.nb_questions = nb_questions
    def select_arms(self):
        new_questions = int(self.nb_questions/3)
        old_questions = self.nb_questions - new_questions
        random_values = random.sample(self.probabilities, new_questions)
        remaining_values = [
            val for val in self.probabilities if val not in random_values
        ]
        max_values = heapq.nlargest(old_questions, remaining_values)
        all_questions = list(max_values + random_values)
        random.shuffle(all_questions)
        return [self.probabilities.index(val) for val in all_questions]
    def get_reward(self, failures, successes, times, times_index, sum_times):
        alpha1 = failures if failures > 0 else 1
        beta1 = successes if successes > 0 else 1
        a = random.betavariate(alpha1, beta1)
        print(times_index[-1] if len(times_index) > 0 else 100)
        alpha2 = times[times_index[-1]] if len(times_index) > 0 else 100
        beta2 = sum_times/len(times_index) if len(times_index) > 0 else 100
        b = random.betavariate(float(alpha2), abs(float(beta2)))
        return a + b / 2.5
    def update_review(self,user ,questions: list, answers: list, timer: list):
        answers_bool_list = is_correct(questions,answers)
        student_questions = [StudentQuestions.objects.get(student=user, question=Question.objects.get(id= question[1]['id'])) for question in questions]  # type: ignore
        for index,answer in enumerate(answers_bool_list):
            time_taking = student_questions[index].time_taking
            
            if answer:
                student_questions[index].successes += 1
                student_questions[index].successes_time += float(timer[index])
                student_questions[index].successes_time_index.append(len(time_taking))
            else:
                student_questions[index].failures += 1
            time_taking.append(timer[index]) 
            student_questions[index].reward = self.get_reward(
                student_questions[index].failures,
                student_questions[index].successes,
                time_taking,
                student_questions[index].successes_time_index,
                student_questions[index].successes_time,
            )
            student_questions[index].save()

        # alpha1 = self.failures[arm] + 1
        # beta1 = self.successes[arm] + 1
        # a = random.betavariate(alpha1, beta1)
        # alpha2 = self.times[arm][-1] if len(self.times[arm]) >= 1 else 1
        # beta2 = mean(self.times[arm]) if len(self.times[arm]) >= 2 else 1
        # b = random.betavariate(alpha2, abs(beta2))
        # if new :
        #     self.probabilities.append(a + b / 2.5)
        # else :
        #     self.probabilities[arm] = a + b / 2.5
        # pass
