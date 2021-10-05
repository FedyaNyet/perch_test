from decimal import Decimal

class Median:
    """
    Helper method class to allow queryset aggregated calculation for Median
    """

    def __init__(self, queryset, term):
      self.queryset = queryset
      self.term = term

    def aggregate(self):
        count = self.queryset.count()
        values = self.queryset.values_list(self.term, flat=True).order_by(self.term)
        if count < 1:
            return 0
        if count % 2 == 1:
            return values[int((count-1)/2)]
        else:
            return sum(values[count/2-1:count/2+1])/Decimal(2.0)
