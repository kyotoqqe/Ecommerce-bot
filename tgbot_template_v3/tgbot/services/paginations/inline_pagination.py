from math import ceil

class Paginator:

    ELLIPSIS = "..."

    def __init__(self,queryset,page_size):
        self.queryset = queryset
        self.page_size = page_size
    
    @property
    def page_counter(self):
        if len(self.queryset)==0:
            return 0
        
        return ceil(self.count/self.page_size)
    


    @property
    def count(self):
        return len(self.queryset)
    
    def page(self,number):
        start = (number-1)*self.page_size
        end = start+self.page_size
        return self.page_builder(self.queryset[start:end],number,self)
    
    def page_builder(self,*args, **kwargs):
        return Page(*args, **kwargs)

    @property
    def get_pages(self):
        return range(1,self.page_counter+1)

    def get_pages_markup(self,number=1,onside=2,onends=2):
        if self.page_counter <= onside+onends:
            yield from self.get_pages
            return
        #суть в том что для того чтобы вставить ... нужно по крайней мере пропускать 2 страницы
        if number > (1+onends+onside)+1:
            yield from range(1,onends+1)
            yield self.ELLIPSIS
            yield from range(number-onside,number+1)
        else:
            yield from range(1,self.page_counter+1)
        
        if number < (self.page_counter-(onends+onside)-1):
            yield from range(number,number+onside+1)
            yield self.ELLIPSIS
            yield from range(self.page_counter-onends,self.page_counter+1)
        else:
            yield from range(number+1,self.page_counter+1)

        




class Page:
    def __init__(self,queryset,page_number,paginator):
        self.queryset = queryset
        self.page_number = page_number
        self.paginator = paginator
    
    def __iter__(self):
        for elem in self.queryset:
            yield elem