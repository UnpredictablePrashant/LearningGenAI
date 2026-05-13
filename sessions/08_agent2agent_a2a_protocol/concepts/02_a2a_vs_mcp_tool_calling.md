# 02. A2A vs MCP vs Tool Calling

A2A, MCP, and tool calling are related, but they solve different integration
problems.

## Short Version

| Pattern | Best For | Mental Model |
|---------|----------|--------------|
| Tool calling | One model selecting functions inside one app loop | Function dispatch |
| MCP | An agent or model accessing external tools/resources | Tool and resource protocol |
| A2A | Independent agents collaborating as peers | Agent service protocol |

## Tool Calling

Tool calling lets a model emit a structured function call:

```
model -> call get_incident("INC-1001") -> tool result -> model answer
```

The application owns:

- Tool definitions
- Argument validation
- Function execution
- Error handling
- Final response loop

Tool calling is ideal when one app controls the model and all tools.

## MCP

Model Context Protocol standardizes how an AI application connects to tools,
resources, and prompts exposed by MCP servers.

It is useful when:

- You want reusable tool servers.
- Tools should be discoverable by a client.
- Data sources and actions need structured schemas.
- Multiple clients should use the same tool server.

In this course, Session 05 covered MCP as a protocol for tool and resource
access.

## A2A

A2A standardizes collaboration between agents.

An A2A server agent is not just a function. It can:

- Own a long-running task.
- Maintain its own context.
- Ask clarifying questions.
- Stream progress.
- Produce artifacts.
- Hide internal implementation.
- Use MCP tools internally.

The client agent delegates work and receives task state/results.

## A2A and MCP Together

The official A2A specification describes A2A and MCP as complementary. MCP is
focused on tools/resources; A2A is focused on independent agents collaborating.
An A2A server agent may use MCP tools internally while fulfilling an A2A task.

Reference: [A2A relationship to MCP](https://a2a-protocol.org/latest/specification/#appendix-b-relationship-to-mcp-model-context-protocol)

Example:

```
client support agent
  -> A2A request to SRE incident agent
      -> SRE agent uses MCP server for PagerDuty
      -> SRE agent uses MCP server for Kubernetes
      -> SRE agent returns A2A artifact
```

The client sees an agent contract. The server agent privately decides which
tools to call.

## Practical Comparison

| Question | Tool Calling | MCP | A2A |
|----------|--------------|-----|-----|
| Who owns execution? | App loop | MCP client calls server tools | Remote agent |
| Is the callee an agent? | Usually no | Usually tool/resource server | Yes |
| Can work be long-running? | App-specific | Tool-specific | First-class task pattern |
| Does callee expose internals? | Function schema | Tool/resource schemas | Capability/skill contract |
| Main object | Tool call | Tool/resource/prompt | Task/message/artifact |
| Good boundary | Same app | Tool provider | Agent provider |

## DevOps Analogy

Tool calling is like importing a function in your service.

MCP is like calling a standardized internal platform API for tools and resources.

A2A is like asking another service team to own a workflow and return the result
through a service contract.

## Common Mistakes

Mistake: "A2A replaces MCP."

Reality: A2A and MCP can be used together.

Mistake: "Every tool should become an A2A agent."

Reality: A database lookup tool should probably stay a tool. Use A2A when the
callee has meaningful agency, workflow ownership, or independent lifecycle.

Mistake: "A2A means sharing chain-of-thought between agents."

Reality: A2A is designed for collaboration without requiring internal state or
private reasoning to be exposed.

## Key Takeaways

1. Use tool calling for functions in one app loop.
2. Use MCP for reusable tools/resources.
3. Use A2A for peer agent collaboration and delegation.
4. An A2A server agent can use MCP internally.
5. Choose the smallest boundary that gives you the operational control you need.

