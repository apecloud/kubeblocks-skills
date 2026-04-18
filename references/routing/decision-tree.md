# Decision Tree

1. No Kubernetes cluster -> local cluster creation skill
2. Kubernetes exists but KubeBlocks absent -> install skill
3. Environment readiness unknown -> preflight
4. Create intent:
   - Tier-1 engine -> dedicated engine entry
   - uncovered engine -> generic fallback
5. Existing cluster operation -> op skill
6. Security / account management -> configure-tls or manage-accounts
7. Monitoring / observability -> observability router
8. Failures / unknown state at any phase -> troubleshoot, then recovery-only skills if needed
