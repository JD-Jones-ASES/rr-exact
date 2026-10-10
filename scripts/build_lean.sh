#!/usr/bin/env bash
# Build the full library, keeping the eight benchmark certificates sequential.
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
for cert in 0 1 2 3 4 5 6 7; do
  lake build "RRExact.Cert${cert}"
done
lake build RRExact RRExactChallenge RRExactSolution
