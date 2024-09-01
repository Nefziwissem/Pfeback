# marchand/urls.py
from django.urls import path
from .views import DocumentAssignmentView, FilleDeleteView, FilleDetailView, FilleDownloadView, FilleUploadView, MarchandListCreate, MarchandDetail, MarchandSalesView,SendReminderView,create_marchand, sales_data

urlpatterns = [
    path('marchands/', MarchandListCreate.as_view(), name='marchand-list-create'),
    path('marchands/create/', create_marchand, name='marchand-list-create'),

    path('marchands/<int:pk>/', MarchandDetail.as_view(), name='marchand-detail'),
    path('send-reminders1/', SendReminderView.as_view(), name='send-reminders'),
    path('marchands/<int:pk>/update/', MarchandDetail.as_view(), name='marchand-detail'),

    path('marchands/<int:marchand_id>/upload-file/', FilleUploadView.as_view(), name='upload-file'),
    path('marchands/<int:marchand_id>/files/<int:pk>/', FilleDetailView.as_view(), name='file-detail'),
    path('marchands/files/<int:fille_id>/download/', FilleDownloadView.as_view(), name='download-file'),
    path('marchands/<int:marchand_id>/documents/<int:fille_id>/', FilleDeleteView.as_view(), name='delete_file'),
    path('marchands/<int:marchand_id>/sales/', MarchandSalesView.as_view(), name='marchand-sales'),
    path('marchands/sales-data/', sales_data, name='sales-data'),
    
]