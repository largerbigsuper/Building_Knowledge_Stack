import json
import random

from django.db import models
from django.db.models import Count
from django_extensions.db.fields.json import JSONField

from server.settings import DB_PREFIX
from lib.modelmanager import ModelManager
from lib.common import strtime


class QuestionManager(ModelManager):

    cache_key = 'q_{pk}'

    def get_random_questions(self, subject_id, qtype, count):
        all_id_list = self.filter(
            subject_id=subject_id, qtype=qtype).values_list('id', flat=True)
        all_id_list = list(all_id_list)
        if count > len(all_id_list):
            return all_id_list
        else:
            return random.sample(all_id_list, count)

    def get_question(self, pk, use_cache=True):
        if use_cache is True:
            cached = self.cache.get(self.cache_key.format(pk=pk))
            if not cached:
                q = self.filter(pk=pk).first()
                if q is None:
                    data = {}
                else:
                    data = q.dict
                self.cache.set(self.cache_key.format(pk=pk), data)
                return data
            else:
                return cached


class Question(models.Model):
    """题目"""

    subject = models.ForeignKey('subjects.Subject',
                                on_delete=models.SET_NULL, blank=True, null=True, verbose_name='科目')
    qtype = models.PositiveSmallIntegerField(choices=ModelManager.Question_Type,
                                             default=ModelManager.Question_Type_Danxuanti,
                                             verbose_name='题型')
    content = models.TextField(verbose_name='题目内容')
    choices = JSONField(default='[]', verbose_name='选项列表')
    # [{"label": "A", "content": "选项内容"}, {"label": "A", "content": "选项内容"},]
    images = JSONField(default='[]', verbose_name='图片列表')
    # [{"url": "https:xxx.jpg", "name": "图1"}]
    answer = JSONField(default='[]', verbose_name='正确答案')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = QuestionManager()

    class Meta:
        db_table = DB_PREFIX + 'questions'
        ordering = ['-id']

    def __str__(self):
        return '<{qid}: {content}>'.format(qid=self.id, content=self.content[:10])

    def is_correct_answer(self, answer_list):
        """判断答案对错"""
        upper_correct_answer = [choice.upper() for choice in list(self.answer)]
        upper_answer_list = [choice.upper() for choice in answer_list]
        if len(upper_correct_answer) != len(upper_answer_list):
            return ModelManager.Answer_Result_Wrong
        for item in upper_correct_answer:
            if item not in upper_answer_list:
                return ModelManager.Answer_Result_Wrong
        return ModelManager.Answer_Result_Correct

    @property
    def dict(self):
        data = {
            'id': self.id,
            'subject_id': self.subject_id,
            'qtype': self.qtype,
            'content': self.content,
            'choices': self.choices,
            'images': self.images,
            'answer': self.answer,
            'update_at': strtime(self.update_at),
            'create_at': strtime(self.create_at)
        }
        return data


class ExamManager(ModelManager):

    def _gen_an_exam(self, customer_id, subject_id):
        """生成试卷题目"""
        panduan_count = danxuan_count = duoxuan_count = 1
        panduan_list = mm_Question.get_random_questions(
            subject_id, self.Question_Type_Panduanti, panduan_count)
        danxuan_list = mm_Question.get_random_questions(
            subject_id, self.Question_Type_Danxuanti, danxuan_count)
        duoxuan_list = mm_Question.get_random_questions(
            subject_id, self.Question_Type_Duouanti, duoxuan_count)
        questions = panduan_list + danxuan_list + duoxuan_list

        exam = self.create(customer_id=customer_id,
                           subject_id=subject_id, questions=questions)

        return exam

    def _gen_exam_result(self, exam_id=None, exam=None):
        """提交试卷"""
        if exam is not None:
            _exam = exam
        else:
            _exam = self.get(pk=exam_id)
        questions = _exam.questions
        result_list = mm_QuestionRecord.filter(pk__in=questions).values_list(
            'is_correct').annotate(total=Count('id'))
        result_dict = dict(result_list)
        correct_count = result_dict.get(self.Answer_Result_Correct, 0)
        wrong_count = result_dict.get(self.Answer_Result_Wrong, 0)
        blank_count = len(questions) - correct_count - wrong_count
        result = {
            'correct_cout': correct_count,
            'wrong_cout': wrong_count,
            'blank_count': blank_count
        }
        _exam.result = result
        _exam.save()
        return _exam


class Exam(models.Model):
    """模拟考试"""

    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, verbose_name='考试人')
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.DO_NOTHING, verbose_name='所属科目', null=True, blank=True)
    questions = JSONField(default='[]', verbose_name='题目列表')
    # [id1, id2,]
    answer = JSONField(default='[]', verbose_name='答案列表')
    # [{"id": qid, "answer": [], "is_correct": True},]
    result = JSONField(default='{}', verbose_name='考试结果')
    # {"correct_count": 20, "wrong_cout": 10, "blank_count": 0, "score": 100}
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = ExamManager()

    class Meta:
        db_table = DB_PREFIX + 'exams'


class QuestionRecordManager(ModelManager):

    def my_records(self, customer_id, subject_id=None, exam_id=None):
        queryset = self.filter(customer_id=customer_id)
        if subject_id is not None:
            queryset = queryset.filter(question__subject_id=subject_id)
        if exam_id is not None:
            queryset = queryset.filter(exam_id=exam_id)
        return queryset


class QuestionRecord(models.Model):
    """题目提交记录"""

    # FIXME 修改为一题只有一条提交记录，并及时更新答题结果
    question = models.ForeignKey(
        'questions.Question', on_delete=models.DO_NOTHING, verbose_name='作业')
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, verbose_name='提交人')
    answer = JSONField(verbose_name='考生答案')
    is_correct = models.PositiveSmallIntegerField(choices=ModelManager.Answer_Result,
                                                  default=ModelManager.Answer_Result_Correct,
                                                  verbose_name='正确/错误')
    exam = models.ForeignKey('questions.Exam',
                             on_delete=models.DO_NOTHING,
                             blank=True, null=True, verbose_name='模拟考试')
    update_at = models.DateTimeField(auto_now=True,
                                     verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = QuestionRecordManager()

    class Meta:
        db_table = DB_PREFIX + 'question_records'


mm_Question = Question.objects
mm_Exam = Exam.objects
mm_QuestionRecord = QuestionRecord.objects
