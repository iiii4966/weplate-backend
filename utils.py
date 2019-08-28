import jwt, json
from weplate.my_settings import SECRET_KEY
from django.http import JsonResponse
from comments.models import Comment

def login_required(func):
    def decorated_function(self, request, *args, **kwargs):
            
        access_token = request.headers.get('Authorization', None)
            
        if access_token:
            try:
                payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
                user_id = payload['user_id']
                user = Account.objects.get(user_id = user_id)
                request.user = user

            except jwt.DecodeError:
                return JsonResponse({"error_code":"invalid_token"}, status = 401)
            
            except Comment.DoesNotExist:
                return JsonResponse({"message":"ID does not exists"}, status = 400)
                
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({"message":"login is required"}, status = 401)
        
    return decorated_function 
 
