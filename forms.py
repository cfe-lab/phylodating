from django.forms import ModelForm
from django.forms import TextInput
from django.forms import FileInput
from .models import Job

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = [
            'email',
            'info_csv',
            'unrooted_tree',
            # 'rooted_tree_out',
            # 'data_out',
            # 'stats_out'
        ]
        widgets = {
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email here'
            }),
            'info_csv': FileInput(attrs={
                'class': 'custom-file-input',
            }),
            'unrooted_tree': FileInput(attrs={
                'class': 'custom-file-input',
            }),
        }
        # labels = {
        #     'email': 'Email'
        # }