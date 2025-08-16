from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Card
from .serializers import CardSerializer, CardItemSerializer


class CardCreate(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Card, CardItem
from crud.models import Product   # sening model noming bo‘yicha o‘zgartir
from .serializers import CardSerializer


class AddToCard(APIView):
    permission_classes = [IsAuthenticated]  # faqat login qilgan user qo‘sha oladi

    def post(self, request):
        product_id = request.data.get("product_id")
        amount = request.data.get("amount", 1)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Bunday mahsulot topilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if amount<=0 or amount>100:
            return Response(
                {"error": "hato malumot kiritdingiz"},
                status=status.HTTP_400_BAD_REQUEST
            )
        card, _ = Card.objects.get_or_create(user=request.user)

        card_item, created = CardItem.objects.get_or_create(
            card=card,
            product=product,
            amount=amount
        )
        if not created:
            card_item.amount += amount
            card_item.save()

        serializer = CardItemSerializer(card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Product_update(APIView):
    def post(self, request, pk):
        count = request.data.get('count', None)
        mtd = request.data.get('mtd', None)
        product = CardItem.objects.get(card__user = request.user, id=pk)
        if count:
            product.amount = count
            product.save()

        elif mtd:
            if mtd == '+':
                product.amount += 1
            elif mtd == "-":
                if product.amount==1:
                    product.delete()
                else:
                    product.amount -= 1
                    product.save()
        else:
            return Response({'error':'error'})
        serializer = CardItemSerializer(product)
        return Response({'data':serializer.data})












