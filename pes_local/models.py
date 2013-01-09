# -*- coding:utf-8 -*-
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from djrdf.import_rdf.models import EntrySite
from pes.tag.models import Tag as BaseTag
from pes.thess.models import Concept as BaseConcept
from pes.thess.models import Scheme as BaseScheme
from pes.agenda.models import Event as BaseEvent
from pes.article.models import Article as BaseArticle
from pes.exchange.models import Product as BaseProduct
from pes.exchange.models import Exchange as BaseExchange
from pes.org.models import Organization as BaseOrganization
from pes.org.models import Person as BasePerson

import time
from rdfalchemy.orm import mapper

# Becareful for rdfalchemy mapper, the rdf_type attribut HAS to be set here


class Person(BasePerson):
    rdf_type = settings.NS.person.Person  # on peut aussi bien ecrire rdf_type = FOAF.Person



class Organization(BaseOrganization):
    rdf_type = settings.NS.org.Organization


class Exchange(BaseExchange):
    rdf_type = settings.NS.ess.Exchange


class Product(BaseProduct):
    rdf_type = settings.NS.schema.Product


class Event(BaseEvent):
    rdf_type = settings.NS.vcal.Vevent


class Article(BaseArticle):
    rdf_type = settings.NS.dcmi.Text


class Concept(BaseConcept):
    rdf_type = settings.NS.skos.Concept

    # generic method,'pred' is a string denoting 'prefLabels', 'altLabels'
    # or 'hiddenLabels'
    def linkToLabel(self, pred, label):
        getattr(self, pred, []).append(label)
        self.db.add((self, self.__class__._getdescriptor(pred).pred, label))
        # et ajouter d'autre triplets dans le store
        # label ess:labelFor self context si label rdf:type skosxl:Label context
        for es in EntrySite.objects.all():
            ctx = es.defaultCtxName
            # check if label is in context ctx
            in_ctx = len(list(self.db.triples((label, settings.NS.rdf.type, label.rdf_type), ctx))) == 1
            if in_ctx:
                self.db.add((label, settings.NS.ess.labelFor, self), context=ctx)
                schemes = list(self.db.objects(label, settings.NS.skos.inScheme, context=ctx))
                for s in schemes:
                    self.db.add((self, settings.NS.inScheme, s), context=ctx)

    @models.permalink
    def get_absolute_url(self):
        return ('pes.thess.views.detailConcept', [str(self.id)])




class Scheme(BaseScheme):
    rdf_type = settings.NS.skos.ConceptScheme


class Tag(BaseTag):
    rdf_type = settings.NS.skosxl.Label

    created_by = models.CharField(max_length=100, null=True)
    edited_by = models.CharField(max_length=100, null=True)
    isNew = models.BooleanField(default=True)

    def is_prefLabel_of(self):
        return map(Concept, list(self.db.subjects(settings.NS.skosxl.prefLabel, self)))

    def is_altLabel_of(self):
        return map(Concept, list(self.db.subjects(settings.NS.skosxl.altLabel, self)))

    def is_hiddenLabel_of(self):
        return map(Concept, list(self.db.subjects(settings.NS.skosxl.hidenLabel, self)))

    def isLinkToConcept(self):
        if self.isNew:
            return None
        else:
            concepts = self.db.objects(settings.NS.skosxl.prefLabel, self)
            if concepts == []:
                concepts = self.db.objects(settings.NS.skosxl.altLabel, self)
                if concepts == []:
                    concepts = self.db.objects(settings.NS.skosxl.hiddenLabel, self)
            if concepts == []:
                # should not happend ....
                raise Exception(_("Calling isLinkToConcept shows many concepts links to the label %s" % self))
            else:
                return Concept(concepts[0])

    def create_concept(self):
        uri = Concept.create_uri()
        concept = Concept(uri=uri)
        concept.save()
        # The rdf_type triple is mandatory
        concept.db.add((concept, settings.NS.rdf.type, Concept.rdf_type))
        concept.linkToLabel('prefLabels', self)
        concept.note = [
            _(u" Created from label '%s'" % self.name),
            _(u" Created date : %s" % time.strftime('%d/%m/%y', time.localtime()))
        ]
        concept.save()
        self.isNew = False
        self.save()
        return concept

    class Meta:
        verbose_name = _(u'label')
        verbose_name_plural = _(u'labels')




# This MANDATORY to link attributes trought the rdfSubject instances
mapper()


