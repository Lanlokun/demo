from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    Event,
    Participant,
    ParticipantType,
    AccessCoupon,
    CouponType
)

class EventForm(ModelForm):
    prefix = "Event"

    class Meta:
        model = Event
        fields = ["name", "description", "date", "location"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
    
class InEventForm(forms.Form):
    is_checked = forms.BooleanField(required=False)

class BreakfastForm(forms.Form):
    eaten = forms.BooleanField(required=False)

class LunchForm(forms.Form):
    eaten = forms.BooleanField(required=False)
    
    

class ParticipantForm(ModelForm):
    prefix = "Participant"

    class Meta:
        model = Participant
        fields = [
            "event",
            "full_name",
            "email",
            "phone_number",
            "address",
            "image",
            "type",
            "in_event",
            "breakfast",
            "lunch",
        ]    

    # make image field optional   
    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields["image"].required = False 


class ParticipantTypeForm(ModelForm):
    prefix = "ParticipantType"

    class Meta:
        model = ParticipantType
        fields = ["name", "description"]

class CouponTypeForm(ModelForm):
    prefix = "CouponType"

    class Meta:
        model = CouponType
        fields = ["name", "start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

class AccessCouponForm(ModelForm):
    prefix = "AccessCoupon"

    class Meta:
        model = AccessCoupon
        fields = ["participant", "coupon_type", "redeemed", "redeemed_at"]
        widgets = {
            "redeemed_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    
    
    
    