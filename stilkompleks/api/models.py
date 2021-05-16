from django.db import models
import string
import random
from enum import Enum
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class Machine(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=255, null=False)
    image = models.ImageField('ИЗБЕРИ СНИМКА', null=True, blank=True)


    def __str__(self):
        return self.name

class MaterialType(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Obekti(models.Model):
    name = models.CharField("Име",
        max_length=50)
    investor = models.CharField("Инвеститор", max_length=50)
    image = models.ImageField('ИЗБЕРИ СНИМКА', null=True, blank=True)
    address = models.CharField("Адрес", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    base = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Material(models.Model):
    class Type(models.TextChoices):
        KOFRAJPLOCHI = 'Kp', _('Кофражи за Плочи')
        KOFRAJVERTIKALI = 'Kv', _('Кофражи за Вертикали')
        SKELE = 'Sk', _('Скеле')

    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    amount_type = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField('ИЗБЕРИ СНИМКА', null=True, blank=True)
    type = models.ForeignKey(
        MaterialType,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name} - {self.amount_type}'

    @property
    def get_total_per_material(self, pk):
        material_set = self.materialperobekt_set.all()
        sum = 0
        for mat in material_set:
            if mat.material.id == pk:
                sum += mat.amount
        return sum


class MaterialPerObekt(models.Model):
    obekt = models.ForeignKey(
        Obekti,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=5)


    def __str__(self):
        return f'{self.material.name} - {self.obekt.name}'

    def clean(self):
        materialperobekt = MaterialPerObekt.objects.filter(obekt=self.obekt, material=self.material)

        if materialperobekt.exists() and materialperobekt[0].id != self.pk:
            raise ValidationError(_('Този материал вече го има в зададения обект.'))


class Personal(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    class Position(models.TextChoices):
        TECHNICAL = 'Tc', _('Технически Ръководители')
        DELIVERY = 'De', _('Снабдители и Шофьори')
        ADMIN = 'Ad', _('Администратори')

    image = models.ImageField('ИЗБЕРИ СНИМКА', null=True, blank=True)
    name = models.CharField(max_length=50, null=False)
    position = models.CharField(max_length=255, choices=Position.choices, null=False)
    obekt = models.ForeignKey(
        Obekti,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    mail = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    machine = models.ForeignKey(Machine, models.SET_NULL,
    blank=True,
    null=True)

    def __str__(self):
        return self.name

    def clean(self):
        obekt = self.obekt
        personal = Personal.objects.filter(obekt=obekt)
        if self.position == 'Tc':
            for p in personal:
                if p.position == 'Tc' and p.id != self.pk:
                    raise ValidationError("Този обект вече има зададен технически ръководител!")



class OrderMat(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    date = models.DateField('ИЗБЕРИ ДАТА', null=True)
    complete = models.BooleanField(default=False)
    approved = models.BooleanField(default=False, null=True, blank=True)
    obekt = models.ForeignKey(
        Obekti,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    transport = models.ForeignKey(
        Machine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return "ЗАЯВКА {}".format(self.obekt.name.upper())


class OrderMaterial(models.Model):
    order = models.ForeignKey(OrderMat, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    null=True,
                                    blank=True
                                )

    material = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return str(self.id)



class OrderMaterialPerObekt(models.Model):
    order_material = models.ForeignKey(
        OrderMaterial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    obekt = models.ForeignKey(
        Obekti,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    null=True,
                                    blank=True
                                )
    allowed = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    null=True,
                                    blank=True
                                )



class OrderMachine(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    class Hours(models.TextChoices):
        opt1 = '1', _('8:00 - 12:00')
        opt2 = '2', _('13:00 - 17:00')
        opt3 = '3', _('8:00 - 17:00')

    hours = models.CharField(max_length=255, choices=Hours.choices, null=False)
    obekt = models.ForeignKey(
        Obekti,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    machine = models.ForeignKey(
        Machine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    date = models.DateField('ИЗБЕРИ ДАТА', null=True)

    def __str__(self):
        return str(self.id)