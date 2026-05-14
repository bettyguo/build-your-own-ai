# Calibration / hallucination check — from scratch

> _**[original]** · placeholder — full write-up lands in Phase 4._

Index entry: [Evaluation → Calibration / hallucination check](../README.md#evaluation)

## The one-line promise

A model that says "I'm 90% sure" should be right about 90% of the time. The
gap between stated confidence and real accuracy — Expected Calibration
Error (ECE) — is the single most useful number for spotting hallucinations
that look confident.

## The minimum implementation

The full walkthrough — eliciting confidence, binning predictions, plotting
the reliability diagram, computing ECE, and using it for selective
prediction ("answer only when confident enough") — will be written in
Phase 4.
