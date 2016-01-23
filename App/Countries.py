# -*- coding: utf-8 -*-
import pycountry

"""
One might wish to handle currencies here, too
"""
class Country(object):

    def select(self):
        country_select = []
        for country in pycountry.countries:
            country_select.append({
                "name": country.name,
                "code": country.alpha2,
                })
        return country_select

    def subdivision(self, country_code):
        sd_type = ", ".join(list(set((
            i.type for i in
            list(pycountry.subdivisions.get(country_code=country_code))))))

        subdivisions = {
                "sd_type": sd_type,
                "subdivisions": []
                }
        for sd in pycountry.subdivisions.get(country_code=country_code):
            subdivisions["subdivisions"].append({
                "name": sd.name,
                "code": sd.code,
                })
        subdivisions["subdivisions"].sort()
        return subdivisions
