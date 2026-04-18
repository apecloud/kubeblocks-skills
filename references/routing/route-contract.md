# Route Contract

The route contract defines three things:

1. Required profiles before an engine can be created
2. Allowed next hops for each intent
3. Forbidden paths that must be treated as errors
4. Legacy-name compatibility through `references/routing/shim-map.yaml`

Examples:

- `mysql` / `postgresql` on an unknown ACK environment:
  - required profile: `kubeblocks-preflight`
  - allowed next hop: dedicated engine skill
  - forbidden path: `kubeblocks-engine-generic`

- broad monitoring request:
  - allowed next hop: `kubeblocks-observability-router`
  - follow-up: `existing-stack` or `bootstrap-stack`

- old V1 engine entry names:
  - allowed only as shim targets
  - forbidden as primary recommended routes in root router or README

- family labels:
  - allowed in taxonomy, comparison, or fallback explanation
  - forbidden as the primary create-time route for Tier-1 engines

- runtime protocol:
  - allowed only as optional templates under `references/templates/*`
  - forbidden as an implicit dependency for cold-start routing
