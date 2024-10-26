from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload Excel/CSV File", help_text="Only .csv or .xlsx files")
