# -*- coding: utf-8 -*-
from flask.ext import restful
from App.Countries import Country
import pycountry

def countries(app):

    api = restful.Api(app)
    countries = Country()

    class CountrySelect(restful.Resource):
        def get(self):
            return countries.select()
            
    class Subdivision(restful.Resource):
        def get(self, country_code):
            return countries.subdivision(country_code)
           
    class CountryCurrency(restful.Resource):
        def get(self, country_code):
            return countries.currency(country_code)

    api.add_resource(CountrySelect, "/api/country/select")
    api.add_resource(
            Subdivision, "/api/country/subdivision/<string:country_code>")
    api.add_resource(
            CountryCurrency, "/api/country/currency/<string:country_code>")

    #TODO I suggest you take a look at zipapottam.us.
