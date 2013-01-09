# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from haystack.views import  search_view_factory
from pes_local.models import Tag, Concept, Scheme
from pes.forms import PESFacetedSearchForm
from pes_local.views import HomeSearchView
from django.views.generic import ListView



urlpatterns = patterns('',
    url(r'^$', search_view_factory(
        view_class=HomeSearchView,
        template='home.html',
        # searchqueryset=sqs,
        form_class=PESFacetedSearchForm,
        load_all=False
    ), name='haystack_search'),


    url(r'^tag/(\d+)/edit/$', 'pes_local.views.editTag'),
    url(r'^tag/new/$', 'pes_local.views.newTag'),

    url(r'^concept/(\d+)/edit/$', 'pes_local.views.editConcept'),
    url(r'^concept/new/(\d+)/$', 'pes_local.views.newConcept'),
    url(r'^concept/new/$', 'pes_local.views.newConcept'),


    (r'^', include('pes.urls')),

)
