# Routing Intents

V2 routing should normalize user asks into a small, stable set of intent classes:

- install KubeBlocks
- run preflight / environment profiling
- create a database engine
- operate an existing cluster
- manage security / accounts
- configure observability
- troubleshoot

Engine-create intents must then resolve to one of:

- Tier-1 dedicated entry
- Tier-3 generic fallback

Family labels remain useful for taxonomy, comparison, and low-frequency explanation, but they are not a cold-start create-time primary entry.

Tier-1 intents must never default to the generic fallback.
