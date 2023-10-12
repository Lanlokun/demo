from django.urls import path

from .views import (
    IndexView,
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    ParticipantListView,
    ParticipantCreateView,
    ParticipantUpdateView,
    ParticipantDeleteView,
    ParticipantDetailView,
    ParticipantTypeListView,
    ParticipantTypeCreateView,
    ParticipantTypeUpdateView,
    ParticipantTypeDeleteView,
    CouponTypeCreateView,
    CouponTypeDeleteView,
    CouponTypeListView,
    CouponTypeUpdateView,
    AccessCouponCreateView,
    AccessCouponDeleteView,
    AccessCouponListView,
    AccessCouponUpdateView,
    download_all_participants,
    DownloadCSVViewdownloadcsv,
    ParticipantBulkUploadView,
    update_in_event,
    update_breakfast,
    update_lunch,
    

    
)

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("events", EventListView.as_view(), name="events"),
    path("event/add", EventCreateView.as_view(), name="add_event"),
    path("event/<int:pk>/update", EventUpdateView.as_view(), name="update_event"),
    path("event/<int:pk>/delete", EventDeleteView.as_view(), name="delete_event"),
    # path("event/<int:pk>/detail", EventDetailView.as_view(), name="event_detail"),
    path("participants", ParticipantListView.as_view(), name="participants"),
    path("participant/add", ParticipantCreateView.as_view(), name="add_participant"),
    path("participant/<int:pk>/update", ParticipantUpdateView.as_view(), name="update_participant"),
    path("participant/<int:pk>/delete", ParticipantDeleteView.as_view(), name="delete_participant"),
    path("participant/<int:pk>/detail", ParticipantDetailView.as_view(), name="participant_detail"),
    path("participant-types", ParticipantTypeListView.as_view(), name="participant_types"),
    path("participant-type/add", ParticipantTypeCreateView.as_view(), name="add_participant_type"),
    path("participant-type/<int:pk>/update", ParticipantTypeUpdateView.as_view(), name="update_participant_type"),
    path("participant-type/<int:pk>/delete", ParticipantTypeDeleteView.as_view(), name="delete_participant_type"),
    path("coupon-types", CouponTypeListView.as_view(), name="coupon_types"),
    path("coupon-type/add", CouponTypeCreateView.as_view(), name="add_coupon_type"),
    path("coupon-type/<int:pk>/update", CouponTypeUpdateView.as_view(), name="update_coupon_type"),
    path("coupon-type/<int:pk>/delete", CouponTypeDeleteView.as_view(), name="delete_coupon_type"),
    path("access-coupons", AccessCouponListView.as_view(), name="access_coupons"),
    path("access-coupon/add", AccessCouponCreateView.as_view(), name="add_access_coupon"),
    path("access-coupon/<int:pk>/update", AccessCouponUpdateView.as_view(), name="update_access_coupon"),
    path("access-coupon/<int:pk>/delete", AccessCouponDeleteView.as_view(), name="delete_access_coupon"),
    path('download_all_participants/', download_all_participants, name='download_all_participants'),
    path("download-csv/", DownloadCSVViewdownloadcsv.as_view(), name="download-csv"),
    path("upload/", ParticipantBulkUploadView.as_view(), name="participant-upload"),
    path("update-in-event/<int:participant_id>/", update_in_event, name="update-in-event"),
    path("update-breakfast/<int:participant_id>/", update_breakfast, name="update-breakfast"),
    path("update-lunch/<int:participant_id>/", update_lunch, name="update-lunch"),






]
