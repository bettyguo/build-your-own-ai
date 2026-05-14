# KV cache — from scratch

> _**[original]** · placeholder — full write-up lands in Phase 4._

Index entry: [Inference → KV cache](../README.md#inference)

## The one-line promise

A KV cache turns autoregressive decoding from O(n²) to O(n) by remembering
the keys and values it has already computed. It is the single biggest
inference optimization for transformer LMs.

## The minimum implementation

The full walkthrough — a ~100-line cached `generate()`, the cache layout, the
memory accounting, and a benchmark of cached vs. uncached decoding — will be
written in Phase 4 of this repo's build.
