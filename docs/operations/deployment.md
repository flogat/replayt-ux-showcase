# Deployment

This document describes how to build and publish container images for the replayt-ux-showcase project, including credential requirements and optional overrides.

## GitHub Container Registry (GHCR) Publishing

### Credential Model: Default vs. Custom

The workflow uses **two tiers** of credentials for GHCR authentication:

| Tier | Variables | Required? | When Used |
|------|-----------|-----------|-----------|
| **Default (GitHub-native)** | `GITHUB_TOKEN`, `GITHUB_ACTOR` | Always available in GitHub Actions | Fallback when custom credentials are absent |
| **Custom (Repository secrets)** | `GHCR_USERNAME`, `GHCR_TOKEN` | Optional | When publishing to a different org/actor, or when the default token lacks permissions |

### Default Credentials (No Configuration Required)

When **no** repository secrets are defined, the workflow automatically uses:

- **`GITHUB_TOKEN`** — GitHub-provided ephemeral token with `packages:write` scope (when `permissions: packages: write` is declared)
- **`GITHUB_ACTOR`** — The user or app that triggered the workflow run

This works for:
- Publishing to `ghcr.io/${{ github.repository }}` (same repository namespace)
- Standard CI/CD triggers on `push`, `pull_request`, or `workflow_dispatch`

### Custom GHCR Credentials (Optional Overrides)

Define these **repository secrets** only when you need behavior the default token cannot provide:

| Secret | Purpose | When Needed |
|--------|---------|-------------|
| `GHCR_USERNAME` | Custom actor for authentication | Cross-organization publishing, or when `GITHUB_ACTOR` resolution fails for technical reasons |
| `GHCR_TOKEN` | Custom PAT or fine-grained token | The default `GITHUB_TOKEN` lacks `packages:write` permission, or you need a long-lived token for external integrations |

#### Use Cases for Custom Credentials

1. **Cross-organization publishing**  
   Your workflow publishes to `ghcr.io/other-org/image` but runs in `my-org/repo`. The default `GITHUB_TOKEN` can only publish within `my-org`.

2. **Repository permissions restrictions**  
   Some organizations restrict `GITHUB_TOKEN` permissions via **Settings > Actions > General > Workflow permissions**. If `packages:write` is not granted, use a classic PAT with `write:packages` scope stored in `GHCR_TOKEN`.

3. **External integrations**  
   Build systems outside GitHub Actions (e.g., Jenkins, GitLab CI mirroring) may require a long-lived classic PAT instead of the ephemeral `GITHUB_TOKEN`.

### Workflow Behavior

The workflow `.github/workflows/build-and-publish-images.yml` evaluates credentials in this order:

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  # Use custom secrets if defined; fall back to GitHub-native defaults
  GHCR_USERNAME: ${{ secrets.GHCR_USERNAME || github.actor }}
  GHCR_TOKEN: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}
```

**Key properties:**
- The workflow **never fails** when custom secrets are absent — it uses defaults transparently.
- If **both** custom secrets **and** the default token are unavailable (e.g., in a fork without `packages:write`), the login step fails with a clear authentication error.
- Custom secrets are evaluated **per-job**, so mixed configurations (one secret defined, the other not) resolve via fallback on the undefined value only.

### Security Considerations

| Concern | Guidance |
|---------|----------|
| Token scope | Prefer `GITHUB_TOKEN` when possible — it is scoped to the workflow run and expires automatically. Classic PATs in `GHCR_TOKEN` should use the minimum scope (`write:packages` only, not `repo` or `admin` if avoidable). |
| Secret rotation | If using a PAT in `GHCR_TOKEN`, document an owner and rotation cadence (e.g., quarterly) in your team runbook. |
| Fork safety | Forks do not inherit repository secrets. Fork-based CI builds will use defaults and may skip publishing or fail login — this is expected and safe. |
| Least privilege | When cross-org publishing is required, consider a **fine-grained PAT** targeting only the destination organization with `packages:write` scope. Classic PATs grant broader access by default. |

### Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `denied: installation not allowed to Write organization package` | `GITHUB_TOKEN` lacks `packages:write` in organization settings | Enable **Settings > Actions > General > Workflow permissions > Read and write permissions**, or use a custom `GHCR_TOKEN` PAT. |
| `unauthorized: authentication required` | No credentials available (fork CI, or secrets not configured and `GITHUB_TOKEN` disabled) | Confirm `permissions: packages: write` in workflow, or add `GHCR_USERNAME` + `GHCR_TOKEN` secrets. |
| Published to wrong namespace (e.g., `ghcr.io/user/repo` vs `ghcr.io/org/repo`) | `GITHUB_ACTOR` resolves to the triggering user, not the organization | Set `GHCR_USERNAME` explicitly to the desired org name (e.g., `my-org`). |

## Related

- **CI workflow:** [`.github/workflows/build-and-publish-images.yml`](../../.github/workflows/build-and-publish-images.yml)
- **Design principles:** [`docs/DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#github-actions-ci-workflow)
- **Manual image build:** `docker build -t ghcr.io/${GITHUB_REPOSITORY}:local .` (requires local `docker login ghcr.io`)
