from django.shortcuts import render
from OCR.main import OCRcls
from OCR.imageconverter import imgconverter
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser , FormParser, MultiPartParser 
from rest_framework import status
from Ocr_service.models import  DocFormat #Vendor,
from Ocr_service.serializers import  DocFormatSerializer #VendorSerializer,
from rest_framework.decorators import api_view
from django.core.serializers import serialize
import json
import base64
import cv2
import numpy as np
import tempfile
import os
from rest_framework.decorators import api_view, parser_classes
# Create your views here.

    
# @api_view(['GET', 'POST'])
# def vendor_list(request):
#     if request.method == 'GET':
#         vendors = Vendor.objects.all()
        
#         Name = request.GET.get('Name', None)
#         if Name is not None:
#             vendors = vendors.filter(Name__icontains=Name)
       
#         vendors_serializer = VendorSerializer(vendors, many=True)
#         return JsonResponse(vendors_serializer.data, safe=False)
#     elif request.method == 'POST':
#         vendor_data = JSONParser().parse(request)
#         vendor_serializer = VendorSerializer(data=vendor_data)
#         print(vendor_serializer)
#         if vendor_serializer.is_valid():
#             vendor_serializer.save()
#             return JsonResponse(vendor_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def vendor_detail(request, pk):
#     try: 
#         vendor = Vendor.objects.get(_id=pk) 
#     except Vendor.DoesNotExist: 
#         return JsonResponse({'message': 'The vendor does not exist'}, status=status.HTTP_404_NOT_FOUND) 
#     if request.method == 'GET': 
#         vendor_serializer = VendorSerializer(vendor) 
#         return JsonResponse(vendor_serializer.data) 
    
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])
def DocFormat_list(request):
    #parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    if request.method == 'GET':
        docformats = DocFormat.objects.all()
        format_type = request.GET.get('format_type', None)
        if format_type is not None:
            docformats = docformats.filter(format_type__icontains=format_type)
        docformats_serializer = DocFormatSerializer(docformats, many=True)
        
        return JsonResponse(docformats_serializer.data, safe=False)
    elif request.method == 'POST':
        # print(request)
        # VendorId = request.POST.get('vendor_id')
        # FormData = request.POST.get('format_type')
        # RefImg = request.FILES.get('ref_img').read()
        # PxlTupl = request.POST.get('pixeltuple')
        # print(VendorId)
        # print(FormData)
        # print(RefImg)
        # print(PxlTupl)
        #docformat_data = FormParser().parse(request)
        # docformat_serializer = DocFormatSerializer(data=docformat_data)
        print( request.FILES.get('ref_img'))
        docformat_serializer = DocFormatSerializer(data=request.data)
        #print(docformat_serializer)
        if docformat_serializer.is_valid():
            print( request.FILES.get('ref_img'))
            ref_img = request.FILES.get('ref_img')
            print(ref_img)
            if ref_img is not None:
               docformat_serializer.validated_data['ref_img'] = ref_img.read()
            docformat_serializer.save()
            return JsonResponse(docformat_serializer.data, status=status.HTTP_201_CREATED) 
        
        return JsonResponse(docformat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def DocFormat_detail(request, pk):
    try: 
        docformat = DocFormat.objects.get(_id=pk) 
    except DocFormat.DoesNotExist: 
        return JsonResponse({'message': 'The DocFormat does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        docformat_serializer = DocFormatSerializer(docformat)
        return JsonResponse(docformat_serializer.data) 
    
@api_view(['POST'])
def OCR(request):
    try: 
        docformat_obj = DocFormat.objects.get(vendor_email=request.POST.get('vendor_email'), format_type = request.POST.get('format_type'))
        docformats_serializer = DocFormatSerializer(docformat_obj)
        jsonresponse = JsonResponse(docformats_serializer.data)
        response_data = json.loads(jsonresponse.content)
        # name_of_file = request.FILES['image'].name
        # print(name_of_file)
        # file = request.FILES['image'].read()
        # print("Now its type is ", type(name_of_file))
        # if name_of_file.endswith('.pdf'):
        #     req_image = imgconverter.pdftoimage(file)
        #     print("true")
        # elif name_of_file.endswith('.jpg'):
        #     req_image = request.FILES.get('image').read()
        #     print("true jpg")
        #     print(req_image)
        req_image = request.FILES.get('image').read()
        print(req_image)
        req_vid = request.POST.get('id')
        #print(req_vid)
        qry_refimg = base64.b64decode(response_data['ref_img'])
        #print(qry_refimg)
        qry_pixeltuple =response_data['pixeltuple']
        #print(qry_pixeltuple)
        
        req_image_np = np.frombuffer(req_image, dtype=np.uint8)
        ref_image_np = np.frombuffer(qry_refimg, dtype=np.uint8)

        # print(base64.encodebytes(req_image))
        with tempfile.NamedTemporaryFile(delete=False) as f:
            
            req_temp_file_path = f.name
            print(req_temp_file_path)
            f.write(req_image_np)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            
            ref_temp_file_path = f.name
            print(ref_temp_file_path)
            f.write(ref_image_np)


        dictionary = OCRcls.ocrfunction(ref_temp_file_path,qry_pixeltuple,req_temp_file_path)
        # Reqimg = cv2.imread(temp_file_path,cv2.IMREAD_COLOR)
        # #print(Reqimg)
        # cv2.imshow("2",Reqimg)
        
        os.remove(req_temp_file_path)
        os.remove(ref_temp_file_path)

        #ocrjson = OCRcls.ocrfunction(qry_refimg,qry_pixeltuple,req_image)
        # return JsonResponse(json.dumps({
        #     "Tupel": qry_pixeltuple,
        #     "RefImage": base64.decodebytes(req_image).decode('utf-8')
            
            
        # }), safe=False)
        # return ocrjson
        #return JsonResponse(json.dumps(ocrjson), safe=False)
        #return JsonResponse(docformats_serializer.data)
        return JsonResponse(dictionary)
    
    except DocFormat.DoesNotExist: 
         return JsonResponse({'message': 'The DocFormat does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    # docformats_serializer = DocFormatSerializer(docformat_obj)
    # print(docformats_serializer)
    # qry_refimg = docformats_serializer.data('ref_img')
    # qry_pixeltuple = docformats_serializer.data('pixeltuple')
    # #req_image = request.image
    # req_image = request.FILES.get('image').read()
    # ocrjson = OCRcls.ocrfunction(qry_refimg,qry_pixeltuple,req_image)
    # return ocrjson

 
    