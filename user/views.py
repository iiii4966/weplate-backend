from weplate.my_settings import SECRET_KEY
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import User
from datetime import datetime, timedelta

import bcrypt
import jwt, json

class SignUp(View):
    
    def post(self, request):
        data = json.loads(request.body)
        
        if 'user_id' in data and len(data['user_id']) >= 8:
            user_id = data['user_id']
        else:
            return JsonResponse({"message":"ID_INVALID"}, status = 400)

        if 'password' in data and len(data['password']) >= 8:
            password = data['password']
        else:
            return JsonResponse({"message":"PWD_INVALID"}, status = 400)        

        hashed_pwd = bcrypt.hashpw(bytes(password, "UTF-8"), bcrypt.gensalt())
        account = User(user_id = user_id, password = hashed_pwd.decode("UTF-8"))
        
        try:
            account.save()
            return  HttpResponse(status = 200)
        except:
            return JsonResponse({"message":"ID_EXIST"}, status = 400)

class LogIn(View):

    def post(self, request):
        data = json.loads(request.body)
        
        if 'user_id' in data and 'password' in data:
            user_id = data['user_id']    
            password = data['password']
        else:
            return JsonResponse({'message':'MISSING_DATA'}, status = 400)

        if User.objects.filter(user_id = user_id).exists():
            user_password = User.objects.get(user_id = user_id).password
        else:
            return JsonResponse({"message":"ID_NOT_EXIST"}, status = 401)
        
        if bcrypt.checkpw(password.encode("UTF-8"), user_password.encode("UTF-8")):
            payload_id = user_id
            payload = {
                'user_id': user_id,
                    'exp': datetime.utcnow() + timedelta(60 * 60 * 24)
            }
            token = jwt.encode(payload, SECRET_KEY)
            
            return JsonResponse({"access_token":token.decode("UTF-8")}, status = 200)
        else:
            return JsonResponse({"message":"PWD_INVALID"}, status = 401)
