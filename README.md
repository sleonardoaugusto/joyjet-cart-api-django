# joyjet-cart-api
An ecommerce carts parser

## Setup
1. Clone this repo<br/>
`$ git clone https://github.com/sleonardoaugusto/joyjet-cart-api-django`
2. Create a virtualenv using Python 3.7<br/>
`$ cd joyjet-cart-api-django`<br/>
`$ python -m venv .joyjet-cart-api-django`
3. Activate it<br/>
`$ source .joyjet-cart-api-django/bin/activate`
4. Install dependencies<br/>
`$ pip install -r requirements.txt`

## Migrations
1. Make migrations<br/>
`$ python manage.py makemigrations`
2. Migrate<br/>
`$ python manage.py migrate`
3. Populate database<br/>
`$ python manage.py loaddata joyjet_cart_api/core/fixtures/*.json`

## Running
* Server<br/>
`$ python manage.py runserver`
* Tests<br/>
`$ python manage.py test`

## Consuming API
The application will run at **localhost:8000**

### Resources
`/carts`