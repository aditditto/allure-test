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


class CreateReviewMutation(graphene.Mutation):
    class Arguments:
        product_UUID = graphene.UUID(required=True)
        review_title = graphene.String(required=True)
        review_text = graphene.String(required=True)

    review = graphene.Field(ReviewType)

    def mutate(root, info, product_UUID, review_title, review_text):
        try:
            product = Product.objects.get(UUID=product_UUID)
        except Product.DoesNotExist:
            raise Exception("Product with given UUID not found.")

        if len(review_title) > 200:
            raise Exception(
                "Review title should not be longer than 200 characters")

        created = product.review_set.create(
            review_title=review_title, review_text=review_text, is_published=True)

        return CreateReviewMutation(review=created)


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
        ReviewType, product_uuid=graphene.UUID(required=False),
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

    def resolve_reviews(root, info, published_only, product_uuid=None):
        reviews = Review.objects.all()
        if product_uuid:
            reviews = reviews.filter(product=product_uuid)
        if published_only:
            reviews = reviews.filter(is_published=True)
        return reviews


class Mutation(graphene.ObjectType):
    create_review = CreateReviewMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
