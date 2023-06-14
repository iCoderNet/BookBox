from .models import Person

def mydata(request):
    if request.user.is_authenticated:
        try:
            mydata = Person.objects.get(user=request.user) 
            return {'mydata': mydata}
        except Person.DoesNotExist:
            Person.objects.create(user=request.user)
            mydata = Person.objects.get(user=request.user) 
            return {'mydata': mydata}
    else:
        return {'mydata': None}