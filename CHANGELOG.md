# CHANGELOG
All notable changes to this project will be documented in this file. `[Unreleased]` section at the top, will be used to track upcoming changes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- When updating the Changelog:

- Please follow Keep a Changelog guiding principles: https://keepachangelog.com/en/1.1.0/#how.
- Make sure you add your entry to the correct section.

Thankyou! -->

## [Unreleased]

### Added 
* #### Objects
    1. Added `auth_factor` object. #949

### Improved
* #### Event Classes
    1. Added `auth_factors` array to Authentication event class. #949
* #### Objects
    1. Added `lat`, `long`, `geohash` attributes to `location`  object. #971

### Bugfixes
1. Changed datatype of `priority` from `integer_t` to `string_t` #959

### Deprecated
1. Deprecated `coordinates` attrubute in favor of specific `lat`, `long` attributes. #971

### Misc
1. New Extension registration for Sedara. #951

  #### Objects
  1. Added `risk_score`, `risk_level_id`, `risk_level` to the User object. Issue #972.

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

## [v1.2.0-dev] - February 7th, 2024

### Added
* #### Event Classes
    1. Added `Data Security Finding` event class.
* #### Objects
    1. Added new `data_security` object.

### Improved
* #### Objects
    1. Added two new enums to `confidentiality` object: `5 - Private` and `6 - Restricted`

## [v1.1.0] - January 25th, 2024

### Added
* #### Categories
    `n/a`
* #### Event Classes
    1. Added `User Inventory Info` event class. #667
    2. Added `Vulnerability Finding` event class. #698
    2. Added `NTP Activity` event class #705
    3. Added `OS Patch State` event class. #746
    4. Added `Datastore Activity` event class 6005. #874
    5. Added `Detection Finding` event class. #877
    6. Added `Incident Finding` event class. #903
    7. Added `Device Config Sate Change` event class. #914
    8. Added `Scan Activity` event class. #915
    9. Added `File Hosting Activity` event class. #917

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
