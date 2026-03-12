# KubeBlocks Agent Skills

A collection of [Agent Skills](https://docs.cursor.com/context/skills) for managing [KubeBlocks](https://kubeblocks.io/) — the Kubernetes operator for databases.

These skills work with any AI coding agent that supports markdown-based skill files (Cursor, Claude Code, OpenClaw, etc.).

## Available Skills

| Skill | Description |
|-------|-------------|
| [install-kubeblocks](./install-kubeblocks/SKILL.md) | Install the KubeBlocks operator on any Kubernetes cluster. Handles prerequisite tool installation (kubectl, Helm), version selection, network environment detection (China/global), image registry configuration, and post-install verification. |
| [create-local-k8s-cluster](./create-local-k8s-cluster/SKILL.md) | Create a local Kubernetes test cluster using Kind, Minikube, or k3d. Use when no existing cluster is available for development or testing. |

## How to Use

### Cursor

Copy or symlink the skill directory into your Cursor skills folder:

```bash
# Personal skill (available across all projects)
cp -r install-kubeblocks ~/.cursor/skills/

# Project skill (shared via repository)
cp -r install-kubeblocks .cursor/skills/
```

### Claude Code

Reference the SKILL.md file when prompting:

```
Read install-kubeblocks/SKILL.md and follow the instructions to install KubeBlocks on my cluster.
```

### Other Agents

Point the agent to the `SKILL.md` file in the skill directory. The instructions are written in standard markdown and are agent-agnostic.

## Skill Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md          # Main instructions (entry point)
└── reference.md      # Detailed reference material (read on demand)
```

- **SKILL.md**: Concise step-by-step workflow. This is what the agent reads first.
- **reference.md**: Detailed configuration options, troubleshooting, and additional procedures. The agent reads this only when deeper information is needed.

## Documentation

- [KubeBlocks Official Docs](https://kubeblocks.io/docs/preview/user_docs/overview/introduction)
- [KubeBlocks GitHub](https://github.com/apecloud/kubeblocks)
- [KubeBlocks LLM Index](https://kubeblocks.io/llms-full.txt)

## Contributing

To add a new skill:

1. Create a new directory under the repository root (e.g., `manage-mysql-cluster/`)
2. Add a `SKILL.md` with YAML frontmatter (`name` and `description` fields)
3. Optionally add `reference.md` for detailed supplementary material
4. Update this README's "Available Skills" table

## License

[Apache 2.0](LICENSE)
