import json

from django.db import models
from django_extensions.db.fields.json import JSONField

from server.settings import DB_PREFIX
from lib.modelmanager import ModelManager


class QuestionManager(ModelManager):
    pass


class Question(models.Model):
    """题目"""

    subject = models.ForeignKey('subjects.Subject',
                                on_delete=models.SET_NULL, blank=True, null=True, verbose_name='科目')
    qtype = models.PositiveSmallIntegerField(choices=ModelManager.Question_Type,
                                             default=ModelManager.Question_Type_Danxuanti,
                                             verbose_name='题型')
    content = models.TextField(verbose_name='题目内容')
    choices = JSONField(verbose_name='选项列表')
    # [{"label": "A", "content": "选项内容"}, {"label": "A", "content": "选项内容"},]
    images = JSONField(verbose_name='图片列表')
    # [{"url": "https:xxx.jpg", "name": "图1"}]
    answer = JSONField(verbose_name='正确答案')
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


class ExamManager(ModelManager):
    pass


class Exam(models.Model):
    """模拟考试"""

    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, verbose_name='考试人')
    questions = JSONField(verbose_name='题目列表')
    # [id1, id2,]
    answer = JSONField(verbose_name='答案列表')
    # [{"id": qid, "answer": [], "is_correct": True},]
    result = JSONField(verbose_name='考试结果')
    # {"correct_cout": 20, "wrong_cout": 10, "blank_count": 0, "score": 100}
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
