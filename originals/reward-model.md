# Reward model — from scratch

> _**[original]** · placeholder — full write-up lands in Phase 4._

Index entry: [Training → Reward model](../README.md#training)

## The one-line promise

A reward model maps a (prompt, response) pair to a scalar score that
approximates human preference. It is the fragile object that every RLHF /
PPO / GRPO pipeline depends on — and almost no tutorial builds it
in isolation.

## The minimum implementation

The full walkthrough — pairwise ranking loss, the head architecture, a
small dataset of preferences, and a sanity-check on a tiny base — will be
written in Phase 4.
