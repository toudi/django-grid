#-*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.db import models

class GridColumn(object):
    def __init__(self, request, colname, label, is_sortable = False):
        self.colname = colname
        self.label = label
        self.is_sortable = is_sortable
        self.request = request
        
    @property
    def sortable(self):
        return self.is_sortable
        
    @property
    def order(self):
        sort = self.colname
        if self.colname in self.request.GET.get("order", "") and self.request.GET["order"][0] != "-":
            sort = "-" + sort
        return sort
    
    def __unicode__(self):
        return "%s (%s)" % (self.colname, self.sortable)
    
class Grid(object):
    def __init__(self, request, per_page = 50, queryset = None, order_by = None):
        self.request = request
        self.queryset = queryset
        self._paginator = None
        self.custom_columns = {}
        self.pageno = int(request.GET.get("page", 1))
        self.adjacent_pages = 5
        
        meta = getattr(self, "Meta", None)
        
        _columns = []
        self._columns = []
        order = self.request.GET.get("order", order_by)
        
        if meta:
            if queryset is None:
                queryset = meta.model.objects
            sortable = getattr(meta, "sortable", ())
            nonsortable = getattr(meta, "nonsortable", ())            
            _model_columns = meta.model._meta.get_all_field_names()
            ##
            # Autor: Toudi
            ##
            self._model_columns = _model_columns
            self.meta = meta
            self.sortable = sortable
            self.nonsortable = nonsortable
            _columns = getattr(meta, "columns", _model_columns)
            self.custom_columns = getattr(meta, "custom_columns", {})
            self.setColumns(_columns)
                
        self.queryset = queryset
        if order:
            self.queryset = self.queryset.order_by(order)
            
        self._paginator = Paginator(self.queryset.all(), per_page)

    ##
    # Autor: Toudi
    ##
    def setColumns(self, _columns = []):
        self._columns = []
        for col in _columns:
            col_sortable = False
            if type(col) == str or type(col) == unicode:
                label = col
                if col in self._model_columns:
                    label = self.meta.model._meta.get_field(col).verbose_name
                    col_sortable = True
                    if self.sortable or self.nonsortable:
                        if col in self.nonsortable or (self.sortable and col not in self.sortable):
                            col_sortable = False
            else:
                label = col[1]
                col   = col[0]
            self._columns.append(GridColumn(self.request, col, label, col_sortable))
    
    
    @property
    def order(self):
        return self.request.GET.get("order", None)
                    
    @property            
    def page(self):
        return self._paginator.page(self.pageno)

    @property        
    def paginator(self):
        return self._paginator
    
    @property
    def columns(self):
        return self._columns
    
    @property
    def url(self):
        url = self.request.get_full_path()
        if not self.request.GET:
            url += "?"
        return url
    
    @property
    def paginator_page_range(self):
        start_page = max(self.pageno - self.adjacent_pages, 1)
        end_page   = min((self.page.number + self.adjacent_pages), self.paginator.num_pages)
        
        return [n for n in range(start_page, end_page + 1)]
    
    @property    
    def paginator_show_first(self):
        return 1 not in self.paginator_page_range

    @property    
    def paginator_show_last(self):
        return self.paginator.num_pages not in self.paginator_page_range
    
class MongoGrid(Grid):
    
    def __init__(self, request, per_page = 50, queryset = None, order_by = None, filtr = None, skip = False):
        self.request = request
        self.per_page = per_page
        self._columns = []
        self.skip = skip
        findParams = {}
        order = self.request.GET.get("order", order_by)
        queryset = queryset.find(filtr)
        self.pageno = int(request.GET.get("page", 1))
        self.adjacent_pages = 5
        #print(filtr)
        if order:
            import pymongo
            order = order.split("-")
            order_dir = pymongo.ASCENDING
            if len(order) > 1:
                order_dir = pymongo.DESCENDING
            queryset = queryset.sort(order[-1], order_dir)
        self.queryset = queryset
        
    def setColumns(self, columns):
        from copy import copy
        for column in columns:
            col = column
            if type(col) == str or type(col) == unicode:
                label = col
            else:
                label = col[1]
                col   = col[0]
            self._columns.append(GridColumn(self.request, col, label, True))
        query_count = copy(self.queryset)
        page = self.pageno - 1
        if self.skip:
            objects = self.queryset#.limit(self.per_page).skip(page*self.per_page)
        else:
            objects = self.queryset.limit(self.per_page).skip(page*self.per_page)
        self.objects = [o for o in objects]
        self._paginator = Paginator(self.objects, self.per_page)
        self._paginator._count = query_count.count()
        
    @property
    def page(self):
        page = self._paginator.page(self.pageno)
        page.object_list = self.objects
        return page