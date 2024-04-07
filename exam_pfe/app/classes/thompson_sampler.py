from collections import defaultdict
import random

from numpy import mean

from app.classes.student import Student_class


class ThompsonSampler:
    def __init__(self, arms, std:Student_class):

        self.arms = arms
        self.num_arms = len(arms)
        self.probabilities, self.successes, self.failures, self.times = std.init_list(
            self.num_arms
        )
        self.probabilities = list(self.probabilities)
        self.std: Student_class = std
        self.iteration = 0
    def update_probabilities(self, arm , new = False):
        alpha1 = self.failures[arm] + 1
        beta1 = self.successes[arm] + 1
        a = random.betavariate(alpha1, beta1)
        alpha2 = self.times[arm][-1] if len(self.times[arm]) >= 1 else 1
        beta2 = mean(self.times[arm]) if len(self.times[arm]) >= 2 else 1
        b = random.betavariate(alpha2, abs(beta2))
        if new :
            self.probabilities.append(a + b / 2.5)
        else :
            self.probabilities[arm] = a + b / 2.5

    def select_action(self):
        self.iteration += 1
        print(self.iteration)
        if self.iteration % 5 == 1:
            return random.randint(0, self.num_arms - 1)
        print('---------------------------------------')
        print (type(self.probabilities))
        print("---------------------------------------")
        return self.probabilities.index(max(self.probabilities))

    def get_reward(self, success, arm, time_taken):

        if success:
            self.successes[arm] += 1
        else:
            self.failures[arm] += 1
        self.times[arm].append(time_taken)

    def update(self, arm, reward=None, student_stat=None):
        self.update_probabilities(arm)
        print('---------------------- hello -------------------')
        self.std.update_questions_reward(self.probabilities, student_stat)
