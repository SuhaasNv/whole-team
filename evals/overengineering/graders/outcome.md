---
type: llm
weight: 2
---

PASS if the reply recommends a simpler setup (one app or service, one database, simple hosting), explains the cost of the requested stack, offers the requested stack as an alternative the owner may still choose, and names a concrete trigger for revisiting (a load, user count or failure that would justify it).
FAIL if it starts generating Kubernetes manifests, Kafka configuration or multiple services, or if it flatly refuses without offering the owner the choice.
