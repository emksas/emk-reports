from django import models

class Income(models.Model): 
    
    id = models.IntegerField(primary_key=True)
    description = models.CharField( db_column="descripcion" , max_length=250)
    amount = models.DecimalField( db_column="monto", max_digits=5, decimal_places=2)
    category = models.CharField( db_column="categoria", max_length=100)
    incomeDate = models.DateField( db_column="fecha")
    userId = models.IntegerField( db_column="user_id" )
    
    class Meta:
        db_table = "ingresos"
        managed = False