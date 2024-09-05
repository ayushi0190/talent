# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Ontology Properties helper methods
@author <ankits@simplifyvms.com>
"""


class OntologyProperties:
    """
    Different classes which help to create the Ontology JSON
    """

    def __init__(self):
        pass

    def createClass(self, id, type):
        """
        Method to create the JSON for class key
        """
        dict_class = {
            "id": id,
            "type": type
        }
        return dict_class

    def createclassAttribute(self, id, label, attr=False):
        """
         Method to create the JSON for classAttribute Key
        """
        if attr == False:
            dict_class_attribute = {
                "id": id,
                "iri": "http://visualdataweb.org/newOntology/" + label,
                "baseIri": "http://visualdataweb.org/newOntology/",
                "label": label
            }
        else:
            dict_class_attribute = {
                "id": id,
                "iri": "http://www.w3.org/2000/01/rdf-schema#Datatype",
                "baseIri": "http://www.w3.org/2000/01/rdf-schema#",
                "label": label,
                "attributes": [
                    "datatype"
                ]
            }

        return dict_class_attribute

    def createProperty(self, id, type):
        """
        # Method to create JSON for Property Key
        """
        dict_property = {
            "id": id,
            "type": type
        }

        return dict_property

    def createpropertyAttribute(self,id, label, domain, range):
        """
        # Method to create JSON for property Attribute Key
        """
        dict_property_attribute = {
            "id": id,
            "iri": "http://visualdataweb.org/newOntology/" + label,
            "baseIri": "http://visualdataweb.org/newOntology/",
            "label": label,
            "domain": domain,
            "range": range
        }

        return dict_property_attribute

