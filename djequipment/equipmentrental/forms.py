from django import forms


class BookingForm(forms.Form):
    phone_number = forms.RegexField(regex=r'^\+\d{9,15}$', required=True, error_messages={'invalid': 'Phone number must be entered in the format: +999999999'})
    comment = forms.CharField(widget=forms.Textarea, required=False)


