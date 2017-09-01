# -*- coding: utf-8 -*-
#
# django-codenerix-invoicing
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import datetime
from django.core.urlresolvers import reverse
from django.db import models, transaction, IntegrityError
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from codenerix.models import GenInterface, CodenerixModel
from codenerix.models_people import GenRole
from codenerix_extensions.helpers import get_external_method
from codenerix_extensions.files.models import GenDocumentFile

from codenerix_invoicing.models import Haulier, BillingSeries
from codenerix_invoicing.models_purchases import PAYMENT_DETAILS
from codenerix_invoicing.settings import CDNX_INVOICING_PERMISSIONS
 
from codenerix_pos.models import POSSlot

from codenerix_products.models import ProductFinal, TypeTax, ProductFinalOption
from codenerix_storages.models import Storage
from codenerix_payments.models import PaymentRequest

    
ROLE_BASKET_SHOPPINGCART = 'SC'
ROLE_BASKET_BUDGET = 'BU'
ROLE_BASKET_WISHLIST = 'WL'

ROLE_BASKET = (
    (ROLE_BASKET_SHOPPINGCART, _("Shopping cart")),
    (ROLE_BASKET_BUDGET, _("Budget")),
    (ROLE_BASKET_WISHLIST, _("Wish list")),
)

STATUS_BUDGET_PENDING_PAYMENT = 'PP'
STATUS_BUDGET_PAYMENT_ACCETED = 'PA'
STATUS_BUDGET_DRAFT = 'DR'

STATUS_BUDGET = (
    (STATUS_BUDGET_DRAFT, _("Draft")),
    (STATUS_BUDGET_PENDING_PAYMENT, _("Pending payment")),
    (STATUS_BUDGET_PAYMENT_ACCETED, _("Payment accepted")),
)

STATUS_ORDER = (
    ('PE', _("Pending")),
    ('PA', _("Payment accepted")),
    ('SE', _("Sent")),
    ('DE', _("Delivered")),
)


STATUS_WISHLIST_PUBLIC = 'PU'
STATUS_WISHLIST = (
    (STATUS_WISHLIST_PUBLIC, _('Public')),
    ('PR', _('Private')),
)

TYPE_PRIORITY_MEDIUM = 'L'
TYPE_PRIORITIES = (
    ('XS', _('Muy baja')),
    ('S', _('Baja')),
    (TYPE_PRIORITY_MEDIUM, _('Media')),
    ('XL', _('Alta')),
    ('XXL', _('Urgente')),
)


class ABSTRACT_GenCustomer(models.Model):  # META: Abstract class

    class Meta(object):
        abstract = True


class Customer(GenRole, CodenerixModel):
    class CodenerixMeta:
        abstract = ABSTRACT_GenCustomer
        rol_groups = {
            'Customer': CDNX_INVOICING_PERMISSIONS['customer'],
        }
        rol_permissions = [
            'add_city',
            'add_citygeonameen',
            'add_citygeonamees',
            'add_continent',
            'add_continentgeonameen',
            'add_continentgeonamees',
            'add_corporateimage',
            'add_country',
            'add_countrygeonameen',
            'add_countrygeonamees',
            'add_customer',
            'add_customerdocument',
            'add_person',
            'add_personaddress',
            'add_province',
            'add_provincegeonameen',
            'add_provincegeonamees',
            'add_region',
            'add_regiongeonameen',
            'add_regiongeonamees',
            'add_salesbasket',
            'add_saleslinebasket',
            'add_timezone',
            'change_city',
            'change_citygeonameen',
            'change_citygeonamees',
            'change_continent',
            'change_continentgeonameen',
            'change_continentgeonamees',
            'change_corporateimage',
            'change_country',
            'change_countrygeonameen',
            'change_countrygeonamees',
            'change_customer',
            'change_customerdocument',
            'change_person',
            'change_personaddress',
            'change_province',
            'change_provincegeonameen',
            'change_provincegeonamees',
            'change_region',
            'change_regiongeonameen',
            'change_regiongeonamees',
            'change_salesbasket',
            'change_saleslinebasket',
            'change_timezone',
            'change_user',
            'delete_city',
            'delete_citygeonameen',
            'delete_citygeonamees',
            'delete_continent',
            'delete_continentgeonameen',
            'delete_continentgeonamees',
            'delete_corporateimage',
            'delete_country',
            'delete_countrygeonameen',
            'delete_countrygeonamees',
            'delete_customer',
            'delete_customerdocument',
            'delete_person',
            'delete_personaddress',
            'delete_province',
            'delete_provincegeonameen',
            'delete_provincegeonamees',
            'delete_region',
            'delete_regiongeonameen',
            'delete_regiongeonamees',
            'delete_salesbasket',
            'delete_saleslinebasket',
            'delete_timezone ',
            'list_billingseries',
            'list_city',
            'list_continent',
            'list_corporateimage',
            'list_country',
            'list_customer',
            'list_customerdocument',
            'list_legalnote',
            'list_personaddress',
            'list_productdocument',
            'list_province',
            'list_purchaseslineinvoice',
            'list_region',
            'list_salesalbaran',
            'list_salesbasket',
            'list_salesinvoice',
            'list_salesinvoicerectification',
            'list_saleslinealbaran',
            'list_saleslinebasket',
            'list_saleslineinvoice',
            'list_saleslineinvoicerectification',
            'list_saleslineorder',
            'list_saleslineticket',
            'list_saleslineticketrectification',
            'list_salesorder',
            'list_salesreservedproduct',
            'list_salesticket',
            'list_salesticketrectification',
            'list_timezone',
            'list_typedocument',
            'list_typedocumenttexten',
            'list_typedocumenttextes',
            'view_billingseries',
            'view_city',
            'view_continent',
            'view_corporateimage',
            'view_country',
            'view_customer',
            'view_customerdocument',
            'view_legalnote',
            'view_personaddress',
            'view_province',
            'view_region',
            'view_salesbasket',
            'view_saleslinebasket',
            'view_timezone',
            'view_typedocument',
            'view_typedocumenttexten',
            'view_typedocumenttextes',
        ]

        force_methods = {
            'foreignkey_customer': ('CDNX_get_fk_info_customer', _('---')),
            'get_email': ('CDNX_get_email', ),
        }

    currency = models.CharField(_("Currency"), max_length=250, blank=True, null=True)
    # serie de facturacion
    billing_series = models.ForeignKey(BillingSeries, related_name='billing_series', verbose_name='Billing series')
    # datos de facturación
    # saldo final
    final_balance = models.CharField(_("Balance"), max_length=250, blank=True, null=True)
    # credito o riesgo maximo autorizado
    credit = models.CharField(_("Credit"), max_length=250, blank=True, null=True)
    # Aplicar recargo de equivalencia
    apply_equivalence_surcharge = models.BooleanField(_("Apply equivalence surcharge"), blank=False, default=False)
    # Tipo de iva
    type_tax = models.ForeignKey(TypeTax, related_name='customers', verbose_name=_("Type tax"), null=True)
    default_customer = models.BooleanField(_("Default customer"), blank=False, default=False)

    @staticmethod
    def foreignkey_external():
        return get_external_method(Customer, Customer.CodenerixMeta.force_methods['foreignkey_customer'][0])

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.external))

    def __fields__(self, info):
        fields = []
        fields.append(('final_balance', _("Balance")))
        fields.append(('credit', _("Credit")))
        fields.append(('currency', _("Currency")))
        fields.append(('billing_series', _("Billing series")))
        fields.append(('apply_equivalence_surcharge', _("Currency")))
        fields.append(('type_tax', _("Type tax")))
        fields.append(('default_customer', _("Default customer")))
        fields = get_external_method(Customer, '__fields_customer__', info, fields)
        return fields

    def save(self, *args, **kwards):
        with transaction.atomic():
            if self.default_customer:
                Customer.objects.exclude(pk=self.pk).update(default_customer=False)
            else:
                if not Customer.objects.exclude(pk=self.pk).filter(default_customer=True).exists():
                    self.default_customer = True
        return super(Customer, self).save(*args, **kwards)

    def buy_product(self, product_pk):
        """
        determina si el customer ha comprado un producto
        """
        if self.invoice_sales.filter(line_invoice_sales__line_order__product__pk=product_pk).exists() \
            or self.ticket_sales.filter(line_ticket_sales__line_order__product__pk=product_pk).exists():
            return True
        else:
            return False


# customers
class GenCustomer(GenInterface, ABSTRACT_GenCustomer):  # META: Abstract class
    customer = models.OneToOneField(Customer, related_name='external', verbose_name=_("Customer"), null=True, on_delete=models.SET_NULL, blank=True)

    class Meta(GenInterface.Meta, ABSTRACT_GenCustomer.Meta):
        abstract = True

    @classmethod
    def permissions(cls):
        group = 'Customer'
        perms = []
        print(cls.customer.field.related_model)

        return None

        # print({group: {'gperm': None, 'dperm': perms, 'model': None},})


class Address(CodenerixModel):
    def __unicode__(self):
        if hasattr(self, 'external_delivery'):
            return u"{}".format(smart_text(self.external_delivery.get_summary()))
        elif hasattr(self, 'external_invoice'):
            return u"{}".format(smart_text(self.external_invoice.get_summary()))
        else:
            return 'No data!'
            # raise Exception(_('Address unkown'), self.__dict__)

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        if hasattr(self, 'external_delivery'):
            fields.append(('external_delivery', _("Address delivery")))
        elif hasattr(self, 'external_invoice'):
            fields.append(('external_invoice', _("Address invoice")))
        else:
            raise Exception(_('Address unkown'))
        return fields


class ABSTRACT_GenAddress():  # META: Abstract class
    class Meta(object):
        abstract = True


class GenAddress(GenInterface, ABSTRACT_GenAddress):  # META: Abstract class
    class Meta(GenInterface.Meta, ABSTRACT_GenAddress.Meta):
        abstract = True

    class CodenerixMeta:
        force_methods = {
            'foreignkey_address': ('CDNX_get_fk_info_address', _('---')),
            'get_summary': ('get_summary', ),
        }

    def save(self, *args, **kwards):
        if hasattr(self, 'address_delivery') and self.address_delivery is None:
            address_delivery = Address()
            address_delivery.save()
        elif hasattr(self, 'address_delivery'):
            address_delivery = self.address_delivery
        
        if hasattr(self, 'address_invoice') and self.address_invoice is None:
            address_invoice = Address()
            address_invoice.save()
        elif hasattr(self, 'address_invoice'):
            address_invoice = self.address_invoice
            
        if hasattr(self, 'address_delivery'):
            self.address_delivery = address_delivery
        if hasattr(self, 'address_invoice'):
            self.address_invoice = address_invoice
        return super(GenAddress, self).save(*args, **kwards)


# address delivery
class GenAddressDelivery(GenAddress):  # META: Abstract class
    class Meta(object):
        abstract = True
    address_delivery = models.OneToOneField(Address, related_name='external_delivery', verbose_name=_("Address delivery"), null=True, on_delete=models.SET_NULL, blank=True, editable=False)
    

# address invoice
class GenAddressInvoice(GenAddress):  # META: Abstract class
    class Meta(object):
        abstract = True
    address_invoice = models.OneToOneField(Address, related_name='external_invoice', verbose_name=_("Address invoice"), null=True, on_delete=models.SET_NULL, blank=True, editable=False)
    

# documentos de clientes
class CustomerDocument(CodenerixModel, GenDocumentFile):
    customer = models.ForeignKey(Customer, related_name='customer_documents', verbose_name=_("Customer"))
    type_document = models.ForeignKey('TypeDocument', related_name='customer_documents', verbose_name=_("Type document"), null=True)

    def __unicode__(self):
        return u"{}".format(smart_text(self.customer))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _("Customer")))
        fields.append(('type_document', _("Type document")))
        return fields


# #####################################
# ######## VENTAS #####################
# #####################################
# GenVersion
class GenVersion(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True
        unique_together = (("code", "parent_pk"))

    # número de versión del documento
    # version = models.IntegerField(_("Version"), blank=False, null=False)
    # indica si la versión esta bloqueada
    lock = models.BooleanField(_("Lock"), blank=False, default=False)
    # pk de la versión original
    parent_pk = models.IntegerField(_("Parent pk"), blank=True, null=True)
    code = models.CharField(_("Code"), max_length=64, blank=False, null=False)
    date = models.DateTimeField(_("Date"), blank=False, null=False, default=timezone.now)
    observations = models.TextField(_("Observations"), max_length=256, blank=True, null=True)
    """
    si al guardar una linea asociada a un documento bloqueado (lock==True), duplicar el documento en una nueva versión
    """
    # additional information
    subtotal = models.FloatField(_("Subtotal"), blank=False, null=False, default=0, editable=False)
    discounts = models.FloatField(_("Discounts"), blank=False, null=False, default=0, editable=False)
    taxes = models.FloatField(_("Taxes"), blank=False, null=False, default=0, editable=False)
    total = models.FloatField(_("Total"), blank=False, null=False, default=0, editable=False)
    # logical deletion
    removed = models.BooleanField(_("Removed"), blank=False, default=False, editable=False)

    @staticmethod
    def getcode(model, real=False):
        if real is False:
            code = 0
        else:
            last = model.objects.order_by('-pk').first()
            if last:
                code = int(last.code) + 1
            else:
                code = 1
        return code

    def save(self, *args, **kwards):
        force_save = kwargs.get('force_save', False)
        if self.pk:
            obj = self._meta.model.objects.get(pk=self.pk)

            #####################
            # En esta sección compruebo si solo se bloquea o si es un cambio.
            #####################
            # Var for check if change must duplicate or only its locking the instance.
            need_duplicate = False

            # Itero por todas las claves
            for key in self.__dict__.keys():
                # Si la clave está en obj, no es block y no es un atributo propio de self (empieza por _) comprueba si son iguales.
                if key in obj.__dict__ and key not in ['lock', 'role', 'updated', 'code', 'created'] and not key.startswith("_"):
                    if need_duplicate is False:
                        # Si son iguales, need_duplicate se mantendrá a false. Solo se activa si son distintos.
                        if type(self.__dict__[key]) == datetime.datetime and obj.__dict__[key]:
                            need_duplicate = self.__dict__[key].strftime("%Y-%m-%d %H:%M") != obj.__dict__[key].strftime("%Y-%m-%d %H:%M")
                        else:
                            need_duplicate = self.__dict__[key] != obj.__dict__[key]
                    else:
                        break

            #####################
            # Fin de comprobacion
            #####################

            # Si está bloqueado y además se ha cambiado algo más, además del lock, se duplica
            if force_save is False and obj.lock is True and need_duplicate is True:
                # parent pk
                if self.parent_pk is None:
                    self.parent_pk = self.pk

                # reset object
                self.pk = None
                self.lock = False
                self.code = GenVersion.getcode(self._meta.model, True)
        else:
            self.code = GenVersion.getcode(self._meta.model, True)

        return super(GenVersion, self).save(*args, **kwards)

    def delete(self):
        if not hasattr(settings, 'CDNX_INVOICING_LOGICAL_DELETION') or settings.CDNX_INVOICING_LOGICAL_DELETION is False:
            return super(GenVersion, self).delete()
        else:
            self.removed = True
            self.save(force_save=True)

    def update_totales(self, force_save=True):
        # calculate totals and save
        totales = self.calculate_price_doc_complete()
        self.subtotal = totales['subtotal']
        self.total = totales['total']
        self.discounts = sum(totales['discounts'].values())
        self.taxes = sum(totales['taxes'].values())
        if force_save:
            self.save()

    def calculate_price_doc_complete(self, queryset=None):
        # calculate totals with details
        if queryset:
            subtotal = 0
            tax = {}
            discount = {}
            total = 0
            for line in queryset:
                subtotal += line.subtotal
                
                if line.tax not in tax:
                    tax[line.tax] = 0
                price_tax = line.taxes
                tax[line.tax] += price_tax
                
                if line.discount not in discount:
                    discount[line.discount] = 0
                price_discount = line.discounts
                discount[line.discount] += price_discount
                
                total += line.subtotal - price_discount + price_tax
        
            return {'subtotal': subtotal, 'taxes': tax, 'total': total, 'discounts': discount}
        else:
            raise Exception(_("Queryset undefined!!"))


class GenLineProductBasic(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)
    notes = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # additional information
    subtotal = models.FloatField(_("Subtotal"), blank=False, null=False, default=0, editable=False)
    discounts = models.FloatField(_("Discounts"), blank=False, null=False, default=0, editable=False)
    taxes = models.FloatField(_("Taxes"), blank=False, null=False, default=0, editable=False)
    total = models.FloatField(_("Total"), blank=False, null=False, default=0, editable=False)
    # logical deletion
    removed = models.BooleanField(_("Removed"), blank=False, default=False, editable=False)

    def __save__(self, args, kwargs, **conditional):
        other_line = self._meta.model.objects.filter(**conditional)
        if self.pk:
            other_line = other_line.exclude(pk=self.pk)
        other_line = other_line.first()
        if not self.pk and other_line:
            if hasattr(self, 'product') and not self.product.is_pack():
                other_line.quantity += self.quantity
                other_line.save()
                return other_line.pk
            else:
                kwargs['standard_save'] = True
                return self.save(*args, **kwargs)

        elif self.pk and other_line and not other_line.product.is_pack():
            other_line.quantity += self.quantity
            self.delete()
            other_line.save()
            return other_line.pk
        else:
            kwargs['standard_save'] = True
            return self.save(*args, **kwargs)

    def delete(self):
        if not hasattr(settings, 'CDNX_INVOICING_LOGICAL_DELETION') or settings.CDNX_INVOICING_LOGICAL_DELETION is False:
            return super(GenLineProductBasic, self).delete()
        else:
            self.removed = True
            self.save(force_save=True)


# lineas de productos
class GenLineProduct(GenLineProductBasic):  # META: Abstract class
    class Meta(GenLineProductBasic.Meta):
        abstract = True

    price_recommended = models.FloatField(_("Recomended price"), blank=False, null=False)
    # valores aplicados
    """
    desde el formulario se podrá modificar el precio y la descripcion del producto
    se guarda el tax usado y la relacion para poder hacer un seguimiento
    """
    description = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    discount = models.FloatField(_("Discount"), blank=False, null=False, default=0)
    price = models.FloatField(_("Price"), blank=False, null=False)
    tax = models.FloatField(_("Tax"), blank=True, null=True, default=0)

    def __str__(self):
        description = ''
        if hasattr(self, 'description'):
            description = self.description
        elif hasattr(self, 'line_invoice'):
            description = self.line_invoice.description
        elif hasattr(self, 'line_ticket'):
            description = self.line_ticket.description
        return u"{} - {}".format(smart_text(description), smart_text(self.quantity))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('description', _("Description")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('price', _("Price")))
        fields.append(('discount', _("Discount")))
        fields.append(('tax', _("Tax")))
        fields.append(('total', _("Total")))
        return fields

    def calculate_total(self):
        # compatibility with old version
        return self.total

    def update_total(self, force_save=True):
        # calculate totals
        self.subtotal = self.price * self.quantity
        self.taxes = (self.subtotal * self.tax / 100.0)
        self.discounts = (self.subtotal * self.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes
        if force_save:
            self.save()

    @staticmethod
    def create_document_from_another(pk, list_lines,
        MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
        url_reverse, related_line, related_object,
        msg_error_relation, msg_error_not_found, unique):
        """
        pk: pk del documento origen
        list_lines: listado de pk de lineas de origen
        MODEL_SOURCE: modelo del documento origen
        MODEL_FINAL: model del documento final
        MODEL_LINE_SOURCE: modelo de la linea origen
        MODEL_LINE_FINAL: modelo de la linea final
        url_reverse: url del destino
        related_line: campo del modelo linea final en el que irá asignada la linea origen
        related_object: campo del modelo linea final en el que irá asignado el objeto final
        msg_error_relation: Mensaje de error indicando que las lineas ya están relacionadas
        msg_error_not_found: Mensaje de error indicando que no se encuentra el objeto origen
        unique: (True/False) Indica si puede haber más de una linea asociada a otras lineas
        """
        context = {}
        obj_src = MODEL_SOURCE.objects.filter(pk=pk).first()
        if list_lines and obj_src:
            # parse to int
            list_lines = [int(x) for x in list_lines]
            # list of lines objects
            if unique:
                create = not MODEL_LINE_FINAL.objects.filter(**{"{}__pk__in".format(related_line): list_lines}).exists()
            else:
                create = True

            """
            si debiendo ser filas unicas no las encuentra en el modelo final, se crea el nuevo documento
            """
            if create:
                with transaction.atomic():
                    obj_final = MODEL_FINAL()
                    obj_final.customer = obj_src.customer
                    obj_final.date = datetime.datetime.now()
                    if isinstance(obj_final, SalesOrder):
                        obj_final.budget = obj_src
                    obj_final.save()

                    for lb_pk in list_lines:
                        line_src = MODEL_LINE_SOURCE.objects.filter(pk=lb_pk).first()
                        if line_src:
                            line_final = MODEL_LINE_FINAL(**{"{}_id".format(related_object): obj_final.pk, related_line: line_src})
                            # line_final.order = obj_final
                            # line_final.line_budget = line_src
                            src_list_fields = [f.name for f in line_src._meta.get_fields()]
                            dst_list_fields = [f.name for f in line_final._meta.get_fields()]
                            if 'product' in src_list_fields and 'product' in dst_list_fields:
                                line_final.product = line_src.product
                            if 'description' in src_list_fields and 'description' in dst_list_fields:
                                line_final.description = line_src.description
                            # if hasattr(line_src, 'line_order') and hasattr(line_final, 'line_order'):
                            if 'line_order' in src_list_fields and 'line_order' in dst_list_fields:
                                line_final.line_order = line_src.line_order
                            line_final.quantity = line_src.quantity
                            line_final.price = line_src.price
                            # if hasattr(line_src, 'price_recommended') and hasattr(line_final, 'price_recommended'):
                            if 'price_recommended' in src_list_fields and 'price_recommended' in dst_list_fields:
                                line_final.price_recommended = line_src.price_recommended
                            line_final.tax = line_src.tax
                            # line_final.type_tax = line_src.type_tax
                            line_final.discount = line_src.discount
                            line_final.save()

                            if hasattr(line_src, 'line_basket_option_sales') and line_src.line_basket_option_sales.exists():
                                for opt_src in line_src.line_basket_option_sales.all():
                                    opt_dst = SalesLineOrderOption()
                                    opt_dst.line_order = line_final
                                    opt_dst.product_option = opt_src.product_option
                                    opt_dst.product_final = opt_src.product_final
                                    opt_dst.quantity = opt_src.quantity
                                    opt_dst.save()

                    # bloqueamos el documento origen
                    obj_src.lock = True
                    obj_src.save()

                    # context['url'] = reverse('ordersaless_details', kwargs={'pk': order.pk})
                    context['url'] = "{}#/{}".format(reverse(url_reverse), obj_final.pk)
                    context['obj_final'] = obj_final
            else:
                # _("Hay lineas asignadas a pedidos")
                context['error'] = msg_error_relation
        else:
            # _('Budget not found')
            context['error'] = msg_error_not_found

        return context

    def save(self, *args, **kwards):
        if self.pk is None:
            if hasattr(self, 'product'):
                if not self.description:
                    self.description = self.product
                self.price_recommended = self.product.price
            elif hasattr(self, 'line_order'):
                if not self.description:
                    self.description = self.line_order.product
                self.price_recommended = self.line_order.price

        if hasattr(self, 'tax') and hasattr(self, 'type_tax'):
            self.tax = self.type_tax.tax
        """
        si al guardar una linea asociada a un documento bloqueado (lock==True), duplicar el documento en una nueva versión
        """
        self.update_total(force_save=False)
        if 'force_save' in kwards:
            kwards.pop('force_save')
        return super(GenLineProduct, self).save(*args, **kwards)

    def __save__(self, args, kwargs, **conditional):
        if hasattr(self, 'product'):
            conditional["product"] = self.product
        if hasattr(self, 'line_order'):
            conditional["line_order"] = self.line_order
        if hasattr(self, 'basket'):
            conditional["basket"] = self.basket

        return super(GenLineProduct, self).__save__(args, kwargs, **conditional)

    @staticmethod
    def create_order_from_budget_all(order):
        lines_budget = order.budget.line_basket_sales.all()
        for lb in lines_budget:
            lo = SalesLineOrder()
            lo.order = order
            lo.line_budget = lb
            lo.product = lb.product
            lo.quantity = lb.quantity
            lo.notes = lb.notes
            lo.price_recommended = lb.price_recommended
            lo.description = lb.description
            lo.discount = lb.discount
            lo.price = lb.price
            lo.tax = lb.tax
            lo.save()

        order.budget.role = ROLE_BASKET_BUDGET
        order.budget.save()

        return lines_budget.count() == order.line_order_sales.all().count()

    @staticmethod
    def create_order_from_budget(pk, list_lines):
        MODEL_SOURCE = SalesBasket
        MODEL_FINAL = SalesOrder
        MODEL_LINE_SOURCE = SalesLineBasket
        MODEL_LINE_FINAL = SalesLineOrder
        url_reverse = 'CDNX_invoicing_ordersaless_list'
        # type_doc
        related_line = 'line_budget'
        related_object = 'order'
        msg_error_relation = _("Hay lineas asignadas a pedidos")
        msg_error_not_found = _('Budget not found')

        # duplicamos el presupuesto si el numero de lineas es diferente
        # relacionando el pedido a este nuevo presupuesto
        if list_lines and len(list_lines) != MODEL_LINE_SOURCE.objects.filter(basket=pk).count():
            budget = MODEL_SOURCE.objects.get(pk=pk)
            # el presupuesto tiene que estar firmado para poder generar el pedido
            if not budget.signed:
                context = {}
                context['error'] = _("Unsigned budget")
                return context
            else:
                new_budget = budget.duplicate(MODEL_LINE_SOURCE, list_lines)
                pk = new_budget.pk
                list_lines = [x[0] for x in MODEL_LINE_SOURCE.objects.filter(basket=pk).values_list('pk')]

        return GenLineProduct.create_document_from_another(pk, list_lines,
            MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
            url_reverse, related_line, related_object,
            msg_error_relation, msg_error_not_found, True)

    @staticmethod
    def create_albaran_automatic(pk, list_lines):
        """
        creamos de forma automatica el albaran
        """
        line_bd = SalesLineAlbaran.objects.filter(line_order__pk__in=list_lines).values_list('line_order__pk')
        if line_bd.count() == 0 or len(list_lines) != len(line_bd[0]):
            # solo aquellas lineas de pedidos que no estan ya albarandas
            if line_bd.count() != 0:
                for x in line_bd[0]:
                    list_lines.pop(list_lines.index(x))

            GenLineProduct.create_albaran_from_order(pk, list_lines)

    @staticmethod
    def create_albaran_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesAlbaran
        MODEL_LINE_SOURCE = SalesLineOrder
        MODEL_LINE_FINAL = SalesLineAlbaran
        url_reverse = 'CDNX_invoicing_albaransaless_list'
        # type_doc
        related_line = 'line_order'
        related_object = 'albaran'
        msg_error_relation = _("Hay lineas asignadas a albaranes")
        msg_error_not_found = _('Order not found')

        return GenLineProduct.create_document_from_another(pk, list_lines,
            MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
            url_reverse, related_line, related_object,
            msg_error_relation, msg_error_not_found, False)

    @staticmethod
    def create_ticket_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesTicket
        MODEL_LINE_SOURCE = SalesLineOrder
        MODEL_LINE_FINAL = SalesLineTicket
        url_reverse = 'CDNX_invoicing_ticketsaless_list'
        # type_doc
        related_line = 'line_order'
        related_object = 'ticket'
        msg_error_relation = _("Hay lineas asignadas a ticket")
        msg_error_not_found = _('Order not found')

        with transaction.atomic():
            GenLineProduct.create_albaran_automatic(pk, list_lines)
            return GenLineProduct.create_document_from_another(pk, list_lines,
                MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
                url_reverse, related_line, related_object,
                msg_error_relation, msg_error_not_found, False)

    @staticmethod
    def create_invoice_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesInvoice
        MODEL_LINE_SOURCE = SalesLineOrder
        MODEL_LINE_FINAL = SalesLineInvoice
        url_reverse = 'CDNX_invoicing_invoicesaless_list'
        # type_doc
        related_line = 'line_order'
        related_object = 'invoice'
        msg_error_relation = _("Hay lineas asignadas a facturas")
        msg_error_not_found = _('Order not found')

        with transaction.atomic():
            GenLineProduct.create_albaran_automatic(pk, list_lines)
            return GenLineProduct.create_document_from_another(pk, list_lines,
                MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
                url_reverse, related_line, related_object,
                msg_error_relation, msg_error_not_found, False)

    @staticmethod
    def create_ticket_from_albaran(pk, list_lines):
        """
        la pk y list_lines son de albaranes, necesitamos la info de las lineas de pedidos
        """
        context = {}
        if list_lines:
            new_list_lines = [x[0] for x in SalesLineAlbaran.objects.values_list('line_order__pk').filter(
                pk__in=[int(x) for x in list_lines]
            ).exclude(invoiced=True)]
            if new_list_lines:
                lo = SalesLineOrder.objects.values_list('order__pk').filter(pk__in=new_list_lines)[:1]
                if lo and lo[0] and lo[0][0]:
                    new_pk = lo[0][0]
                    context = GenLineProduct.create_ticket_from_order(new_pk, new_list_lines)
                    if 'error' not in context or not context['error']:
                        SalesLineAlbaran.objects.filter(
                            pk__in=[int(x) for x in list_lines]
                        ).exclude(invoiced=True).update(invoiced=True)
                    return context
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context

    @staticmethod
    def create_invoice_from_albaran(pk, list_lines):
        """
        la pk y list_lines son de albaranes, necesitamos la info de las lineas de pedidos
        """
        context = {}
        if list_lines:
            new_list_lines = [x[0] for x in SalesLineAlbaran.objects.values_list('line_order__pk').filter(
                pk__in=[int(x) for x in list_lines]
            ).exclude(invoiced=True)]
            if new_list_lines:
                lo = SalesLineOrder.objects.values_list('order__pk').filter(pk__in=new_list_lines)[:1]
                if lo and lo[0] and lo[0][0]:
                    new_pk = lo[0][0]
                    context = GenLineProduct.create_invoice_from_order(new_pk, new_list_lines)
                    if 'error' not in context or not context['error']:
                        SalesLineAlbaran.objects.filter(
                            pk__in=[int(x) for x in list_lines]
                        ).exclude(invoiced=True).update(invoiced=True)
                    return context
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context

    @staticmethod
    def create_invoice_from_ticket(pk, list_lines):
        """
        la pk y list_lines son de ticket, necesitamos la info de las lineas de pedidos
        """
        context = {}
        if list_lines:
            new_list_lines = [x[0] for x in SalesLineTicket.objects.values_list('line_order__pk').filter(pk__in=[int(x) for x in list_lines])]
            if new_list_lines:
                lo = SalesLineOrder.objects.values_list('order__pk').filter(pk__in=new_list_lines)[:1]
                if lo and lo[0] and lo[0][0]:
                    new_pk = lo[0][0]
                    return GenLineProduct.create_invoice_from_order(new_pk, new_list_lines)
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context


# facturas rectificativas
class GenInvoiceRectification(GenVersion):  # META: Abstract class
    class Meta(GenVersion.Meta):
        abstract = True

    def __unicode__(self):
        return u"Rct-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        return fields


# reserva de productos
class SalesReservedProduct(CodenerixModel):
    customer = models.ForeignKey(Customer, related_name='reservedproduct_sales', verbose_name=_("Customer"))
    product = models.ForeignKey(ProductFinal, related_name='reservedproduct_sales', verbose_name=_("Product"))
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.customer))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _("Customer")))
        fields.append(('product', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('created', _("Created")))
        return fields


# nueva cesta de la compra
class SalesBasket(GenVersion):
    customer = models.ForeignKey(Customer, related_name='basket_sales', verbose_name=_("Customer"))
    pos_slot = models.ForeignKey(POSSlot, related_name='basket_sales', verbose_name=_("Point of Sales"), null=True)
    role = models.CharField(_("Role basket"), max_length=2, choices=ROLE_BASKET, blank=False, null=False, default=ROLE_BASKET_SHOPPINGCART)
    signed = models.BooleanField(_("Signed"), blank=False, default=False)
    public = models.BooleanField(_("Public"), blank=False, default=False)
    payment = models.ManyToManyField(PaymentRequest, verbose_name=_(u"Payment Request"), blank=True, related_name='basket_sales')
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    address_delivery = models.ForeignKey(Address, related_name='order_sales_delivery', verbose_name=_("Address delivery"), blank=True, null=True)
    address_invoice = models.ForeignKey(Address, related_name='order_sales_invoice', verbose_name=_("Address invoice"), blank=True, null=True)
    expiration_date = models.DateTimeField(_("Expiration date"), blank=True, null=True, editable=False)
    haulier = models.ForeignKey(Haulier, related_name='basket_sales', verbose_name=_("Haulier"), blank=True, null=True)
    
    def __unicode__(self):
        return u"Order-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('name', _('Name')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('role', _('Role basket')))
        fields.append(('signed', _('Signed')))
        fields.append(('public', _('Public')))
        fields.append(('address_delivery', _('Address delivery')))
        fields.append(('address_invoice', _('Address invoice')))
        fields.append(('haulier', _('Haulier')))
        fields.append(('subtotal', _('Subtotal')))
        fields.append(('discounts', _('Discounts')))
        fields.append(('taxes', _('Taxes')))
        fields.append(('total', _('Total')))
        return fields

    def pass_to_budget(self, lines=None):
        if self.role != ROLE_BASKET_BUDGET and lines and self.line_basket_sales.count() != len(lines):
            # duplicate object
            lines = [int(x) for x in lines]
            obj = copy.copy(self)
            obj.pk = None
            obj.role = ROLE_BASKET_BUDGET
            obj.save()
            for line in self.line_basket_sales.filter(pk__in=lines):
                new_line = copy.copy(line)
                new_line.pk = None  # reset
                new_line.basket = obj  # relation to new object
                new_line.save()
            return obj
        else:
            self.role = ROLE_BASKET_BUDGET
            self.save()
            return self

    def pass_to_shoppingcart(self):
        self.role = ROLE_BASKET_SHOPPINGCART
        self.save()
        return self

    def pass_to_order(self, payment_request=None):
        if not hasattr(self, 'order_sales'):
            with transaction.atomic():
                if type(payment_request) == int:
                    payment_request = PaymentRequest.objects.get(pk=payment_request)

                order = SalesOrder()
                order.customer = self.customer
                order.budget = self
                order.payment = payment_request
                order.save()

                for line in self.line_basket_sales.all():
                    lorder = SalesLineOrder()
                    lorder.order = order
                    lorder.line_budget = line
                    lorder.product = line.product
                    lorder.price_recommended = line.price_recommended
                    lorder.description = line.description
                    lorder.discount = line.discount
                    lorder.price = line.price
                    lorder.tax = line.tax
                    lorder.quantity = line.quantity
                    lorder.save()
                
            self.lock = True
            self.role = ROLE_BASKET_BUDGET
            self.expiration_date = None
            self.save()

    def lock_delete(self, request=None):
        # Solo se puede eliminar si:
        # * el pedido no tiene un pago realizado
        # * no se ha generado un albaran, ticket o factura relaciondos a una linea

        if hasattr(self, 'order_sales') and self.order_sales:
            if self.order_sales.payment is not None:
                return _('Cannot delete, it is related to payment')
            if self.order_sales.line_order_sales.count() != 0:
                lines_order = [x['pk'] for x in self.order_sales.line_order_sales.all().values('pk')]
                if SalesLineAlbaran.objects.filter(line_order__in=lines_order).count() != 0:
                    return _('Cannot delete, it is related to albaran')
                if SalesLineTicket.objects.filter(line_order__in=lines_order).count() != 0:
                    return _('Cannot delete, it is related to tickets')
                if SalesLineInvoice.objects.filter(line_order__in=lines_order).count() != 0:
                    return _('Cannot delete, it is related to invoices')

        return super(SalesBasket, self).lock_delete()

    def calculate_price_doc_complete(self):
        return super(SalesBasket, self).calculate_price_doc_complete(self.line_basket_sales.filter(removed=False))
        
    def list_tickets(self):
        # retorna todos los tickets en los que hay lineas de la cesta
        return SalesTicket.objects.filter(line_ticket_sales__line_order__order__budget=self).distinct()


# nueva linea de la cesta de la compra
class SalesLineBasket(GenLineProduct):
    basket = models.ForeignKey(SalesBasket, related_name='line_basket_sales', verbose_name=_("Basket"))
    product = models.ForeignKey(ProductFinal, related_name='line_basket_sales', verbose_name=_("Product"))

    def __fields__(self, info):
        fields = super(SalesLineBasket, self).__fields__(info)
        fields.insert(0, ('basket', _("Basket")))
        fields.append(('line_basket_option_sales', _('Options')))
        return fields

    def lock_delete(self, request=None):
        # Solo se puede eliminar si no se ha generado un albaran, ticket o factura apartir de ella
        if hasattr(self.basket, 'order_sales') and hasattr(self, 'line_order_sales'):
            if self.line_order_sales.line_albaran_sales.count() != 0:
                return _("Cannot delete line, it is related to albaran")
            elif self.line_order_sales.line_ticket_sales.count() != 0:
                return _("Cannot delete line, it is related to tickets")
            elif self.line_order_sales.line_invoice_sales.count() != 0:
                return _("Cannot delete line, it is related to invoices")

        return super(SalesLineBasket, self).lock_delete(request)

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.basket.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if 'standard_save' in kwargs:
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.basket.update_totales()
                return result
            else:
                return self.__save__(args, kwargs)

    def remove_options(self):
        self.line_basket_option_sales.all().delete()

    def set_options(self, options):
        """
        options = [{
            'product_option': instance of ProductFinalOption,
            'product_final': instance of ProductFinal,
            'quantity': Float
        }, ]
        """
        with transaction.atomic():
            for option in options:
                opt = self.line_basket_option_sales.filter(
                    product_option=option['product_option']
                ).first()
                if opt:  # edit
                    change = False
                    if opt.quantity != option['quantity']:
                        opt.quantity = option['quantity']
                        change = True
                    if opt.product_final != option['product_final']:
                        opt.product_final = option['product_final']
                        change = True
                    if change:
                        opt.save()
                else:  # new
                    opt = SalesLineBasketOption()
                    # raise Exception(self.pk, self.__dict__, self)
                    # raise Exception(self.pk)
                    opt.line_budget = SalesLineBasket.objects.get(pk=self.pk)
                    opt.product_option = option['product_option']
                    opt.product_final = option['product_final']
                    opt.quantity = option['quantity']
                    opt.save()


class SalesLineBasketOption(CodenerixModel):
    line_budget = models.ForeignKey(SalesLineBasket, related_name='line_basket_option_sales', verbose_name=_("Line budget"))
    product_option = models.ForeignKey(ProductFinalOption, related_name='line_basket_option_sales', verbose_name=_("Option"))
    product_final = models.ForeignKey(ProductFinal, related_name='line_basket_option_sales', verbose_name=_("Product"))
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{} - {}".format(self.product_option, self.product_final)

    def __fields__(self, info):
        fields = []
        fields.append(('line_budget', _('Line budget')))
        fields.append(('product_option', _('Product option')))
        fields.append(('product_final', _('Product final')))
        fields.append(('quantity', _('Quantity')))
        return fields


# pedidos
class SalesOrder(GenVersion):
    budget = models.OneToOneField(SalesBasket, related_name='order_sales', verbose_name=_("Budget"), null=True, blank=True)
    customer = models.ForeignKey(Customer, related_name='order_sales', verbose_name=_("Customer"))
    storage = models.ForeignKey(Storage, related_name='order_sales', verbose_name=_("Storage"), blank=True, null=True)
    payment = models.ForeignKey(PaymentRequest, related_name='order_sales', verbose_name=_(u"Payment Request"), blank=True, null=True)
    number_tracking = models.CharField(_("Number of tracking"), max_length=128, blank=True, null=True)
    status_order = models.CharField(_("Status"), max_length=2, choices=STATUS_ORDER, blank=False, null=False, default='PE')
    payment_detail = models.CharField(_("Payment detail"), max_length=3, choices=PAYMENT_DETAILS, blank=True, null=True)
    source = models.CharField(_("Source of purchase"), max_length=250, blank=True, null=True)

    def __unicode__(self):
        return u"Order-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('storage', _('Storage')))
        fields.append(('status_order', _('Status')))
        fields.append(('payment_detail', _('Payment detail')))
        fields.append(('source', _('Source of purchase')))
        fields.append(('number_tracking', _('Number of tracking')))
        fields.append(('budget__address_delivery', _('Address delivery')))
        fields.append(('budget__address_invoice', _('Address invoice')))
        return fields

    def calculate_price_doc(self):
        return self.total
    
    def calculate_price_doc_complete(self):
        return super(SalesOrder, self).calculate_price_doc_complete(self.line_order_sales.filter(removed=False))


# lineas de pedidos
class SalesLineOrder(GenLineProduct):
    order = models.ForeignKey(SalesOrder, related_name='line_order_sales', verbose_name=_("Order"))
    line_budget = models.OneToOneField(SalesLineBasket, related_name='line_order_sales', verbose_name=_("Line budget"), null=True)
    product = models.ForeignKey(ProductFinal, related_name='line_order_sales', verbose_name=_("Product"))

    def __fields__(self, info):
        fields = super(SalesLineOrder, self).__fields__(info)
        fields.insert(0, ('order', _("Order")))
        fields.append(('line_budget', _("Line budget")))
        return fields

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.order.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if 'standard_save' in kwargs:
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.order.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, order=self.order, line_budget=self.line_budget)


class SalesLineOrderOption(CodenerixModel):
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_order_option_sales', verbose_name=_("Line Order"))
    product_option = models.ForeignKey(ProductFinalOption, related_name='line_order_option_sales', verbose_name=_("Option"))
    product_final = models.ForeignKey(ProductFinal, related_name='line_order_option_sales', verbose_name=_("Product"))
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"Order-{}".format(smart_text(self.code))

    def __fields__(self, info):
        fields = []
        fields.append(('line_order', _('Line order')))
        fields.append(('product_option', _('Product option')))
        fields.append(('product_final', _('Product final')))
        fields.append(('quantity', _('Quantity')))
        return fields


# albaranes
class SalesAlbaran(GenVersion):
    tax = models.FloatField(_("Tax"), blank=False, null=False, default=0)
    summary_delivery = models.TextField(_("Address delivery"), max_length=256, blank=True, null=True)

    def __unicode__(self):
        return u"Albaran-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('tax', _('Tax')))
        fields.append(('summary_delivery', _('Address delivery')))
        return fields

    def calculate_price_doc(self):
        return self.total
    
    def calculate_price_doc_complete(self):
        return super(SalesAlbaran, self).calculate_price_doc_complete(self.line_albaran_sales.filter(removed=False))


# lineas de albaranes
class SalesLineAlbaran(GenLineProductBasic):
    albaran = models.ForeignKey(SalesAlbaran, related_name='line_albaran_sales', verbose_name=_("Albaran"))
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_albaran_sales', verbose_name=_("Line orders"), null=True)
    invoiced = models.BooleanField(_("Invoiced"), blank=False, default=False)

    def __unicode__(self):
        return u"{} - {}".format(smart_text(self.line_order.product), smart_text(self.quantity))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('line_order__order', _("Order")))
        fields.append(('line_order__product', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('invoiced', _("Invoiced")))
        return fields

    def update_total(self, force_save=True):
        self.subtotal = self.line_order.price * self.quantity
        self.taxes = (self.subtotal * self.tax / 100.0)
        self.discounts = (self.subtotal * self.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes
        if force_save:
            self.save()

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.albaran.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if 'standard_save' in kwargs:
                kwargs.pop('standard_save')
                self.update_total(force_save=False)
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.albaran.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, albaran=self.albaran, line_order=self.line_order)

    def calculate_total(self):
        return self.total


# ticket y facturas son lo mismo con un check de "tengo datos del customere"
class SalesTicket(GenVersion):
    customer = models.ForeignKey(Customer, related_name='ticket_sales', verbose_name=_("Customer"))

    def __unicode__(self):
        return u"Ticket-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('line_ticket_sales__line_order__product', _('Products')))
        fields.append(('date', _('Date')))
        fields.append(('total', _('Total')))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self):
        return super(SalesTicket, self).calculate_price_doc_complete(self.line_ticket_sales.filter(removed=False))


class SalesLineTicket(GenLineProduct):
    ticket = models.ForeignKey(SalesTicket, related_name='line_ticket_sales', verbose_name=_("Ticket"))
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_ticket_sales', verbose_name=_("Line order"), null=True)

    def __fields__(self, info):
        fields = super(SalesLineTicket, self).__fields__(info)
        fields.insert(0, ('ticket', _("Ticket")))
        fields.append(('line_order', _("Line order")))
        return fields

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.ticket.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if 'standard_save' in kwargs:
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.ticket.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, ticket=self.ticket, line_order=self.line_order)


# puede haber facturas o tickets rectificativos
# factura rectificativa
class SalesTicketRectification(GenInvoiceRectification):
    ticket = models.ForeignKey(SalesTicket, related_name='ticketrectification_sales', verbose_name=_("Ticket"), null=True)

    def __fields__(self, info):
        fields = super(SalesTicketRectification, self).__fields__(info)
        fields.insert(0, ('ticket', _("Ticket")))
        fields.insert(0, ('ticket__customer', _("Customer")))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self):
        return super(SalesTicketRectification, self).calculate_price_doc_complete(self.line_ticketrectification_sales.filter(removed=False))


class SalesLineTicketRectification(GenLineProductBasic):
    ticket_rectification = models.ForeignKey(SalesTicketRectification, related_name='line_ticketrectification_sales', verbose_name=_("Ticket rectification"))
    line_ticket = models.ForeignKey(SalesLineTicket, related_name='line_ticketrectification_sales', verbose_name=_("Line ticket"))

    def __fields__(self, info):
        fields = []
        fields.append(('ticket_rectification', _("Ticket rectification")))
        fields.append(('line_ticket', _("Line ticket")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def update_total(self, force_save=True):
        self.subtotal = self.line_ticket.price * self.quantity
        self.taxes = (self.subtotal * self.tax / 100.0)
        self.discounts = (self.subtotal * self.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes
        if force_save:
            self.save()

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.ticket_rectification.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if 'standard_save' in kwargs:
                kwargs.pop('standard_save')
                self.update_total(force_save=False)
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.create_ticket_from_order.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, ticket_rectification=self.ticket_rectification, line_ticket=self.line_ticket)

    def calculate_total(self):
        return self.total


# facturas
# una factura puede contener varios ticket o albaranes
class SalesInvoice(GenVersion):
    customer = models.ForeignKey(Customer, related_name='invoice_sales', verbose_name=_("Customer"))
    summary_invoice = models.TextField(_("Address invoice"), max_length=256, blank=True, null=True)
    billing_series = models.ForeignKey(BillingSeries, related_name='invoice_sales', verbose_name='Billing series')

    def __unicode__(self):
        return u"Invoice-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('billing_series', _('Billing series')))
        fields.append(('summary_invoice', _('Address invoice')))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self):
        return super(SalesInvoice, self).calculate_price_doc_complete(self.line_invoice_sales.filter(removed=False))


class SalesLineInvoice(GenLineProduct):
    invoice = models.ForeignKey(SalesInvoice, related_name='line_invoice_sales', verbose_name=_("Invoice"))
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_invoice_sales', verbose_name=_("Line order"), null=True)

    def __fields__(self, info):
        fields = super(SalesLineInvoice, self).__fields__(info)
        fields.insert(0, ('invoice', _("Ticket invoices")))
        fields.append(('line_order', _("Line order")))
        return fields

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.invoice.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if 'standard_save' in kwargs:
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.invoice.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, invoice=self.invoice, line_order=self.line_order)


# factura rectificativa
class SalesInvoiceRectification(GenInvoiceRectification):
    invoice = models.ForeignKey(SalesInvoice, related_name='invoicerectification_sales', verbose_name=_("Invoice"), null=True)

    def __fields__(self, info):
        fields = super(SalesInvoiceRectification, self).__fields__(info)
        fields.insert(0, ('invoice', _("Invoices")))
        fields.insert(0, ('invoice__customer', _("Customer")))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self):
        return super(SalesInvoiceRectification, self).calculate_price_doc_complete(self.line_invoicerectification_sales.filter(removed=False))


class SalesLineInvoiceRectification(GenLineProductBasic):
    invoice_rectification = models.ForeignKey(SalesInvoiceRectification, related_name='line_invoicerectification_sales', verbose_name=_("Invoice rectification"))
    line_invoice = models.ForeignKey(SalesLineInvoice, related_name='line_invoicerectification_sales', verbose_name=_("Line invoice"))

    def __fields__(self, info):
        fields = []
        fields.append(('invoice_rectification', _("Invoices rectification")))
        fields.append(('line_invoice', _("Line invoice")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def update_total(self, force_save=True):
        self.subtotal = self.line_invoice.price * self.quantity
        self.taxes = (self.subtotal * self.tax / 100.0)
        self.discounts = (self.subtotal * self.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes
        if force_save:
            self.save()

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.invoice_rectification.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if 'standard_save' in kwargs:
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.update_total(force_save=False)
                self.invoice_rectification.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, invoice_rectification=self.invoice_rectification, line_invoice=self.line_invoice)

    def calculate_total(self):
        return self.total
