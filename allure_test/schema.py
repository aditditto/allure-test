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
    products = graphene.List(
        ProductType, published_only=graphene.Boolean(
            required=False, default_value=False)
    )
    product = graphene.Field(
        ProductType, uuid=graphene.UUID(required=True),
        published_only=graphene.Boolean(required=False, default_value=False)
    )
    reviews = graphene.List(
        ReviewType, productUUID=graphene.UUID(required=False),
        published_only=graphene.Boolean(required=False, default_value=False)
    )

    def resolve_products(root, info, published_only):
        products = Product.objects.all()
        if published_only:
            return products.filter(is_published=True)
        else:
            return products

    def resolve_product(root, info, uuid, published_only):
        product = Product.objects.get(UUID=uuid)
        if published_only and not product.is_published:
            return None
        else:
            return product

    def resolve_reviews(root, info, published_only, productUUID=None):
        reviews = Review.objects.all()
        if productUUID:
            reviews = reviews.filter(product=productUUID)
        if published_only:
            reviews = reviews.filter(is_published=True)
        return reviews


schema = graphene.Schema(query=Query)
