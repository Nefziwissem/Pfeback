from django.urls import path
from .views import MachineListCreate, MachineDetail, SendMachineRemindersView, create_machine, delete_machine

urlpatterns = [
    path('machines/', MachineListCreate.as_view(), name='machine-list-create'),
    path('machines/<int:pk>/', MachineDetail.as_view(), name='machine-detail'),
    path('machines/<int:pk>/update/', MachineDetail.as_view(), name='machine-detail'),

    path('machines/send_payment_reminders/', SendMachineRemindersView.as_view(), name='send-payment-reminders'),
    path('machines/create/', create_machine, name='create-client'),
    path('machines/delete/<str:id_machine>/', delete_machine, name='delete-machine'),
]
