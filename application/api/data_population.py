from models import *
from django.http import HttpResponse

def populate_database(request=None):
    populate_user()
    populate_resto()
    populate_commande()

    return HttpResponse({'success': True})

def populate_user():
    # script that will populate the database with users

    if not User.objects.filter(username='admin@resto.com').exists():
        user = User.objects.create_user(
            username='admin@resto.com',
            first_name='admin',
            last_name='f',
            email='admin@resto.com',
            password='asd')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='5148800928',
            is_admin=True)

    if not User.objects.filter(username='entrepreneur@resto.com').exists():
        user = User.objects.create_user(
            username='entrepreneur@resto.com',
            first_name='entrepreneur',
            last_name='f',
            email='entrepreneur@resto.com',
            password='asd')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='5148800928',
            is_entrepreneur=True)

    if not User.objects.filter(username='restaurateur@resto.com').exists():
        user = User.objects.create_user(
            username='restaurateur@resto.com',
            first_name='restaurateur',
            last_name='f',
            email='restaurateur@resto.com',
            password='asd')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='5148800928',
            is_restaurateur=True)

    if not User.objects.filter(username='livreur@resto.com').exists():
        user = User.objects.create_user(
            username='livreur@resto.com',
            first_name='livreur',
            last_name='f',
            email='livreur@resto.com',
            password='asd')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='5148800928',
            is_livreur=True)

    if not User.objects.filter(username='client@resto.com').exists():
        user = User.objects.create_user(
            username='client@resto.com',
            first_name='client',
            last_name='f',
            email='client@resto.com',
            password='asd')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='5148800928')

    if not User.objects.filter(username='andy@hotmail.com').exists():
        user = User.objects.create_user(
            username='andy@hotmail.com',
            first_name='Andy',
            last_name='Su',
            email='andy@hotmail.com',
            password='patate')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='26 mars 2010',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='5148800928',
            is_restaurateur=True)

    if not User.objects.filter(username='jacques@hotmail.com').exists():
        user = User.objects.create_user(
                username= 'jacques@hotmail.com',
            first_name='jacques',
            last_name='gabriel',
            email='jacques@hotmail.com',
            password='potato')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='28 mars 2000',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='1234567514',
            is_restaurateur=True)

    if not User.objects.filter(username='mdupuis@hotmail.ca').exists():
        user = User.objects.create_user(
            username= 'mdupuis@hotmail.ca',
            first_name='maxime',
            last_name='dupuis',
            email='mdupuis@hotmail.ca',
            password='asd')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='27 mars 1990',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='1234561234')

    if not User.objects.filter(username='philippe@hotmail.com').exists():
        user = User.objects.create_user(
            username= 'philippe@hotmail.com',
            first_name='philippe',
            last_name='murray',
            email='philippe@hotmail.com',
                password='potate')

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='25 mars 1980',
            adresse=['1100 Rue Notre-Dame Ouest'],
            telephone='5432102020',
            is_restaurateur=True)

def populate_resto():
    # a script that populates the database with restaurants

    restaurateurs = UserProfile.objects.filter(is_restaurateur=True)

    if not Restaurant.objects.filter(name='Pataterie').exists():
        resto = Restaurant.objects.create(
            name='Pataterie',
            address='1877 Rue Amherst',
            user=restaurateurs[1].user,
            menu={
                'sous_menus': [
                    {'name': 'menu matin',
                     'items': [
                        {'name': 'patate',
                         'desc': 'des patates',
                         'price': '3'},
                        {'name': 'patate small',
                         'desc': 'des petites patates',
                         'price': '5'}
                    ]},
                    {'name': 'menu soir',
                     'items': [{
                         'name': 'poutine',
                         'desc': 'de la poutine',
                         'price': '7'},
                        {'name': 'hotdog',
                         'desc': 'des hotdogs',
                         'price': '6'},
                    ]}
                ]
            })

    if not Restaurant.objects.filter(name='Subway').exists():
        resto = Restaurant.objects.create(
            name='Subway',
            address='2020 Rue University',
            user=restaurateurs[2].user,
            menu={
                'sous_menus': [
                    {'name': 'menu matin',
                     'items': [
                    {'name': 'sous-marin',
                         'desc': '12 pouces',
                         'price': '5'}
                    ]}
                ]
            })

    if not Restaurant.objects.filter(name='McDonalds').exists():
        resto = Restaurant.objects.create(
            name='McDonalds',
            address='895 Rue de la Gauchetiere',
            user=restaurateurs[3].user,
            menu={
                'sous_menus': [
                    {'name': 'eat fat',
                     'items': [
                         {'name': 'BigMac',
                         'desc': '100% boeuf',
                         'price': '7'}
                    ]}
                ]
            })

    if not Restaurant.objects.filter(name='Buffet').exists():
        resto = Restaurant.objects.create(
            name='Buffet',
            address='67 Rue de la Gauchetiere',
            user=None,
            menu={})

def populate_commande():
    # a script that populates the database with restaurants

    restaurant = Restaurant.objects.get(name='Pataterie')
    restaurant2 = Restaurant.objects.get(name='Subway')

    commande = Commande.objects.create(
        restaurant=restaurant,
        status='paid',
        details={
            'commande': [{
                'desc':'des patates',
                'name':'patate',
                'price':'3',
                'qty':'1'}],
            'notify': False,
            'addressTo': 'XX_destination',
            'addressFrom': 'XX_adresse_resto',
            'requestedTime': "2015-03-18T20:15:02.449Z",
        })

    commande = Commande.objects.create(
        restaurant=restaurant,
        status='paid',
        details={
            'commande': [{
                'name': 'poutine',
                'desc': 'de la poutine',
                'price': '7',
                'qty':'1'}],
            'notify': False,
            'addressTo': 'XX_destination',
            'addressFrom': 'XX_adresse_resto',
            'requestedTime': "2015-03-18T20:15:02.449Z",
        })

    commande = Commande.objects.create(
        restaurant=restaurant2,
        status='paid',
        details={
            'commande': [{
                'name': 'sous-marin',
                'desc': '12 pouces',
                'price': '5',
                'qty':'1'}],
            'notify': False,
            'addressTo': 'XX_destination',
            'addressFrom': 'XX_adresse_resto',
            'requestedTime': "2015-03-18T20:15:02.449Z",
        })
