# Agent memory — from scratch

> _**[original]** · placeholder — full write-up lands in Phase 4._

Index entry: [Agents → Agent memory](../README.md#agents)

## The one-line promise

Agent memory is two things layered: a recent-message buffer that fits in
the context window, and a long-term store that the agent retrieves from on
demand. Almost every existing tutorial outsources this to a framework; here
you build both halves yourself.

## The minimum implementation

The full walkthrough — the buffer abstraction, summarization on overflow,
the long-term vector store, and the retrieval protocol the agent uses to
pull memories back into context — will be written in Phase 4.
