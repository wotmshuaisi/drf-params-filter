# request_params_filter

[![forthebadge](http://forthebadge.com/images/badges/built-by-codebabes.svg)](http://forthebadge.com)  

to filter the database record with GET params is easily, but trouble, so i wrote this plugin for DRF3,  hope it works for you

# Getting Started

to filter record you need to create a class base on BaseFilter, then write a dict `fields` with format {'params': 'django_orm_conditions'}
## Example

- project/api/filter.py

```python
from request_params_filter.filter import BaseFilter

class CustomFilter(BaseFilter):
    fields = {
        'date': 'datetime_startswith',
        'name': 'name',
        'max_amount': 'amount__gte',
        'min_amount': 'amount__lte'
    }
```

- project/api/viewsets/test_viewset.py

```python
from test.models import Test
from project.api.filter import CustomFilter

class TestViewSet(viewset.Viewset):
    def list(self, request):
        queryset = Test.objects.filter(user=request.user).all()
        filter_obj = CustomFilter(request.query_params, queryset)
        # normal
        queryset = filter_obj.conditions_queryset()
        # to skip some params
        # queryset = filter_obj.conditions_queryset(['max_amount', 'min_amount'])        
        return Response(queryset)
```


## Depends

- django.db.models.Q()
