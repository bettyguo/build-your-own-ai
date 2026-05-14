# Multi-agent orchestration — from scratch

> _**[original]** · placeholder — full write-up lands in Phase 4._

Index entry: [Agents → Multi-agent orchestration](../README.md#agents)

## The one-line promise

A planner agent decomposes a task and dispatches it to worker agents; the
planner aggregates results and decides when the task is done. The whole
loop in ~150 lines, no CrewAI, no AutoGen — so you can see exactly where
the coordination cost is.

## The minimum implementation

The full walkthrough — the planner prompt, the worker dispatcher, the
result aggregator, and a brutally honest comparison with one well-prompted
agent on the same task — will be written in Phase 4.
