from collections import defaultdict
import random

from numpy import mean


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
