from weplate.my_settings import SECRET_KEY
from django.http import JsonResponse
from django.views import View
from .models import User
from datetime import datetime, timedelta

import bcrypt
import jwt, json
import pdb

# Create your views here.

class Signup(View):
    
    def post(self, request):

        data = json.loads(request.body)
        hashed_pwd = bcrypt.hashpw(bytes(data['password'], "UTF-8"), bcrypt.gensalt())
        account = User(user_id = data['user_id'], password = hashed_pwd.decode("UTF-8"))
        
        try:
            account.save()
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except:
            return JsonResponse({"message":"same ID exists"}, status = 400)

class Login(View):

    def post(self, request):
        
        data = json.loads(request.body)
        
        user_id = data['user_id']
        password = data['password']
        
        if User.objects.filter(user_id = user_id).exists():
            user_password = User.objects.get(user_id = user_id).password
        else:
            return JsonResponse({"message":"ID does not exists"}, status = 401)
        
        if bcrypt.checkpw(password.encode("UTF-8"), user_password.encode("UTF-8")):
            
            payload_id = user_id
            payload = {
                'user_id': user_id,
                    'exp': datetime.utcnow() + timedelta(60 * 60 * 24)
            }
            token = jwt.encode(payload, SECRET_KEY)
            
            return JsonResponse({"access_token":token.decode("UTF-8")}, status = 200)
        else:
            return JsonResponse({"message":"pwd is invalid"}, status = 401)
        




        


