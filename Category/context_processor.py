from .models import Category_Model


def Category_context(request):
    category_context = Category_Model.objects.all()

    if category_context:
          return {'category_context': category_context}
    else:
         return {'category_context': 'No Available'}
    
    # the context processor method always return dictionary that this method can be access in any template 
    # after that he must be add in template 