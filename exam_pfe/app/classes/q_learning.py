from collections import defaultdict
import json
import random
import numpy as np
class Q_learning:

    def __init__(self, questions, student=[]):
        self.n_states = len(questions)
        self.states = questions
        self.n_actions = 1
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.15
        self.successes = defaultdict(int)
        self.failures = defaultdict(int)
        self.times = defaultdict(list)
        self.student = student
        if student.questions_reward == [] :
            self.q_table = (np.ones(self.n_states) * 2) + (
                np.random.rand(self.n_states) / 5
            )
            self.update_student(self.q_table.tolist())
            student.questions_reward = json.dumps(self.q_table.tolist())
            student.save()
        else:
            self.q_table = json.loads(student.questions_reward)
        self.successive = defaultdict(int)
        self.print_q_table()
    def update_student(self,tbl):
        self.student.questions_reward = json.dumps(tbl)
        self.student.save()
    def select_action(self, state = None, chose_rand=False):
        old_state = state
        new_state = None
        # Select next question using epsilon-greedy policy
        if random.random() < self.epsilon or chose_rand:
            new_state = random.choice(range(self.n_states))
        else:
            new_state = np.argmax(self.q_table[:])
        if old_state == new_state:
            if(self.successive[new_state] > 2):
                new_state = self.select_action(state=new_state,chose_rand=True)
            else:
                self.successive[new_state] += 1
        else:
            self.successive[new_state] = self.successive[new_state] - 1 if self.successive[new_state] > 0 else 0
        return new_state
    def get_reward(self, answer,arm,time_taken):
        # Return reward based on answer
        if answer :
            self.successes[arm] += 1
            self.times[arm].append(time_taken)
        else:
            self.failures[arm] += 1
        t = time_taken/60000 if answer else 0 
        rand = np.random.random( )/4
        return (
            (
                (self.failures[arm] - self.successes[arm] * 4)
                / (1 + self.failures[arm] + self.successes[arm])
            )
            + t
            + rand
        )
    def update(self, state, reward):
        self.q_table[state] = 1 + self.alpha * (
            reward + self.gamma * np.max(self.q_table[:]) - self.q_table[state]
        )
        self.update_student(self.q_table)
        self.print_q_table()
    def print_q_table(self):
        for q in self.q_table:
            print(q, end=" - ")

        print("\n")
