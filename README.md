# allure-test

A GraphQL API built using Django and graphene. Made as an excerise for Allure AI Backend Engineer Internship candidates.

## Getting started

### Dependencies

* Docker
* Python >3.6 (developed in python 3.8)

### Running in development mode

to run this project, open this repo in your terminal and run these commands:

```
docker build . -t aditditto/allure-test
docker run -d -p 8000:8000 --name=<CONTAINER_NAME> aditditto/allure-test
```

after that, you might have to run these commands to migrate the database and create an admin user:

```
docker exec -it <CONTAINER_NAME> python manage.py migrate
docker exec -it <CONTAINER_NAME> python manage.py createsuperuser
```

after that, the project should be running at `localhost:8000`. The admin dashboard is located at `localhost:8000/admin` and the GraphiQL is located at `localhost:8000/graphql`

## Queries

Here are some of the queries that the GraphQL API support:

### List products: list all products having the published attribute set to true.
```
query listProducts {
  products(publishedOnly: true) {
    UUID
    productName
  }
}
```

### Get product details: given product UUID, return the details of the Product IF the product is published.
```
query productDetail {
  product(uuid: <PRODUCT_UUID>, publishedOnly: true) {
    UUID
    productName
    productDescription
    isPublished
    lastCreated
    lastUpdated
  }
}
```

### List product reviews: given product UUID, return all reviews relating to that product having the published attribute set to true.
```
query productReviews {
  reviews(productUuid:<PRODUCT_UUID>,publishedOnly:true) {
    product {
      UUID
    }
    reviewTitle
    isPublished
    
  }
}
```

### Write product review: given product UUID, review title, and review text, write a review with appropriate attributes.
```
mutation addReview {
  createReview(productUuid: <PRODUCT_UUID>, reviewTitle: <REVIEW_TITLE>, reviewText: <REVIEW_TEXT>) {
    review {
      product {
        UUID
      }
      reviewTitle
      reviewText
      lastCreated
    }
  }
}
```
