from django.core.paginator import Paginator

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
        
        meta = getattr(self, "Meta", None)
        
        _columns = []
        self._columns = []
        order = self.request.GET.get("order", order_by)
        
        if meta:
            if not queryset:
                queryset = meta.model.objects
            sortable = getattr(meta, "sortable", ())
            nonsortable = getattr(meta, "nonsortable", ())            
            _model_columns = meta.model._meta.get_all_field_names()
            _columns = getattr(meta, "columns", _model_columns)
            for col in _columns:
                col_sortable = False
                label = col
                if col in _model_columns:
                    label = meta.model._meta.get_field(col).verbose_name
                    col_sortable = True
                    if sortable or nonsortable:
                        if col in nonsortable or (sortable and col not in sortable):
                            col_sortable = False
                self._columns.append(GridColumn(request, col, label, col_sortable))
                
        self.queryset = queryset
        if order:
            self.queryset = self.queryset.order_by(order)
            
        self._paginator = Paginator(self.queryset.all(), per_page)

    @property            
    def page(self):
        return self._paginator.page(self.request.GET.get("page", 1))

    @property        
    def paginator(self):
        return self._paginator
    
    @property
    def columns(self):
        return self._columns