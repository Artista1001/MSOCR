from django.db import models
import uuid
import base64

# Create your models here.
# class Vendor(models.Model):
#     v_id = models.CharField(primary_key=True, null=False, max_length=15,  unique=True)
#     name= models.CharField(max_length=50)
#     objects = models.Manager()
#     def __str__(self):
#         return self.name

class DocFormat(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    def set_data(self, data):
        try:
            self.ref_img = base64.encodebytes(data)
        except:
            raise ValueError('Invalid base64 string')
        
    def get_data(self):
        if self.ref_img:
            return base64.decodebytes(self.ref_img).decode('utf-8')
        else:
            return None
    
    data = property(get_data, set_data)

    _id =models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        unique=True
        )
    # vendor_id = models.ForeignKey(Vendor, null=True, on_delete=models.CASCADE)
    vendor_email = models.EmailField(max_length=100, null=False)
    format_type = models.CharField(max_length=100, null=False, unique=True)
    FormatStatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pixeltuple = models.CharField(max_length=10000, null=True)
    FormatRaisedDate = models.DateTimeField(auto_now_add=True)
    format_file_name = models.CharField(max_length=255, null=False)
    ref_img = models.BinaryField(blank=True)
    format_pproverId = models.CharField(max_length=1000, null=True)
    #ref_img = models.TextField(db_column=data,blank=True)

    def __str__(self):
        return self._id

    
    
#https://stackoverflow.com/questions/4915397/django-blob-model-field