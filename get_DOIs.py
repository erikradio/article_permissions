# -*- coding: utf-8 -*-
import requests, json


api_endpoint = 'http://api.crossref.org/prefixes/10.2458/works?rows=1000&cursor=*'
traversed_ids = []

# THIS WILL LOAD EVERY RECORD INTO RAM AT ONCE /disclaimer


def get_it_all(api_endpoint):
    results = []
    r = requests.get(api_endpoint).json()
    # Records that don't have a next cursor don't have the field
    # at all, so use a call to .get with None as the default
    # in order to avoid KeyErrors being raised
    next_cursor = False
    next_cursor = r.get('message', {}).get('next-cursor', False)
    if next_cursor:
        # Prevent circular paths
        if next_cursor not in traversed_ids:
            traversed_ids.append(next_cursor)
            print(next_cursor)
            # Recursion case
            # Gather up anything from the next records
            results = results + get_it_all(
                construct_url_from_next_cursor(next_cursor)
            )
    # Gather up everything from this record
    # We have to be sure this field exists first though
    # This is a really big hack with nested gets
    # Probably don't actually ever do this
    if r.get('message', {}).get('items', False):
        for x in r['message']['items']:
            results.insert(0, x)
    print(len(results))
    return results


def construct_url_from_next_cursor(next_cursor):
    # do stuff here
    # return a valid url as a string
    return api_endpoint[0:-1] + next_cursor

def main():
    with open('results.json', 'w') as f:
        json.dump(get_it_all(api_endpoint),f)

if __name__ == "__main__":
    main()
