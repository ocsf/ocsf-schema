# External Schema & Ontology Research for OCSF v2.0

> Comparative analysis of OCSF against 9 external standards to identify structural
> improvements for the v2.0 redesign. Each section maps findings to specific v2.0
> workstreams.

---

## 1. ISO 21838-2 / Basic Formal Ontology (BFO)

[ISO/IEC 21838-2](https://www.iso.org/obp/ui/en/#iso:std:iso-iec:21838:-2:ed-1:v1:en)
defines BFO, the most widely adopted upper ontology in science and the foundation
for MITRE D3FEND.

### Core Classification

BFO partitions all entities into two top-level categories:

- **Continuants** -- things that persist through time and have no temporal parts
  - **Independent Continuants**: material entities (devices, users, files)
  - **Dependent Continuants**: qualities (severity), roles (actor, victim),
    dispositions (vulnerability)
- **Occurrents** -- things that happen, with temporal extent
  - **Processes**: events, activities
  - **Temporal Regions**: time intervals

### Mapping to OCSF

| BFO Category | OCSF Equivalent | Gap |
|---|---|---|
| Independent Continuant | `_entity` objects (user, device, file) | 17 entity-like objects still on `object` base |
| Dependent Continuant (Role) | `actor` | `actor` is modeled as an entity, not a role |
| Dependent Continuant (Quality) | `severity`, `confidence`, `risk_level` | Correctly modeled as attributes, not objects |
| Process / Occurrent | Event classes (authentication, file_activity) | No formal distinction in schema metadata |
| Relation | `edge` with `relation_id` | Newly added; not yet compiler-generated |

### Key Insight: Actor as Role

In BFO, a **role** is a dependent continuant that inheres in an independent
continuant. The "actor" is not a thing -- it is a role borne by a user or process
in the context of a specific event. OCSF models `actor` as a standalone object
with its own `uid`, which conflates the role with the role-bearer.

**v2.0 recommendation:** Restructure `actor` as a role-bearing wrapper that
references the underlying entity (user, process, service) rather than being an
entity itself. The `actor.user`, `actor.process`, `actor.session` pattern already
partially does this, but `actor` should not have its own `uid` in the identity
sense.

### Key Insight: Continuant vs. Occurrent Metadata

BFO suggests that continuants and occurrents should carry different metadata.
Continuants have qualities and bear roles. Occurrents have temporal extent and
participants. OCSF could formalize this:

- `_entity` (continuant): `uid`, `name`, `created_time`, `modified_time`
- Event (occurrent): `time`, `duration`, `start_time`, `end_time`, `participants`
  (the entities involved)

---

## 2. STIX 2.1 (Structured Threat Information eXpression)

STIX is the OASIS standard for sharing cyber threat intelligence. It is the
closest external standard to OCSF's threat/finding model.

### Design Patterns

| Pattern | STIX | OCSF 1.x | Gap |
|---|---|---|---|
| Object identity | Mandatory UUID (`id`) on every object | Optional `uid` on some objects | Many objects lack `uid` |
| Relationships | First-class `relationship` type | `edge` object (new) | Not compiler-generated |
| Object lifecycle | `created`, `modified` on every object | Inconsistent (`created_time` on some) | No standard lifecycle on `_entity` |
| Type discrimination | String `type` field | Integer `type_id` + string `type` | OCSF is stronger here |
| Versioning | `spec_version` per object | `metadata.version` per event | No object-level versioning |
| Marking/TLP | `object_marking_refs` | `data_classification` profile | OCSF is weaker |

### Key Insight: Mandatory Identity

STIX requires every domain object to have a UUID (`id`). This is fundamental to
graph construction, deduplication, and cross-reference. OCSF's `_entity` has
`uid` as recommended with `at_least_one(name, uid)` -- this should become
`required` in v2.0 for all promoted entities.

### Key Insight: Relationship as First-Class Object

STIX's `relationship` type has:
```json
{
  "type": "relationship",
  "id": "relationship--uuid",
  "relationship_type": "uses",
  "source_ref": "threat-actor--uuid",
  "target_ref": "malware--uuid"
}
```

OCSF's `edge` object with `relation_id`, `source`, `target` is equivalent. The
v2.0 compiler should auto-generate edges from event structure (e.g.,
`actor.user` -> `dst_endpoint` implies an `authenticates-to` edge in an
Authentication event).

**Applies to: Workstream 1 (Entity Identity), Workstream 7 (Graph Maturation)**

---

## 3. Elastic Common Schema (ECS)

ECS is OCSF's main competitor for SIEM event normalization.

### Event Categorization Hierarchy

ECS uses four orthogonal dimensions (all can be arrays):

```
event.kind:     alert | event | metric | state | signal
event.category: [authentication, network]     ← ARRAY
event.type:     [start, connection, info]     ← ARRAY
event.outcome:  success | failure | unknown
```

OCSF uses a rigid single-class model:
```
class_uid:    3002 (Authentication)
category_uid: 3 (IAM)
activity_id:  1 (Logon)
status_id:    1 (Success)
```

### Key Insight: Multi-Category Events

An SSH login is simultaneously an `authentication` event AND a `network`
event in ECS. In OCSF, you must choose one class (Authentication 3002 or
SSH Activity 4007). This is the root cause of the IAM class confusion and
many mapping disputes.

**v2.0 recommendation:** Allow `category_uid` to be an array. An event can
belong to multiple categories. This does not change the `class_uid` (still
singular), but lets consumers filter by category without losing context. A
secondary approach: allow `tags` or `categories` arrays for ad-hoc classification.

### Key Insight: Related Fields

ECS has `related.ip[]`, `related.user[]`, `related.hash[]`, `related.hosts[]`
as flat arrays that aggregate all IPs/users/hashes in the event for easy
searching. OCSF's `observables` serves a similar purpose but requires structured
objects with `type_id` and `value`. The ECS approach is simpler for search;
OCSF's is richer for analytics.

**v2.0 recommendation:** Keep `observables` but consider adding flat `related_*`
arrays as a search-optimized projection (similar to how `event_graph` is an
analytics projection).

### Symmetric Source/Destination

ECS uses completely symmetric `source.*` and `destination.*` field sets:
```
source.ip, source.port, source.bytes, source.packets, source.mac
destination.ip, destination.port, destination.bytes, destination.packets
```

OCSF uses `src_endpoint` and `dst_endpoint` as object references, which is more
structured but harder to query flat. Neither is wrong -- they serve different
consumption patterns.

**Applies to: Workstream 3 (IAM), Workstream 5 (Network), Workstream 6 (Framework)**

---

## 4. Splunk CIM (Common Information Model)

CIM uses tag-based data models rather than rigid class hierarchies.

### Tag-Based Classification

CIM events are classified by tags, not by class inheritance. An event tagged
`authentication` AND `network` automatically populates both the Authentication
and Network Traffic data models. This is more flexible than class-based typing.

### Network Traffic Data Model Fields

CIM's Network Traffic model uses minimal, flat, search-optimized fields:

| CIM Field | OCSF Equivalent | Notes |
|---|---|---|
| `src` | `src_endpoint.ip` | CIM is flatter |
| `dest` | `dst_endpoint.ip` | Same |
| `src_port` | `src_endpoint.port` | CIM at top level |
| `dest_port` | `dst_endpoint.port` | CIM at top level |
| `transport` | `connection_info.protocol_name` | CIM simpler |
| `app` | `app_name` | Similar |
| `action` | `action` (security_control profile) | Similar |
| `bytes_in` / `bytes_out` | `traffic.bytes_in` / `traffic.bytes_out` | Similar |
| `direction` | `connection_info.direction_id` | Similar |

### Key Insight: Flattened Query Fields

CIM's strength is query simplicity. `index=main sourcetype=firewall src=10.0.1.50`
is trivially faster than navigating nested OCSF objects. While OCSF shouldn't
abandon its rich object model, it should consider a "query projection" — a flat
view generated at index time.

**Applies to: Workstream 6 (Framework)**

---

## 5. Zeek Network Logs

Zeek (formerly Bro) is the gold standard for deep protocol analysis and produces
structured logs per protocol.

### Protocol-Specific Logs with Shared Correlation UID

| Log Type | Fields | Correlation |
|---|---|---|
| `conn.log` | uid, id.orig_h/p, id.resp_h/p, proto, service, duration, orig_bytes, resp_bytes, conn_state, history | Hub |
| `dns.log` | uid, query, qtype, rcode, answers | Linked via uid |
| `http.log` | uid, method, host, uri, status_code, response_body_len | Linked via uid |
| `ssl.log` | uid, version, cipher, server_name, subject, issuer | Linked via uid |
| `files.log` | fuid, tx_hosts, rx_hosts, source, mime_type, md5, sha1 | Linked via conn_uid |
| `x509.log` | fingerprint, certificate.subject, certificate.issuer, san.dns | Linked via fuid |

This is effectively a **graph** — `conn.log` is the hub node, protocol-specific
logs are spoke nodes connected by the shared `uid`. OCSF embeds all protocol
detail into a single event, which is richer per-event but harder to correlate.

### Key Insight: Connection State Machine

Zeek's `conn.log` tracks the TCP connection state machine:

- `conn_state`: S0 (SYN no reply), S1 (established), SF (normal close), REJ (rejected), S2 (established SYN-ACK), S3 (established SYN-ACK-ACK), RSTO (RST by originator), RSTR (RST by responder), RSTOS0, RSTRH, SH, SHR, OTH
- `history`: Character string tracking each packet type (S=SYN, H=SYN-ACK, A=ACK, D=data, F=FIN, R=RST, etc.)

OCSF has `activity_id` values for Open/Close/Traffic/Reset but no fine-grained
state tracking. For forensic analysis, connection state is critical.

### Key Insight: Tunnel Unwrapping Chain

Zeek's `tunnel_parents` is a flat array of connection UIDs representing the
encapsulation stack. This cleanly solves OCSF's recursive `network_proxy`
problem (#996).

```json
{ "uid": "conn-inner", "tunnel_parents": ["conn-outer-vpn", "conn-outer-gre"] }
```

### Key Insight: Directional Counters

Zeek uses `orig_*` and `resp_*` prefixes for directional metrics:
- `orig_bytes` / `resp_bytes` (not `bytes_in` / `bytes_out`)
- `orig_pkts` / `resp_pkts`
- `orig_ip_bytes` / `resp_ip_bytes`

This is unambiguous — "originator" and "responder" are always relative to the
connection initiator. OCSF's `bytes_in`/`bytes_out` is ambiguous (from whose
perspective?).

**v2.0 recommendations:**
1. Add `conn_state_id` enum tracking TCP connection state
2. Replace recursive `network_proxy` with `tunnel_chain` array of UIDs
3. Use `orig_*`/`resp_*` directional naming (or `initiator_*`/`responder_*`)
4. Consider protocol-specific profiles rather than protocol-specific classes
5. Add `connection_history` string field for raw state machine tracking

**Applies to: Workstream 5 (Network Redesign)**

---

## 6. IPFIX / NetFlow v9 (RFC 7011)

IPFIX is the IETF standard for IP flow export. It directly addresses several
open OCSF issues.

### Bidirectional Flow Support

IPFIX has native bidirectional flow handling:

| IPFIX Element | ID | Description |
|---|---|---|
| `biflowDirection` | 239 | 0=arbitrary, 1=initiator, 2=reverseInitiator |
| `octetDeltaCount` | 1 | Forward byte count |
| `reverseOctetDeltaCount` | 32769 | Reverse byte count |
| `packetDeltaCount` | 2 | Forward packet count |
| `reversePacketDeltaCount` | 32770 | Reverse packet count |

This directly solves #1554 (`is_src_dst_assignment_known` does not handle
bi-flow correctly).

**v2.0 recommendation:** Add `flow_direction_id` enum to network events:

```
0: Unknown — Direction could not be determined
1: Initiator — Metrics from connection initiator perspective
2: Responder — Metrics from connection responder perspective
3: Bidirectional — Metrics include both directions
```

### Template-Based Field Declaration

IPFIX uses templates where producers declare which Information Elements they
will send. This is conceptually similar to OCSF's profile system but applied
at the producer level. Producers "activate" profiles for the fields they can
populate.

### Information Element Registry

IPFIX has a formal IANA-registered element registry where every field has a
unique ID, data type, and semantics. OCSF's `dictionary.json` serves a similar
purpose but is less formal. v2.0 could assign stable numeric IDs to dictionary
attributes for machine-readable field identification.

**Applies to: Workstream 5 (Network), Workstream 6 (Framework)**

---

## 7. UCO/CASE (Unified Cyber Ontology)

UCO is built for digital forensics and investigation. Its **facet-based
composition** model is the most relevant architectural insight for OCSF v2.0.

### Facet-Based Composition

Instead of deep inheritance trees, UCO objects can have multiple **facets**
composed onto them:

```
uco-observable:CyberItem "some-file"
  ← uco-observable:FileFacet
      filename: "malware.exe"
      path: "/tmp/"
      size: 45321
  ← uco-observable:ContentDataFacet
      hash_md5: "abc123..."
      mime_type: "application/x-dosexec"
  ← uco-observable:WindowsFileFacet
      sid: "S-1-5-21-..."
      zone_identifier: 3
```

This is fundamentally different from OCSF's approach where a `file` object
inherits from `_entity` and has all possible attributes defined. With facets:

- Platform-specific attributes become platform facets (replacing extensions)
- Analysis-specific attributes become analysis facets
- Objects stay small and composable
- No diamond inheritance problems

### Mapping to OCSF

| UCO Concept | OCSF Equivalent | v2.0 Opportunity |
|---|---|---|
| Facet | Profile (event-level only) | Extend profiles to object level |
| Action | Event class | Similar |
| Relationship | `edge` object | Similar |
| Observable | `observable` / `_entity` | Similar |
| Tool | `product` in metadata | Similar |
| Investigation | No equivalent | Could add forensic context |

### Key Insight: Object-Level Profiles

OCSF profiles currently only apply at the **event class** level. UCO's facets
apply at the **object** level. This would solve several problems:

- **Extensions replacement** (#1395): Instead of Windows/Linux/macOS extensions
  that patch objects, use platform facets: `process` + `windows_process_facet`,
  `process` + `linux_process_facet`
- **Composition vs. inheritance** (#1396): Objects compose capabilities via
  facets rather than inheriting from deep class trees
- **Object bloat**: The `file` object has 48 attributes because it must cover
  every platform and use case. With facets, the base `file` has ~10 core
  attributes and platform/analysis facets add the rest

**v2.0 recommendation:** Introduce object-level profiles (facets). The syntax
could mirror event-level profiles:

```json
{
  "name": "file",
  "extends": "_entity",
  "profiles": ["windows_file", "malware_analysis"],
  "attributes": { ... core attributes ... }
}
```

**Applies to: Workstream 6 (Framework), Workstream 8 (Object Improvements)**

---

## 8. D3FEND (MITRE Defensive Ontology)

D3FEND is built on BFO (ISO 21838) and provides a formal defensive cybersecurity
ontology. OCSF already references D3FEND in several class definitions.

### Alignment Points

| D3FEND Concept | OCSF Equivalent | Alignment |
|---|---|---|
| DigitalArtifact | `_entity` | Strong |
| DefensiveTechnique | Remediation activity_id | Strong |
| OffensiveTechnique | `attacks` (ATT&CK) | Strong |
| AuthenticationEvent | Authentication (3002) | Direct reference |
| AuthorizationEvent | Authorize Session (3003) | Direct reference |
| NetworkTrafficAnalysis | Network Activity classes | Partial |
| FileAnalysis | File System Activity (1001) | Partial |

### Key Insight: Ontology References

D3FEND classes have stable URIs (e.g., `d3f:AuthenticationEvent`). OCSF classes
reference these in their `references` blocks but don't machine-link them.

**v2.0 recommendation:** Add `ontology_refs` array to event class and object
definitions:

```json
{
  "ontology_refs": [
    {"ontology": "d3fend", "uri": "d3f:AuthenticationEvent"},
    {"ontology": "stix", "type": "identity"},
    {"ontology": "ecs", "category": "authentication"}
  ]
}
```

This enables automated cross-schema mapping and validates OCSF's alignment with
formal ontologies.

**Applies to: Workstream 7 (Graph Maturation)**

---

## 9. OpenTelemetry Semantic Conventions

OTel is primarily for observability but has relevant patterns for OCSF's
temporal and trace models.

### Trace/Span Model

OTel's distributed tracing uses a tree of spans:

```
Trace (trace_id)
  └─ Span A (span_id, parent_span_id=null)
       ├─ Span B (span_id, parent_span_id=A)
       └─ Span C (span_id, parent_span_id=A)
            └─ Span D (span_id, parent_span_id=C)
```

This is a natural temporal/causal graph. OCSF already has a `trace` profile
with `trace_id` and `span_id`, but it lacks `parent_span_id` for explicit
parent-child linking.

### Key Insight: Parent Event UID

OTel's `parent_span_id` enables explicit event-to-event causality chains
without requiring a full graph structure. For OCSF, adding `parent_event_uid`
to the base event would enable lightweight temporal chains:

```json
{
  "class_uid": 2004,
  "message": "Lateral movement detected",
  "parent_event_uid": "evt-initial-access-001",
  "trace_id": "investigation-42"
}
```

This complements the `event_graph` (full graph projection) with a simple linked
list for event chains — useful for high-volume sources where full graph is too
expensive.

### Resource Context

OTel uses flat resource attributes for context:
```
service.name: "auth-service"
service.namespace: "production"
service.version: "2.1.0"
host.name: "web-01"
host.id: "i-0123456789"
os.type: "linux"
```

OCSF's `metadata.product` + `device` is more structured but the flat pattern
is worth considering for `metadata` simplification.

**Applies to: Workstream 7 (Graph), Workstream 6 (Framework)**

---

## Consolidated v2.0 Impact Matrix

### Per-Workstream Additions from External Research

| WS | Addition | Source |
|---|---|---|
| **1: Entity Identity** | `actor` as role-bearer, not entity; mandatory UUID on all `_entity`; lifecycle timestamps (`created_time`/`modified_time`) on `_entity` base | BFO, STIX |
| **2: Remove Deprecated** | (No changes -- external research validates removal) | -- |
| **3: IAM Consolidation** | Multi-category tagging (array `category_uid`) so events can be both IAM and Network | ECS |
| **4: Finding Consolidation** | UCO facets for finding-type-specific attributes instead of subclasses | UCO/CASE |
| **5: Network Redesign** | `flow_direction_id` enum (IPFIX); `conn_state_id` enum (Zeek); `tunnel_chain` array replacing recursive proxy (Zeek); `orig_*`/`resp_*` directional counters (Zeek); protocol-specific profiles instead of classes | IPFIX, Zeek |
| **6: Framework** | Object-level profiles/facets (#1396); `ontology_refs` array for cross-schema mapping; stable numeric dictionary attribute IDs (IPFIX); `parent_event_uid` for lightweight causal chains (OTel) | UCO, IPFIX, OTel |
| **7: Graph Maturation** | BFO role modeling for `actor`; STIX relationship alignment; D3FEND ontology references; OTel trace model for temporal graphs | BFO, STIX, D3FEND, OTel |
| **8: Object Improvements** | OTel resource context for `metadata`; Zeek service detection for protocol identification | OTel, Zeek |
| **9: Discovery Redesign** | (No significant additions from external research) | -- |

### Architectural Principles Derived from External Research

1. **Continuant/Occurrent distinction** (BFO): Formalize the difference between
   entities that persist and events that happen. This is already implicit in
   OCSF but should be explicit in metadata.

2. **Mandatory identity** (STIX): Every entity that can be a graph node must
   have a unique identifier. `uid` should be `required` on all `_entity` types.

3. **Multi-dimensional classification** (ECS): Events should support array-based
   category tagging for cross-domain events (auth + network, finding + system).

4. **Facet-based composition** (UCO): Object-level profiles replace deep
   inheritance and platform extensions. Keeps objects small, composable, and
   platform-agnostic at the core.

5. **Protocol as profile, not class** (Zeek): Consider whether DNS, HTTP, SSH
   details should be profiles activated on a single Network Activity class
   rather than 14 separate classes.

6. **Directional symmetry** (IPFIX, Zeek): Network metrics must be unambiguously
   directional. Use initiator/responder semantics, not in/out.

7. **Lightweight causality** (OTel): `parent_event_uid` for simple event chains
   alongside `event_graph` for full graph projection. Different consumers need
   different complexity levels.

8. **Cross-schema references** (D3FEND): Machine-readable links to external
   ontologies validate OCSF's alignment and enable automated mapping.
