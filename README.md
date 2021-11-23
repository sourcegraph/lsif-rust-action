# Sourcegraph Rust LSIF Indexer GitHub Action

This action generates LSIF data from Rust source code using [rust-analyzer](https://github.com/rust-analyzer/rust-analyzer). The LSIF data can be further uploaded to Sourcegraph using [lsif-upload-action](https://github.com/sourcegraph/lsif-upload-action).

## Pre-requisites

- GitHub-provided Runners should work out-of-the-box.
- Self-hosted runners need to have Python 3.5+ and `curl` installed, and the runner's target needs to be one for which [`rust-analyzer` release binaries](https://github.com/rust-analyzer/rust-analyzer/releases) are available.

## Usage

The following inputs can be set.

| name         | default   | description |
| ------------ | --------- | ----------- |
| `project_root` | `.`       | The root of the repository. |

The following is a complete example that generates the LSIF index and uploads it to [sourcegraph.com](https://sourcegraph.com). Save it in `.github/workflows/lsif.yaml`.

```
name: LSIF
on:
  - push
jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate LSIF data
        uses: sourcegraph/lsif-rust-action@main
      - name: Upload LSIF data
        uses: sourcegraph/lsif-upload-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Contributing

If you run into issues using this GitHub Action,
please [file an issue](https://github.com/sourcegraph/lsif-rust-action/issues),
including relevant CI logs.

Contributors should abide by the [Sourcegraph Code of Conduct](https://handbook.sourcegraph.com/community/code_of_conduct).
