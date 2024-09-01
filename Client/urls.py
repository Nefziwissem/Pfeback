from django.urls import path
from .views import (
    ClientCommentDetailView, ClientCommentLikeView, ClientCommentListView, ClientCommentView, ClientListView, ClientDetailView, toggle_active,
    SendPaymentRemindersView,create_client, trigger_send_reminders_view,
    ClientCheckUnpaidView, FileUploadView,  FileDeleteView, FileDownloadView,
    ClientDocumentsView,update_client,DocumentAssignmentView , FileDetailView # Import the new view
)

urlpatterns = [   
    path('clients/create/', create_client, name='create-client'),
    path('clients/<int:pk>/update/', update_client, name='update_client'),


    path('clients/<int:client_id>/documents/assign/', DocumentAssignmentView.as_view(), name='document-assign'),
    path('clients/<int:client_id>/files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),

    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:pk>/toggle_active/', toggle_active, name='toggle-active'),
    path('clients/send_payment_reminders/', SendPaymentRemindersView.as_view(), name='send-payment-reminders'),
    path('clients/trigger_send_reminders/', trigger_send_reminders_view, name='trigger-send-reminders'),
    path('clients/check_unpaid/', ClientCheckUnpaidView.as_view(), name='check-unpaid'),
    path('clients/<int:client_id>/upload-file/', FileUploadView.as_view(), name='upload-file'),
    path('clients/<int:client_id>/documents/', ClientDocumentsView.as_view(), name='client-documents'),
    path('clients/<int:client_id>/documents/<int:file_id>/', FileDeleteView.as_view(), name='delete_file'),
    path('files/<int:file_id>/download/', FileDownloadView.as_view(), name='download-file'),
    path('clients/<int:client_id>/comments/', ClientCommentView.as_view(), name='client-comments-list'),  # GET, POST
    path('comments/<int:comment_id>/', ClientCommentView.as_view(), name='client-comment-detail'),  # PUT, DELETE
    path('clients/<int:client_id>/comments/list/', ClientCommentListView.as_view(), name='client-comment-list'),  # GET, POST
    path('comments/<int:comment_id>/like/', ClientCommentLikeView.as_view(), name='client-comment-like'),  # POST
 path('client/comments/<int:comment_id>/', ClientCommentDetailView.as_view(), name='comment-detail'),

path('client/<int:client_id>/comments/', ClientCommentView.as_view(), name='client-comments'),
path('client/<int:client_id>/comments/list/', ClientCommentListView.as_view(), name='client-comments-list'),
path('comments/<int:comment_id>/like/', ClientCommentLikeView.as_view(), name='client-comment-like'),
path('comments/<int:comment_id>/', ClientCommentDetailView.as_view(), name='client-comment-detail'),  # GET, PUT, DELETE
]