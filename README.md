# Golden Path Example Services

This repository, intended for `https://github.com/cbssmh/golden-path-example-services.git` on `main`, contains Service A only: a minimal Python standard-library HTTP service returning its fixed v0.1.0 status payload at `GET /`.

## Test

```bash
python -m unittest discover -s tests -v
```

## Container image

The GitHub Actions workflow builds on pull requests and builds plus pushes on pushes to `main` or version tags. The image repository is `ghcr.io/cbssmh/golden-path-service-a`; no token is stored in the repository. Images use Git SHA tags, never `latest`.

The GitOps repository deliberately pins a validated image tag manually. This workflow does not modify GitOps manifests or create pull requests.

**Current state: IMPLEMENTED BUT NOT RUNTIME VERIFIED.** No Kubernetes runtime verification has been claimed before the public GitOps repository is published.
