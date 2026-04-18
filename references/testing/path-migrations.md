# Path Migrations

| old path / old phrasing | new path / new phrasing | visibility | shim / fallback | recommended one-liner | do-not-say |
|---|---|---|---|---|---|
| `install -> kubeblocks-create-cluster` | `install -> preflight -> engine entry` | customer-visible | no | 首次建库前先做 preflight，先把存储/拓扑/监控路径定下来。 | 装好 KubeBlocks 就能直接建任意数据库。 |
| `kubeblocks-create-cluster` | `kubeblocks-engine-generic` | internal-only | yes | generic fallback 统一收口到 engine-generic。 | create-cluster 继续作为冷启动主入口。 |
| `kubeblocks-create-cluster` for MySQL / PG / Redis / MongoDB / Kafka | dedicated `kubeblocks-engine-*` entry | customer-visible | yes, generic path kept only for `other-addons` | 高频引擎默认走对应 engine 入口，generic 只兜底其他引擎。 | 高频引擎继续推荐走 generic 模板。 |
| `kubeblocks-setup-monitoring` as one big skill | `kubeblocks-observability-router` -> `observability-existing-stack` or `observability-bootstrap-stack` | customer-visible | yes | 先判断是接入现有监控，还是新装一套监控基座。 | 有 metrics 就等于监控已经交付。 |
| Root skill mixes routing and long-form docs | Root skill is router only; deep explanation lives in README / leaf skills | internal-only | no | 根入口只做下一跳判断。 | 根入口里继续堆所有实现细节。 |
| `kubeblocks-addon-mysql` | `kubeblocks-engine-mysql` | internal-only | yes | MySQL 建库统一走 dedicated engine entry。 | 继续把 addon-mysql 当作冷启动主入口。 |
| `kubeblocks-addon-postgresql` | `kubeblocks-engine-postgresql` | internal-only | yes | PostgreSQL 建库统一走 dedicated engine entry。 | 继续把 addon-postgresql 当作冷启动主入口。 |
| `kubeblocks-addon-redis` | `kubeblocks-engine-redis` | internal-only | yes | Redis 建库统一走 dedicated engine entry。 | 继续把 addon-redis 当作冷启动主入口。 |
| `kubeblocks-addon-mongodb` | `kubeblocks-engine-mongodb` | internal-only | yes | MongoDB 建库统一走 dedicated engine entry。 | 继续把 addon-mongodb 当作冷启动主入口。 |
| `kubeblocks-addon-kafka` | `kubeblocks-engine-kafka` | internal-only | yes | Kafka 建库统一走 dedicated engine entry。 | 继续把 addon-kafka 当作冷启动主入口。 |
| `kubeblocks-addon-elasticsearch` | `kubeblocks-engine-elasticsearch` | internal-only | yes | Elasticsearch 建库统一走 dedicated engine entry。 | 继续把 addon-elasticsearch 当作冷启动主入口。 |
| `kubeblocks-addon-milvus` | `kubeblocks-engine-milvus` | internal-only | yes | Milvus 建库统一走 dedicated engine entry。 | 继续把 addon-milvus 当作冷启动主入口。 |
| `kubeblocks-addon-qdrant` | `kubeblocks-engine-qdrant` | internal-only | yes | Qdrant 建库统一走 dedicated engine entry。 | 继续把 addon-qdrant 当作冷启动主入口。 |
| `kubeblocks-addon-rabbitmq` | `kubeblocks-engine-rabbitmq` | internal-only | yes | RabbitMQ 建库统一走 dedicated engine entry。 | 继续把 addon-rabbitmq 当作冷启动主入口。 |
| `kubeblocks-cluster-lifecycle` | `kubeblocks-op-lifecycle` | customer-visible | yes | 生命周期动作统一收口到共享 Day-2 层。 | 停启重启仍然作为独立主入口保留。 |
| `kubeblocks-horizontal-scaling` | `kubeblocks-op-horizontal-scale` | customer-visible | yes | 横向扩缩统一走 ops 能力入口，再按 capability matrix 判断支持面。 | 所有数据库都默认支持同一种横向扩缩。 |
| `kubeblocks-vertical-scaling` | `kubeblocks-op-vertical-scale` | customer-visible | yes | 纵向扩缩先看该引擎是否支持、是否需重启。 | 资源修改不需要 capability 判断。 |
| `kubeblocks-volume-expansion` | `kubeblocks-op-volume-expansion` | customer-visible | yes | 先看 StorageClass 扩容能力，再决定是否允许扩容。 | 卷扩容对所有存储类都一样。 |
| `kubeblocks-reconfigure-parameters` | `kubeblocks-op-reconfigure` | customer-visible | yes | 参数改动要区分动态/静态与引擎支持面。 | 参数改动总能无重启生效。 |
| `kubeblocks-backup` | `kubeblocks-op-backup` | customer-visible | yes | 先看该引擎与环境是否具备备份链路。 | 所有数据库都天然支持同一种备份。 |
| `kubeblocks-restore` | `kubeblocks-op-restore` | customer-visible | yes | 恢复入口和备份入口解耦，但都受 capability matrix 约束。 | 只要能备份就一定能同路径恢复。 |
| `kubeblocks-expose-service` | `kubeblocks-op-expose` | customer-visible | yes | 暴露方式统一收口，但需结合网络与安全前提。 | 暴露数据库只是一条 Service 改动。 |
| `kubeblocks-switchover` | `kubeblocks-op-switchover` | customer-visible | yes | 主备切换必须看引擎拓扑和 HA 机制。 | 任意主从库都能同样 switchover。 |
| `kubeblocks-minor-version-upgrade` | `kubeblocks-op-upgrade` | internal-only | yes | 升级入口统一收口，但能力与风险由 matrix 驱动。 | 升级路径只看版本号，不看引擎与拓扑。 |
