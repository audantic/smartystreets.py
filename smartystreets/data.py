"""
Data structures module for SmartyStreets API.

These structures simply wrap Python built in data structures that match the API's JSON responses,
including some convenience methods for simple access.
"""
import logging


class Address(dict):
    """
    Class for handling a single address response
    """

    @property
    def location(self):
        """
        Returns the geolocation as a lat/lng pair
        """
        try:
            lat, lng = self['metadata']['latitude'], self['metadata']['longitude']
        except KeyError:
            return None
        if not lat or not lng:
            return None
        return lat, lng

    @property
    def confirmed(self):
        """
        Returns a boolean whether this address is DPV confirmed
        The property does not specify *how* or what extent.
        """
        valid = ['Y', 'S', 'D']
        match_code = self.get('analysis', {}).get('dpv_match_code', '')
        return match_code in valid

    @property
    def id(self):
        """
        Returns the input id
        """
        try:
            return self['input_id']
        except KeyError:
            return None

    @property
    def index(self):
        """
        Returns the input_index
        """
        try:
            return self['input_index']
        except KeyError:
            return None

    @property
    def vacant(self):
        if 'dpv_vacant' in self['analysis']:
            return 1 if self['analysis']['dpv_vacant'] == 'Y' else 0
        return None

    # function that checks if fields exist, returns None if not
    def lookup(self, group, field):
        if group in self:
            if field in self[group]:
                return self[group][field]
            # logging.getLogger('smarystreets').error('[group] {} [field] {}'.format(group, field))
            return None
        # logging.getLogger('smarystreets').error('[group] {}'.format(group))
        return None

    @property
    def addressee(self):
        """Returns addressee"""
        return self.get('addressee', None)

    @property
    def delivery_line_1(self):
        return self.get('delivery_line_1', None)

    @property
    def delivery_line_2(self):
        return self.get('delivery_line_2', None)

    @property
    def last_line(self):
        return self.get('last_line', None)

    @property
    def footnotes(self):
        return self['analysis'].get('footnotes', None)

    @property
    def analysis_active(self):
        return self['analysis'].get('active', None)

    @property
    def analysis_dpv_vacant(self):
        return self['analysis'].get('dpv_vacant', None)

    @property
    def analysis_dpv_cmra(self):
        return self['analysis'].get('dpv_cmra', None)

    @property
    def components_street_suffix(self):
        return self['components'].get('street_suffix', None)

    @property
    def primary_number(self):
        return self['components'].get('primary_number', None)

    @property
    def components_street_name(self):
        return self['components'].get('street_name', None)

    @property
    def components_city_name(self):
        return self['components'].get('city_name', None)

    @property
    def components_state_abbreviation(self):
        return self['components'].get('state_abbreviation', None)

    @property
    def components_zipcode(self):
        return self['components'].get('zipcode', None)

    @property
    def components_plus4_code(self):
        return self['components'].get('plus4_code', None)

    @property
    def metadata_dst(self):
        return self['metadata'].get('dst', None)

    @property
    def metadata_county_name(self):
        return self['metadata'].get('county_name', None)

    @property
    def metadata_congressional_district(self):
        return self['metadata'].get('congressional_district', None)

    @property
    def metadata_county_fips(self):
        return self['metadata'].get('county_fips', None)


class AddressCollection(list):
    """
    Class for handling multiple responses.
    """
    id_lookup = {}  # For user supplied input_id
    index_lookup = {}  # For SmartyStreets input_index

    def __init__(self, results):
        """
        Constructor for an AddressCollection

        :param addresses: a list of dictionaries providing address information
        :return:
        """
        addresses = []
        for index, result in enumerate(results):
            address = Address(result)
            addresses.append(address)
            self.index_lookup[address.index] = index
            if address.id:
                self.id_lookup[address.id] = index
        super(AddressCollection, self).__init__(addresses)

    def get(self, key):
        """
        Returns an address by user controlled input ID

        :param key: an input_id used to tag a lookup address
        :return: a matching Address
        """
        try:
            return self[self.id_lookup.get(key)]
        except TypeError:
            raise KeyError

    def get_index(self, key):
        """
        Returns an address by input index, a value that matches the list index of the provided
        lookup value, not necessarily the result.

        :param key: an input_index matching the index of the provided address
        :return: a matching Address
        """
        try:
            return self[self.index_lookup.get(key)]
        except TypeError:
            raise KeyError
