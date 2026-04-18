# Decision Tree

1. No Kubernetes cluster -> local cluster creation skill
2. Kubernetes exists but KubeBlocks absent -> install skill
3. Environment readiness unknown -> preflight
4. Create intent:
   - Tier-1 engine -> dedicated engine entry
   - uncovered engine -> generic fallback
5. Existing cluster operation -> shared capability layer (`kubeblocks-op-*`)
6. Access / security asks -> `manage-accounts` or `configure-tls`
7. Monitoring / observability -> observability router
8. Failures / unknown state at any phase -> troubleshoot first
9. Replica repair or HA recovery after diagnosis -> recovery path such as `rebuild-replica`
10. Destructive teardown -> `delete-cluster` only after data-protection checks
