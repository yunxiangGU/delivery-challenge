import argparse
import logging
import requests

log = logging.getLogger(__name__)


class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    """

    def __init__(self):
        pass

    def connect(self, inc_column=None, max_inc_value=None):
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def getDataBatch(self, batch_size):
        """
        Generator - Get data from source on batches.

        :returns One list for each batch. Each of those is a list of
                 dictionaries with the defined rows.
        """
        # TODO: implement - this dummy implementation returns one batch of data
        base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
        payload = {'api-key': self.args.api_key, 'q': self.args.query}
        try:
            response = requests.get(base_url, params=payload)
            if response.status_code == 200:
                data = response.json()['response']['docs']
                flattened_data = list(map(self.flatten_dict, data))
                reshaped_data = self.reshape_list(flattened_data, batch_size)
                return reshaped_data
            else:
                print(
                    f"Request failed with status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def reshape_list(self, original_list, batch_size):
        """
        Utility to reshape a long list

        :return a list for each batch, size passed in argument.
        """
        return [original_list[i: i + batch_size] for i in range(0, len(original_list), batch_size)]

    def flatten_dict(self, nested_dict, parent_key='', sep='.'):
        """
        Utility to flatten a single news article data entry

        :return a flatten dictionary, joining parent key and child key with seperator passed in argument.
        """
        items = {}
        for key, value in nested_dict.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.update(self.flatten_dict(value, new_key, sep))
            else:
                items[new_key] = value
        return items

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """

        schema = [
            "title",
            "body",
            "created_at",
            "id",
            "summary",
            "abstract",
            "keywords",
        ]

        return schema


if __name__ == "__main__":
    config = {
        "api_key": "ZIz3PgBIjfVnHNHDUKcsnPLsrZ5j6icB",  # My personal API key
        "query": "Silicon Valley",
    }
    source = NYTimesSource()

    # This looks like an argparse dependency - but the Namespace class is just
    # a simple way to create an object holding attributes.
    source.args = argparse.Namespace(**config)

    for idx, batch in enumerate(source.getDataBatch(10)):
        print(f"{idx} Batch of {len(batch)} items")
        for item in batch:
            print(f"  - {item['_id']} - {item['headline.main']}")
