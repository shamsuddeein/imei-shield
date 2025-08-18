from django import forms
from .models import Report
from .validators import validate_imei


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            "imei",
            "owner_name",
            "phone_model",
            "last_seen_location",
            "contact_info",
            "proof_of_ownership",
        ]

        widgets = {
            "imei": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter 15-digit IMEI"}
            ),
            "owner_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your full name"}
            ),
            "phone_model": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Brand & Model (e.g. Samsung Galaxy S23)"}
            ),
            "last_seen_location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Where was the phone last seen?"}
            ),
            "contact_info": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Email or Phone Number"}
            ),
            "proof_of_ownership": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean_imei(self):
        imei = self.cleaned_data.get("imei")
        validate_imei(imei)  # run Luhn validation
        return imei


class ImeiCheckForm(forms.Form):
    imei = forms.CharField(
        max_length=15,
        validators=[validate_imei],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter IMEI to check"}
        ),
    )
