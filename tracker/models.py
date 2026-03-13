from django.db import models

# Create your models here.


class Category(models.Model):
    name =models.CharField(max_length=100)
    color = models.CharField(max_length=7 ,default='#6366f1')
    icon = models.CharField(max_length=100,default='💰')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

class Expense(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete = models.CASCADE,
                                 related_name ='expenses')
    
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date =models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - ${self.amount}'
    
    class Meta:
        ordering = ['-date']


    