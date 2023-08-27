from dataclasses import asdict
from requests import Session, Response
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
        self.session = Session()
        self.session.headers[
            "Authorization"] = f"sso-key {self.api_key}:{self.api_secret}"

    def domains_available(self,
                          domain: str) -> Union[DomainAvailable, Response]:
        """
        Check if domain is available to be purchased.
        Within DomainAvailable dataclass, there is `available` boolean field.
        In case of exception, it returns whole response.
        """
        response = self.session.get(f"{self.api_url}v1/domains/available",
                                    params={"domain": domain})

        try:
            data = response.json()
            return DomainAvailable(data["available"], data["currency"],
                                   data["definitive"], data["domain"],
                                   data["period"], data["price"])
        except Exception:
            return response

    def add_records(self, domain: str,
                    records: list[DomainRecord]) -> Response:
        """
        Returns entire response.
        """

        record_dictionaries = [asdict(record) for record in records]
        response = self.session.patch(
            f"{self.api_url}v1/domains/{domain}/records",
            json=record_dictionaries)

        return response

    def records_for_domain(self,
                           domain: str) -> Union[list[DomainRecord], Response]:
        """
        Returns list of existing records for the domain,
        or response if request was not successful. 
        """
        response = self.session.get(
            f"{self.api_url}v1/domains/{domain}/records")

        if response.status_code == 200:
            return [
                DomainRecord(record["data"], record["name"], 0, 0, "", "",
                             record["ttl"], record["type"], 0)
                for record in response.json()
            ]
        else:
            return response

    def add_a_record(self, domain: str, record_name: str,
                     ip_address: str) -> Response:
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

    def remove_a_record(self, domain: str, record_name: str) -> Response:
        """
        Returns entire response.
        Status code `204` means it's successful.
        Status code `404` means record didn't exist.
        """
        record_type = 'A'
        return self.session.delete(
            f"{self.api_url}v1/domains/{domain}/records/{record_type}/{record_name}"
        )

    def set_a_record(self, domain: str, record_name: str,
                     ip_address: str) -> Response:
        """
        Removes the record and adds it again. Returns response from
        request that adds the record, so successful status code is `200`. 
        """
        self.remove_a_record(domain, record_name)
        return self.add_a_record(domain, record_name, ip_address)

    def list_domains(self):
        """
        Lists domains owned.
        """

        response = self.session.get(f"{self.api_url}v1/domains")

        return response.json() if response.status_code == 200 else response
