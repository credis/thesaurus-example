# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes_local.models import Tag, Concept
from pes_local.forms import ConceptForm
from pes.tag.forms import TagForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from haystack.views import FacetedSearchView
from django.contrib.sites.models import Site
from pes.utils import get_ordererd_list
from django.contrib.auth.decorators import login_required




def editTag(request, l_id):
    try:
        tag = Tag.objects.get(id=l_id)
    except Tag.DoesNotExist:
        raise Http404
    form = TagForm().form(tag)
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        # As we have some select=multiple and rebind uses the .items() methode
        form.rebind(tag, data=request.POST.lists())
        if form.validate():
            form.sync()
            # import pdb; pdb.set_trace()
            tag.save()
            return render_to_response('tag/edit.html', {'tag': tag, 'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('errorForm.html', {'name': tag._meta.verbose_name, 'fields': form.errors.keys()})
    return render_to_response('tag/edit.html', {'tag': tag, 'form': form}, context_instance=RequestContext(request))




# @login_required
def newTag(request):
    tag = Tag()
    form = TagForm().form(tag)
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        # As we have some select=multiple and rebind uses the .items() methode
        form.rebind(tag, data=request.POST.lists())
        if form.validate():
            uri = Tag.create_uri(form.name.value)
            try:
                tag = Tag.objects.get(uri=uri)
            except Tag.DoesNotExist:
                form.sync(uri)
            return render_to_response('tag/new.html', {'tag': tag, 'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('errorForm.html', {'name': tag._meta.verbose_name, 'fields': form.errors.keys()})
    return render_to_response('tag/new.html', {'tag': tag, 'form': form}, context_instance=RequestContext(request))



def newConcept(request, tag_id=None):
    concept = None
    if not tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            raise Http404
        concept = tag.create_concept()
    if not concept:
        concept = Concept()
    form = ConceptForm().form(concept)
    if request.method == 'POST':
        form.rebind(concept, data=request.POST.lists())
        if form.validate():
            if not concept.uri:
                uri = Concept.create_uri()
                form.sync(uri)
            else:
                form.sync()
            return render_to_response('concept/new.html', {'concept': concept, 'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('errorForm.html', {'name': concept._meta.verbose_name, 'fields': form.errors.keys()})
    return render_to_response('concept/new.html', {'concept': concept, 'form': form}, context_instance=RequestContext(request))



def editConcept(request, l_id):
    try:
        concept = Concept.objects.get(id=l_id)
    except Concept.DoesNotExist:
        raise Http404
    form = TagForm().form(concept)
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        # As we have some select=multiple and rebind uses the .items() methode
        form.rebind(concept, data=request.POST.lists())
        if form.validate():
            form.sync()
            # import pdb; pdb.set_trace()
            concept.save()
            return render_to_response('concept/edit.html', {'concept': concept, 'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('errorForm.html', {'name': concept._meta.verbose_name, 'fields': form.errors.keys()})
    return render_to_response('concept/edit.html', {'concept': concept, 'form': form}, context_instance=RequestContext(request))


# def createConceptFromLabel(request, l_id):
#     try:
#         label = Tag.objects.get(id=l_id)
#     except Tag.DoesNotExist:
#         raise Http404
#     concept = label.create_concept()
#     form = ConceptForm().form(concept)
#     return render_to_response('concept/detail.html', {'concept': concept, 'form': form}, context_instance=RequestContext(request))



class HomeSearchView(FacetedSearchView):

    def __name__(self):
        return "HomeSearchView"

    def extra_context(self):
        context = super(HomeSearchView, self).extra_context()
        context['intro'] = u"%s" % Site.objects.get_current().name
        context['last_tag'] = get_ordererd_list(Tag, 10)     
        context['last_concept'] = get_ordererd_list(Concept, 10) 
        return context

