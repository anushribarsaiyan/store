#****(1) Return all Customer From customer table
customers=customer.objects.all()
# (2) Return First customer in table
firstCustomer=Customer.objects.first()
#(3)Return last customer in table
lastCustomer=customer.objects.last()
#(4)Retuen single customer by name
customersByName=custome.objects.get(name="anubhav")
#(5)Return single customer by name
customersById=customer.objects.get(id=4)
#(6)Return all orders related to customer(firstCustomer variable set above)
firstCustomer.order_set.all()
#7)Return orers customer name(query parent model values)
order=Order.objects.first()
parentName=order.customer.name
#8 Return orders products from products table with "out door" in category attibute
products=products.objects.filter(category="out Door")
#order/soort objects by id
leastToGreatest=product.objects.all().order_by('id')
greatestToleast=Product.object.all().order_by('-id')

#10 Return all products with tag og sports:(query Many Many fields)
productsFiltered=product.objects.filters(tags_name="sports")

'''(11)Bonus
Q: If the customer has more than 1 ball, how would you reflect it in the database?
A: Because there are many different products and this value changes constantly you would most 
likly not want to store the value in the database but rather just make this a function we can run
each time we load the customers profile
'''

#Returns the total count for number of time a "Ball" was ordered by the first customer
ballOrders = firstCustomer.order_set.filter(product__name="Ball").count()

#Returns total count for each product orderd
allOrders = {}

for order in firstCustomer.order_set.all():
	if order.product.name in allOrders:
		allOrders[order.product.name] += 1
	else:
		allOrders[order.product.name] = 1

#Returns: allOrders: {'Ball': 2, 'BBQ Grill': 1}


#RELATED SET EXAMPLE
class ParentModel(models.Model):
	name = models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
	parent = models.ForeignKey(Customer)
	name = models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
#Returns all child models related to parent
parent.childmodel_set.all()

