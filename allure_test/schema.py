import graphene
from graphene_django import DjangoObjectType

from products.models import Product, Review


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = '__all__'


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    reviews = graphene.List(ReviewType)
    # product_detail = graphene.Field(
    #     ProductType, uuid=graphene.UUID(required=True))
    # product_reviews = graphene.List(ReviewType)

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_reviews(root, info):
        return Review.objects.all()


schema = graphene.Schema(query=Query)
