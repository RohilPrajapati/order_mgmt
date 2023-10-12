from .models import DistributedOrder
def check_got_qty(order_id,got_qty):
    if DistributedOrder.objects.filter(got_order=order_id).exists():
        total_distrubuted_qty = DistributedOrder.objects.filter(got_order=order_id).aggregate(Sum('distributed_qty'))
        print(total_distrubuted_qty)
        if got_qty and total_distrubuted_qty < got_qty:
            return True
    return False