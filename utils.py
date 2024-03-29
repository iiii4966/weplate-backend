import jwt, json
from weplate.my_settings import SECRET_KEY
from django.http import JsonResponse
from user.models import User

def login_required(func):
    def decorated_function(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
         
        if access_token:
            try:
                payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
                user_id = payload['user_id']
                request.user = User.objects.get(user_id = user_id)
            except jwt.DecodeError:
                return JsonResponse({"error":"INVALID_TOKEN"}, status = 401)
            except User.DoesNotExist:
                return JsonResponse({"error":"ID_NOT_EXIST"}, status = 401)
                
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({"error":"LOGIN_REQUIRED"}, status = 401)
        
    return decorated_function 
 
