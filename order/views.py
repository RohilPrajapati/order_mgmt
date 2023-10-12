from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import GotOrder,DistributedOrder, Person
from .serializers import GotOrderModelSerializer,GotOrderCreateSerializer,DistributedOrderModelSerializer,DistributedOrderCreateSerializer, PersonModelSerializer,PersonCreateSerializer
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .utils import check_got_qty
from django.db.models import ProtectedError

# Create your views here.

class GotOrderView(APIView):
    def get(self,request):
        c_status = request.GET.get('c_status')
        print(c_status)
        got_order = GotOrder.objects.all()
        if c_status == 'true':
            got_order = got_order.filter(complete_status = True)
        elif c_status == 'false':
            got_order = got_order.filter(complete_status = False)
        serializer = GotOrderModelSerializer(got_order,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = GotOrderCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            order_by = serializer.validated_data['order_by']
            order_date = datetime.now()
            got_qty = serializer.validated_data['got_qty']

            got_order = GotOrder.objects.create(
                order_by = order_by,
                order_date = order_date.date(),
                got_qty = got_qty,
            )
            response = {
                'data': GotOrderModelSerializer(got_order).data
            }
            return Response(response,status=status.HTTP_201_CREATED)

class GotOrderDetailView(APIView):
    def get(self,request,pk):
        order = get_object_or_404(GotOrder,id=pk)
        serializer = GotOrderModelSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        serializer = GotOrderCreateSerializer(data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            order = get_object_or_404(GotOrder,id=pk)
            got_qty = serializer.validated_data.get('got_qty',order.got_qty)
            order.order_by = serializer.validated_data.get('order_by',order.order_by)
            order.complete_status = serializer.validated_data.get('complete_status',order.complete_status)
            order.got_qty = got_qty
            order.save()
            response ={
                'message':'Order have been Updated'
            }
            return Response(response,status=status.HTTP_200_OK)

    def delete(self,request,pk):
        order = get_object_or_404(GotOrder,id=pk)
        try:
            order.delete()
            response = {
                'message':'Order have been deleted'
            }
            return Response(response,status=status.HTTP_200_OK)
        except ProtectedError:
            response = {
                'message':'Cannot delete order it have been distributed Order'
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

class DistributeOrderView(APIView):
    def get(self,request):
        dist_order = DistributedOrder.objects.all()
        order_id = request.GET.get('order_id')
        if order_id:
            dist_order = dist_order.filter(got_order = order_id)
        serializer = DistributedOrderModelSerializer(dist_order)
        return Response(serializer,status=status.HTTP_200_OK)

    def post (self,request):
        serializer = DistributedOrderCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            got_order_id = serializer.validated_data['got_order']
            person_id = serializer.validated_data['person_id']
            person = Person.objects.get(id=person_id)
            distributed_date = datetime.now().date()
            distributed_qty = serializer.validated_data['distributed_qty']

            got_order = GotOrder.objects.get(id=got_order_id)
            order_data = GotOrderModelSerializer(got_order).data
            print(order_data)
            new_rem_qty = order_data['remaining_qty'] - distributed_qty
            if  new_rem_qty < 0:
                return Response(
                    {
                        'message':'Distributed Quantity is higher then remaining quantity'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            dist_order = DistributedOrder.objects.create(
                got_order= got_order,
                person = person,
                distributed_qty= distributed_qty,
                completed_qty=0,
                distributed_date=distributed_date
            )
            # got_order.distributed_qty += distributed_qty
            # got_order.save()
            response = {
                'data': GotOrderModelSerializer(got_order).data
            }
            return Response(response, status=status.HTTP_201_CREATED)

class DistributeOrderDetailView(APIView):
    def get(self,request,pk):
        d_order = get_object_or_404(GotOrder, id=pk)
        serializer = DistributedOrderModelSerializer(d_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,pk):
        serializer = DistributedOrderCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            dist_order = get_object_or_404(DistributedOrder, id=pk)
            completed_qty = serializer.validated_data['completed_qty']
            distributed_qty = serializer.validated_data['distributed_qty']
            damage_qty = serializer.validated_data['damage_qty']
            return_qty = serializer.validated_data['return_qty']
            person_id = serializer.validated_data.get('person_id')
            if dist_order.got_order.got_qty < distributed_qty:
                response = {
                    'message': "Received Order Quantity can't be less then Distributed Quantity"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            calc = distributed_qty- ( completed_qty + damage_qty + return_qty )
            if calc < 0:
                response = {
                    'message': 'Completed Qty , Return Qty and Damage Qty cant be greater then Distributed Quantity'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if person_id:
                dist_order.person = Person.objects.get(id = person_id)
            dist_order.distributed_qty = distributed_qty
            dist_order.completed_qty = completed_qty
            dist_order.return_qty = return_qty
            dist_order.damage_qty = damage_qty
            dist_order.save()
            response = {
                'message': 'Distributed Order have been Updated'
            }
            return Response(response, status=status.HTTP_200_OK)
    def delete(self,request,pk):
        print("working")
        dist_order = get_object_or_404(DistributedOrder, id=pk)
        try:
            # got_order = dist_order.got_order
            # got_order.distributed_qty -= dist_order.distributed_qty
            # got_order.save()
            dist_order.delete()
            response = {
                'message': 'Distributed Order have been deleted'
            }
            return Response(response, status=status.HTTP_200_OK)
        except ProtectedError:
            response = {
                'message': 'Cannot delete Distributed order'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PersonView(APIView):
    def get(self, request):
        person = Person.objects.all()
        serializer = PersonModelSerializer(person, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PersonCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            address = serializer.validated_data['address']
            phone_no = serializer.validated_data['phone_no']

            person = Person.objects.create(
                name = name,
                address=address,
                phone_no=phone_no,
            )
            response = {
                'data': PersonModelSerializer(person).data
            }
            return Response(response, status=status.HTTP_201_CREATED)

class PersonDetailView(APIView):
    def get(self, request, pk):
        person = get_object_or_404(Person, id=pk)
        serializer = PersonModelSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = PersonCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            person = get_object_or_404(Person, id=pk)
            person.name = serializer.validated_data.get('name', person.name)
            person.address = serializer.validated_data.get('address', person.address)
            person.phone_no = serializer.validated_data.get('phone_no', person.phone_no)
            person.save()
            response = {
                'message': 'Person have been Updated'
            }
            return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        person = get_object_or_404(Person, id=pk)
        try:
            person.delete()
            response = {
                'message': 'Person have been deleted'
            }
            return Response(response, status=status.HTTP_200_OK)
        except ProtectedError:
            response = {
                'message': 'Cannot delete person it have been Distributed Order'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

