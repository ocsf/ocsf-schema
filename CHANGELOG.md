# CHANGELOG
All notable changes to this project will be documented in this file. `[Unreleased]` section at the top, will be used to track upcoming changes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- When updating the Changelog:

- Please follow Keep a Changelog guiding principles: https://keepachangelog.com/en/1.1.0/#how.
- Make sure you add your entry to the correct section.

Thankyou! -->

## [Unreleased]

<!-- All available sections in the Changelog:

### Added
* #### Categories
* #### Event Classes
* #### Profiles
* #### Objects
* #### Platform Extensions

### Improved
* #### Categories
* #### Event Classes
* #### Profiles
* #### Objects
* #### Platform Extensions

### Bugfixes

### Deprecated

### Breaking changes

### Misc

-->

## [v1.2.0] - April 23rd, 2024

### Added
* #### Categories
    n/a
* #### Event Classes
    1. Added `Data Security Finding` event class. #953
    2. Added `File Query` event class. #967
    3. Added `Folder Query` event class. #967
    4. Added `Group Query` event class. #967
    5. Added `Job Query` event class. #967
    6. Added `Kernel Object Query` event class. #967
    7. Added `Module Query` event class. #967
    8. Added `Network Connection Query` event class. #967
    9. Added `Networks Query` event class. #967
    10. Added `Peripheral Device Query` event class. #967
    11. Added `Prefetch Query` event class. #967
    12. Added `Process Query` event class. #967
    13. Added `Registry Key Query` event class. #967
    14. Added `Registry Value Query` event class. #967
    15. Added `Service Query` event class. #967
    16. Added `Session Query` event class. #967
    17. Added `User Query` event class. #967
    18. Added `Tunnel Activity` event class. #1012

* #### Profiles
    1. Added `data_classification` profile. #998

* #### Objects
    1. Added `auth_factor` object. #949
    2. Added `data_security` object. #953
    3. Added `autonomous_system` object. #978
    4. Added `agent` object. #987
    5. Added `data_classification` object. #998

* #### Observables
    1. Added `port_t` `subnet_t` `cmd_line` `country` `pid` `cwe.uid` `cve.uid` `user_agent` enum items. #1035

* #### Platform Extensions
    n/a

### Improved
* #### Categories
    n/a
* #### Event Classes
    1. Added `auth_factors` array to Authentication event class. #949
    2. Modified all classes such that primary attributes are at least recommended. #974
    3. Added `src_endpoint`, `http_request` attributes to all IAM category classes. #976
    4. Added `autonomous_system` to `network_endpoint` objects. #978
    5. Added `List`, `Encrypt` and `Decrypt` activities to `datastore` event class. #989 
    6. Added `file` attribute to `http`, `rdp`, `ssh`, and `ftp` event classes. #985
    7. Added a `Preauth` `activity_id` to the `Authentication` class. #1018
    8. Added the `Security Control` profile to the `Datastore Activity` class. #1030
    9. Added `risk_details` to Detection Finding. #1032

* #### Profiles
    n/a
* #### Objects 
    1. Expanded `type_id` enum in `analytic` object to account for more use-cases: #953
        - `5 - Fingerprinting`
        - `6 - Tagging`
        - `7 - Keyword Match`
        - `8 - Regular Expressions`
        - `9 - Exact Data Match`
        - `10 - Partial Data Match`
        - `11 - Indexed Data Match`
    2. Added `lat`, `long`, `geohash` attributes to `location` object. #971.
    3. Added `risk_score`, `risk_level_id`, `risk_level` to `user` object. Issue #972.
    4. Added `app_name`, `app_uid` to `actor` object.  Issue #966, PR #979.
    5. Added `container`, `database`, `databucket` to the `evidences` object. #984
    6. Added `owner` to `endpoint` object. #987
    7. Added `is_applied` Boolean attribute to `policy` object. #987
    8. Added `agent_list` as an array of `agent` objects. #987
    9. Added `policies` object as an array of `policy` objects. #987
    10. Added `agent_list` to `endpoint` object. #987 
    11. Added `labels` to the `Account` object. #1028
    12. Added `data_classification` profile to `database`, `databucket`, `email`, `file`, `metadata`, `product`, `resource_details` and `web_resource` objects. #998

* #### Platform Extensions
    n/a

### Bugfixes
1. Changed datatype of `priority` attribute, from `integer_t` to `string_t` #959
2. Extended `email_t` regexp to allow characters from RFC5322 before @.
3. Updated `logon_type_id` enum to include `0` as `Unknown`. Added enum item `1` as `System`. #1055

### Deprecated
1. Deprecated `coordinates` attribute in favor of specific `lat`, `long` attributes. #971
2. Deprecated `invoked_by` attribute in the `Actor` object in favor of `app_name`. #979.

### Breaking changes

### Misc
1. New Extension registration for Sedara. #951
2. Corrected punctuation for the `transmit_time` attribute. #1001
3. New ways to define observables in the metaschema. #982 and #993
    * (Current) Dictionary types using `observable` property in dictionary types. This allows defining all occurrences of attributes of this type as an observable.
    * (Current) Objects using top-level `observable` property. This allows defining all occurrences attributes whose type is this object as an observable.
    * _**(New)**_ Dictionary attributes using `observable` property in attribute. This allows defining all occurrences of this attribute as an observable.
    * _**(New)**_ Object-specific attributes using `observable` property class's attributes. This allows defining object attributes as observables _only_ within instances of this specific object.
    * _**(New)**_ Event class-specific attributes using `observable` property class's attributes. This allows defining class attributes as observables _only_ within instances of this specific class.
    * _**(New)**_ Event class-specific attribute _paths_ using top-level `observables` property. The `observables` property holds an object mapping from a dotted attribute path to an observable `type_id`. This allows defining an observable _only_ within instances of this specific class, and only for the attributes at these paths, even for attributes that are within nested objects and arrays. This can also be used for top-level class attributes, which can be more convenient that defining a class attribute observable for classes that extend another, but don't otherwise change an attribute definition.
4. Metaschema improvements. #993 
    * Detect unexpected top-level properties in object and event class definitions. This was added at this point to detect invalid observable definitions: invalid `observable` property in event classes, and invalid `observables` property in objects.
    * Remove hard-coded list of categories from `metaschema/categories.schema.json`, leaving this to the `ocsf-validator`. This change makes testing with alternate schemas that may add extra categories easier, as well as making it possible to validate private extensions that contain new categories.
5. Metaschema error reporting #1027
    * Updated the definition of `object` and `event` so that metaschema errors reported by the validator with nested properties correctly attribute the error to the property with the error, rather than the top-level class.

## [v1.1.0] - January 25th, 2024

### Added
* #### Categories
    `n/a`
* #### Event Classes
    1. Added `User Inventory Info` event class. #667
    2. Added `Vulnerability Finding` event class. #698 
    3. Added `NTP Activity` event class #705
    4. Added `OS Patch State` event class. #746
    5. Added `Datastore Activity` event class 6005. #874
    6. Added `Detection Finding` event class. #877
    7. Added `Incident Finding` event class. #903
    8. Added `Device Config Sate Change` event class. #914
    9. Added `Scan Activity` event class. #915
    10. Added `File Hosting Activity` event class. #917
   
* #### Profiles
	1. Added `Network Proxy` Profile for the `Network Activity` and `Application Activity` classes. #705 
    2. Added `Load Balancer` Profile for the Network Activity classes. #897 

* #### Objects
    1. Added new `cwe` object to `cve` and `vulnerability` objects. #678 
    2. Added Firewall Rule object. #685
    3. Added new `kb_article` object to house Knowledgebase Article info. #709 #862 #924 
    4. Added new `epss` object to the `cve` object. #741
    
### Improved
* #### Categories
    1. Improved Findings Category, with new and domain specific event classes (Vulnerability Finding, Compliance Finding, Detection Finding, Incident Finding), description updates across the board. #895 #907 #903 #698 #718

* #### Event Classes
    1. Added `MFA Enable` and `Disable` to `activity_id` to the Account Change event class. #724
    2. Added `Service Ticket Renew` to `activity_id` of the Authentication event class. #765 
    3. Added `url` attribute to Network Activity event class. #857
    4. Added `http_request`, `http_response`, `tls` attributes, `network_proxy` profile to Web Resources Activity event class. #895
    5. Adjusted requirement of `dst_endpoint` from `required` to `recommended` in the DNS Activity event class. #901 
    6. Added `Create` and `Delete` to `activity_id` of the Group Management event class. #929
    
* #### Profiles
    1. Improved `security_control` profile to include access control semantics, firewall properties. #851 #888 #889 #906

* #### Objects
    1. Added `url_string` attribute to the `product` and the `web_resource` objects. #675
    2. Added `type` and `type_id` attributes to the `endpoint` object. #690
    3. Added `cwe`, `desc`, `references` and `title` to `cve` object. #698
    4. Added `affected_package` object and`affected_packages` attribute to `vulnerability` object. #698
    5. Added `purl` to `package` object. #698
    6. Added `cpe_name` attribute to the `product` and os objects. #713 #731
    7. Added `container` and `data` to `response` and `request` objects. #738
    8. Added `group` to the `api` object. #738
    9. Added `namespace` to the `resource_details` object. #738
    10. Added `log_level` to the `metadata` object. #738
    11. Added `length` to the `http_request` object. #768
    12. Added `is_exploit_available` to the `vulnerability` object. #777
    13. Added `domain` attribute to the `group` object. #871
    14. Adjusted attribute requirements in `dns_query`, `dns_answer` objects. #879
    15. Added firewall, router, switch, hub to endpoint `type_id` enum. #921
    16. Added `is_vpn` to the `session` object. #922
    17. Added `state` to `network_connection_info` object. #932

### Bugfixes
`n/a`

### Deprecated
1. Deprecated `cwe_uid` and `cwe_url` attributes and removed from `cve` object. #678
2. Deprecated `http_status` attribute from `HTTP Activity` event to be replaced by `http_response.code`. #767
3. Deprecated `finding` object in favor of `finding_info` object. #769
4. Deprecated `proxy` attribute from the dictionary, in favor of `Network Proxy` profile. #856
5. Deprecated `group_name` attribute. #873
6. Deprecated `Security Finding` class to be replaced by the new specific classes according to the use-case: `Vulnerability Finding`, `Compliance Finding`, `Detection Finding`, `Incident Finding`. #877
7. Deprecated `Web Resources Access Activity` event class. #890
8. Deprecated `Network File Activity` event class in favor of `File Hosting Activity `#917
9. Deprecated `extension_list` in TLS object in favor of `tls_extension_list`. #936

### Breaking changes
`n/a`

### Misc
1. New Extension registration for SentinelOne. #706
2. Added json-schema based metaschema validation to ensure correctness, consistency of the JSON definitions. #736 #830 #867 #892
3. Increased `max_len` for `subnet_t` type from `40` to `42`. #745
4. Improved the regex for `ip_t` type. #745
5. Updated the `datetime_t` validation regex to enable validation of timestamps, and to ensure that timestamps not matching `RFC-3339` are not considered valid. #753
6. Added version information to the native extensions. #881
7. Updated caption and description of Observable type - `File Hash` to read `Hash`. #900
8. New Extension registration for DataBee. #912
9. Changed data-type of `type_uid` to `long_t` from `int_t`. #928

## [v1.0.0]

Initial release of OCSF.
