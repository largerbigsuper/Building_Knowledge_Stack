from rest_framework import routers

from apps.customer.customers.viewsets import CustomerViewSet
from apps.customer.subjects.viewsets import CustomerSubjectViewSet, CustomerSubjectermViewSet, CustomerApplicationViewSet
from apps.customer.questions.viewsets import CustomerQuestionViewSet, CustomerQuestionRecordViewSet, CustomerExamViewSet
from apps.customer.sms.viewsets import CustomerSMSViewSet
from apps.customer.articles.viewsets import CustomerArticleViewSet, CustomerTagViewSet
from apps.customer.feedback.viewsets import CustomerFeedbackViewSet
from apps.customer.invite.viewsets import CustomerInviteRecordViewSet, CustomerBlanceRecordViewSet, CustomerWithDrawRecordViewSet

customer_router = routers.DefaultRouter()

customer_router.register('u', CustomerViewSet, base_name='customer')
customer_router.register('subject', CustomerSubjectViewSet, base_name='customer-subject')
customer_router.register('subject-term', CustomerSubjectermViewSet, base_name='customer-subject-term')
customer_router.register('question', CustomerQuestionViewSet, base_name='customer-question')
customer_router.register('question-record', CustomerQuestionRecordViewSet, base_name='customer-question-record')
customer_router.register('exam', CustomerExamViewSet, base_name='exam')
customer_router.register('sms', CustomerSMSViewSet, base_name='sms')
customer_router.register('tag', CustomerTagViewSet, base_name='tag')
customer_router.register('article', CustomerArticleViewSet, base_name='article')
customer_router.register('application', CustomerApplicationViewSet, base_name='application')
customer_router.register('feedback', CustomerFeedbackViewSet, base_name='feedback')
customer_router.register('invite_record', CustomerInviteRecordViewSet, base_name='invite_record')
customer_router.register('blance_record', CustomerBlanceRecordViewSet, base_name='blance_record')
customer_router.register('withdraw_record', CustomerWithDrawRecordViewSet, base_name='withdraw_record')
