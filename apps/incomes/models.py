from django.db import models

class Income(models.Model):
    id = models.AutoField(primary_key=True)

    value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        db_column="valor"
    )

    source = models.CharField(
        max_length=255,
        db_column="fuente",
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=100,
        db_column="categoria",
        null=True,
        blank=True
    )

    payment_method = models.CharField(
        max_length=100,
        db_column="metododepago",
        null=True,
        blank=True
    )

    date = models.DateTimeField(
        db_column="fecha"
    )

    reference = models.CharField(
        max_length=255,
        db_column="referencia",
        null=True,
        blank=True
    )

    financial_planning_id = models.IntegerField(
        db_column="idplanificacionfinanciera",
        null=True,
        blank=True
    )

    accounting_account_id = models.IntegerField(
        db_column="cuentacontable_id",
        null=True,
        blank=True
    )

    user_id = models.IntegerField(
        db_column="user_id"
    )

    class Meta:
        db_table = "ingreso"   # 👈 nombre exacto de la tabla
        managed = False        # 👈 NO deja que Django la toque

    def __str__(self):
        return f"{self.source} - {self.value}"