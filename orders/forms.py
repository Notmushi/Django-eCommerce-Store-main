from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, label='Full Name')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Phone')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Address')
    city = forms.CharField(max_length=100, label='City')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
