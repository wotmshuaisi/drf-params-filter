from django.db.models import Q


class BaseFilter(object):
    # fields dict, params_name: conditions
    fields = {}

    def __init__(self, query_params, queryset):
        self.q_obj = Q()
        self.query_params = query_params
        self.queryset = queryset

    def __filter_field(self, field_name, field_val):
        self.q_obj.children.append((field_name, field_val))

    def __generate_queryset(self,):
        if self.q_obj.children.__len__() > 1:
            self.q_obj.connector = 'and'
        return self.queryset.filter(self.q_obj)

    def __params_is_valid(self, ):
        """
        Judgment the params is valid or not
        """
        if not self.query_params:
            return False
        for item in self.fields.keys():
            if item in self.query_params:
                return True
        else:
            return False

    def conditions_queryset(self, exclude_params=[]):
        # if params not valid, return origin querset
        if not self.__params_is_valid():
            return self.queryset
        # auto add conditions from fields dict
        for key, condition in self.fields.items():
            # pass unknow params
            if not key in self.query_params:
                continue
            # pass exclude params
            if key in exclude_params:
                continue
            # pass null params
            if not self.query_params.get(key):
                continue
            self.__filter_field(
                condition,
                self.query_params.get(key))
        # return a conditional queryset
        return self.__generate_queryset()
