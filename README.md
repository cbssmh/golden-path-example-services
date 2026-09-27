# Golden Path Example Services

This repository, intended for
`https://github.com/cbssmh/golden-path-example-services.git` on `main`,
contains Service A only: a minimal Python standard-library HTTP service
returning its fixed v0.1.0 status payload at `GET /`.

## Test

```bash
python -m unittest discover -s tests -v
```

## Container image

The GitHub Actions workflow runs `test-and-build` for pull requests and pushes.
That job has no package-write permission. The dependent `publish` job runs only
for pushes to `main` or `v*` tags and is the only job with `packages: write`.
The image repository is `ghcr.io/cbssmh/golden-path-service-a`; no long-lived
registry token is stored in the repository. Published images use Git commit
tags, never `latest`.

The GitOps repository deliberately pins a separately reviewed OCI digest, not
a mutable image tag. This workflow does not modify GitOps manifests or create
pull requests. Publishing the SC-1 image did not change the deployed Golden
Path digest.

## Supply-chain controls

- every external Action reference uses a full commit SHA;
- repository Actions policy permits only the Action repositories used by the
  workflow and requires SHA pinning;
- Python, Buildx, QEMU/binfmt, and BuildKit inputs are explicit;
- the Dockerfile pins Python 3.12.12 on Alpine 3.21 by manifest-list digest;
- `main-governance` requires a current pull request and successful
  `test-and-build`, with force push and deletion blocked and no bypass actors;
- `release-tag-protection` blocks update and deletion of `v*` tags.

The successful SC-1 main workflow run `36313661725` published source commit
`37a08f0e837635f15bea1bd692ac1a9997789912` for linux/amd64 and linux/arm64.
These controls are `SOURCE-CONFIRMED`, `TEST-VERIFIED`, and `RELEASED`.

Service A itself has been observed Ready and serving its endpoint in the
disposable Golden Path runtime exercises. That runtime evidence applies to the
GitOps-pinned deployment digest, not automatically to every later image
published by this repository.
