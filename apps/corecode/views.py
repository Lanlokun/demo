from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, View, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import io
import csv
import zipfile
from django.http import HttpResponse
from .models import Participant, ParticipantBulkUpload, AccessCoupon



from .forms import (
    EventForm,
    ParticipantForm,
    ParticipantTypeForm,
    AccessCouponForm,
    CouponTypeForm,
)
from .models import (
    Event,
    Participant,
    ParticipantType,
    AccessCoupon,
    CouponType
)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

class EventListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Event
    template_name = "corecode/event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EventForm()
        return context


# class EventDetailView(LoginRequiredMixin, SuccessMessageMixin, ListView):
#     model = Event
#     template_name = "corecode/event_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = EventForm()
#         return context
    


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    fields = "__all__"
    template_name = "corecode/mgt_form.html"
    success_message = "New event successfully added"

    def get_success_url(self):
        return reverse_lazy("add-events")


class EventUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy("events")
    success_message = "Event successfully updated."
    template_name = "corecode/mgt_form.html"


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy("events")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The event {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(EventDeleteView, self).delete(request, *args, **kwargs)



class ParticipantListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Participant
    template_name = "corecode/participant_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParticipantForm()
        return context

class ParticipantDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Participant
    template_name = "corecode/participant_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParticipantForm()
        return context


@csrf_exempt  # You may need to disable CSRF protection for this view.
@require_POST  # Use POST request for QR code scanning.
def qr_code_scan(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the POST request.
            data = json.loads(request.body.decode('utf-8'))
            
            # Extract participant ID or UUID from the QR code data.
            participant_id = data.get('participant_id')
            
            # Look up the participant by their unique identifier.
            participant = get_object_or_404(Participant, id=participant_id)
            
            # Update the participant's in_event, breakfast, and lunch columns.
            participant.in_event = True
            participant.breakfast = True  # You can adjust this as needed.
            participant.lunch = True  # You can adjust this as needed.
            
            # Save the updated participant record.
            participant.save()
            
            # Return a success response.
            return HttpResponse("Participant updated successfully.")
        except Exception as e:
            # Handle any exceptions that may occur during the update process.
            return HttpResponse("Error updating participant: " + str(e))
    
    return HttpResponse("Invalid request method.")


def generate_qr_code(participant):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Generate a unique identifier for the participant (e.g., participant ID)
    participant_identifier = participant.id  # You can adjust this based on your data structure
    
    # Build the full URL that includes the domain (local server)
    qr_code_scan_url = settings.SITE_DOMAIN + reverse('qr_code_scan') + f'?participant_id={participant_identifier}'
    
    # Add the QR code scanning URL to the QR code data
    qr.add_data(qr_code_scan_url)
    qr.make(fit=True)

    # Create a PIL Image
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create a BytesIO object to hold the image data
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")

    # Create an InMemoryUploadedFile from the BytesIO object
    qr_code_image = InMemoryUploadedFile(
        ContentFile(buffer.getvalue()),
        None,  # Field name
        f"qr_codes/{participant.full_name}.png",  # File name/path in your media directory
        "image/png",  # Content type
        buffer.tell,  # File size
        None,  # Content type extra headers
    )

    # Save the QR code image to the participant's qr_code_image field
    participant.qr_code_image = qr_code_image
    participant.save()

class ParticipantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("participants")
    success_message = "New participant successfully added"

    def form_valid(self, form):
        # Create a Participant instance but don't save it yet
        participant = form.save(commit=False)
    
        # Save the participant instance to get an ID
        participant.save()

        # Generate the QR code with the updated participant instance
        generate_qr_code(participant)

        # Save the participant instance again to ensure it gets an ID
        participant.save()

        return super().form_valid(form)



class ParticipantUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    success_url = reverse_lazy("participants")
    success_message = "Participant successfully updated."
    template_name = "corecode/mgt_form.html"


class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
    model = Participant
    success_url = reverse_lazy("participants")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The participant {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.full_name))
        return super(ParticipantDeleteView, self).delete(request, *args, **kwargs)

class ParticipantBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ParticipantBulkUpload
    template_name = "corecode/participants_upload.html"
    fields = ["csv_file"]
    success_url = "/participant/list"
    success_message = "Successfully uploaded participants"

class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="participant_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "event",
                "full_name",
                "email",
                "phone_number",
                "address",
                "type",

            ]
        )

        return response

 
class ParticipantTypeListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = ParticipantType
    template_name = "corecode/participant_type_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParticipantTypeForm()
        return context

class ParticipantTypeDetailView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = ParticipantType
    template_name = "corecode/participant_type_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParticipantTypeForm()
        return context


class ParticipantTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ParticipantType
    form_class = ParticipantTypeForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("participant_types")
    success_message = "New participant type successfully added"


class ParticipantTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ParticipantType
    form_class = ParticipantTypeForm
    success_url = reverse_lazy("participant_types")
    success_message = "Participant type successfully updated."
    template_name = "corecode/mgt_form.html"


class ParticipantTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = ParticipantType
    success_url = reverse_lazy("participant_types")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The participant type {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ParticipantTypeDeleteView, self).delete(request, *args, **kwargs)

@login_required
def download_all_participants(request):
    participants = Participant.objects.all()

    # Create an in-memory ZIP file to store participant images
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for participant in participants:
            # Add each participant's image to the ZIP file
            if participant.image:
                image_data = participant.image.read()
                zip_file.writestr(f'{participant.full_name}.jpg', image_data)

    # Prepare the response with the ZIP file
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=participants.zip'
    return response

class CouponTypeListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = CouponType
    template_name = "corecode/coupon_type_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CouponTypeForm()
        return context

class CouponTypeDetailView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = CouponType
    template_name = "corecode/coupon_type_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CouponTypeForm()
        return context    
        

class CouponTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CouponType
    form_class = CouponTypeForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("coupon_types")
    success_message = "New coupon type successfully added"


class CouponTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CouponType
    form_class = CouponTypeForm
    success_url = reverse_lazy("coupon_types")
    success_message = "Coupon type successfully updated."
    template_name = "corecode/mgt_form.html"


class CouponTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = CouponType
    success_url = reverse_lazy("coupon_types")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The coupon type {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(CouponTypeDeleteView, self).delete(request, *args, **kwargs)

class AccessCouponListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AccessCoupon
    template_name = "corecode/access_coupon_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AccessCouponForm()
        return context


class AccessCouponDetailView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AccessCoupon
    template_name = "corecode/access_coupon_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AccessCouponForm()
        return context

class AccessCouponCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AccessCoupon
    form_class = AccessCouponForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("access_coupons")
    success_message = "New access coupon successfully added"


class AccessCouponUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AccessCoupon
    form_class = AccessCouponForm
    success_url = reverse_lazy("access_coupons")
    success_message = "Access coupon successfully updated."
    template_name = "corecode/mgt_form.html"



class AccessCouponDeleteView(LoginRequiredMixin, DeleteView):
    model = AccessCoupon
    success_url = reverse_lazy("access_coupons")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The access coupon {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.participant))
        return super(AccessCouponDeleteView, self).delete(request, *args, **kwargs)


def redeem_coupon(request, qr_code_data):
    # Extract participant's unique identifier from QR code data
    participant_id = qr_code_data  # Replace this with your actual logic to extract the identifier

    # Check if the participant exists
    participant = get_object_or_404(Participant, qr_code_reference=participant_id)

    # Check if there are any unredeemed coupons for the participant
    unredeemed_coupons = AccessCoupon.objects.filter(participant=participant, redeemed=False)

    if unredeemed_coupons.exists():
        # Redeem the first unredeemed coupon (you can modify the logic as needed)
        coupon_to_redeem = unredeemed_coupons.first()
        coupon_to_redeem.redeemed = True
        coupon_to_redeem.redeemed_at = timezone.now()  # Import timezone
        coupon_to_redeem.save()

        # You can also implement additional logic here, such as sending an email confirmation

        return redirect('coupon_redeemed_success')
    else:
        # No unredeemed coupons found for the participant
        return redirect('no_coupons_to_redeem')
