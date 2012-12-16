from myfruitcake.models import Shipment
from forum.models import Post
from django.db import connection

def my_shipments_context_processor(request):
    return {
            'my_shipments' : Shipment.objects.filter(sender_id=request.user.id).order_by('-dt')
            }

def my_latest_shipment_context_processor(request):
    return {
            'my_latest_shipment' : Shipment.objects.filter(sender_id=request.user.id).order_by('-dt')[0]
            }

def my_posts_context_processor(request):
    return {
            'my_posts' : Post.objects.filter(creator_id=request.user.id).order_by('-created')
            }

def my_latest_post_context_processor(request):
    return {
            'my_latest_post' : Post.objects.filter(creator_id=request.user.id).order_by('-created')[0]
            }

def get_chain(pk):
    cursor = connection.cursor()
    current = Shipment.objects.get(pk=pk)
    qry = "select id, parent_id, origin_id from myfruitcake_shipment where origin_id=%s;" % current.parent.id
    cursor.execute(qry)
    results = cursor.fetchall()
    return { 'chain': results }

