from collections import defaultdict
import json
import random
import numpy as np

from app.classes.student import Student_class


class Q_learning:
    def __init__(self, questions,std):
        self.n_states = len(questions)
        self.states = questions
        self.n_actions : int= 1
        self.alpha : float = 0.1
        self.gamma : float = 0.9
        self.epsilon : float = 0.1
        self.successes = defaultdict(int)
        self.failures = defaultdict(int)
        self.times = defaultdict(list)
        self.index : int = 1
        self.randomNum : int = random.randint(1,100)
        self.std: Student_class = std
        self.successive = defaultdict(int)
        self.q_table, self.successes, self.failures, self.times = std.init_list(self.n_states)

        self.print_q_table()
    def select_action(self):
        chose_rand = False
        calc = int((self.randomNum * len(self.q_table) )/ 100)+1
        if self.index % calc == 0:
            chose_rand = True
            self.randomNum = random.randint(1, 100)
            self.index = 1
        else:
            self.index = self.index + 1
        # Select next question using epsilon-greedy policy
        if random.random() < self.epsilon or chose_rand:
            return random.choice(range(self.n_states))
        else:
            return (
                np.argmax(self.q_table[:])
                if len(self.q_table) > 0
                else random.choice(range(self.n_states))
            )
    def get_reward(self, answer,arm,time_taken):
        # Return reward based on answer
        if answer :
            self.successes[arm] += 1
            self.times[arm].append(time_taken)
        else:
            self.failures[arm] += 1

        avrg = sum(self.times[arm])/len(self.times[arm]) if len(self.times[arm]) > 0 else 0
        m = max(self.times[arm])-min(self.times[arm]) if len(self.times[arm]) >= 2 else (max(self.times[arm]) if len(self.times[arm]) > 0 else 1)
        # rand = np.random.random( )/4
        return (
            (
                (self.failures[arm] - self.successes[arm] * 2.5)
                / (1 + self.failures[arm] + self.successes[arm])
            )
            + ((avrg / m+1))/5 if len(self.times[arm]) >= 2 else 0 
        )
    def update(self, state, reward, student_stat):
        self.q_table[state] = 1 + self.alpha * (
            reward + self.gamma * np.max(self.q_table[:]) - self.q_table[state]
        )
        self.std.update_questions_reward(self.q_table, student_stat)
    def print_q_table(self,state= None):
        if state != None:
            print(f"{state}")

        for q in self.q_table:
            print(f"{q:.2f}", end=" - ")

        print("\n")
