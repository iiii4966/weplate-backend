from django.http import JsonResponse
from django.views import View
from .models import Comment
from utils import login_required
import json

class CommentView(View):
    
    @login_required
    def post(self, request, *args, **kwargs):
       
        data = json.loads(request.body)
        
        if len(data['comment']) > 500:
            return JsonResponse({"error_code":"500 Character Limit"}, status = 400)
            
        try:
            pk = kwargs['pk']
                             
            update_comment = Comment.objects.get(pk = pk)
            update_comment.comments = data['comment']
            update_comment.save()
        
            message = {'message':'SUCCESS'}
            status_code = 200

        except:
            pk = None
        
        if pk is None:

            Comment(user_id = request.user, comments = data['comment']).save()

            message = {'message':'SUCCESS'}
            status_code = 200

        return JsonResponse(message, status = status_code)

    def get(self, request):

        data = list(Comment.objects.values())

        return JsonResponse(data, safe = False, status = 200)
    
    @login_required
    def delete(self, request, *args, **kwargs):
        
        pk = kwargs['pk']
    
        if Comment.objects.filter(pk = pk).exists():
            
            Comment.objects.get(pk = pk).delete()
            
            message = {'message':'SUCCESS'} 
            status_code = 200
        else:
            
            message = {'message':'NO Authorization'}
            status_code = 400
        
        return JsonResponse(message, status = status_code)