from django.http        import JsonResponse, HttpResponse
from django.views       import View
from .models            import Comment
from restaurant.models  import Restaurant
from utils              import login_required

import json

class CommentView(View):

    @login_required
    def post(self, request):
        
        try:
            data = json.loads(request.body)

            if 'restaurant_id' not in data or 'content' not in data and len(data['content']) > 500 or len(data['content']) < 1:
                return JsonResponse({"error_code":"INVALID_REQUEST"}, status = 400)

            restaurant = Restaurant.objects.get(id = data['restaurant_id'])
            Comment(user = request.user, Restaurant = restaurant, content = data['content']).save()
            
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except Restaurant.DoesNotExist:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
        except Comment.DoesNotExist:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
       except ValueError as err:
            return JsonResponse({"error":"INVALID_REQUEST"}, status = 400)

    def get(self, request):
        restaurant_id = request.GET.get('restaurant_id', '')
        
        try:
            data = list(Comment.objects.values(
                    'id', 
                    'user_id', 
                    'user__user_id', 
                    'content', 
                    'created_at'
                    ).filter(deleted = False, Restaurant = int(restaurant_id)))
        except Comment.DoesNotExist as err:
                data = [] 
        except ValueError as err:
                return JsonResponse({"error":"NOT_FOUND"}, status = 404)

        return JsonResponse(data, safe = False, status = 200)
    
class CommentUpdateDeleteView(View):
    
    @login_required
    def post(self, request, comment_id):
        data = json.loads(request.body)
        
        if 'content' not in data and len(data['content']) > 500 or len(data['content']) < 1:
            return JsonResponse({"error":"INVALID_REQUEST"}, status = 400)

        try:
            update_comment = Comment.objects.get(pk = comment_id)
    
            if update_comment.user_id is request.user.pk:
                update_comment.content = data['content']
                update_comment.save()
                
                message = {'message':'SUCCESS'}
                status_code = 200
            else:
                message = {'error':'INVALID_USER'}
                status_code = 401
        except Comment.DoesNotExist as err:
            message = {'error':"NOT_FOUND"}
            status_code = 404
         
        return JsonResponse(message, status = status_code)
            
    @login_required
    def delete(self, request, comment_id):
        try:
            del_comment = Comment.objects.get(pk = comment_id)
            
            if del_comment.user_id is request.user.pk:
                del_comment.delete = True
                del_comment.save()

                message = {'message':'SUCCESS'}
                status_code = 200
            else:
                message = {'erro':'INVALID_USER'}
                status_code = 401
        except Comment.DoesNotExist as err:
            message = {'error':'NOT_FOUND'}
            status_code = 404

        return JsonResponse(message, status = status_code)

