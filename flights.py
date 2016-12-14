import requests
from bs4 import BeautifulSoup

# Constants
DESTCLASS = {'class': 'flights__table__col--destination'}
FLIGHTCLASS = {'class': 'stylish-table__row stylish-table__row--body'}
FLIGHTNUM = {'class': 'main-flight'}


class Cphdk:

    def __init__(self):
        r = requests.get(
            'https://www.cph.dk/en/flight-information/departures/')
        if r.status_code == 200:
            self._departures = BeautifulSoup(r.content, 'html.parser')
        else:
            self._departures = None
            print('Departures request failed with code: %i' % r.status_code)

        r = requests.get(
            'https://www.cph.dk/en/flight-information/arrivals/')
        if r.status_code == 200:
            self._arrivals = BeautifulSoup(r.content, 'html.parser')
        else:
            self._arrivals = None
            print('Arrivals request failed with code: %i' % r.status_code)

    def parse_departure_table(self):
        flights = self._departures.find_all('div', FLIGHTCLASS)
        departures = []
        for flight in flights:
            departure = {}
            departure['time'] = self._get_flight_time(flight)
            departure['airline'] = self._get_flight_airline(flight)
            departure['destination'] = self._get_flight_destination(flight)
            departure['number'] = self._get_flight_number(flight)
            departures.append(departure)
        return departures

    def parse_arrival_table(self):
        flights = self._arrivals.find_all('div', FLIGHTCLASS)
        arrivals = []
        for flight in flights:
            arrival = {}
            arrival['time'] = self._get_flight_time(flight)
            arrival['airline'] = self._get_flight_airline(flight)
            arrival['destination'] = self._get_flight_destination(flight)
            arrival['number'] = self._get_flight_number(flight)
            arrivals.append(arrival)
        return arrivals

    def _get_flight_time(self, flight):
        return flight.find_all('em')[0].text.strip()

    def _get_flight_airline(self, flight):
        return flight.find_all(
            'div', {
                'class': 'stylish-table__cell v--desktop-only'
            })[1].find_all('span')[1].text.strip()

    def _get_flight_destination(self, flight):
        return flight.find_all(
            'div', DESTCLASS)[0].find_all('span')[1].text.strip()

    def _get_flight_number(self, flight):
        return flight.find_all('span', FLIGHTNUM)[0].text.strip()
