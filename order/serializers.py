from rest_framework import serializers
from .models import GotOrder,DistributedOrder,Person
from django.db.models import Sum

class GotOrderModelSerializer(serializers.ModelSerializer):
    dist_order = serializers.SerializerMethodField()
    dist_order_qty = serializers.SerializerMethodField()
    remaining_qty = serializers.SerializerMethodField()
    completed_qty = serializers.SerializerMethodField()
    return_qty = serializers.SerializerMethodField()
    damage_qty = serializers.SerializerMethodField()
    class Meta:
        model=GotOrder
        fields = '__all__'
        depth = 1
    def get_dist_order(self,obj):
        dist_order = DistributedOrder.objects.filter(got_order = obj)
        serializer = DistributedOrderModelSerializer(dist_order,many=True)
        return serializer.data

    def get_dist_order_qty(self,obj):
        if DistributedOrder.objects.filter(got_order=obj.id).exists():
            dist_qty = DistributedOrder.objects.filter(got_order=obj.id).aggregate(sum = Sum("distributed_qty"))
            return dist_qty['sum']
        return 0
    def get_remaining_qty(self,obj):
        if DistributedOrder.objects.filter(got_order=obj.id).exists():
            dist_qty = DistributedOrder.objects.filter(got_order=obj.id).aggregate(sum = Sum("distributed_qty"))
            return obj.got_qty - dist_qty['sum']
        return obj.got_qty
    def get_completed_qty(self,obj):
        if DistributedOrder.objects.filter(got_order=obj.id).exists():
            dist_qty = DistributedOrder.objects.filter(got_order=obj.id).aggregate(sum = Sum("completed_qty"))
            return dist_qty['sum']
        return 0
    def get_return_qty(self,obj):
        if DistributedOrder.objects.filter(got_order=obj.id).exists():
            dist_qty = DistributedOrder.objects.filter(got_order=obj.id).aggregate(sum = Sum("return_qty"))
            return dist_qty['sum']
        return 0
    def get_damage_qty(self,obj):
        if DistributedOrder.objects.filter(got_order=obj.id).exists():
            dist_qty = DistributedOrder.objects.filter(got_order=obj.id).aggregate(sum = Sum("damage_qty"))
            return dist_qty['sum']
        return 0
    
class GotOrderCreateSerializer(serializers.Serializer):
    order_by = serializers.CharField()
    # order_date = serializers.DateField()
    got_qty = serializers.IntegerField()
    company_id = serializers.IntegerField(required=False,allow_null=True)
    complete_status = serializers.BooleanField(required=False,allow_null=True)
    # remaining_qty = serializers.IntegerField()
    # distributed_qty = serializers.IntegerField()

class DistributedOrderModelSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        print("working")
        exclude = kwargs.pop("exclude",None)
        super(DistributedOrderModelSerializer,self).__init__(*args, **kwargs)
        print(exclude)
        if exclude is not None:
            for field_name in exclude:
                print(field_name)
                self.fields.pop(field_name)
    class Meta:
        model = DistributedOrder
        fields = '__all__'
        depth=1

class DistributedOrderCreateSerializer(serializers.Serializer):
    got_order = serializers.IntegerField()
    person_id = serializers.CharField()
    distributed_qty = serializers.IntegerField()
    completed_qty = serializers.IntegerField(default=0)
    damage_qty = serializers.IntegerField(required=False,allow_null=True)
    return_qty = serializers.IntegerField(required=False,allow_null=True)
    complete_status = serializers.BooleanField(required=False,allow_null=True)

class PersonModelSerializer(serializers.ModelSerializer):
    dist_order= serializers.SerializerMethodField()
    ttl_received_order= serializers.SerializerMethodField()
    ttl_no_received_order= serializers.SerializerMethodField()
    ttl_completed_order = serializers.SerializerMethodField()
    ttl_no_completed_order = serializers.SerializerMethodField()
    ttl_damage_order = serializers.SerializerMethodField()
    dist_return_order = serializers.SerializerMethodField()
    class Meta:
        model= Person
        fields ='__all__'
    def get_dist_order(self,obj):
        dist_order = DistributedOrder.objects.filter(person = obj).order_by('-id')
        serializer = DistributedOrderModelSerializer(dist_order,exclude=['person'],many=True)
        return serializer.data
    def get_ttl_received_order(self,obj):
        total = DistributedOrder.objects.filter(person= obj).aggregate(total=Sum('distributed_qty'))['total']
        return total
    def get_ttl_no_received_order(self,obj):
        total = DistributedOrder.objects.filter(person = obj, complete_status = True).count()
        return total
    def get_ttl_completed_order(self,obj):
        total = DistributedOrder.objects.filter(person=obj).aggregate(total=Sum('completed_qty'))['total']
        return total
    def get_ttl_no_completed_order(self,obj):
        total = DistributedOrder.objects.filter(person=obj).count()
        return total
    def get_ttl_damage_order(self,obj):
        total = DistributedOrder.objects.filter(person=obj).aggregate(total=Sum('damage_qty'))['total']
        return total
    def get_dist_return_order(self,obj):
        total = DistributedOrder.objects.filter(person=obj).aggregate(total=Sum('return_qty'))['total']
        return total

class PersonCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    phone_no  = serializers.CharField()