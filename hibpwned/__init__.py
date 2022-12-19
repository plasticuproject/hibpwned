"""A human friendly python API wrapper for https://haveibeenpwned.com
   All data is sourced from https://haveibeenpwned.com
   Visit https://haveibeenpwned.com/API/v3 to read the Acceptable Use Policy
   for rules regarding acceptable usage of this API.

   Copyright (C) 2022  plasticuproject@pm.me

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License.
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
"""

import hashlib
from typing import Dict, List, Union, Optional
import requests


def _check(resp: requests.models.Response) -> None:
    """Helper function to check the response code and prints anything
    other than a 200 OK."""

    try:
        if resp.status_code == 400:
            print("Bad request: The account does not comply with an" +
                  " acceptable format (i.e. it's an empty string)")
        elif resp.status_code == 401:
            print("Unauthorized — the API key provided was not valid")
        elif resp.status_code == 403:
            print("Forbidden: No user agent has" +
                  " been specified in the request")
        elif resp.status_code == 404:
            print("Not found: The account could not be found and" +
                  " has therefore not been pwned")
        elif resp.status_code == 429:
            print("Too many requests: The rate limit has been exceeded\n")
            print(resp.text)
    except requests.RequestException:
        print("ERROR: Could not connect to server")


class Pwned:
    """All functions, with the exception of search_password and
    search_hashes, return JSON formated data related to the function and
    arguments/search terms from https://haveibeenpwned.com. The
    search_password and search_hashes functions will return an integer
    and plaintext string of hashes, respectively.

    Authorisation is required for all API requests. A HIBP subscription
    key is required to make an authorised call and can be obtained on
    the API key page at https://haveibeenpwned.com/API/Key.

    User must initialize the Pwned class with the account (email
    address being queried) and a User-Agent (the name of your
    application), even if an account is not applicable to the
    function.

    A "breach" is an instance of a system having been compromised by
    an attacker and the data disclosed. Each breach contains a number
    of attributes describing the incident. In the future these
    attributes may expand. The current attributes are:

    ATTRIBUTE     TYPE      DESCRIPTION

    Name          string    A Pascal-cased name representing the breach
                            which is unique across all other breaches.
                            This value never changes and may be used to
                            name dependent assets (such as images) but
                            should not be shown directly to end users
                            (see the "Title" attribute instead).

    Title         string    A descriptive title for the breach suitable
                            for displaying to end users. It's unique
                            across all breaches but individual values
                            may change in the future (i.e. if another
                            breach occurs against an organisation
                            already in the system). If a stable value is
                            required to reference the breach, refer to
                            the "Name" attribute instead.

    Domain        string    The domain of the primary website the breach
                            occurred on. This may be used for
                            identifying other assets external systems may
                            have for the site.

    BreachDate    date      The date (with no time) the breach
                            originally occurred on in ISO 8601 format.
                            This is not always accurate — frequently
                            breaches are discovered and reported long
                            after the original incident. Use this
                            attribute as a guide only.

    AddedDate     datetime  The date and time (precision to the minute)
                            the breach was added to the system in ISO
                            8601 format.

    ModifiedDate  datetime  The date and time (precision to the minute)
                            the breach was modified in ISO 8601 format.
                            This will only differ from the AddedDate
                            attribute if other attributes represented
                            here are changed or data in the breach
                            itself is changed (i.e. additional data is
                            identified and loaded). It is always either
                            equal to or greater then the AddedDate
                            attribute, never less than.

    PwnCount      integer   The total number of accounts loaded into the
                            system. This is usually less than the total
                            number reported by the media due to
                            duplication or other data integrity issues
                            in the source data.

    Description   string    Contains an overview of the breach
                            represented in HTML markup. The description
                            may include markup such as emphasis and
                            strong tags as well as hyperlinks.

    DataClasses   string    This attribute describes the nature of the
                            data compromised in the breach and contains
                            an alphabetically ordered string array of
                            impacted data classes.

    IsVerified    boolean   Indicates that the breach is considered
                            unverified. An unverified breach may not
                            have been hacked from the indicated website.
                            An unverified breach is still loaded into
                            HIBP when there's sufficient confidence that
                            a significant portion of the data is
                            legitimate.

    IsFabricated  boolean   Indicates that the breach is considered
                            fabricated. A fabricated breach is unlikely
                            to have been hacked from the indicated
                            website and usually contains a large amount
                            of manufactured data. However, it still
                            contains legitimate email addresses and
                            asserts that the account owners were
                            compromised in the alleged breach.

    IsSensitive   boolean   Indicates if the breach is considered
                            sensitive. The public API will not return
                            any accounts for a breach flagged as
                            sensitive.

    IsRetired     boolean   Indicates if the breach has been retired.
                            This data has been permanently removed and
                            will not be returned by the API.

    IsSpamList    boolean   Indicates if the breach is considered a spam
                            list. This flag has no impact on any other
                            attributes but it means that the data has
                            not come as a result of a security compromise.


    RESPONSE CODES:

    Semantic HTTP response codes are used to indicate the result of the
    search:

    CODE    DESCRIPTION

    200     Ok — everything worked and there's a string array of pwned
            sites for the account.

    400    Bad request — the account does not comply with an acceptable
           format (i.e. it's an empty string).

    401    Unauthorized — the API key provided was not valid

    403    Forbidden — no user agent has been specified in the request.

    404    Not found — the account could not be found and has therefore
           not been pwned.

    429    Too many requests — the rate limit has been exceeded.


    ___________________________________________________________________
    -------------------------------------------------------------------

       Class Functions:: (see function DocStrings for details)

           search_all_breaches
           all_breaches
           single_breach
           data_classes
           search_pastes
           search_password
           search_hashes


       Usage::

         >>> foo = Pwned("test@example.com", "My_App", "My_API_Key")
         >>> data = foo.search_password("BadPassword")
    """
    ReturnAlias = (Union[int, List[Dict[str, Union[str, int, bool]]]])
    AltReturnAlias = (Union[int, List[Dict[str, Union[str, int, bool]]],
                            List[str]])
    DataAlias = (Union[List[Dict[str, Union[str, int, bool]]],
                       Dict[str, Union[str, int, bool]]])
    AltDataAlias = (Union[List[Dict[str, Union[str, int, bool]]],
                          Dict[str, Union[str, int, bool]], List[str]])
    url: str
    resp: requests.models.Response
    truncate_string: str
    domain_string: str
    unverified_string: str
    classes: List[str]
    hashes: str
    hash_list: List[str]
    hexdig: str
    hsh: str
    pnum: str
    data: DataAlias
    alt_data: AltDataAlias

    def __init__(self, account: str, agent: str, key: str) -> None:
        self.account = account
        self.agent = agent
        self.key = key
        self.header: Dict[str, str] = {
            "User-Agent": self.agent,
            "hibp-api-key": self.key
        }

    # pylint: disable=undefined-variable
    def search_all_breaches(
            self,
            truncate: Optional[bool] = False,
            domain: Optional[str] = None,
            unverified: Optional[bool] = False) -> AltReturnAlias:
        """The most common use of the API is to return a list of all
        breaches a particular account has been involved in.

        By default, only the name of the breach is returned rather than the
        complete breach data, thus reducing the response body size by
        approximately 98%. The name can then be used to either retrieve a
        single breach or it can be found in the list of all breaches in the
        system. If you'd like complete breach data returned in the API call,
        a non-truncated response can be specified via query string parameter:

        `?truncateResponse=false`

        Note: In version 2 of the API this behaviour was the opposite -
        responses were not truncated by default.

        The result set can also be filtered by domain by passing the
        "domain='example.com'" argument. This filters the result set to
        only breaches against the domain specified. It is possible that
        one site (and consequently domain), is compromised on multiple
        occasions.

        The public API will not return accounts from any breaches
        flagged as sensitive or retired. By default, the API also won't
        return breaches flagged as unverified, however these can be
        included by passing the argument "unverified=True". This
        returns breaches that have been flagged as "unverified". By
        default, only verified breaches are returned when performing a
        search.


           Usage::

             >>> foo = Pwned('test@example.com', 'My_App', "My_API_Key")
             >>> data = foo.search_all_breaches()
             >>> data = foo.search_all_breaches(domain='adobe.com')
             >>> data = foo.search_all_breaches(truncate=True, unverified=True)
        """
        url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
        if truncate:
            truncate_string = ""
        else:
            truncate_string = "?truncateResponse=false"
        if not domain:
            domain_string = ""
        else:
            domain_string = "?domain=" + domain
        if unverified:
            unverified_string = "?includeUnverified=true"
        else:
            unverified_string = ""
        resp = requests.get(url + self.account + truncate_string +
                            domain_string + unverified_string,
                            headers=self.header)
        _check(resp)
        if resp.status_code == 200:
            alt_data = resp.json()
            if not isinstance(alt_data, list):
                return [alt_data]
            return alt_data
        return resp.status_code

    # pylint: disable=undefined-variable
    def all_breaches(self, domain: Optional[str] = None) -> ReturnAlias:
        """Retrieves all breached sites from the system. The result set
        can also be filtered by domain by passing the argument
        "domain='example.com'". This filters the result set to only
        breaches against the domain specified. It is possible that one
        site (and consequently domain), is compromised on multiple
        occasions.


           Usage::

             >>> foo = Pwned("test@example.com", "My_App", "My_API_Key")
             >>> data = foo.all_breaches()
             >>> data = foo.all_breaches(domain="adobe.com")
        """
        url = "https://haveibeenpwned.com/api/v3/breaches"
        if not domain:
            domain_string = ""
        else:
            domain_string = "?domain=" + domain
        resp = requests.get(url + domain_string, headers=self.header)
        _check(resp)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                return data
        return resp.status_code

    def single_breach(self, name: str) -> ReturnAlias:
        """
        Returns a single breached site queried by name. Sometimes just
        a single breach is required and this can be retrieved by the
        breach "name". This is the stable value which may or may not be
        the same as the breach "title" (which can change).


           Usage::

             >>> foo = Pwned("test@example.com", "My_App", "My_API_Key")
             >>> data = foo.single_breach("adobe")
        """
        url = "https://haveibeenpwned.com/api/v3/breach/"
        resp = requests.get(url + name, headers=self.header)
        _check(resp)
        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, list):
                return [data]
            # return data  # Pretty sure will never hit
        return resp.status_code

    def data_classes(self) -> Union[int, List[str]]:
        """Returns all data classes in the system.


           Usage::

             >>> foo = Pwned("test@example.com", "My_App", "My_API_Key")
             >>> data = foo.data_classes()
        """
        url = "https://haveibeenpwned.com/api/v3/dataclasses"
        resp = requests.get(url, headers=self.header)
        _check(resp)
        if resp.status_code == 200:
            classes = resp.json()
            if isinstance(classes, list):
                return classes
        return resp.status_code

    def search_pastes(self) -> ReturnAlias:
        """Returns all pastes for an account. Unlike searching for
        breaches, usernames that are not email addresses cannot be
        searched for. Searching an account for pastes always returns a
        collection of the paste entity. The collection is sorted
        chronologically with the newest paste first.

        Each paste contains a number of attributes describing it. In
        the future, these attributes may expand. The current
        attributes are:

        ATTRIBUTE     TYPE      DESCRIPTION

        Source        string    The paste service the record was
                                retrieved from. Current values are:
                                Pastebin, Pastie, Slexy, Ghostbin,
                                QuickLeak, JustPaste, AdHocUrl, OptOut

        Id            string    The ID of the paste as it was given at
                                the source service. Combined with the
                                "Source" attribute, this can be used to
                                resolve the URL of the paste.

        Title         string    The title of the paste as observed on
                                the source site. This may be null and
                                if so will be omitted from the
                                response.

        Date          date      The date and time (precision to the
                                second) that the paste was posted. This
                                is taken directly from the paste site
                                when this information is available but
                                may be null if no date is published.

        EmailCount     integer  The number of emails that were found
                                when processing the paste. Emails are
                                extracted by using the regular
                                expression \b+(?!^.{256})[a-zA-Z0-9\\.\\-
                                _\\+]+@[a-zA-Z0-9\\.\\-_]+\\.[a-zA-Z]+\b


           Usage::

             >>> foo = Pwned("test@example.com", "My_App", "My_API_Key")
             >>> data = foo.search_pastes()
        """
        url = "https://haveibeenpwned.com/api/v3/pasteaccount/"
        resp = requests.get(url + self.account, headers=self.header)
        _check(resp)
        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, list):
                return [data]
            return data
        return resp.status_code

    def search_password(self, password: str) -> Union[int, str]:
        """Returns an integer of how many times the password appears in
        the Pwned Passwords repository, where each password is stored
        as a SHA-1 hash of a UTF-8 encoded password. When a password
        hash with the same first 5 characters is found in the Pwned
        Passwords repository, the API will respond with an HTTP 200
        and include the suffix of every hash beginning with the
        specified prefix, followed by a count of how many times it
        appears in the data set. The function then searches the results
        of the response for the presence of the source hash and if not
        found, the password does not exist in the data set.

        In order to protect the value of the source password being
        searched for, Pwned Passwords also implements a k-Anonymity
        model that allows a password to be searched for by partial
        hash. This allows the first 5 characters of a SHA-1 password
        hash (not case-sensitive) to be passed to the API.


            Usage::

              >>> foo = Pwned("test@example.com", "My_App", "My_API_Key")
              >>> data = foo.search_password("BadPassword")
        """
        url = "https://api.pwnedpasswords.com/range/"
        hash_object = hashlib.sha1(bytes(password, encoding="utf-8"))
        hexdig = hash_object.hexdigest()
        hexdig = hexdig.upper()
        hsh = hexdig[:5]
        pnum = '0'
        resp = requests.get(url + hsh, headers=self.header)
        _check(resp)
        if resp.status_code == 200:
            hash_list = resp.text.splitlines()
            for item in hash_list:
                if item[0:35] == hexdig[5:]:
                    pnum = item[36:]
            return pnum
        return resp.status_code

    def search_hashes(self, hsh: str) -> Union[int, str]:
        """Returns a string of plaintext hashes which are suffixes to the
        first 5 characters of the searched hash argument. When a
        password hash with the same first 5 characters is found in the
        Pwned Passwords repository, the API will respond with an HTTP
        200 and include the suffix of every hash beginning with the
        specified prefix, followed by a count of how many times it
        appears in the data set. The API consumer can then search the
        results of the response for the presence of their source hash
        and if not found, the password does not exist in the data set.

        In order to protect the value of the source password being
        searched for, Pwned Passwords also implements a k-Anonymity
        model that allows a password to be searched for by partial
        hash. This allows the first 5 characters of a SHA-1 password
        hash (not case-sensitive) to be passed to the API.

        Each password is stored as a SHA-1 hash of a UTF-8 encoded
        password. The hash and password count are delimited with a
        colon (:).

           Usage::

             >>> foo = Pwned("test@example.com", "My_App", "My_API_Key")
             >>> data = foo.search_hashes("21BD1")
        """
        url = "https://api.pwnedpasswords.com/range/"
        hsh = hsh[:5]
        resp = requests.get(url + hsh, headers=self.header)
        _check(resp)
        if resp.status_code == 200:
            hashes = resp.text
            return hashes
        return resp.status_code
