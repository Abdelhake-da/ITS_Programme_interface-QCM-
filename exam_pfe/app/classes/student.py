from collections import defaultdict
import json
import numpy as np
from app.models import Course, Student, Student_Course_Reward

# lqs
class Student_class:
    def __init__(self) -> None:
        self.student: Student = None
        self.student_course_reward: Student_class = None
    def init_list(self,n_states):
        successes, failures, times = (
            defaultdict(int),
            defaultdict(int),
            defaultdict(list),
        )
        list_ : list = []
        if (
            self.student_course_reward.questions_reward == []
            or self.student_course_reward.questions_reward == "[]"
        ):
            list_ = (np.ones(n_states) * 4) + (
                np.random.rand(n_states) / 5
            )
            self.update_questions_reward(list_.tolist())
            self.student_course_reward.questions_reward = json.dumps(list_.tolist())
            self.student_course_reward.save()
        else:
            list_ = json.loads(str(self.student_course_reward.questions_reward))
            successes, failures, times = self.get_stat()
        return list_, successes, failures, times
    def get_stat(self):
        successes, failures, times = (
            defaultdict(int),
            defaultdict(int),
            defaultdict(list),
        )
        stat = self.student_course_reward.student_stat
        for key, value in stat.items():
            for val in value:
                if val["success"]:
                    successes[int(key)] += 1
                else:
                    failures[int(key)] += 1
                times[int(key)].append(val["time_taken"])
        return successes,failures,times
    def update_questions_reward(self, tbl, stat = {}):
        try:
            self.student_course_reward.questions_reward = json.dumps(tbl)
        except:
            pass
        if stat != {}:
            if str(stat["key"]) not in self.student_course_reward.student_stat:
                self.student_course_reward.student_stat[str(stat["key"])] = []
            self.student_course_reward.student_stat[str(stat["key"])].append(stat["value"])
        print(tbl)

        self.student_course_reward.save()
    def create_student(self,student_id, user_name, password, name):
        Student.objects.create(student_id = student_id, user_name = user_name,password = password, name = name)
    def get_student(self,student_id):
        self.student = Student.objects.get(student_id=student_id)
    def get_or_create_course_reward(self, course_name):
        self.student_course_reward = Student_Course_Reward.objects.get_or_create(
            student=self.student, course=Course.objects.get(name=course_name)
        )
