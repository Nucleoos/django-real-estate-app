import operator
from django.http import HttpResponse, Http404
from django.core.exceptions import ImproperlyConfigured
from django.utils import simplejson
from django.conf import settings 
from real_estate_app.conf.settings import REAL_ESTATE_APP_AJAX_SEARCH, MEDIA_PREFIX


def radomstring(max=10):
	import random
	string='abcdefghijklmnopqrstuvxywz1234567890'
	a=''
	for i in random.sample(string,max):
		a+=i
	return a


def make_dv(num,max_num=11,b_start=1):
	dv1=0
	for ct, n in enumerate(num,start=b_start):
		dv1+=int(n)*ct

	dv1=dv1%11

	if dv1 == 10: dv1=0;

	num=num+str(dv1)
	if len(num) != max_num:
		num=make_dv(num,max_num=max_num,b_start=0)
	
	return num or None

class AutoCompleteObject(object):

	def __init__(self,model):

		self.model=model
		self.module_name=self.model._meta.module_name
		self.image_fields=[]
		try:
			self.fields_search=REAL_ESTATE_APP_AJAX_SEARCH[self.module_name]['search_fields']
			self.return_values=REAL_ESTATE_APP_AJAX_SEARCH[self.module_name]['return_values']
		except KeyError:
			raise ImproperlyConfigured("settings.REAL_ESTATE_APP_AJAX_SEARCH not configured correctly for %s." % self.module_name)


	def getSpecialField(self,models,fields=''):
		from django.core.files.images import ImageFile
		from django.db.models.query import QuerySet

		if isinstance(models,QuerySet) and isinstance(fields,(list,tuple)) :
			from itertools import product 
			return [field for model,field in product(models,fields) 
			        if isinstance(getattr(model,field,None),ImageFile) and not field in ('pk','id')]

		return []

	def filter(self,value='',**kwargs):
		from django.db.models import Q


		queryset = self.model.objects.all()

		if self.fields_search and value:
			query=[Q(**{'%s__icontains' %field: value}) for field in self.fields_search]
			queryset=queryset.filter(reduce(operator.or_,query))

		if kwargs and not value:
			queryset=queryset.filter(**kwargs)

		if isinstance(self.return_values,(list,tuple)) and self.return_values:
			self.image_fields=self.getSpecialField(queryset,self.return_values)
			queryset=queryset.values(*self.return_values)

		return queryset

	def render(self,value='',**kwargs):
		from django.utils.safestring import mark_safe
		from django.template.loader import render_to_string
		return [{
					'pk':model['pk'],
					'real_value':' '.join([model[f] for f in self.return_values if not (f in ('pk','id') or f in self.image_fields)]),
					'value': mark_safe(render_to_string(
										  				('real_estate_app/autocompleteselectmultiple_response_ajax.html',
									   	   				'admin/real_estate_app/autocompleteselectmultiple_response_ajax.html'
									   	   				),
									   	   				# Problema com ordenacao do dict
									   	 				{
									   	 					'model':model,
									   	 					'image_fields':self.image_fields,
									   	 					'MEDIA_PREFIX':MEDIA_PREFIX,
									   	 					'MEDIA_URL':settings.MEDIA_URL
									   	 				}
							   			)
					),
				} for model in self.filter(value,**kwargs)]

							

	def getFieldsShow(self):
		return self.return_values