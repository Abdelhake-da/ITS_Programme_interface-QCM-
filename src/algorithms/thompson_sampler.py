from statistics import mean
from algorithms.methods import is_correct, calc_note
import heapq
import random
from app.models import Question
from exam.models import Exam, Subject_answers_for_student
from student.models import StudentQuestions, Student


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
    def update_review(self,student:Student ,questions: list, answers: list, timer: list, module, courses):

        questions_id = [ question[1]['id'] for question in questions ]
        answers_bool_list , detail_answers = is_correct(questions,answers)
        detail_answers = [ [detail_answers[i],t] for i,t in enumerate(timer)]
        student_questions = [StudentQuestions.objects.get(student=student, question=Question.objects.get(id= question[1]['id'])) for question in questions]  # type: ignore
        for index,answer in enumerate(answers_bool_list):
            time_taking = student_questions[index].time_taking
            sub_ans_std = Subject_answers_for_student.objects.get_or_create(student=student, course=student_questions[index].question.course)[0]
            sub_ans_std.time_taking += float(timer[index])
            if answer:
                student_questions[index].successes += 1
                sub_ans_std.correct_answers += 1
                student_questions[index].successes_time += float(timer[index])
                student_questions[index].successes_time_index.append(len(time_taking))
            else:
                sub_ans_std.wrong_answers += 1
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
            sub_ans_std.save()
        exam = Exam.objects.create(student= student,module =  module)
        exam.courses.set(courses)
        exam.response_questions = {k: l for k, l in zip(questions_id, list(zip(answers_bool_list,detail_answers)))}
        exam.time_taken = sum(list(map(float, timer)))
        exam.note = float(calc_note(answers_bool_list))
        exam.num_correct_answers = list(answers_bool_list).count(True)
        exam.save()
        student.courses_exams.add(*courses)
        student.module_exams.add(exam.module)
        student.save

        return exam
