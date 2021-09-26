from django.db import models


# Create your models here.

class Liste(models.Model):
    """Eine Vokabelliste fuer die Abfrage"""
    name = models.CharField(max_length=500)
    beschreibung = models.CharField(max_length=2000, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    file = models.FileField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Listen'

    def __str__(self):
        """Return Beschreibung"""
        return self.name


class Vokabel(models.Model):
    """Ein einziges Vokabelpaar"""
    # Allgemeines
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE)
    deutsch = models.CharField(max_length=100)
    franzoesisch = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    # Statistik
    abfragen = models.IntegerField(default=0)
    korrekt = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = 'Vokabeln'

    def __str__(self):
        """Return Vokabelpaar"""
        return str(self.deutsch) + ' - ' + str(self.franzoesisch)


class Abfrage(models.Model):
    """Abfrage einer Vokabelliste"""
    liste = models.ForeignKey(Liste, on_delete=models.PROTECT)
    vokabeln = models.ManyToManyField(Vokabel)
    date_added = models.DateTimeField(auto_now_add=True)
    reihenfolge = models.CharField(max_length=10000)

    class Meta:
        verbose_name_plural = 'Abfragen'
