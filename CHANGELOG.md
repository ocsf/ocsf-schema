# CHANGELOG
All notable changes to this project will be documented in this file. `[Unreleased]` section at the top, will be used to track upcoming changes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- When updating the Changelog:

- Please follow Keep a Changelog guiding principles: https://keepachangelog.com/en/1.1.0/#how.
- Make sure you add your entry to the correct section.

Thankyou! -->

<!-- All available sections in the Changelog:

### Added
* #### Categories
* #### Event Classes
* #### Profiles
* #### Objects
* #### Observables
* #### Platform Extensions
* #### Dictionary Attributes

### Improved
* #### Categories
* #### Event Classes
* #### Profiles
* #### Objects
* #### Observables
* #### Platform Extensions
* #### Dictionary Attributes

### Bugfixes

### Deprecated

### Breaking changes

### Misc

-->

## [Unreleased]

### Added
* #### Categories
* #### Event Classes
* #### Profiles
  1. Added `ai_operation` profile with essential attributes for AI operation event mapping. [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
* #### Objects
  1. Added `ai_model` object with core fields (`name`, `ai_provider`, `version`) for AI operation events. [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
  1. Added `message_context` object for AI system interactions with role-based identification and token usage metrics (`prompt_tokens`, `completion_tokens`, `total_tokens`). [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
* #### Observables
* #### Platform Extensions
* #### Dictionary Attributes
  1. Added `ai_provider` attribute for AI model identification. [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
  1. Added `ai_role_id`, `ai_role` attributes for AI communication context with proper sibling relationship. [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
  1. Added `prompt_tokens`, `completion_tokens`, `total_tokens` attributes for AI token usage metrics. [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
  1. Added `embedding_model` attribute for AI retrieval systems. [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
  1. Added `imported_symbols` attribute for reporting an executable file's imports.  [#1553](https://github.com/ocsf/ocsf-schema/pull/1553)
  1. Added `Imphash (18)` enum to the `algorithm_id` attribute of the `fingerprint` object. [#1553](https://github.com/ocsf/ocsf-schema/pull/1553)

### Improved
* #### Categories
* #### Event Classes
* #### Profiles
* #### Objects
  1. Extended `database` object with AI-specific database types (`Vector (7)`, `Knowledge Graph (8)`) and `embedding_model` field for AI retrieval systems. [#1488](https://github.com/ocsf/ocsf-schema/pull/1488)
  1. Expanded on `created_time` attribute description within the `related_event` object. [1552](https://github.com/ocsf/ocsf-schema/pull/1552)
  1. Added `imported_symbols` attribute to the `file` object.  [#1553](https://github.com/ocsf/ocsf-schema/pull/1553)
* #### Observables
* #### Platform Extensions
* #### Dictionary Attributes

### Bugfixes

### Deprecated

### Breaking changes

### Misc
### Bugfixes
* #### Event Classes
  1. Removed erroneous `at_least_one` constraint in `Live Evidence Info` class [#1357](https://github.com/ocsf/ocsf-schema/pull/1537)

### Improved
* #### Objects
  1. Added `signatures` to the `file` object. [#1546](https://github.com/ocsf/ocsf-schema/pull/1546)

### Deprecated
1. Deprecated the `signature` attribute of the file object in favour of the `signatures` attribute. [#1546](https://github.com/ocsf/ocsf-schema/pull/1546)




## [v1.7.0] - Nov 14th, 2025

### Added
* #### Categories
* #### Event Classes
  1. Added `Peripheral Activity` event class to the System category. [#1471](https://github.com/ocsf/ocsf-schema/pull/1471)
* #### Profiles
* #### Objects
  1. Added `reporter` object. [#1476](https://github.com/ocsf/ocsf-schema/pull/1476)
  1. Added Windows extension to the `process` object.
  1. Added the `function_invocation` and `parameter` objects. [#1497](https://github.com/ocsf/ocsf-schema/pull/1497)
* #### Observables
  1. Set `network_endpoint.uid` as an Observable type - `type_id: 48`. [#1502](https://github.com/ocsf/ocsf-schema/pull/1502)
* #### Platform Extensions
* #### Dictionary Attributes
  1. Added `vendor_id_list` as a `string_t` array. [#1471](https://github.com/ocsf/ocsf-schema/pull/1471)
  1. Added `post_value`, `pre_value` and `return_value` as `string_t`. [#1497](https://github.com/ocsf/ocsf-schema/pull/1497)
  1. Added `launch_type_id` enum and `launch_type` sibling. [#1517](https://github.com/ocsf/ocsf-schema/pull/1517)
  1. Added `log_source` `log_source_uid` `log_format` as `string_t`. [#1483](https://github.com/ocsf/ocsf-schema/pull/1483)

### Improved
* #### Categories
* #### Event Classes
  1. Added `auth_factors` as an attribute to the `Account Change` class and updated related activity names. [#1455](https://github.com/ocsf/ocsf-schema/pull/1455)
  1. Added `Invoke` as an `activity_id` value for the `Module Activity` class. [#1497](https://github.com/ocsf/ocsf-schema/pull/1497)
  1. Added `launch_type_id` and `launch_type` as attributes to the `Process Activity` event class. [#1517](https://github.com/ocsf/ocsf-schema/pull/1517)
  1. Added descriptions to values of `activity_id` enum in `Process Activity` event class. [#1517](https://github.com/ocsf/ocsf-schema/pull/1517)
  1. Added missing context classification to `windows_service_activity.win_service`. [#1531](https://github.com/ocsf/ocsf-schema/pull/1531)
  1. Added missing requirement to `process_activity.launch_type`. [#1531](https://github.com/ocsf/ocsf-schema/pull/1531)
  1. Added `cumulative_traffic` attribute to the base `Network` event. Updated `traffic` description. [#1529](https://github.com/ocsf/ocsf-schema/pull/1529)
* #### Profiles
* #### Objects
  1. Added `type`, `type_uid`, and `vendor_id_list` to the `peripheral_device` object. [#1471](https://github.com/ocsf/ocsf-schema/pull/1471)
  1. Relaxed the `class` attribute requirement to `optional` in the `peripheral_device` object. [#1471](https://github.com/ocsf/ocsf-schema/pull/1471)
  1. Set the `vendor_name` requirement to `recommended` in the `peripheral_device` object. [#1471](https://github.com/ocsf/ocsf-schema/pull/1471)
  1. Added `reporter` to the `metadata` object. [#1476](https://github.com/ocsf/ocsf-schema/pull/1476)
  1. Added `event_uid` and `type_uid` to the `observable` object. [#1503](https://github.com/ocsf/ocsf-schema/pull/1503)
  1. Set `load_type_id` requirement to `recommended` in the `module` object. [#1497](https://github.com/ocsf/ocsf-schema/pull/1497)
  1. Added `at_least_one` constraint on `load_type_id` and `function_name` in the `module` object. [#1497](https://github.com/ocsf/ocsf-schema/pull/1497)
  1. Modified descriptions in the `module` object to accommodate `Module Activity: Invoke` event. [#1497](https://github.com/ocsf/ocsf-schema/pull/1497)
  1. Added `function_invocation` to the `module` object. [#1497](https://github.com/ocsf/ocsf-schema/pull/1497)
  1. Relaxed the `file` attribute requirement to `optional` in the `job` object. [#1509](https://github.com/ocsf/ocsf-schema/pull/1509)
  1. Relaxed the `name` and `uid` requirement to `recommended` with `at_least_one` constraint in the `extension` object. [#1511](https://github.com/ocsf/ocsf-schema/pull/1511)
  1. Added `hosting_process`, `service_file` and `service_dll_file` to the `win_service` object.
  1. Added `hosted_services`, array to the `process` object.
  1. Added `source`, `type`, `log_source`, `original_event_uid`,`log_format`, `transmit_time` to `metadata`. `log_format` to `logger`[#1483](https://github.com/ocsf/ocsf-schema/pull/1483)
  1. Added `start_time`, `end_time` and `timespan` to the `network_traffic` object. Updated `network_traffic` description. [#1529](https://github.com/ocsf/ocsf-schema/pull/1529)
* #### Observables
* #### Platform Extensions
* #### Dictionary Attributes
  1. Added `Local (4)` enum to the `direction_id` attribute. [#1475](https://github.com/ocsf/ocsf-schema/pull/1475)
  1. Added `Atom (38)` enum as an available `type_id` for `win_resource` object. [#1477](https://github.com/ocsf/ocsf-schema/pull/1477)
  1. Updated reference descriptions/urls for win_resource types, including `Directory (1)`, `Event (2)`, `Timer (3)`, `Device (4)`, `Mutant (5)`, `File (7)`, `Token (8)`, `Thread (9)`, `Section (10)`, `WindowStation (11)`, `Driver (15)`, `IoCompletion (16)`, `Controller (17)`, `SymbolicLink (18)`, `WmiGuid (19)`, `Process (20)`, `Profile (21)`, `Desktop (22)`, `KeyedEvent (23)`, `Adapter (24)`, `Callback (27)`, `Semaphore (28)`, `Job (29)`, `ALPC Port (32)`, `SAM_ALIAS (33)`, `SAM_GROUP (34)`, `SAM_USER (35)`, `SAM_DOMAIN (36)`, `SAM_SERVER (37)`, and `Atom (38)`. [#1477](https://github.com/ocsf/ocsf-schema/pull/1477)
  1. Added `hosted_services` to the Windows extension to the `process` object.
  1. Added multiple values to the `state_id` enum attribute for the `digital_signature` object. [#1520](https://github.com/ocsf/ocsf-schema/pull/1520)
  1. Added `WFP Filter (39)`, `WFP Callout (40)`, `WFP Layer (41)`, `WFP Sub-layer (42)`, `WFP Provider (43)` and `WFP Provider Context (44)` WindowsFilteringPlatform-related enums as an available `type_ids` for `win_resource` object. [#1530](https://github.com/ocsf/ocsf-schema/pull/1530)
  1. Added `cumulative_traffic` of `network_traffic` type. [#1529](https://github.com/ocsf/ocsf-schema/pull/1529)

### Bugfixes

### Deprecated

### Breaking changes

### Misc
  1. Updated description for the `peripheral_device` object and the `vendor_name` attribute within it. [#1471](https://github.com/ocsf/ocsf-schema/pull/1471)
  1. Corrected the deprecation note for the `Web Resource Access Activity` event class. [#1492](https://github.com/ocsf/ocsf-schema/pull/1492)

## [v1.6.0] - Aug 1st, 2025

### Added
* #### Event Classes
  1. Added `IAM Analysis Finding` event class to the Findings category. [#1389](https://github.com/ocsf/ocsf-schema/pull/1389)
* #### Dictionary Attributes
  1. Added `from_list`, `from_mailboxes`,`reply_to_list`, `return_path`, `sender` and `sender_mailbox`. [#1454](https://github.com/ocsf/ocsf-schema/pull/1454)
  1. Added `access_level`, `programmatic_credentials`, `last_authentication_time`, `access_analysis_result`, `last_used_time`, `accessors`, `granted_privileges`, `identity_activity_metrics`, `password_last_used_time`, `access_type`, `permission_analysis_results`, `additional_restrictions`, `unused_privileges_count`, `condition_keys`, `applications`, `role`, `role_id`. [#1389](https://github.com/ocsf/ocsf-schema/pull/1389)
  1. Added `reg_binary_data`, `reg_integer_data`, `reg_string_data`, `reg_string_list_data` to Windows extension. [#1468](https://github.com/ocsf/ocsf-schema/pull/1468)
  1. Added `is_src_dst_assignment_known` as a boolean. [#1464](https://github.com/ocsf/ocsf-schema/pull/1464)
  1. Added `network_scope`, `network_scope_id`, `observation_point` and `observation_point_id`. [#1481](https://github.com/ocsf/ocsf-schema/pull/1481)

* #### Objects
  1. Added  `access_analysis_result`, `additional_restriction`, `identity_activity_metrics`, `permission_analysis_result`, `programmatic_credential`. [#1389](https://github.com/ocsf/ocsf-schema/pull/1389)
  1. Added `port_info` object. [#1466](https://github.com/ocsf/ocsf-schema/pull/1466)

### Improved
* #### Event Classes
  1. Added `Disconnect` and `Reconnect` activities in the `RDP Activity` class. [#1415](https://github.com/ocsf/ocsf-schema/pull/1415)
  1. Added `user` as an attribute to the `RDP Activity` class. [#1419](https://github.com/ocsf/ocsf-schema/pull/1419)
  1. Added `raw_data_hash` as an attribute to `base_event`. [#1420](https://github.com/ocsf/ocsf-schema/pull/1420)
  1. Added `Add Subgroup`, and `Remove Subgroup` activities in the `Group Management` class. [#1447](https://github.com/ocsf/ocsf-schema/pull/1447)
  1. Added `MTA Relay` activity and `to`/`from` attributes to the `Email Activity` class. [#1454](https://github.com/ocsf/ocsf-schema/pull/1454)
  1. Added `http_request` and `http_response` objects to the `File Hosting Activity` Class [#1458](https://github.com/ocsf/ocsf-schema/pull/1458)
  1. Added `Account Switch` activity_id to the `Authentication` class. Added `account_switch_type` and `account_switch_type_id` attributes to the `Authentication` class. [#1460](https://github.com/ocsf/ocsf-schema/pull/1460)
  1. Added `is_src_dst_assignment_known` attribute to `Network Activity` class. [#1464](https://github.com/ocsf/ocsf-schema/pull/1464)
  1. Added `observation_point` and `observation_point_id` to the base `Network` event. [#1481](https://github.com/ocsf/ocsf-schema/pull/1481)

* #### Objects
  1. Added more `algorithm_id` values and references to the `fingerprint` object. [#1412](https://github.com/ocsf/ocsf-schema/pull/1412)
  1. Added xxHash H3's 64-bit and 128-bit variants to `algorithm_id` on the `fingerprint` object. [#1420](https://github.com/ocsf/ocsf-schema/pull/1412)
  1. Added `Service` to `user` `type_id` enum. [#1428](https://github.com/ocsf/ocsf-schema/pull/1428)
  1. Added `Deleted` to `finding` `status_id` enum. [#1437](https://github.com/ocsf/ocsf-schema/pull/1437)
  1. Added `status` to `related_event` object. [#1434](https://github.com/ocsf/ocsf-schema/pull/1434)
  1. Added `attack_graph` to `finding_info`. [#1436](https://github.com/ocsf/ocsf-schema/pull/1436)
  1. Added `Executable File` to `file` `type_id` enum. Added `is_readonly` as an optional attribute. [#1438](https://github.com/ocsf/ocsf-schema/pull/1438)
  1. Added `ptid` (type `long_t`) to `process` and deprecated `tid` (type `integer_t`) [#1450](https://github.com/ocsf/ocsf-schema/pull/1450)
  1. Added `state_id` and `state` to `analytic`. [#1448](https://github.com/ocsf/ocsf-schema/pull/1448)
  1. Added `from_list`, `from_mailboxes`,`reply_to_list`, `return_path`, `sender` and `sender_mailbox` attributes to `email` object. [#1454](https://github.com/ocsf/ocsf-schema/pull/1454)
  1. Added `role`, `role_id` to `resource_details` object, `type` to `policy` object,  [#1389](https://github.com/ocsf/ocsf-schema/pull/1389)
  1. Added `is_truncated` and `untruncated_size` to `metadata`, `logger` objects. [#1461](https://github.com/ocsf/ocsf-schema/pull/1461)
  1. Added `open_ports` to the `network_interface` object. [#1466](https://github.com/ocsf/ocsf-schema/pull/1466)
  1. Added `reg_binary_data`, `reg_integer_data`, `reg_string_data`, `reg_string_list_data` to `reg_value` object in Windows extension. [#1468](https://github.com/ocsf/ocsf-schema/pull/1468)
  1. Added `network_scope` and `network_scope_id` to the `network_endpoint` object. [#1481](https://github.com/ocsf/ocsf-schema/pull/1481)
  

### Misc
  1. Fixed spelling errors throughout the project and added spell checking to the CI linter workflow. [#1411](https://github.com/ocsf/ocsf-schema/pull/1411)
  1. Improved description of the `Application Error` class. [#1424](https://github.com/ocsf/ocsf-schema/pull/1424)
  1. Fixed links to ocsf-docs repo [#1453](https://github.com/ocsf/ocsf-schema/pull/1453)
  1. Set `device.uid` as an Observable type - type_id: 47 [#1446](https://github.com/ocsf/ocsf-schema/pull/1446)
  1. Improved descriptions of `src_endpoint` and `dst_endpoint` attributes in `Network Activity` class. [#1464](https://github.com/ocsf/ocsf-schema/pull/1464)
  1. Improved the description of the `bytestring_t` data type. [#1468](https://github.com/ocsf/ocsf-schema/pull/1468)

### Deprecated
  1. Deprecated usage of `group` attribute in favor of `groups` in the `databucket` object. [#1344](https://github.com/ocsf/ocsf-schema/pull/1344)
  1. Deprecated usage of `credential_uid` attribute in favor of `programmatic_credentials` in the `user` object. [#1389](https://github.com/ocsf/ocsf-schema/pull/1389)
  1. Deprecated usage of items `3` and `4` in the `type_id` enum in `account` object, in favor of the `type_id` enum in the `user` object. [#1389](https://github.com/ocsf/ocsf-schema/pull/1389)
  1. Deprecated item `9` (`REG_QWORD_LITTLE_ENDIAN`) in the `type_id` enum in the `reg_value` object. Its presence was an error. [#1468](https://github.com/ocsf/ocsf-schema/pull/1468)

## [v1.5.0] - April 28th, 2025

### Added
* #### Event Classes
  1. Added `Application Security Posture Finding` event class to the Findings category. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `Live Evidence Info` event class to Discovery category. [#1382](https://github.com/ocsf/ocsf-schema/pull/1382)
* #### Dictionary Attributes
  1. Added `boot_uid` as a `string_t`. [#1335](https://github.com/ocsf/ocsf-schema/pull/1335)
  1. Added `cpid` as a `uuid_t`. [#1246](https://github.com/ocsf/ocsf-schema/pull/1246)
  1. Added `raw_data_size` as a `long_t`. [#1347](https://github.com/ocsf/ocsf-schema/pull/1347)
  1. Added `assessments` as an array of `assessment` objects. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `meets_criteria` as a `boolean_t`. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `display_name` attribute as a `string_t`. [#1341](https://github.com/ocsf/ocsf-schema/pull/1341)
  1. Added `is_directed` as a `boolean_t`, `relation` as a `string_t`, `query_language` & `query_language_id` a sibling pair. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `resource_relationship` of type `graph`, `nodes` of type `node`, `edges` of type `edge`. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `fix_coverage` as `string_t` and `fix_coverage_id` as `int_t`. [#1350](https://github.com/ocsf/ocsf-schema/pull/1350)
  1. Added `eid`, `iccid`, and `meid` as `string_t`. [#1346](https://github.com/ocsf/ocsf-schema/pull/1346)
  1. Added `is_backed_up`, `is_mobile_account_active`, and `is_shared` as `boolean_t`. [#1346](https://github.com/ocsf/ocsf-schema/pull/1346)
  1. Added `detection_pattern_type` an `detection_pattern_type_id` as a `string_t` and `int_t` respectively. [#1310](https://github.com/ocsf/ocsf-schema/pull/1310)
  1. Added `external_id` as an `string_t`. [#1310](https://github.com/ocsf/ocsf-schema/pull/1310)
  1. Added `intrusion_sets` as an array `string_t`. [#1310](https://github.com/ocsf/ocsf-schema/pull/1310)
  1. Added `uploaded_time` as an `timestamp_t`. [#1310](https://github.com/ocsf/ocsf-schema/pull/1310)
  1. Added `isp_org` as `string_t`. [#1351](https://github.com/ocsf/ocsf-schema/pull/1351)
  1. Added `ldap` protocol to `auth_protocol_id` enum. [#1359](https://github.com/ocsf/ocsf-schema/pull/1359)
  1. Added `observation_parameter`, `observation_type`, `observed_pattern` as `string_t` and `occurrences` as an array of `occurrence_details`. [#1358](https://github.com/ocsf/ocsf-schema/pull/1358)
  1. Added `analysis_targets` as an array of type `analysis_target`. [#1371](https://github.com/ocsf/ocsf-schema/pull/1371)
  1. Added `num_volumes`, `num_infected` as `int_t`, `unique_malware_count`, `volume` as `string_t`. [#1373](https://github.com/ocsf/ocsf-schema/pull/1373)
  1. Added `end_column` and `start_column` as `integer_t`. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `dependency_chain`, `exploit_requirement`, and `exploit_type` as `string_t`. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `exploit_ref_url`, `license_url`, `package_manager_url`, and `uri` as `url_t`. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `transformation_info_list` [#1392](https://github.com/ocsf/ocsf-schema/pull/1392)
  1. Added `authentication_token` as `authentication_token`, `kerberos_flags` as `string_t` and `is_renewable` as `boolean_t`. [#1391](https://github.com/ocsf/ocsf-schema/pull/1391)
  1. Added `tickets` as an array of `ticket` objects. [#1402](https://github.com/ocsf/ocsf-schema/pull/1402)
  1. Added `is_read` as `boolean_t`. [#1406](https://github.com/ocsf/ocsf-schema/pull/1406)
  1. Added `query_type` and `query_type_id` as `string` and `integer_t` respectively. [#1382](https://github.com/ocsf/ocsf-schema/pull/1382)
  1. Added `tcp_state_id` as `integer_t`. [#1382](https://github.com/ocsf/ocsf-schema/pull/1382)
  1. Added `query_evidence` as type `query_evidence`. [#1382](https://github.com/ocsf/ocsf-schema/pull/1382)
  1. Added `checks` as type `check`. [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)
  1. Added 'is_readonly' as type `boolean_t` with a "See specific usage" description. [#1438](https://github.com/ocsf/ocsf-schema/pull/1438)
* #### Objects
  1. Added `assessment` object to capture evaluations/assessments of configurations/signals. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `node`, `edge`, `graph` objects. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `anomaly`, `anomaly_analysis`, `baseline`, `observation` objects. [#1358](https://github.com/ocsf/ocsf-schema/pull/1358)
  1. Added `trait` object. [#1363](https://github.com/ocsf/ocsf-schema/pull/1363)
  1. Added `mitigation` object. [#1348](https://github.com/ocsf/ocsf-schema/pull/1348)
  1. Added `analysis_target` object. [#1371](https://github.com/ocsf/ocsf-schema/pull/1371)
  1. Added `malware_scan_info` object. [#1373](https://github.com/ocsf/ocsf-schema/pull/1373)
  1. Added `application` object. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `campaign` object [#1310](https://github.com/ocsf/ocsf-schema/pull/1310)
  1. Added `threat_actor` object [#1310](https://github.com/ocsf/ocsf-schema/pull/1310)
  1. Added `transformation_info` [#1392](https://github.com/ocsf/ocsf-schema/pull/1392)
  1. Added `authentication_token` object. [#1391](https://github.com/ocsf/ocsf-schema/pull/1391)
  1. Added `query_evidence` object. [#1382](https://github.com/ocsf/ocsf-schema/pull/1382)
  1. Added `check` object [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)
* #### Observables
  1. Added `process_entity.uid` as an Observable type - `type_id: 39`. [#1380](https://github.com/ocsf/ocsf-schema/pull/1380)
  1. Added `email.subject` and `email.uid` as an Observable types - `type_id: 40` and `type_id: 41`. [#1380](https://github.com/ocsf/ocsf-schema/pull/1380)
  1. Added `message_uid` as Observable type - `type_id: 42`. [#1380](https://github.com/ocsf/ocsf-schema/pull/1380)
  1. Added `reg_value.name` as an Observable type - `type_id: 43`. [#1380](https://github.com/ocsf/ocsf-schema/pull/1380)
  1. Added `advisory.uid` as Observable type `type_id: 44`. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Updated `resource_details.uid`, `web_resource.uid`, and `win_resource.uid` to be observable `type_id: 10` [#1394](https://github.com/ocsf/ocsf-schema/pull/1394)
  1. Added `file_path_t` as an Observable type - `type_id: 45` and marked fields as this type [#1381](https://github.com/ocsf/ocsf-schema/pull/1381)
     - `lineage` dictionary attribute
     - `affected_package.path` object attribute
     - `file.path` object attribute
     - `image.path` object attribute
     - `kernel.path` object attribute
     - `malware.path` object attribute
     - `process_entity.path` object attribute
  1. Added `extensions/windows/reg_key_path_t` as an Observable type - `type_id: 46` and marked fields as this type [#1381](https://github.com/ocsf/ocsf-schema/pull/1381)
     - `reg_key.path` object attribute
     - `reg_value.path` object attribute


### Improved
* #### Event Classes
  1. Added `assessments` to `config_state`. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `raw_data_size` to `base_event`. [#1347](https://github.com/ocsf/ocsf-schema/pull/1347)
  1. Added `anomaly_analyses` to `detection_finding`. [#1358](https://github.com/ocsf/ocsf-schema/pull/1358)
  1. Added `Detect` value for `activity_id` in Remediation events. [#1362](https://github.com/ocsf/ocsf-schema/pull/1362)
  1. Added `resources` to `user_access`. [#1374](https://github.com/ocsf/ocsf-schema/pull/1374)
  1. Added `malware_scan_info`, `malware` to `detection_finding`. [#1373](https://github.com/ocsf/ocsf-schema/pull/1373)
  1. Added `authentication_token` to `authentication`. [#1391](https://github.com/ocsf/ocsf-schema/pull/1391)

* #### Objects
  1. Added `boot_uid` to `device` object. [#1335](https://github.com/ocsf/ocsf-schema/pull/1335)
  1. Relaxed constraint to provide `email_addr`, `phone_number`, or `security_questions` on `auth_factor`. [#1339](https://github.com/ocsf/ocsf-schema/pull/1339)
  1. Added `cpid` to `process_entity` object. [#1246](https://github.com/ocsf/ocsf-schema/pull/1246)
  1. Added `boot_uid` to `device` object. [#1335](https://github.com/ocsf/ocsf-schema/pull/1335)
  1. Added `meets_criteria` and `policy` to `assessment` object. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `assessments` to `compliance` object. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `data` to `policy` object. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `display_name` attribute to the `user` and `ldap_person` objects. [#1341](https://github.com/ocsf/ocsf-schema/pull/1341)
  1. Added `resource_relationship` to `resource_details` object. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Added `fix_coverage`, `fix_coverage_id` to `vulnerability` object. [#1350](https://github.com/ocsf/ocsf-schema/pull/1350)
  1. Added `eid`, `iccid`, `is_backed_up`, `is_mobile_account_active`, `is_shared`, and `meid` to `device`. [#1346](https://github.com/ocsf/ocsf-schema/pull/1346)
  1. Added `is_backed_up` to `resource_details`. [#1346](https://github.com/ocsf/ocsf-schema/pull/1346)
  1. Added `isp`, `isp_org` to `network_endpoint` & `whois` objects. [#1351](https://github.com/ocsf/ocsf-schema/pull/1351)
  1. Reduced requirement of `standards` to recommended in the `compliance` object. [#1352](https://github.com/ocsf/ocsf-schema/pull/1352)
  1. Updated MITRE `attack`, `tactic`, `technique`, `subtechnique` captions, descriptions, references to include MITRE ATLAS. Used standard requirements for `_entity` extended objects. [#1355](https://github.com/ocsf/ocsf-schema/pull/1355).
  1. Added `name`, `resources`, `uid`, `verdict`, and `verdict_id` to `evidences`. [#1337](https://github.com/ocsf/ocsf-schema/pull/1337)
  1. Added `algorithm` to `analytic` object. [#1358](https://github.com/ocsf/ocsf-schema/pull/1358)
  1. Added 'Network Zone' type to the `managed_entity` object enum list. [#1364](https://github.com/ocsf/ocsf-schema/pull/1364)
  1. Added 'count' `start_time` `end_time` to `timespan` object. [#1365](https://github.com/ocsf/ocsf-schema/pull/1365)
  1. Added `traits` to `related_event` object. [#1363](https://github.com/ocsf/ocsf-schema/pull/1363)
  1. Updated `timespan` to include a Time Window `type_id` and `start_time`, `end_time` to the `at_least_one` constraint. [#1372](https://github.com/ocsf/ocsf-schema/pull/1372)
  1. Added `mitigation` to `attack` object. [#1348](https://github.com/ocsf/ocsf-schema/pull/1348)
  1. Added `timespan` object to `observation` object. [#1371](https://github.com/ocsf/ocsf-schema/pull/1371)
  1. Added `end_column`, `rule`, and `start_column` to `affected_code` object. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `category` and `desc` to `compliance` object. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `uri` to the `file` object. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `license_url`, `package_manager`, `package_manager_url`, `src_url`, and `uid` to `package` object. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `type`, `type_id`, `uid`, and `version` to `sbom` object. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `category`, `dependency_chain`, `exploit_ref_url`, `exploit_requirement`, and `exploit_type` to `vulnerability` object. [#1357](https://github.com/ocsf/ocsf-schema/pull/1357)
  1. Added `status`, `status_id`, `status_details` to `ticket` object; `uid_alt`, `created_time` to `_resource` object; `traits` to `finding_info` object. [#1402](https://github.com/ocsf/ocsf-schema/pull/1402)
  1. Added `modified_time` to `_resource` object; `zone` to `resource_details` object. [#1403](https://github.com/ocsf/ocsf-schema/pull/1403)
  1. Added `countermeasures` to `mitigation` object. [#1348](https://github.com/ocsf/ocsf-schema/pull/1348)
  1. Added `is_read` to `email` object. [#1406](https://github.com/ocsf/ocsf-schema/pull/1406)
  1. Added `cis_controls` to `remediation` object [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)
  1. Added `check` object to `compliance` object [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)
  1. Added `Patch` as a value of `http_method` in the `http_request` object. [#1427](https://github.com/ocsf/ocsf-schema/pull/1427)

* #### Profiles
  1. Added `malware_scan_info` to `security_control` profile. [#1373](https://github.com/ocsf/ocsf-schema/pull/1373)
  1. Added `campaign`, `category`, `created_time`, `creator`, `desc`, `expiration_time`, `external_id`, `labels`, `malware`, `modified_time`, `name`, `detection_pattern`, `detection_pattern_type`, `detection_pattern_type_id`, `intrusion_sets`, `risk_score`, `references`, `uploaded_time`, `severity`, `uid` and `threat_actor` to `osint` object. [#1310](https://github.com/ocsf/ocsf-schema/pull/1310)
  1. Added `tickets` to `incident` profile. [#1402](https://github.com/ocsf/ocsf-schema/pull/1402)

### Deprecated
  1. Deprecated usage of `isp` attribute in the `location` object. [#1351](https://github.com/ocsf/ocsf-schema/pull/1351)
  1. Deprecated usage of `occurrence_details` in favor of `occurrences` in `discovery_details` object. [#1358](https://github.com/ocsf/ocsf-schema/pull/1358)
  1. Deprecated usage of `resource` in favor of `resources` in the `user_access` class. [#1374](https://github.com/ocsf/ocsf-schema/pull/1374)
  1. Deprecated usage of `ticket` in favor of `tickets` in `incident` profile and `incident_finding` event class. [#1402](https://github.com/ocsf/ocsf-schema/pull/1402)
  1. Deprecated `kernel_object_query`, `file_query`, `folder_query`, `admin_group_query`, `job_query`, `module_query`, `network_connection_query`, `networks_query`, `peripheral_device_query`, `process_query`, `service_query`, `user_session_query`, `user_query`, `startup_item_query`, `registry_key_query`, `registry_value_query`, and `prefetch_query` classes in favor of the `live_evidence_info` class. [#1382](https://github.com/ocsf/ocsf-schema/pull/1382)
  1. Deprecated `compliance_references` and `compliance_standards` in favor of the `check` object. [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)
  1. Deprecated `cis_csc` in favor of `cis_control` object. [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)
  1. Deprecated the `Device Config State` class in favor of the `Compliance Finding` class. [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)

### Misc
  1. Updated description of `config_state` to reflect the addition of the `assessments` object. [#1343](https://github.com/ocsf/ocsf-schema/pull/1343)
  1. Updated description of `hw_info.uuid` to clarify usage especially in presence of new `device.udid` field. [#1354](https://github.com/ocsf/ocsf-schema/pull/1354)
  1. Updated dictionary descriptions and references of MITRE `attacks`, `tactic`, `technique`, `subtechnique`. [#1355](https://github.com/ocsf/ocsf-schema/pull/1355)
  1. Added enhanced descriptions and references to `requirements`, `standards`, `control_parameters`, and `control` in the `compliance` object for clarity and usage. [#1369](https://github.com/ocsf/ocsf-schema/pull/1369)

## [v1.4.0] - January 31st, 2025

### Added
* #### Categories
    1. Added new `Unmanned Systems` Category. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
* #### Event Classes
    1. Added `OSINT Inventory Info` event class to the Discovery category. [#1154](https://github.com/ocsf/ocsf-schema/pull/1154)
    1. Added `Script Activity` event class to the System category. [#1159](https://github.com/ocsf/ocsf-schema/pull/1159)
    1. Added `Startup Item Query` event class. [#1119](https://github.com/ocsf/ocsf-schema/pull/1119)
    1. Added `Drone Flights Activity` event class to the Unmanned Systems category. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added `Cloud Resources Inventory Info` event class to the Discovery category. [#1250](https://github.com/ocsf/ocsf-schema/pull/1250)
    1. Added `Airborne Broadcast Activity` event class to the Unmanned Systems category. [#1253](https://github.com/ocsf/ocsf-schema/pull/1253)
    1. Added `Application Error` event class to the Application Activity category. [#1299](https://github.com/ocsf/ocsf-schema/pull/1299)
* #### Profiles
    1. Added `incident` profile. [#1293](https://github.com/ocsf/ocsf-schema/pull/1293)
* #### Dictionary Attributes
    1. Added `has_mfa` as a `boolean_t`. [#1155](https://github.com/ocsf/ocsf-schema/pull/1155)
    1. Added `environment_variables` as an array of `environment_variable` object. [#1172](https://github.com/ocsf/ocsf-schema/pull/1172)
    1. Added `forward_addr` as an `email_t`. [#1179](https://github.com/ocsf/ocsf-schema/pull/1179)
    1. Added `related_cves`, `related_cwes` as arrays of `cve`, `cwe` objects respectively. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
    1. Added `exploit_last_seen_time` as a `timestamp_t`. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
    1. Added `is_alert` as a `boolean_t`. [#1179](https://github.com/ocsf/ocsf-schema/pull/1179)
    1. Added `working_directory` as a `string_t`. [#1195](https://github.com/ocsf/ocsf-schema/pull/1195)
    1. Added `is_deleted` as a `boolean_t`. [#1196](https://github.com/ocsf/ocsf-schema/pull/1196)
    1. Added `body_length` as an `integer_t`. [#1200](https://github.com/ocsf/ocsf-schema/pull/1200)
    1. Added `is_public` as a `boolean_t`. [#1208](https://github.com/ocsf/ocsf-schema/pull/1208)
    1. Added `tags`, `control_parameters` as an array of `key_value_object` object. [#1219](https://github.com/ocsf/ocsf-schema/pull/1219)
    1. Added `community_uid` as a `string_t`. [#1202](https://github.com/ocsf/ocsf-schema/pull/1202)
    1. Added `location` to the `managed_entity` object. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added `unmanned_system_operator` to the dictionary, extends `user`. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added `locations` to the dictionary, an array type of the `location` object, used within the new `operating_area` object. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added `altitude_ceiling`, `altitude_floor`, `geodetic_altitude`, `aerial_height`, `horizontal_accuracy`, `pressure_altitude`, `radius`, `speed`, `track_direction`, and `vertical_speed` all to support `operating_area` and `unmanned_aerial_system` objects. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added `imei_list` as an array `string_t`. [#1225](https://github.com/ocsf/ocsf-schema/pull/1225)
    1. Added `is_encrypted` as `boolean_t`; `column_name`, `cell_name`, `storage_class`, `key_uid`, `json_path` as `string_t` & `column_number`, `row_number`, `page_number`, `record_index_in_array` as `integer_t`. [#1245](https://github.com/ocsf/ocsf-schema/pull/1245)
    1. Added `group_provisioning_enabled`, `scim_group_schema`, `user_provisioning_enabled`, `scim_user_schema`, `scopes`, `idle_timeout`, `login_endpoint`, `logout_endpoint`, and `metadata_url` entries to the dictionary to support the new `scim` and `sso` objects. [#1239](https://github.com/ocsf/ocsf-schema/pull/1239)
    1. Added new `11: Basic Authentication` enum value to `auth_protocol_id`. [#1239](https://github.com/ocsf/ocsf-schema/pull/1239)
    1. Added `values` as an array of `string_t`. [#1251](https://github.com/ocsf/ocsf-schema/pull/1251)
    1. Added `files` `urls` and `message_trace_uid`. [#1259](https://github.com/ocsf/ocsf-schema/pull/1259)
    1. Added `kernel_release` as a `string_t`. [#1249](https://github.com/ocsf/ocsf-schema/pull/1249)
    1. Added `os_machine_uuid` as a `uuid_t`.  [#1268](https://github.com/ocsf/ocsf-schema/pull/1268)
    1. Added `sbom`, `author`, `related_component`, `relationship`, `relationship_id` and `software_component` to support SBOMs. [#1262](https://github.com/ocsf/ocsf-schema/pull/1262)
    1. Added `related_events_count` as an `int_t`. [#1271](https://github.com/ocsf/ocsf-schema/pull/1271)
    1. Added `event_uid` as a `string_t`. [#1312](https://github.com/ocsf/ocsf-schema/pull/1312)
    1. Added `debug` attribute as a `string_t` array, used in the `metadata` object. [#1308](https://github.com/ocsf/ocsf-schema/pull/1308)
    1. Added `ancestry` as a list of `process_entity`. [#1317](https://github.com/ocsf/ocsf-schema/pull/1317)
    1. Added `internal_name` as a `string_t`. [#1322](https://github.com/ocsf/ocsf-schema/pull/1322)
    1. Added `cc_mailboxes`, `from_mailbox`, `to_mailboxes`, `delivered_to_list` and `reply_to_mailboxes`. [#1307](https://github.com/ocsf/ocsf-schema/pull/1307)
    1. Added `flag_history` and `bytes_missed` attributes. [#1316](https://github.com/ocsf/ocsf-schema/pull/1316)
* #### Objects
    1. Added `environment_variable` object. [#1172](https://github.com/ocsf/ocsf-schema/pull/1172), [#1288](https://github.com/ocsf/ocsf-schema/pull/1288)
    1. Added `advisory` object. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
    1. Added a generic `key_value_object` object. [#1219](https://github.com/ocsf/ocsf-schema/pull/1219)
    1. Added `unmanned_aerial_system` and `unmanned_system_operating_area` objects. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added a `long_string` object. [#1228](https://github.com/ocsf/ocsf-schema/pull/1228)
    1. Added `discovery_details`, `encryption_details`, `occurrence_details` objects. [#1245](https://github.com/ocsf/ocsf-schema/pull/1245)
    1. Added `scim` object. [#1239](https://github.com/ocsf/ocsf-schema/pull/1239)
    1. Added `sso` object. [#1239](https://github.com/ocsf/ocsf-schema/pull/1239)
    1. Added `vendor_attributes` object. [#1257](https://github.com/ocsf/ocsf-schema/pull/1257)
    1. Added `aircraft` object. [#1253](https://github.com/ocsf/ocsf-schema/pull/1253)
    1. Added `software_component` and `sbom` objects. [#1262](https://github.com/ocsf/ocsf-schema/pull/1262)
    1. Added `drive_type` and `drive_type_id` objects. [#1287](https://github.com/ocsf/ocsf-schema/pull/1287)
    1. Added `cpu_architecture` and `cpu_architecture_id` objects. [#1278](https://github.com/ocsf/ocsf-schema/pull/1278)
    1. Added `process_entity` object. [#1317](https://github.com/ocsf/ocsf-schema/pull/1317)

### Improved
* #### Event Classes
    1. Added `evidences` to `compliance_finding` class. [#1157](https://github.com/ocsf/ocsf-schema/pull/1157)
    1. Added `is_alert` to `detection_finding` and `data_security_finding` classes. [#1178](https://github.com/ocsf/ocsf-schema/pull/1178)
    1. Added `risk_details` to `data_security_finding` class. [#1178](https://github.com/ocsf/ocsf-schema/pull/1178)
    1. Removed constraint from `group_management` class. [#1193](https://github.com/ocsf/ocsf-schema/pull/1193)
    1. Added `Archived|5` as an enum item to `status_id` attribute in Findings classes. [#1219](https://github.com/ocsf/ocsf-schema/pull/1219)
    1. Added a `Trace` `activity_id` to the `Email Activity` class. [#1252](https://github.com/ocsf/ocsf-schema/pull/1252)
    1. Added a `message_trace_uid` to the `Email Activity` class. [#1259](https://github.com/ocsf/ocsf-schema/pull/1259)
    1. Added `vendor_attributes` to all `Findings` Category classes. [#1257](https://github.com/ocsf/ocsf-schema/pull/1257)
    1. Added `sbom` to `Software Inventory Info` class. [#1262](https://github.com/ocsf/ocsf-schema/pull/1262)
    1. Relaxed requirements on the `dst_endpoint` attribute in the `network_activity` event class and added an `at_least_one` constraint with `src_endpoint` and `dst_endpoint`. [#1274](https://github.com/ocsf/ocsf-schema/pull/1274)
    1. Relaxed requirements on the `http_request` and `http_response` attributes in the `http_activity` event class and added an `at_least_one` constraint with these attributes. [#1274](https://github.com/ocsf/ocsf-schema/pull/1274)
    1. Added `host` profile to `base_event` and removed this profile elsewhere in the event hierarchy. [#1280](https://github.com/ocsf/ocsf-schema/pull/1280)
    1. Added the `actor` attribute to the IAM base event. [#1280](https://github.com/ocsf/ocsf-schema/pull/1280)
    1. Added `security_control` profile to `base_event` and removed this profile elsewhere in the event hierarchy. [#1281](https://github.com/ocsf/ocsf-schema/pull/1281)
    1. Added `policies` to `Account Change` class. [#1282](https://github.com/ocsf/ocsf-schema/pull/1282)
    1. Added `Unlock` activity to `account_change` class. [#1285](https://github.com/ocsf/ocsf-schema/pull/1285)
    1. Added `incident` profile to `finding` to affect classes that extend it. [#1293](https://github.com/ocsf/ocsf-schema/pull/1293)
    1. Added `keyboard_info` object to RDP event class. [#1313](https://github.com/ocsf/ocsf-schema/pull/1313)
    1. Added attributes and a new Activity ID to the `File Hosting Activity` class for network file share services and authorization check result. Activity ID added: `17` - "Access Check". Optional `context` group attributes added: `access_list`, `access_mask`, `access_result`, `share`, `share_type`, and `share_type_id`. [#1315](https://github.com/ocsf/ocsf-schema/pull/1315)
    1. Added `command` and `protocol_name` to Email Activity event class. [#1307](https://github.com/ocsf/ocsf-schema/pull/1307)
* #### Profiles
    1. Added `is_alert`, `confidence_id`, `confidence`, `confidence_score` attributes to the `security_control` profile. [#1178](https://github.com/ocsf/ocsf-schema/pull/1178)
    1. Added `risk_level_id`, `risk_level`, `risk_score`, `risk_details` attributes to the `security_control` profile.  [#1178](https://github.com/ocsf/ocsf-schema/pull/1178)
    1. Added `policy` attribute to the `security_control` profile. [#1178](https://github.com/ocsf/ocsf-schema/pull/1178)
    1. Added enum values to `action_id` of 'Observed', 'Modified', and 'Unknown'. [#1265](https://github.com/ocsf/ocsf-schema/pull/1265)
    1. Updated `action_id` optionality to `recommended` in the `security_control` profile [#1281](https://github.com/ocsf/ocsf-schema/pull/1281)
* #### Objects
    1. Added `phone_number` to `user` and `ldap_person` objects. [#1155](https://github.com/ocsf/ocsf-schema/pull/1155)
    1. Added `has_mfa` to `user` object. [#1155](https://github.com/ocsf/ocsf-schema/pull/1155)
    1. Added `vendor_name` to `cvss` object. [#1165](https://github.com/ocsf/ocsf-schema/pull/1165)
    1. Added `file`, `reputation`, `subnet`, and `script` to `osint` object. [#1168](https://github.com/ocsf/ocsf-schema/pull/1168)
    1. Added `environment_variables` attribute to the `process` object. [#1172](https://github.com/ocsf/ocsf-schema/pull/1172)
    1. Added `forward_addr` to the `user` object. [#1179](https://github.com/ocsf/ocsf-schema/pull/1179)
    1. Added `src_url` to the `cvss` object. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
    1. Added `advisory`, `exploit_last_seen_time` to the `vulnerability` object. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
    1. Added `related_cwes` to the `cve` object. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
    1. Added `vendor_name` and `model` to `device` object. [#1188](https://github.com/ocsf/ocsf-schema/pull/1188)
    1. Added `http_headers` to `email` object. [#1199](https://github.com/ocsf/ocsf-schema/pull/1199)
    1. Added `working_directory` to `process` object. [#1195](https://github.com/ocsf/ocsf-schema/pull/1195)
    1. Added `is_deleted` to `file` object. [#1196](https://github.com/ocsf/ocsf-schema/pull/1196)
    1. Added entry for VBA macros to `type_id` enum in `script` object. [#1198](https://github.com/ocsf/ocsf-schema/pull/1198)
    1. Added `body_length` to the `http_response` and `http_request` objects. [#1200](https://github.com/ocsf/ocsf-schema/pull/1200)
    1. Added `is_public` to the `databucket` object. [#1208](https://github.com/ocsf/ocsf-schema/pull/1208)
    1. Added `tags` to the `account`, `container`, `image`, `ldap_person`, `metadata`, `resource_details`, `service`, `web_resource` objects. [#1207](https://github.com/ocsf/ocsf-schema/pull/1207)
    1. Added `domain` as a constraint to `network_endpoint` object. [#1224](https://github.com/ocsf/ocsf-schema/pull/1224)
    1. Added `http_request` and `http_response` to the evidences object. [#1212](https://github.com/ocsf/ocsf-schema/pull/1212)
    1. Added `control_parameters` and `status_details` to the compliance object. [#1219](https://github.com/ocsf/ocsf-schema/pull/1219)
    1. Added `geodetic_altitude`, `height`, `horizontal_accuracy`, and `pressure_altitude` to `location`. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added `location` to `managed_entity`. [#1169](https://github.com/ocsf/ocsf-schema/pull/1169)
    1. Added `imei_list` to the `device` object. [#1225](https://github.com/ocsf/ocsf-schema/pull/1225)
    1. Added `tls` and `ja4_fingerprint_list` object to the evidences object. [#1244](https://github.com/ocsf/ocsf-schema/pull/1244)
    1. Added `storage_class` & `is_public` as `cloud` profile attributes to `file` object. Also added `is_encrypted`, `encryption_details`, `tags` to the `file` object. [#1245](https://github.com/ocsf/ocsf-schema/pull/1245)
    1. Added `discovery_details`, `occurrence_details`, `status` trio, `total`, `uid`, `size`, & `src_url` to the `data_classification` object. [#1245](https://github.com/ocsf/ocsf-schema/pull/1245)
    1. `data_bucket` object now inherits `resource_details` instead of `_entity`. Also, added `encryption_details` object to the `data_bucket` object. [#1245](https://github.com/ocsf/ocsf-schema/pull/1245)
    1. Added `auth_factors`, `domain`, `fingerprint`, `has_mfa`, `issuer`, `protocol_name`, `scim`, `sso`, `state`, `state_id`, `tenant_uid`, and `uid` to `idp`. [#1239](https://github.com/ocsf/ocsf-schema/pull/1239)
    1. Added `hostname`, `ip`, and `name` to `resource_details` for purposes of assigning an Observable number. [#1250](https://github.com/ocsf/ocsf-schema/pull/1250)
    1. Added `values` to `key_value_object`. [#1251](https://github.com/ocsf/ocsf-schema/pull/1251)
    1. Added `files`, `urls`, to the `email` object. Relaxed requirements on the `from` and `to` attributes of the object and added the `at_least_one` constraint. [#1259](https://github.com/ocsf/ocsf-schema/pull/1259)
    1. Added `kernel_release` to `os` object. [#1249](https://github.com/ocsf/ocsf-schema/pull/1249)
    1. Added `related_analytics` to `osint` object. [#1264](https://github.com/ocsf/ocsf-schema/pull/1264)
    1. Added `os_machine_uuid` to the `device` object. [#1268](https://github.com/ocsf/ocsf-schema/pull/1268)
    1. Added `uuid` to the `device_hw_info` object. [#1268](https://github.com/ocsf/ocsf-schema/pull/1268)
    1. `unmanned_aerial_system` now extends from `aircraft`. [#1253](https://github.com/ocsf/ocsf-schema/pull/1253)
    1. Added `references` metadata for `win/reg_key`, `win/reg_value`, `account`, `container`, `database`, `fingerprint`, `group`, `http_cookie`, `job`, `script` objects. [#1266](https://github.com/ocsf/ocsf-schema/pull/1266)
    1. Added `cloud_partition` to the `cloud` object. [#1271](https://github.com/ocsf/ocsf-schema/pull/1271)
    1. Added `product`, `related_events_count`, `uid_alt`, `tags` to `finding_info` object. [#1271](https://github.com/ocsf/ocsf-schema/pull/1271)
    1. Added `count`, `created_time`, `desc`, `first_seen_time`, `last_seen_time`, `modified_time`, `product`, `severity`, `severity_id`, `tags` & `title` to `related_event` object. [#1271](https://github.com/ocsf/ocsf-schema/pull/1271)
    1. Added `drive_type` and `drive_type_id` to the `file` object. [#1287](https://github.com/ocsf/ocsf-schema/pull/1287)
    1. Added `cpu_architecture` and `cpu_architecture_id` to `device_hw_info` object. [#1278](https://github.com/ocsf/ocsf-schema/pull/1278)
    1. Added `name` to `script` object. [#1284](https://github.com/ocsf/ocsf-schema/pull/1284)
    1. Relax requirement of `fingerprints` in `certificate` object. [#1302](https://github.com/ocsf/ocsf-schema/pull/1302)
    1. Added `event_uid` to the `logger` object. [#1312](https://github.com/ocsf/ocsf-schema/pull/1312)
    1. Added `debug` attribute to `metadata` object. [#1308](https://github.com/ocsf/ocsf-schema/pull/1308)
    1. Added optional `url` attribute to the `file` object. This allows capturing a file's URL in the File Hosting Activity (6006) event class. [#1289](https://github.com/ocsf/ocsf-schema/pull/1289)
    1. Changed the `process` object to extend the `process_entity` object. [#1317](https://github.com/ocsf/ocsf-schema/pull/1317)
    1. Added `ancestry` to the `process` object. [#1317](https://github.com/ocsf/ocsf-schema/pull/1317)
    1. Added `internal_name` to the `file` object. [#1322](https://github.com/ocsf/ocsf-schema/pull/1322)
    1. Added `cc_mailboxes`, `from_mailbox`, `to_mailboxes`, `delivered_to_list` and `reply_to_mailboxes` to `email` object. [#1307](https://github.com/ocsf/ocsf-schema/pull/1307)
    1. Added `sans` array to `certificate` object. [#1325](https://github.com/ocsf/ocsf-schema/pull/1325)
    1. Added `flag_history` attribute to the `network_connection_info` object. [#1316](https://github.com/ocsf/ocsf-schema/pull/1316)
    1. Added `bytes_missed` attribute to the `network_traffic` object. [#1316](https://github.com/ocsf/ocsf-schema/pull/1316)

### Bugfixes
1. Added sibling definition to `confidence_id` in dictionary, accurately associating `confidence` as its sibling. [#1180](https://github.com/ocsf/ocsf-schema/pull/1180)
1. Added a fix (profile: null) to `OSINT Inventory Info` so that the `osint` attribute is present w/o the OSINT profile, per the class definition.
1. Added `http_response` to all classes that have `http_request`, but no `http_response` object. [#1200](https://github.com/ocsf/ocsf-schema/pull/1200)
1. Removed redundant `name` attribute from Windows extension to the `startup_item` object for consistency with other extensions. [#1203](https://github.com/ocsf/ocsf-schema/pull/1203)
1. Changed `activity_id` requirement from `optional` to `required` in `email_activity`, `email_file_activity` and `email_url_activity` classes. [#1307](https://github.com/ocsf/ocsf-schema/pull/1307)

### Deprecated
1. Deprecated `project_uid` in favor of `account.uid`. [#1166](https://github.com/ocsf/ocsf-schema/pull/1166)
1. Deprecated `kb_article_list` in favor of `advisory` in the vulnerability object. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
1. Deprecated `cwe` in favor of `related_cwes` in the `cve` object. [#1176](https://github.com/ocsf/ocsf-schema/pull/1176)
1. Deprecated `tag` in favor of `labels` or `tags` in `image` & `container` object. [#1207](https://github.com/ocsf/ocsf-schema/pull/1207)
1. Deprecated `status_detail` in favor of `status_details` in `compliance` object. [#1219](https://github.com/ocsf/ocsf-schema/pull/1219)
1. Deprecated `imei` in favor of `imei_list` in `device` object. [#1225](https://github.com/ocsf/ocsf-schema/pull/1225)
1. Deprecated `data_classification` in favor of `data_classifications` in the `data_classification` profile. [#1245](https://github.com/ocsf/ocsf-schema/pull/1245)
1. Deprecated activity_id `4|Suppressed` in the Data Security Finding event class. This shouldn't have been added when we first created it, as the right place for this info is `status_id`. [#1245](https://github.com/ocsf/ocsf-schema/pull/1245)
1. Deprecated `email_file_activity` and `email_url_activity` in favor of updated `email_activity`. [#1259](https://github.com/ocsf/ocsf-schema/pull/1259)
1. Deprecated `package` in `Software Inventory Info` in favour of `sbom`. [#1262](https://github.com/ocsf/ocsf-schema/pull/1262)
1. Deprecated `product_uid` in favor of the `product` object. [#1271](https://github.com/ocsf/ocsf-schema/pull/1271)
1. Deprecated `policy` in favor of `policies` in `Account Change` class. [#1282](https://github.com/ocsf/ocsf-schema/pull/1282)
1. Deprecated `lineage` in the `process` object. [#1317](https://github.com/ocsf/ocsf-schema/pull/1317)
1. Deprecated `smtp_hello`, `smtp_from`, `smtp_to`, `delivered_to` and `reply_to` in favor of `command`, `from`, `to`, `delivered_to_list` and `reply_to_mailboxes` respectively. [#1307](https://github.com/ocsf/ocsf-schema/pull/1307)
1. Deprecated `tls.sans` array in favor of added `tls.certificate.sans` array. [#1325](https://github.com/ocsf/ocsf-schema/pull/1325)

### Misc
1. Added `user.uid` as an Observable type - `type_id: 31`. [#1155](https://github.com/ocsf/ocsf-schema/pull/1155)
1. Added `group.name` and `group.uid` as Observable types - `type_id: 32` and `type_id: 33`, respectively. [#1155](https://github.com/ocsf/ocsf-schema/pull/1155)
1. Added `account.name` and `account.uid` as Observable types - `type_id: 34` and `type_id: 35`, respectively. [#1155](https://github.com/ocsf/ocsf-schema/pull/1155)
1. Added new enumeration items to `account.type_id`. [#1166](https://github.com/ocsf/ocsf-schema/pull/1166)
1. Cleaned up event class definition files, removed /includes dir, simplified definition of `base_event`. [#1167](https://github.com/ocsf/ocsf-schema/pull/1167), [#1171](https://github.com/ocsf/ocsf-schema/pull/1171)
1. Added new `file` enum to `osint.type_id`. [#1168](https://github.com/ocsf/ocsf-schema/pull/1168)
1. Relaxed data-type constraints for `file_hash_t`, `resource_uid_t` & `string_t`. Fixed regex for `datetime_t`. [#1174](https://github.com/ocsf/ocsf-schema/pull/1174)
1. Added new `Email Account` enum to `account.type_id`. [#1179](https://github.com/ocsf/ocsf-schema/pull/1179)
1. Removing regex for `hostname_t`, considering the vast variance in its values. [#1182](https://github.com/ocsf/ocsf-schema/pull/1182)
1. In the metaschema, added support for additional metadata fields: `source` and `references`. [#1189](https://github.com/ocsf/ocsf-schema/pull/1189) [#1237](https://github.com/ocsf/ocsf-schema/pull/1237)
    - The `source` attribute is a string for describing the location where an attribute's value comes from.
    - The `references` attribute is a list objects with `url` and `description` fields. These are intended to for reference to external resources. The `url` and `description` attributes are used to construct anchor (`a`) tags with the `url` used in the anchor's `href` attribute, and `description` used in the entity portion of the tag.
    - The `source` field can be used in attributes defined anywhere in the schema, specifically:
        - Dictionary attributes
        - Event class attributes
        - Object attributes
        - Profile attributes
        - Enum values in all places where attributes occur (the 4 cases above)
    - The `references` field can also be used in attributes anywhere in the schema, as well as for event classes, objects, and enum values; specifically:
        - Dictionary attributes
        - Event class attributes
        - Object attributes
        - Profile attributes
        - Enum values in all places where attributes occur
        - Event classes; top level attribute allowing link(s) about an event class
        - Objects; top level attribute allowing link(s) about an object
    - The `source` and `references` attributes are also supported in when extending or patching event classes and objects.
1. Fixed minor spelling mistakes in attribute descriptions in `dictionary.json`. [#1213](https://github.com/ocsf/ocsf-schema/pull/1213)
1. In the metaschema, added support for `@deprecated` in enum values. [#1237](https://github.com/ocsf/ocsf-schema/pull/1237)
1. Fixed some more formatting of attribute descriptions in `dictionary.json` and `idp.json`. [#1239](https://github.com/ocsf/ocsf-schema/pull/1239)
1. Added `resource_details.name` as an Observable type `type_id: 38`. [#1250](https://github.com/ocsf/ocsf-schema/pull/1250)
1. Added 3 new enums (Registry Value, Registry Key, Command Line) to `osint.type_id` and added TLP:WHITE to `osint.tlp` enums. [#1264](https://github.com/ocsf/ocsf-schema/pull/1264)
1. Relaxed attribute requirement for `name` in `observables` object; `title` in `finding_info` object. [#1271](https://github.com/ocsf/ocsf-schema/pull/1271)
1. Relaxed attribute requirement for `vendor_name` in the `product` object. [#1300](https://github.com/ocsf/ocsf-schema/pull/1300)

## [v1.3.0] - August 1st, 2024

### Added
* #### Categories
    1. Added `Remediation` category. [#1066](https://github.com/ocsf/ocsf-schema/pull/1066)
* #### Event Classes
    1. Added `Event Log Activity` event class to the System Activity category. [#1014](https://github.com/ocsf/ocsf-schema/pull/1014)
    2. Added `Remediation Activity`, `File Remediation Activity`, `Process Remediation Activity`, `Network Remediation Activity` event classes to the Remediation category. [#1066](https://github.com/ocsf/ocsf-schema/pull/1066)
    3. Added `Windows Service Activity` event class to the System Activity category via Windows extension. [#1103](https://github.com/ocsf/ocsf-schema/pull/1103)
    4. Added `Software Inventory Info` event class to the Discovery category. [#1134](https://github.com/ocsf/ocsf-schema/pull/1134)
* #### Profiles
    1. Added `osint` Profile based on the `osint` object. [#992](https://github.com/ocsf/ocsf-schema/pull/992)
* #### Objects
    1. Added `d3fend`, `d3f_tactic`, `d3f_technique` MITRE objects. [#1066](https://github.com/ocsf/ocsf-schema/pull/1066)
    2. Added `ja4_fingerprint` object. [#834](https://github.com/ocsf/ocsf-schema/pull/834)
    3. Added `ja4_fingerprint_list` as a list of `ja4_fingerprint` objects.  [#834](https://github.com/ocsf/ocsf-schema/pull/834)
    4. Added `ticket` object. [#1068](https://github.com/ocsf/ocsf-schema/pull/1068)
    5. Added `osint` object. [#992](https://github.com/ocsf/ocsf-schema/pull/992)
    6. Added `signatures` object, an array of `signature` objects. [#992](https://github.com/ocsf/ocsf-schema/pull/992)
    7. Added `whois` object. [#992](https://github.com/ocsf/ocsf-schema/pull/992)
    8. Added `domain_contact` and array-typed `domain_contacts` object for use with `whois` object. [#992](https://github.com/ocsf/ocsf-schema/pull/992)
    9. Added `Windows Service` object to the Windows extension. [#1103](https://github.com/ocsf/ocsf-schema/pull/1103)
    10. Added `timespan` object. [#1125](https://github.com/ocsf/ocsf-schema/pull/1125)

### Improved
* #### Categories
    n/a
* #### Event Classes
    1. Added `file_result` to File Hosting Activity. [#1045](https://github.com/ocsf/ocsf-schema/pull/1045)
    2. Added entries to `injection_type_id` enum (`Process Activity`) and `activity_id` enum (`Memory Activity`). [#1060](https://github.com/ocsf/ocsf-schema/pull/1060)
    3. Added a `Restart`, `Enable`, `Disable`, and `Update` `activity_id` to the `Application Lifecycle` class. [#1064](https://github.com/ocsf/ocsf-schema/pull/1064)
    4. Added `ja4_fingerprint_list` to base network event class. [#834](https://github.com/ocsf/ocsf-schema/pull/834)
    5. Added `ticket` to `Incident Finding` event class. [#1068](https://github.com/ocsf/ocsf-schema/pull/1068)
    6. Added new activities `Enroll`, `Activate`, `Deactivate`, `Suspend`, and `Resume` to the `Entity Management` class. [#1095](https://github.com/ocsf/ocsf-schema/pull/1095)
    7. Added new activity `Listen` to `Network Activity` and relax requirement of `src_endpoint`. [#1147](https://github.com/ocsf/ocsf-schema/pull/1147)
    8. Added `state`, `state_id` to `Device Config State Change`. [#1143](https://github.com/ocsf/ocsf-schema/pull/1143)
    9. Added `resources` attribute to `Vulnerability Finding` and `Compliance Finding`. [#1150](https://github.com/ocsf/ocsf-schema/pull/1150)
* #### Profiles
    n/a
* #### Objects
    1. Added `ext` to `File` object. [#1046](https://github.com/ocsf/ocsf-schema/pull/1046)
    2. Added `account`, `device`, `email`, `url`, `user` to `evidences` in detection finding. [#1000](https://github.com/ocsf/ocsf-schema/pull/1000)
    3. Added `state_id`, `state` to `Digital Signature` object. [#1069](https://github.com/ocsf/ocsf-schema/pull/1069)
    4. Added `domain` to `Uniform Resource Locator` object. [#1096](https://github.com/ocsf/ocsf-schema/pull/1096)
    5. Added `reg_key` and `reg_value` to `Evidence Artifacts` object. [#1078](https://github.com/ocsf/ocsf-schema/pull/1078)
    6. Added `type_id` and associated entity objects to `Managed Entity`. [#1094](https://github.com/ocsf/ocsf-schema/pull/1094)
    7. Added `vendor_name`, `type`, `type_id` to object `package`. [#1093](https://github.com/ocsf/ocsf-schema/pull/1093)
    8. Added `router`, `ids`, and `ips` entries to `type_id` enum in the `Endpoint` object. [#1121](https://github.com/ocsf/ocsf-schema/pull/1121)
    9. Added `job` to `Evidence Artifacts` object. [#1130](https://github.com/ocsf/ocsf-schema/pull/1130)
    10. Added `ip` to object `load_balancer`. [#1138](https://github.com/ocsf/ocsf-schema/pull/1138)
    11. Added `cpe_name` and `hash` to `Software Package` object. [#1142](https://github.com/ocsf/ocsf-schema/pull/1142)
    12. Added `avg_timespan` to the `kb_article` object. [#1125](https://github.com/ocsf/ocsf-schema/pull/1125)
    13. Added `created_time`,`desc`, `short_desc`, `reputation`, `src_url` to `enrichment` object. [#1149](https://github.com/ocsf/ocsf-schema/pull/1149)
    14. Added `compliance_references`, `compliance_standards` to the `compliance` object. [#1110](https://github.com/ocsf/ocsf-schema/pull/1110)

### Bugfixes
1. Fixed the host profile construction in `patch_state` event class. [#1087](https://github.com/ocsf/ocsf-schema/pull/1087)
2. Removed the optional requirement overrides for `name` and `uid` in `_resource` as they are part of a constraint. [#1087](https://github.com/ocsf/ocsf-schema/pull/1087)
3. Fixed declarations of `data_lifecycle_state_id`, `integrity`, `opcode_id`, `risk_level`, and `analytic.type_id`. [#1111](https://github.com/ocsf/ocsf-schema/pull/1111)

### Deprecated
1. Deprecated `resource` in `Vulnerability Finding` and `Compliance Finding` event classes in favor of `resources`. [#1150](https://github.com/ocsf/ocsf-schema/pull/1150)

### Breaking changes
n/a
### Misc
1. Colorized validator output [#1048](https://github.com/ocsf/ocsf-schema/pull/1048)
    * Updated the GitHub workflow for the `ocsf-validator` to print colorized output.
2. Clarify how to reference profiles in metadata [#1056](https://github.com/ocsf/ocsf-schema/pull/1056)
    * Updated the description of `metadata.profiles` to clarify the correct way to reference a profile in that list.
3. Added a `gitignore` file. [#1071](https://github.com/ocsf/ocsf-schema/pull/1071)
4. New Extension registration for Cisco [#1074](https://github.com/ocsf/ocsf-schema/pull/1074)
5. Cleaned up MITRE trademarks and registrations for captions and descriptions.
6. Declared enums in dictionary.json have sane "0" (Unknown) and "99" (Other) declarations and descriptions where appropriate [#1111](https://github.com/ocsf/ocsf-schema/pull/1111)
7. Adds support for `suppress_checks` controls in attributes to allow tools to automatically validate conventions [#1063](https://github.com/ocsf/ocsf-schema/pull/1063)
    * Updated several attributes that do not follow conventions to disable linting for them
8. Added `credential_uid` as an Observable type - `type_id: 19`. [#1137](https://github.com/ocsf/ocsf-schema/pull/1137)
9. New Extension registration for US Gov [#1140](https://github.com/ocsf/ocsf-schema/pull/1140)
10. Enum definitions are now refactored such that generic enum descriptions have "See specific usage" in the description [#1146](https://github.com/ocsf/ocsf-schema/pull/1146)

## [v1.2.0] - April 23rd, 2024

### Added
* #### Categories
    n/a
* #### Event Classes
    1. Added `Data Security Finding` event class. [#953](https://github.com/ocsf/ocsf-schema/pull/953)
    2. Added `File Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    3. Added `Folder Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    4. Added `Group Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    5. Added `Job Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    6. Added `Kernel Object Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    7. Added `Module Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    8. Added `Network Connection Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    9. Added `Networks Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    10. Added `Peripheral Device Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    11. Added `Prefetch Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    12. Added `Process Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    13. Added `Registry Key Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    14. Added `Registry Value Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    15. Added `Service Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    16. Added `Session Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    17. Added `User Query` event class. [#967](https://github.com/ocsf/ocsf-schema/pull/967)
    18. Added `Tunnel Activity` event class. [#1012](https://github.com/ocsf/ocsf-schema/pull/1012)

* #### Profiles
    1. Added `data_classification` profile. [#998](https://github.com/ocsf/ocsf-schema/pull/998)

* #### Objects
    1. Added `auth_factor` object. [#949](https://github.com/ocsf/ocsf-schema/pull/949)
    2. Added `data_security` object. [#953](https://github.com/ocsf/ocsf-schema/pull/953)
    3. Added `autonomous_system` object. [#978](https://github.com/ocsf/ocsf-schema/pull/978)
    4. Added `agent` object. [#987](https://github.com/ocsf/ocsf-schema/pull/987)
    5. Added `data_classification` object. [#998](https://github.com/ocsf/ocsf-schema/pull/998)

* #### Observables
    1. Added `port_t` `subnet_t` `cmd_line` `country` `pid` `cwe.uid` `cve.uid` `user_agent` enum items. [#1035](https://github.com/ocsf/ocsf-schema/pull/1035)

* #### Platform Extensions
    n/a

### Improved
* #### Categories
* #### Event Classes
    1. Added `auth_factors` array to Authentication event class. [#949](https://github.com/ocsf/ocsf-schema/pull/949)
    2. Modified all classes such that primary attributes are at least recommended. [#974](https://github.com/ocsf/ocsf-schema/pull/974)
    3. Added `src_endpoint`, `http_request` attributes to all IAM category classes. [#976](https://github.com/ocsf/ocsf-schema/pull/976)
    4. Added `autonomous_system` to `network_endpoint` objects. [#978](https://github.com/ocsf/ocsf-schema/pull/978)
    5. Added `List`, `Encrypt` and `Decrypt` activities to `datastore` event class. [#989](https://github.com/ocsf/ocsf-schema/pull/989)
    6. Added `file` attribute to `http`, `rdp`, `ssh`, and `ftp` event classes. [#985](https://github.com/ocsf/ocsf-schema/pull/985)
    7. Added a `Preauth` `activity_id` to the `Authentication` class. [#1018](https://github.com/ocsf/ocsf-schema/pull/1018)
    8. Added the `Security Control` profile to the `Datastore Activity` class. [#1030](https://github.com/ocsf/ocsf-schema/pull/1030)
    9. Added `risk_details` to Detection Finding. [#1032](https://github.com/ocsf/ocsf-schema/pull/1032)
   10. Added `access_mask` to Entity Management class. [#1090](https://github.com/ocsf/ocsf-schema/pull/1090)
   11. Added `access_list` to Entity Management class. [#1090](https://github.com/ocsf/ocsf-schema/pull/1090)

* #### Profiles
    n/a
* #### Objects
    1. Expanded `type_id` enum in `analytic` object to account for more use-cases: [#953](https://github.com/ocsf/ocsf-schema/pull/953)
        - `5 - Fingerprinting`
        - `6 - Tagging`
        - `7 - Keyword Match`
        - `8 - Regular Expressions`
        - `9 - Exact Data Match`
        - `10 - Partial Data Match`
        - `11 - Indexed Data Match`
    2. Added `lat`, `long`, `geohash` attributes to `location` object. [#971](https://github.com/ocsf/ocsf-schema/pull/971).
    3. Added `risk_score`, `risk_level_id`, `risk_level` to `user` object. Issue [#972](https://github.com/ocsf/ocsf-schema/pull/972).
    4. Added `app_name`, `app_uid` to `actor` object.  Issue [#966](https://github.com/ocsf/ocsf-schema/pull/966), PR [#979](https://github.com/ocsf/ocsf-schema/pull/979).
    5. Added `container`, `database`, `databucket` to the `evidences` object. [#984](https://github.com/ocsf/ocsf-schema/pull/984)
    6. Added `owner` to `endpoint` object. [#987](https://github.com/ocsf/ocsf-schema/pull/987)
    7. Added `is_applied` Boolean attribute to `policy` object. [#987](https://github.com/ocsf/ocsf-schema/pull/987)
    8. Added `agent_list` as an array of `agent` objects. [#987](https://github.com/ocsf/ocsf-schema/pull/987)
    9. Added `policies` object as an array of `policy` objects. [#987](https://github.com/ocsf/ocsf-schema/pull/987)
    10. Added `agent_list` to `endpoint` object. [#987](https://github.com/ocsf/ocsf-schema/pull/987)
    11. Added `labels` to the `Account` object. [#1028](https://github.com/ocsf/ocsf-schema/pull/1028)
    12. Added `data_classification` profile to `database`, `databucket`, `email`, `file`, `metadata`, `product`, `resource_details` and `web_resource` objects. [#998](https://github.com/ocsf/ocsf-schema/pull/998)

* #### Platform Extensions
    n/a

### Bugfixes
1. Changed datatype of `priority` attribute, from `integer_t` to `string_t` [#959](https://github.com/ocsf/ocsf-schema/pull/959)
2. Extended `email_t` regexp to allow characters from RFC5322 before @.
3. Updated `logon_type_id` enum to include `0` as `Unknown`. Added enum item `1` as `System`. [#1055](https://github.com/ocsf/ocsf-schema/pull/1055)

### Deprecated
1. Deprecated `coordinates` attribute in favor of specific `lat`, `long` attributes. [#971](https://github.com/ocsf/ocsf-schema/pull/971)
2. Deprecated `invoked_by` attribute in the `Actor` object in favor of `app_name`. [#979](https://github.com/ocsf/ocsf-schema/pull/979).

### Breaking changes
n/a

### Misc
1. New Extension registration for Sedara. [#951](https://github.com/ocsf/ocsf-schema/pull/951)
2. Corrected punctuation for the `transmit_time` attribute. [#1001](https://github.com/ocsf/ocsf-schema/pull/1001)
3. New ways to define observables in the metaschema. [#982](https://github.com/ocsf/ocsf-schema/pull/982) and [#993](https://github.com/ocsf/ocsf-schema/pull/993)
    * (Current) Dictionary types using `observable` property in dictionary types. This allows defining all occurrences of attributes of this type as an observable.
    * (Current) Objects using top-level `observable` property. This allows defining all occurrences attributes whose type is this object as an observable.
    * _**(New)**_ Dictionary attributes using `observable` property in attribute. This allows defining all occurrences of this attribute as an observable.
    * _**(New)**_ Object-specific attributes using `observable` property class's attributes. This allows defining object attributes as observables _only_ within instances of this specific object.
    * _**(New)**_ Event class-specific attributes using `observable` property class's attributes. This allows defining class attributes as observables _only_ within instances of this specific class.
    * _**(New)**_ Event class-specific attribute _paths_ using top-level `observables` property. The `observables` property holds an object mapping from an dotted attribute path to an observable `type_id`. This allows defining an observables _only_ within instances of this specific class, and only for the attributes at these paths, even for attributes that are within nested objects and arrays. This can also be used for top-level class attributes, which can be more convenient that defining a class attribute observable for classes that extend another, but don't otherwise change a attribute definition.
4. Metaschema improvements. [#993](https://github.com/ocsf/ocsf-schema/pull/993)
    * Detect unexpected top-level properties in object and event class definitions. This was added at this point to detect invalid observable definitions: invalid `observable` property in event classes, and invalid `observables` property in objects.
    * Remove hard-coded list of categories from `metaschema/categories.schema.json`, leaving this to the `ocsf-validator`. This change makes testing with alternate schemas that may add extra categories easier, as well as making it possible to validate private extensions that contain new categories.
5. Metaschema error reporting [#1027](https://github.com/ocsf/ocsf-schema/pull/1027)
    * Updated the definition of `object` and `event` so that metaschema errors reported by the validator with nested properties correctly attribute the error to the property with the error, rather than the top-level class.

## [v1.1.0] - January 25th, 2024

### Added
* #### Categories
    `n/a`
* #### Event Classes
    1. Added `User Inventory Info` event class. [#667](https://github.com/ocsf/ocsf-schema/pull/667)
    2. Added `Vulnerability Finding` event class. [#698](https://github.com/ocsf/ocsf-schema/pull/698)
    3. Added `NTP Activity` event class [#705](https://github.com/ocsf/ocsf-schema/pull/705)
    4. Added `OS Patch State` event class. [#746](https://github.com/ocsf/ocsf-schema/pull/746)
    5. Added `Datastore Activity` event class 6005. [#874](https://github.com/ocsf/ocsf-schema/pull/874)
    6. Added `Detection Finding` event class. [#877](https://github.com/ocsf/ocsf-schema/pull/877)
    7. Added `Incident Finding` event class. [#903](https://github.com/ocsf/ocsf-schema/pull/903)
    8. Added `Device Config Sate Change` event class. [#914](https://github.com/ocsf/ocsf-schema/pull/914)
    9. Added `Scan Activity` event class. [#915](https://github.com/ocsf/ocsf-schema/pull/915)
    10. Added `File Hosting Activity` event class. [#917](https://github.com/ocsf/ocsf-schema/pull/917)

* #### Profiles
	1. Added `Network Proxy` Profile for the `Network Activity` and `Application Activity` classes. [#705](https://github.com/ocsf/ocsf-schema/pull/705)
    2. Added `Load Balancer` Profile for the Network Activity classes. [#897](https://github.com/ocsf/ocsf-schema/pull/897)

* #### Objects
    1. Added new `cwe` object to `cve` and `vulnerability` objects. [#678](https://github.com/ocsf/ocsf-schema/pull/678)
    2. Added Firewall Rule object. [#685](https://github.com/ocsf/ocsf-schema/pull/685)
    3. Added new `kb_article` object to house Knowledgebase Article info. [#709](https://github.com/ocsf/ocsf-schema/pull/709) [#862](https://github.com/ocsf/ocsf-schema/pull/862) [#924](https://github.com/ocsf/ocsf-schema/pull/924)
    4. Added new `epss` object to the `cve` object. [#741](https://github.com/ocsf/ocsf-schema/pull/741)

### Improved
* #### Categories
    1. Improved Findings Category, with new and domain specific event classes (Vulnerability Finding, Compliance Finding, Detection Finding, Incident Finding), description updates across the board. [#895](https://github.com/ocsf/ocsf-schema/pull/895) [#907](https://github.com/ocsf/ocsf-schema/pull/907) [#903](https://github.com/ocsf/ocsf-schema/pull/903) [#698](https://github.com/ocsf/ocsf-schema/pull/698) [#718](https://github.com/ocsf/ocsf-schema/pull/718)

* #### Event Classes
    1. Added `MFA Enable` and `Disable` to `activity_id` to the Account Change event class. [#724](https://github.com/ocsf/ocsf-schema/pull/724)
    2. Added `Service Ticket Renew` to `activity_id` of the Authentication event class. [#765](https://github.com/ocsf/ocsf-schema/pull/765)
    3. Added `url` attribute to Network Activity event class. [#857](https://github.com/ocsf/ocsf-schema/pull/857)
    4. Added `http_request`, `http_response`, `tls` attributes, `network_proxy` profile to Web Resources Activity event class. [#895](https://github.com/ocsf/ocsf-schema/pull/895)
    5. Adjusted requirement of `dst_endpoint` from `required` to `recommended` in the DNS Activity event class. [#901](https://github.com/ocsf/ocsf-schema/pull/901)
    6. Added `Create` and `Delete` to `activity_id` of the Group Management event class. [#929](https://github.com/ocsf/ocsf-schema/pull/929)

* #### Profiles
    1. Improved `security_control` profile to include access control semantics, firewall properties. [#851](https://github.com/ocsf/ocsf-schema/pull/851) [#888](https://github.com/ocsf/ocsf-schema/pull/888) [#889](https://github.com/ocsf/ocsf-schema/pull/889) [#906](https://github.com/ocsf/ocsf-schema/pull/906)

* #### Objects
    1. Added `url_string` attribute to the `product` and the `web_resource` objects. [#675](https://github.com/ocsf/ocsf-schema/pull/675)
    2. Added `type` and `type_id` attributes to the `endpoint` object. [#690](https://github.com/ocsf/ocsf-schema/pull/690)
    3. Added `cwe`, `desc`, `references` and `title` to `cve` object. [#698](https://github.com/ocsf/ocsf-schema/pull/698)
    4. Added `affected_package` object and`affected_packages` attribute to `vulnerability` object. [#698](https://github.com/ocsf/ocsf-schema/pull/698)
    5. Added `purl` to `package` object. [#698](https://github.com/ocsf/ocsf-schema/pull/698)
    6. Added `cpe_name` attribute to the `product` and os objects. [#713](https://github.com/ocsf/ocsf-schema/pull/713) [#731](https://github.com/ocsf/ocsf-schema/pull/731)
    7. Added `container` and `data` to `response` and `request` objects. [#738](https://github.com/ocsf/ocsf-schema/pull/738)
    8. Added `group` to the `api` object. [#738](https://github.com/ocsf/ocsf-schema/pull/738)
    9. Added `namespace` to the `resource_details` object. [#738](https://github.com/ocsf/ocsf-schema/pull/738)
    10. Added `log_level` to the `metadata` object. [#738](https://github.com/ocsf/ocsf-schema/pull/738)
    11. Added `length` to the `http_request` object. [#768](https://github.com/ocsf/ocsf-schema/pull/768)
    12. Added `is_exploit_available` to the `vulnerability` object. [#777](https://github.com/ocsf/ocsf-schema/pull/777)
    13. Added `domain` attribute to the `group` object. [#871](https://github.com/ocsf/ocsf-schema/pull/871)
    14. Adjusted attribute requirements in `dns_query`, `dns_answer` objects. [#879](https://github.com/ocsf/ocsf-schema/pull/879)
    15. Added firewall, router, switch, hub to endpoint `type_id` enum. [#921](https://github.com/ocsf/ocsf-schema/pull/921)
    16. Added `is_vpn` to the `session` object. [#922](https://github.com/ocsf/ocsf-schema/pull/922)
    17. Added `state` to `network_connection_info` object. [#932](https://github.com/ocsf/ocsf-schema/pull/932)
    18. Added `community_uid` to `network_connection_info` object. [#1202](https://github.com/ocsf/ocsf-schema/pull/1202)

### Bugfixes
`n/a`

### Deprecated
1. Deprecated `cwe_uid` and `cwe_url` attributes and removed from `cve` object. [#678](https://github.com/ocsf/ocsf-schema/pull/678)
2. Deprecated `http_status` attribute from `HTTP Activity` event to be replaced by `http_response.code`. [#767](https://github.com/ocsf/ocsf-schema/pull/767)
3. Deprecated `finding` object in favor of `finding_info` object. [#769](https://github.com/ocsf/ocsf-schema/pull/769)
4. Deprecated `proxy` attribute from the dictionary, in favor of `Network Proxy` profile. [#856](https://github.com/ocsf/ocsf-schema/pull/856)
5. Deprecated `group_name` attribute. [#873](https://github.com/ocsf/ocsf-schema/pull/873)
6. Deprecated `Security Finding` class to be replaced by the new specific classes according to the use-case: `Vulnerability Finding`, `Compliance Finding`, `Detection Finding`, `Incident Finding`. [#877](https://github.com/ocsf/ocsf-schema/pull/877)
7. Deprecated `Web Resources Access Activity` event class. [#890](https://github.com/ocsf/ocsf-schema/pull/890)
8. Deprecated `Network File Activity` event class in favor of `File Hosting Activity `[#917](https://github.com/ocsf/ocsf-schema/pull/917)
9. Deprecated `extension_list` in TLS object in favor of `tls_extension_list`. [#936](https://github.com/ocsf/ocsf-schema/pull/936)

### Breaking changes
`n/a`

### Misc
1. New Extension registration for SentinelOne. [#706](https://github.com/ocsf/ocsf-schema/pull/706)
2. Added json-schema based metaschema validation to ensure correctness, consistency of the JSON definitions. [#736](https://github.com/ocsf/ocsf-schema/pull/736) [#830](https://github.com/ocsf/ocsf-schema/pull/830) [#867](https://github.com/ocsf/ocsf-schema/pull/867) [#892](https://github.com/ocsf/ocsf-schema/pull/892)
3. Increased `max_len` for `subnet_t` type from `40` to `42`. [#745](https://github.com/ocsf/ocsf-schema/pull/745)
4. Improved the regex for `ip_t` type. [#745](https://github.com/ocsf/ocsf-schema/pull/745)
5. Updated the `datetime_t` validation regex to enable validation of timestamps, and to ensure that timestamps not matching `RFC-3339` are not considered valid. [#753](https://github.com/ocsf/ocsf-schema/pull/753)
6. Added version information to the native extensions. [#881](https://github.com/ocsf/ocsf-schema/pull/881)
7. Updated caption and description of Observable type - `File Hash` to read `Hash`. [#900](https://github.com/ocsf/ocsf-schema/pull/900)
8. New Extension registration for DataBee. [#912](https://github.com/ocsf/ocsf-schema/pull/912)
9. Changed data-type of `type_uid` to `long_t` from `int_t`. [#928](https://github.com/ocsf/ocsf-schema/pull/928)

## [v1.0.0]

Initial release of OCSF.
