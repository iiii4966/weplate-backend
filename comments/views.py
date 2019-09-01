from django.http import JsonResponse
from django.views import View
from .models import Comment
from utils import login_required
import json

class CommentCreateView(View):

    @login_required
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        
        if ('content' not in data) or (len(data['content']) > 500) or (len(data['content']) < 1):
            return JsonResponse({"error_code":"INVALID_REQUEST"}, status = 400)

        Comment(user = request.user , content = data['content']).save()

        return JsonResponse({"message":"SUCCESS"}, status = 200)

    def get(self, request):
        data = Comment.objects.filter(deleted_at = False).values()[:10]
        return JsonResponse(data, safe = False, status = 200)
    
class CommentUpdateDeleteView(View):
    
    @login_required
    def post(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']
        data = json.loads(request.body)
        
        if ('content' not in data) or (len(data['content']) > 500) or (len(data['content']) < 1):
            return JsonResponse({"error_code":"INVALID_REQUEST"}, status = 400)

        try:
            update_comment = Comment.objects.get(pk = comment_id)
    
            if update_comment.user_id is request.user.pk:
                update_comment.content = data['content']
                update_comment.save()
                
                message = {'message':'SUCCESS'}
                status_code = 200
            else:
                message = {'message':'INVALID_USER'}
                status_code = 400

        except Comment.DoesNotExist as err:
            message = {'message':"NONE_COMMENT"}
            status_code = 400
         
        return JsonResponse(message, status = status_code)
            
    @login_required
    def delete(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']

        try:
            del_comment = Comment.objects.get(pk = comment_id)
            
            if del_comment.user_id is request.user.pk:
                del_comment.deleted = True
                del_comment.save()

                message = {'message':'SUCCESS'}
                status_code = 200
            else:
                message = {'message':'INVALID_USER'}
                status_code = 400
                
        except Comment.DoesNotExist as err:
            message = {'message':'NONE_DATA'}
            status_code = 400

        return JsonResponse(message, status = status_code)

