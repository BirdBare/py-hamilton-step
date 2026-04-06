# py-hamilton-step

A Python library that exposes Hamilton Venus steps directly as Python functions. One function per step, all parameters preserved, no additional abstraction.

## Why this exists

Existing approaches to Hamilton automation tend to make decisions on your behalf: they hide parameters, infer behavior, or impose workflow structure. PyHamiltonSteps does none of that. It is a thin, honest binding to Venus, the kind of foundation you can build on without fighting the library.

The intended use case is AI-driven protocol composition, where an agent needs to call steps directly without a library second-guessing its decisions. A system that hides complexity is a liability here; this one doesn't.

## Design principles

**No abstraction.** Every Venus step is exposed with its full parameter set. Nothing is inferred or defaulted away from you.

**Constrained where it matters.** Liquid classes are defined enumerations, not free strings. The places where wrong values cause instrument damage are exactly the places where constraints belong.

**One command at a time.** The execution model is strictly sequential. There is no concurrency, no queueing, no ambiguity about what the instrument is doing.

**Serial over HTTP.** Communication uses a persistent JSON protocol over a virtual serial connection. PyHamilton's HTTP polling approach causes log file flooding; this doesn't.

**Log-based validation.** Hamilton's native log output is the source of truth for test validation, with no parallel truth sources.

## Planned architecture

PyHamiltonSteps is the foundation layer of a three-tier system, currently under development:

- **PyHamiltonSteps** — local Python library communicating with Venus via virtual serial port (com0com on Windows x64, Parallels on development environments)
- **FastAPI layer** — REST interface making the local library network-accessible for multi-instrument orchestration
- **MCP layer** — Model Context Protocol wrapper exposing Hamilton control as tools to AI agents

## License

Apache 2.0
