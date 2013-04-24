from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic.create_update import redirect, apply_extra_context, get_model_and_form_class
from django.contrib.auth.views import redirect_to_login
from django.utils.translation import ugettext
from django.contrib import messages

from django.forms.models import ModelFormMetaclass, ModelForm
from django.views.generic import GenericViewError

def create_object(request, model=None, template_name=None,
                  template_loader=loader, extra_context=None, post_save_redirect=None,
                  login_required=False, context_processors=None, form_class=None , 
                  formset_class=None, initial_form={}, initial_formset={}):
    """
    Custom generic object-creation function.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form for the object
    """
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    formset = formset_class
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)

        if form.is_valid() and not formset_class:
            new_object = form.save()
            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return redirect(post_save_redirect, new_object)
        else:
                
            formset = formset_class(request.POST, request.FILES)
            if formset.is_valid() and form.is_valid():
                new_object=form.save()
                # TODO: Better this generic create_object
                obj=formset.save(commit=False)
                obj.visitor_fk=new_object
                formset.save()

                msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                {"verbose_name": model._meta.verbose_name}
                messages.success(request, msg, fail_silently=True)
                return redirect(post_save_redirect, new_object)


    else:
        form = form_class(**initial_form)

        if formset_class:
            formset = formset_class(**initial_formset)


    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
        'formset':formset
    }, context_processors)
    apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))