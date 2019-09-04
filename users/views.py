import json
import bcrypt
import jwt
import pdb
import requests

from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import datetime
from datetime import timedelta
from weplate.my_settings import SECRET_KEY


class UserLogin(View):
    def post(self, request):
        # pdb.set_trace()
        user_data = json.loads(request.body)  # 파이썬 형식으로 decode된 데이터
        login_user_email = user_data["user_email"]
        login_user_password = user_data["user_password"]
        # Email and password NOT filled in // It is unnecessary if use try/except
        if len(login_user_email) < 1 or len(login_user_password) < 1:
            return JsonResponse({"error_message": "FILL_IN_EMAIL_PASSWORD"}, status=400)

        # Check if email is validusers.models.UserAccount.DoesNotExist
        # pdb.set_trace()
        try:
            user = UserAccount.objects.get(
                user_email=login_user_email)
        except UserAccount.DoesNotExist:
            return JsonResponse({"error_message": "INVALID_EMAIL"}, status=400)

        # Check if password is correct
        # pdb.set_trace()
        # 회원가입시 pw와 현재 로그인으로 들어온 pw 비교함
        if bcrypt.checkpw(user_data["user_password"].encode("UTF-8"), user.user_password.encode("UTF-8")):
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=5),
                "iat": datetime.datetime.utcnow(),
                "sub": login_user_email
            }
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return JsonResponse({
                "user_access_token": encoded_jwt.decode("UTF-8")}, status=200)
        else:
            return JsonResponse({"error_message": "PASSWORD_IS_WRONG"},
                                status=400)


class UserSignUp(View):
    def post(self, request):
        pdb.set_trace()
        new_user_data = json.loads(request.body)
        # Email and password NOT filled in
        login_user_email = new_user_data["user_email"]
        login_user_password = new_user_data["user_password"]
        if len(login_user_email) < 1 or len(login_user_password) < 1:
            return JsonResponse({"error_message": "FILL_IN_EMAIL_PASSWORD"}, status=400)

        if UserAccount.objects.filter(user_email=new_user_data["user_email"]).exists():
            return JsonResponse({"error_message": "EMAIL_ALREADY_TAKEN"},
                                status=401)
        hashed_pwd = bcrypt.hashpw(
            new_user_data["user_password"].encode("UTF-8"), bcrypt.gensalt())
        new_user = UserAccount(user_email=new_user_data["user_email"],
                               created_at=datetime.datetime.now(),
                               user_password=hashed_pwd.decode("UTF-8"),
                               )
        new_user.save()
        return JsonResponse({"message": "SUCCESS"}, status=200)


class KakaoLoginView(View):
    def get(self, request):
        # pdb.set_trace()
        access_token = request.headers["Authorization"]
        headers = ({"Authorization": f"Bearer {access_token}"})
        url = "https://kapi.kakao.com/v2/user/me"
        response = requests.get(url, headers=headers, timeout=3)
        user = response.json()

        if UserAccount.objects.filter(social_login_id=user["id"]).exists():
            user_info = UserAccount.objects.get(social_login_id=user["id"])
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=5),
                "iat": datetime.datetime.utcnow(),
                "id": user_info.id
            }
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            none_member_type = 1
            return JsonResponse({
                "access_token": encoded_jwt.decode("UTF-8"),
                "user_type": none_member_type,
                "user_pk": user_info.id
            }, status=200)
        else:
            # pdb.set_trace()
            new_user_info = UserAccount(
                social_login_id=user["id"],
                social_platform=SocialPlatforms.objects.get(
                    platform="kakao"),
                user_email=user["kakao_account"].get("email")
            )
            new_user_info.save()
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=5),
                "iat": datetime.datetime.utcnow(),
                "id": user_info.id
            }
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            none_member_type = 1
            return JsonResponse({
                "access_token": encoded_jwt.decode("UTF-8"),
                "user_type": none_member_type,
                "user_pk": new_user_info["social_login-id"],
            }, status=200)
