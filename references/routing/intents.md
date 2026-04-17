# Routing Intents

V2 routing should normalize user asks into a small, stable set of intent classes:

- install KubeBlocks
- run preflight / environment profiling
- create a database engine
- operate an existing cluster
- configure observability
- troubleshoot

Engine-create intents must then resolve to one of:

- Tier-1 dedicated entry
- Tier-2 family-backed path
- Tier-3 generic fallback

Tier-1 intents must never default to the generic fallback.
