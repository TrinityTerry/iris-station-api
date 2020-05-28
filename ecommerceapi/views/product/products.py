'''
A django page to handle all product fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product, Customer
from datetime import datetime

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='products',
            lookup_field='id'
        )
        fields = ('id', 'title', 'price', 'description', 'quantity', "location", 'created_at', 'image_path', 'product_type_id')
        depth = 1

class Products(ViewSet):

    '''' a class to handle all the products viewset

    Arguments:
        ViewSet '''

    def create(self, request):
        ''' Handle POST operations and returns JSON serialized product instance'''

        newproduct = Product()
        newproduct.title = request.data["title"]
        newproduct.price = request.data["price"]
        newproduct.description = request.data["description"]
        newproduct.quantity = request.data["quantity"]
        newproduct.location = request.data["location"]
        newproduct.image_path = request.data["image_path"]
        newproduct.created_at = datetime.today().strftime('%Y-%m-%d')
        newproduct.product_type_id = request.data["product_type_id"]
        newcustomer = Customer.objects.get(user = request.auth.user)
        newproduct.customer = newcustomer
        newproduct.save()

        serializer = ProductSerializer(newproduct, context={'request': request})

        return Response(serializer.data)
    
    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        home = self.request.query_params.get('number', None)
        if home is not None:
            products = Product.objects.all()[:20]
        else:
             products = Product.objects.all()

        
        user = self.request.query_params.get('user', None)
        if hasattr(request.auth, "user"):
            customer = Customer.objects.get(user=request.auth.user)

        if user is not None:
            products = products.filter(customer_id=customer.id)

        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        '''handles fetching ony one product'''
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

         
    def update(self, request, pk=None): 
        pass

    def destroy(self, request, pk=None):
        # pass
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    