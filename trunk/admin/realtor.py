# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin 
from django.contrib.auth.models import User 
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from options import RealEstateAppRevertInlineModelAdmin
from real_estate_app.models import Realtor
from real_estate_app.admin.forms import RealtorAdminForm, UserAdminForm
from real_estate_app.conf.settings import MEDIA_PREFIX

LANGUAGE_CODE=getattr(settings,'LANGUAGE_CODE')

class RealtorInlineAdmin(admin.StackedInline):
	model = Realtor
	extra = 1
	formset = RealtorAdminForm
	template = 'admin/real_estate_app/%s/edit_inline/stacked-realtor.html' % LANGUAGE_CODE

	if LANGUAGE_CODE in ('pt_BR','pt-br'):
		from django.contrib.localflavor.br import forms as br_forms
		from real_estate_app.localflavor.br.admin.forms.realtor import realtor_br_custom_fields

		fields = realtor_br_custom_fields

		cpf = br_forms.BRCPFField(
							label=u'CPF',
							required=False
		)

		cnpj = br_forms.BRCNPJField(
							label=u'CNPJ',
							required=False
		)
	
class RealtorAdmin(RealEstateAppRevertInlineModelAdmin):

	revert_inlines = [RealtorInlineAdmin,]
	revert_model = User
	revert_form = UserAdminForm

	class Media:

		if LANGUAGE_CODE == 'pt-br':
			css = {
				'all':(
					MEDIA_PREFIX+"css/tabs.css",
				)
			}

			js = (
				MEDIA_PREFIX+"js/locale/pt_BR/realtor.js",
			)

admin.site.register(Realtor, RealtorAdmin)