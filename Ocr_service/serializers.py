from rest_framework import serializers 
from Ocr_service.models import  DocFormat #Vendor,
import base64

# class VendorSerializer(serializers.ModelSerializer):
 
#     class Meta:
#         model = Vendor
#         fields = ('v_id',
#                   'name',)
        
class DocFormatSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = DocFormat
        fields = ('vendor_email','format_type','FormatStatus','pixeltuple', 'FormatRaisedDate', 'format_file_name', 'ref_img', 'format_pproverId')
