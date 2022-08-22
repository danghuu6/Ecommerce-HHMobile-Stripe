from rest_framework import filters

class ProductSearchFilter(filters.SearchFilter):
    search_param = "product"