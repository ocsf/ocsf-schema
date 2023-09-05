# Add devices to Security Finding

date: 2023-09-05
proposer: Jeremy Fisher
deciders: Kyle, Srot (?)

## Proposed Additions

| Caption       | Name                       | Type       | Description                                      |
| ------------- | -------------------------- | ---------- | ------------------------------------------------ |
| Devices       | `security_finding.devices` | `device`   | Allows associating devices to security findings. |


## Context

Endpoint protection platforms like CrowdStrike provide information about
devices implicated in or associated to security findings. OCSF security
findings can include IP and hostname observables, but OCSF encourages mapping
"primary" data to named objects. It is rather natural for an analyst to want to
review identifying information about the endpoint in security findings about
the endpoint.

This relationship has been discussed in the OCSF Slack workspace; while it
seems to have buy-in, it hasn't been implemented.


## Positive Consequences

We will be able to better present and search on this very relevant information.

## Negative Consequences

OCSF may answer this need differently in the future. This seems unlikely.


## Alternatives Considered

We considered mapping IP and hostname to observables, but decided against it
because: 

1. We don't currently show observables in results†. 
2. OCSF encourages mapping "primary" data from events to named relationships.
3. The device implicated in an endpoint security finding is highly relevant and
   warrants a named relationship.
4. This will better facilitate searching and joining with devices.


_† There is something of a hack in play to search by observables that makes it
complicated to show them without another hack, and we're holding out to fix
both in a way that doesn't break joins and follow up queries soon._
