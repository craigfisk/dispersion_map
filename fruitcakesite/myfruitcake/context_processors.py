from myfruitcake.models import Shipment
from forum.models import Post

def my_shipments_context_processor(request):
    return {
            'my_shipments' : Shipment.objects.filter(sender_id=request.user.id).order_by('-dt')
            }

def my_posts_context_processor(request):
    return {
            'my_posts' : Post.objects.filter(creator_id=request.user.id)  # Note: no dt in model, so can't use .order_by('-dt')
            }

