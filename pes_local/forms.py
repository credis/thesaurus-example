# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from djrdf.forms import djRdfForm
from pes_local.models import Concept, Tag, Scheme
from formalchemy.ext.rdf import RdfSelectFieldRenderer, Field



###################################
# TODO: deplacer ConceptForm dans pes.thess.form
#       surclasser TagForm pour include les prefLabel, altLabel et hiddenLabel
#################################

class ConceptForm(djRdfForm):
    model = Concept

    def _configure(self, fs):
        desc_size = "100x5"

        allConcept = map(lambda x: (x.prefLabels[0].name, x), Concept.objects.all())
        allLabel = map(lambda x: (x.name, x), Tag.objects.all())
        allScheme = map(lambda x: (x.name, x), Scheme.ClassInstances())


        fs.append(Field('prefLabels'))
        fs.append(Field('note'))
        fs.append(Field('definition'))
        fs.append(Field('example'))
        fs.append(Field('offers'))
        fs.append(Field('notation'))
        fs.append(Field('narrower'))
        fs.append(Field('broader'))
        fs.append(Field('related'))
        fs.append(Field('hiddenLabels'))
        fs.append(Field('altLabels'))
        fs.append(Field('inScheme'))
        fs.append(Field('topConceptOf'))




        fs.configure(include=[
            fs.prefLabels.set(multiple=True, options=allLabel),
            fs.note.textarea(size=desc_size),
            fs.definition.textarea(size=desc_size),
            fs.example.textarea(size=desc_size),
            fs.notation.textarea(size=desc_size),

            fs.narrower.set(multiple=True, options=allConcept),
            fs.broader.set(multiple=True, options=allConcept),
            fs.related.set(multiple=True, options=allConcept),
            fs.hiddenLabels.set(multiple=True, options=allLabel),
            fs.altLabels.set(multiple=True, options=allLabel),
            fs.inScheme.set(multiple=True, options=allScheme),
            fs.topConceptOf.set(multiple=True, options=allScheme),


        ])




        fs.inScheme._renderer = RdfSelectFieldRenderer
        fs.topConceptOf._renderer = RdfSelectFieldRenderer

        fs.hiddenLabels._renderer = RdfSelectFieldRenderer
        fs.prefLabels._renderer = RdfSelectFieldRenderer
        fs.altLabels._renderer = RdfSelectFieldRenderer

        fs.broader._renderer = RdfSelectFieldRenderer
        fs.narrower._renderer = RdfSelectFieldRenderer
        fs.related._renderer = RdfSelectFieldRenderer

        return fs



