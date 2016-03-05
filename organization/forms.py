from django import forms

from .models import VerificationChoices


class VerificationForm(forms.Form):
    verification_status = forms.IntegerField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
            choices=VerificationChoices.choices(),
        )
    )

    citation = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Want to provide some citation?',
            'rows': 3
        }),
        required=False,
    )

    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Why are you rejecting this?',
            'rows': 3
        }),
        required=False,
    )

    signature = forms.BooleanField()

    def clean(self):
        cleaned_data = super().clean()
        verification_status = cleaned_data.get('verification_status')
        citation = cleaned_data.get('citation')
        rejection_reason = cleaned_data.get('rejection_reason')

        if verification_status == VerificationChoices.VERIFIED:
            if rejection_reason:
                raise forms.ValidationError(
                    'Rejection reason is entered for an accepted request'
                )

        elif verification_status == VerificationChoices.REJECTED:
            if not rejection_reason:
                raise forms.ValidationError(
                    'Rejection reason is not entered for a rejected request'
                )
            if citation:
                raise forms.ValidationError(
                    'Citation is entered for a rejected request'
                )
