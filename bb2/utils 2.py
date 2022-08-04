from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

def get_or_none(model, **kwargs):
    try: 
        return model.objects.get(**kwargs)
    except:
        return 

