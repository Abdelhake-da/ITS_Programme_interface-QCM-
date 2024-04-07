import datetime
import json
import random
from app.models import  Module, Course, Question, Student_Course_Reward
from app.classes.q_learning import Q_learning
from app.classes.thompson_sampler import ThompsonSampler


def is_correct(answer: list, correct_answer: list) -> bool :  
    if len(answer) == len(correct_answer):
        return all(int(answer[i]) in correct_answer for i in range(len(answer)))
    return False
def solution(question: dict) -> list:
    strs:list = ["", []]
    strs[0] = "Oops, your answer was incorrect."
    strs[1] = [
        str(question["possible_choses"][int(i) - 1]["text"])
        for i in question["correct_answer"]
    ]
    return strs
def get_courses()-> dict:
    modules : list = list(Module.objects.filter())
    courses : dict = {}
    for module in modules:
        courses[module.name] = []
        for course in list(Course.objects.filter(module=module)):
            courses[module.name].append(course.name)
    return courses
def get_data_from_db(module, course, type) -> list:
    module_model : Module = Module.objects.get(name=module)
    course_model : Course = Course.objects.get(name=course, module=module_model)
    questions : Question = Question.objects.get(course=course_model, question_type=type)
    
    questions_list : list = []
    for question in json.loads(questions.question):
        question_text = question["question"]
        possible_choses = list(question["choices"])
        answer = list(question["answers"])
        questions_list.append(
            {
                "question": question_text,
                "possible_choses": possible_choses,
                "correct_answer": answer,
            }
        )

    return questions_list
def get_stats(sampler, questions):
    results = []
    for i, q in enumerate(questions):
        incorrect = sampler.failures[i]
        correct = sampler.successes[i]
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
    return results
def load_data_as_json(file):
    data = json.load(file)
    for module in data:
        module_name = module["module"]
        module_model = Module.objects.get_or_create(name=module_name)
        for course in module["course"]:
            course_name = course["cours"]
            course_model = Course.objects.get_or_create(
                name=course_name, module=module_model[0]
            )

            if len(course["type"]["qcm"]) > 1:
                questions = course["type"]["qcm"]
                Question.objects.get_or_create(
                    course=course_model[0],
                    question_type="qcm",
                    question=json.dumps(questions),
                )

            if len(course["type"]["not qcm"]) > 1:
                questions = course["type"]["not qcm"]
                Question.objects.get_or_create(
                    course=course_model[0],
                    question_type="one_word",
                    question=json.dumps(questions),
                )
def load_data(file):
    data = json.load(file)
    for module in data:
        module_name = module["module"]
        module_model = Module.objects.get_or_create(name=module_name)
        for course in module["course"]:
            course_name = course["cours"]
            course_model = Course.objects.get_or_create(
                name=course_name, module=module_model[0]
            )

            if len(course["type"]["qcm"]) > 1:
                questions = course["type"]["qcm"]
                Question.objects.get_or_create(
                    course=course_model[0],
                    question_type="qcm",
                    question=json.dumps(questions),
                )
            if len(course["type"]["not qcm"]) > 1:
                questions = course["type"]["not qcm"]
                Question.objects.get_or_create(
                    course=course_model[0],
                    question_type="one_word",
                    question=json.dumps(questions),
                )


def get_feedback(index_question, questions, answer):
    return (
        [0, ["You answered correctly!"]]
        if is_correct(answer, questions[index_question]["correct_answer"])
        else [1, solution(questions[index_question])]
    )


def question_treatment(
    answer, questions, index_question, time_taken, sampler
):
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    success = is_correct(answer, questions[index_question]["correct_answer"])

    dict_questions = {
        "key": index_question,
        "value": {
            "time_taken": time_taken,
            "success": success,
            "time": time,
            "answer": answer,
        },
    }

    sampler.update(
        index_question,
        sampler.get_reward(success, index_question, time_taken),
        dict_questions,
    )


def get_context(sampler, questions, student):
    arm = sampler.select_action()
    question = questions[arm]["question"]
    possible_choses = questions[arm]["possible_choses"]
    return {
        "courses": get_courses(),
        "question": question,
        "possible_choses": add_upper_alpha(
            random.sample(possible_choses, len(possible_choses))
        ),
        "arm": arm,
        "feedback": [0, ""],
        "results": get_stats(sampler, questions),
        "student": student.name,
        "state": True,
        "answer": [],
    }


def init_variables(module_name, course_name, std, type = "qcm", function = 1):
    questions = get_data_from_db(module_name, course_name,type)
    std.student_course_reward = Student_Course_Reward.objects.get_or_create(
        student=std.student, course=Course.objects.get(name=course_name)
    )[0]

    sampler = Q_learning(questions,std) if function == 1 else ThompsonSampler(questions, std)
    arm = sampler.select_action()
    question = questions[arm]["question"]
    possible_choses = list(questions[arm]["possible_choses"])
    return questions,sampler,arm,question,possible_choses


def add_upper_alpha(lis):
    exist = lis[0]['text'][1] == '.' if len(lis[0]['text']) > 2 else False
    for i, item in enumerate(lis, 0):
        if exist:
            item["text"] = f"{chr(i + 65)}. {item['text'][2:]}"
        else:
            item["text"] = f"{chr(i + 65)}. {item['text']}"
    return lis
