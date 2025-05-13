from django.db import models

class Venda(models.Model):
    po_number = models.CharField(max_length=20)
    cust_no = models.IntegerField()
    sales_rep = models.IntegerField()
    order_status = models.CharField(max_length=20)
    order_date = models.DateField()
    ship_date = models.DateField()
    data_needed = models.DateField()
    paid = models.BooleanField(default=False)
    qtd_ordered = models.IntegerField()
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    item_type = models.CharField(max_length=20)
    aged = models.IntegerField()

    def __str__(self):
        return f"Venda {self.po_number} | {self.order_status} - {self.total_value} ({self.paid})"