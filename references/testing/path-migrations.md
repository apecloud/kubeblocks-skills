# Path Migrations

| old path / old phrasing | new path / new phrasing | visibility | shim / fallback | recommended one-liner | do-not-say |
|---|---|---|---|---|---|
| `install -> create-cluster` | `install -> preflight -> engine entry` | customer-visible | no | 首次建库前先做 preflight，先把存储/拓扑/监控路径定下来。 | 装好 KubeBlocks 就能直接建任意数据库。 |
| `create-cluster` for MySQL / PG / Redis / MongoDB / Kafka | dedicated `addon-*` engine entry | customer-visible | yes, generic path kept only for `other-addons` | 高频引擎默认走对应 addon 入口，generic 只兜底其他引擎。 | 高频引擎继续推荐走 generic 模板。 |
| `setup-monitoring` as one big skill | `setup-monitoring` shim -> `observability-existing-stack` or `observability-bootstrap-stack` | customer-visible | yes | 先判断是接入现有监控，还是新装一套监控基座。 | 有 metrics 就等于监控已经交付。 |
| Root skill mixes routing and long-form docs | Root skill is router only; deep explanation lives in README / leaf skills | internal-only | no | 根入口只做下一跳判断。 | 根入口里继续堆所有实现细节。 |
