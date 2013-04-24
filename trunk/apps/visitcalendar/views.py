# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import list_detail
from django.views.generic.create_update import update_object
from django.utils.safestring import mark_safe


from real_estate_app.apps.visitcalendar.models import VisitEvent, Visitor
from real_estate_app.apps.visitcalendar.forms import VisitEventForm, VisitorForm
from real_estate_app.apps.visitcalendar.settings import VISITOR_SEARCH_FIELDS
from real_estate_app.apps.propertys.models import Property
from real_estate_app.views.generic import create_object

@requires_csrf_token
def visitcalendar_list_json(request, *args, **kwargs):
	if kwargs.has_key('slug'):
		property=get_object_or_404(Property,slug=kwargs['slug'])
		visitsevents = VisitEvent.objects.filter(property_fk=property)
		events = []
		
		for visitevent in visitsevents:
			events.append(dict(
						title=_('Has visit'),
						start = visitevent.date_visit.strftime('%Y-%m-%d %H:%M:%S'),
						url = visitevent.get_absolute_url()
			))

	else:
		visitsevents = VisitEvent.objects.all()

		events = []
		for visitevent in visitsevents:
			events.append(dict(
						title= _('Has visit: \n %s') % visitevent.property_fk.address,
						start = visitevent.date_visit.strftime('%Y-%m-%d %H:%M:%S'),
						url = visitevent.get_absolute_url()
			))

	return HttpResponse(simplejson.dumps(events),mimetype='application/json')

@requires_csrf_token	
def visitcalendar_list(request, *args, **kwargs):	
	kwargs['queryset'] = VisitEvent.objects.all()
	return list_detail.object_list(request, *args, **kwargs)

@requires_csrf_token
def visitcalendar_list_property_visit(request, *args, **kwargs):
	"""
	A view wrapper around ``django.views.generic.list_detail.object_list`.
	"""
	property=get_object_or_404(Property,slug=kwargs['slug'])
	kwargs['queryset'] = VisitEvent.objects.filter(property_fk=property)
	kwargs.pop('slug')
	kwargs['extra_context']= {'property':property}
	return list_detail.object_list(request, *args, **kwargs)

@requires_csrf_token
def visitcalendar_create_object(request, *args, **kwargs):
	date_visit=request.GET.get('date_visit','')
	property=get_object_or_404(Property,slug=kwargs['slug'])
	kwargs.pop('slug')
	kwargs['form_class']=VisitorForm
	kwargs['formset_class']=VisitEventForm 
	kwargs['initial_formset']={'property_fk':property,'date_visit':date_visit}
	return create_object(request, *args, **kwargs)

@requires_csrf_token
def visitcalendar_update_object(request, *args, **kwargs):
	property=get_object_or_404(Property,slug=kwargs['property_slug'])
	kwargs.pop('property_slug')
	kwargs['form_class']=VisitEventForm
	return update_object(request, *args, **kwargs)

@requires_csrf_token
def visitcalendar_search_visitor(request, *args, **kwargs):
	if 'term' in request.GET:
		try:
			query=VISITOR_SEARCH_FIELDS['fields'][0]+'__icontains'
			q_value={query:request.GET['term']}
			json=serializers.serialize("json",Visitor.objects.filter(**q_value),fields='visitor_first_name')
			return HttpResponse(json,mimetype="text/javascript")
		except:
			raise 