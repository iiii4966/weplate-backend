from django.http import JsonResponse
from django.views import View
from .models import Comment
from utils import login_required
import json

class CommentView(View):

    @login_required
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        
        if ('content' not in data) or (len(data['content']) > 500) or (len(data['content']) < 1):
            return JsonResponse({"error_code":"REQUEST_INVALID"}, status = 400)

        try:
            comment_id = kwargs['pk']

            update_comment = Comment.objects.get(pk = comment_id)
            update_comment.content = data['content']
            update_comment.save()

            message = {'message':'SUCCESS'}
            status_code = 200

        except KeyError as err:
            
            if err is not kwargs:
                Comment(user = request.user , content = data['content']).save()

                message = {'message':'SUCCESS'}
                status_code = 200

        return JsonResponse(message, status = status_code)

    def get(self, request):

        data = Comment.objects.filter(deleted_at = False).values()
        
        return JsonResponse(data, safe = False, status = 200)
    
    @login_required
    def delete(self, request, *args, **kwargs):

        comment_id = kwargs['comment_id']

        if Comment.objects.filter(pk = comment_id).exists():
            
            del_comment = Comment.objects.get(pk = comment_id)
            del_comment.deleted_at = True
            del_comment.save()

            message = {'message':'SUCCESS'}
            status_code = 200
        else:
            message = {'message':'NONE_DATA'}
            status_code = 400

        return JsonResponse(message, status = status_code)
