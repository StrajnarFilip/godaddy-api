from dataclasses import asdict
import requests
import os
from typing import Union
from godaddy_api.data.domain_available import DomainAvailable
from godaddy_api.data.domain_record import DomainRecord


class GodaddyClient:
    """
    This client enables easy interaction with Shopper API provided by GoDaddy Inc.
    Official API docs can be found (at the time of writing) on:
    https://developer.godaddy.com/doc/endpoint/domains
    """

    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 api_url: str = "https://api.godaddy.com/"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url
        self.auth_header = {
            "Authorization": f"sso-key {self.api_key}:{self.api_secret}"
        }

    def domains_available(self, domain: str) -> Union[DomainAvailable, None]:
        response = requests.get(f"{self.api_url}v1/domains/available",
                                params={
                                    "domain": domain
                                },
                                headers=self.auth_header).json()

        try:
            return DomainAvailable(response["available"], response["currency"],
                                   response["definitive"], response["domain"],
                                   response["period"], response["price"])
        except Exception:
            return None

    def add_records(self, domain: str, records: list[DomainRecord]):
        """
        Returns entire response.
        """

        record_dictionaries = [asdict(record) for record in records]
        response = requests.patch(f"{self.api_url}v1/domains/{domain}/records",
                                  json=record_dictionaries,
                                  headers=self.auth_header)

        return response

    def records_for_domain(self,
                           domain: str) -> Union[list[DomainRecord], None]:
        """
        Returns list of existing records for the domain, or None
        if request was not successful. 
        """
        response = requests.get(f"{self.api_url}v1/domains/{domain}/records",
                                headers=self.auth_header)
        if response.status_code == 200:
            return [
                DomainRecord(record["data"], record["name"], 0, 0, "", "",
                             record["ttl"], record["type"], 0)
                for record in response.json()
            ]
        else:
            return None

    def add_a_record(self, domain: str, record_name: str, ip_address: str):
        """
        Returns entire response.
        Status code `200` means it's successful.
        Status code `422` means record already exists.

        Example for `something.com`:

        ```py
        client.add_a_record("something.com", "@", "123.123.123.123")
        ```

        Example for `one.something.com` subdomain:
        ```py
        client.add_a_record("something.com", "one", "123.123.123.123")
        ```
        """

        record = DomainRecord(ip_address, record_name, 1, 1, "", "", 600, "A",
                              1)
        return self.add_records(domain, [record])

    def remove_a_record(self, domain: str, record_name: str):
        """
        Returns entire response.
        Status code `204` means it's successful.
        Status code `404` means record didn't exist.
        """
        record_type = 'A'
        response = requests.delete(
            f"{self.api_url}v1/domains/{domain}/records/{record_type}/{record_name}",
            headers=self.auth_header)

        return response

    def set_a_record(self, domain: str, record_name: str, ip_address: str):
        """
        Removes the record and adds it again. Returns response from
        request that adds the record, so successful status code is `200`. 
        """
        self.remove_a_record(domain, record_name)
        response = self.add_a_record(domain, record_name, ip_address)
        return response
