# py-hamilton-step

A Python library that exposes Hamilton Venus steps directly as Python functions. One function per step, all parameters preserved, no additional abstraction.

## Why this exists

Existing approaches to Hamilton automation tend to make decisions on your behalf: they hide parameters, infer behavior, or impose workflow structure. That is fine but it becomes hard to use as a foundation. So py-hamilton-step performs no extra abstraction. It is a 1 to 1 translation to expose venus steps in a python API.

The intended use case is AI-driven protocol composition, where an agent needs to call steps directly.

## Planned architecture

py-hamilton-step is the foundation layer of a three-tier system, currently under development:

- **py-hamilton-step** — local Python library communicating with Venus via virtual serial port (com0com on Windows x64, Parallels on development environments)
- **FastAPI layer** — REST interface making the local library network-accessible for multi-instrument orchestration
- **MCP layer** — Model Context Protocol wrapper exposing Hamilton control as tools to AI agents

## License

Apache 2.0
