
def create_restaurant(name='patate'):
    resto = Restaurant.objects.create(name='patate')
    resto.save()

    #resto = Restaurant.objects.all()[0] 
