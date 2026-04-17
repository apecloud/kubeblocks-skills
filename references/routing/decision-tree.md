# Decision Tree

1. No Kubernetes cluster -> local cluster creation skill
2. Kubernetes exists but KubeBlocks absent -> install skill
3. Environment readiness unknown -> preflight
4. Create intent:
   - Tier-1 engine -> dedicated engine entry
   - Tier-2 engine -> family guidance + explicit target
   - Tier-3 engine -> generic fallback
5. Existing cluster operation -> op skill
6. Monitoring / observability -> observability router
7. Failures / unknown state -> troubleshoot
