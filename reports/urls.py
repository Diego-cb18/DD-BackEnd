from django.urls import path
from .views import ReportUploadView, ReportListView, MarkAsReviewedView

urlpatterns = [
    path('upload/', ReportUploadView.as_view(), name='upload_report'),
    path('', ReportListView.as_view(), name='list_reports'),
    path('<int:pk>/mark-reviewed/', MarkAsReviewedView.as_view(), name='mark_reviewed'),
]
