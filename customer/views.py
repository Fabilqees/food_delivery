from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        breakfast = MenuItem.objects.filter(category__name__contains='Breakfast')
        lunch = MenuItem.objects.filter(category__name__contains='Lunch')
        dinner = MenuItem.objects.filter(category__name__contains='Dinner')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner,
            'drinks': drinks,
        }

        # render the template

        return render(request, 'customer/order.html', context)
    

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        

        order_items = {
            'items': []
        }

        price = 0
        item_ids = []

       

        items = request.POST.getlist('items[]')

        for item in items:
            try:
                menu_item = MenuItem.objects.get(pk=int(item))
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.name,
                    'price': menu_item.price
                }

                order_items['items'].append(item_data)

                # Accumulate the price for the order (assuming 'price' is an integer or float)
                price += menu_item.price
                item_ids.append(menu_item.pk)
            except MenuItem.DoesNotExist:
                # Handle the case where the menu item does not exist (optional)
                print(f"MenuItem with id {item} does not exist.")

            
        
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

            order = OrderModel(
                price=price,
                name=name,
                email=email,
                street=street,
                city=city,
                state=state,
                zip_code=zip_code
                )
            order.save()
            order.items.add(*item_ids)
            order.save()

            # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        # send_mail(
        #     'Thank You For Your Order!',
        #     body,
        #     'example@example.com',
        #     [email],
        #     fail_silently=False
        # )

        context = {
                'items': order_items['items'],
                'price': price
            }
        
        return redirect('order-confirmation', pk=order.pk)

        
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')
    
class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)