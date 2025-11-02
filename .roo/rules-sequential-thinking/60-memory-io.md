# 60-memory-io.md
> Exact hivemind I/O patterns for Sequential Thinking mode - Memory MCP integration for reasoning chain persistence and retrieval.

## Read Operations (Pre-Flight Consultation)

### Query Historical Reasoning Chains

**Pattern**: Before starting new chains, query for similar past reasoning processes.

```javascript
// Query for reasoning chains by pattern and domain
const historicalChains = await use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {
    query: "type:ReasoningChain pattern:<P1-P10> <task_domain>",
    limit: 3
  }
});

// Example: Query for debugging patterns
const debugChains = await use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {
    query: "type:ReasoningChain pattern:P2 debugging timeout",
    limit: 3
  }
});
```

### Query Reasoning Steps for Specific Patterns

**Pattern**: Get detailed step-by-step approaches from successful chains.

```javascript
// Get step details from successful chains
const successfulSteps = await use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {
    query: "type:ReasoningStep outcome:verified_successful pattern:P2",
    limit: 5
  }
});
```

### Query Evidence Quality Patterns

**Pattern**: Learn from chains with strong evidence backing.

```javascript
// Find chains with high evidence quality
const evidenceBasedChains = await use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {
    query: "type:ReasoningChain evidenceStrength:high outcome:verified_successful",
    limit: 3
  }
});
```

## Write Operations (During Execution)

### Create Reasoning Chain Entity

**Pattern**: At chain completion, create the main reasoning entity.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_entities",
  arguments: {
    entities: [{
      name: "reasoning#<runId>#<sha8(goal)>",
      entityType: "ReasoningChain",
      observations: [{
        type: "reasoning.chain",
        ts: new Date().toISOString(),
        mode: "sequential-thinking@<version>",
        repo: "<repo>",
        branch: "<branch>",
        fingerprint: sha256(JSON.stringify(chainData)),
        data: {
          goal: "<one-line objective>",
          pattern: "<P1-P10>",
          totalSteps: <count>,
          branchCount: <count>,
          decision: "<final_decision>",
          evidenceRefs: ["<entity_refs>"],
          constraints: ["<limits>"],
          outcome: "verified_successful|failed|partial",
          evidenceStrength: "high|medium|low",
          confidence: <percentage>
        }
      }]
    }]
  }
});
```

### Create Reasoning Step Entities

**Pattern**: After each reasoning step, persist it as a step entity.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_entities",
  arguments: {
    entities: [{
      name: "step#<reasoningId>#<thoughtNumber>",
      entityType: "ReasoningStep",
      observations: [{
        type: "reasoning.step",
        ts: new Date().toISOString(),
        mode: "sequential-thinking@<version>",
        repo: "<repo>",
        branch: "<branch>",
        fingerprint: sha256(step.thought),
        data: {
          thoughtNumber: step.thoughtNumber,
          totalThoughts: step.totalThoughts,
          thought: step.thought,
          nextThoughtNeeded: step.nextThoughtNeeded,
          isRevision: step.isRevision || false,
          revisesThought: step.revisesThought || null,
          branchFromThought: step.branchFromThought || null,
          branchId: step.branchId || null,
          metadata: step.metadata || {},
          evidenceGathered: ["<refs>"],
          contradictions: ["<issues>"]
        }
      }]
    }]
  }
});
```

### Add Revision Observations

**Pattern**: When hypotheses are falsified, record the revision.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "add_observations",
  arguments: {
    observations: [{
      entityName: "step#<reasoningId>#<revisedThoughtNumber>",
      contents: [{
        type: "reasoning.revision",
        ts: new Date().toISOString(),
        mode: "sequential-thinking@<version>",
        data: {
          originalThoughtNumber: <original>,
          revisedThoughtNumber: <revised>,
          reason: "<why falsified>",
          newHypothesis: "<corrected reasoning>",
          evidenceForRevision: ["<refs>"]
        }
      }]
    }]
  }
});
```

## Relation Creation (Linking Entities)

### Chain-to-Step Relations

**Pattern**: Link reasoning chain to its constituent steps.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_relations",
  arguments: {
    relations: [{
      from: "reasoning#<runId>#<sha8>",
      to: "step#<reasoningId>#1",
      relationType: "BELONGS_TO"
    },
    {
      from: "step#<reasoningId>#1",
      to: "step#<reasoningId>#2",
      relationType: "DERIVES_FROM"
    }]
  }
});
```

### Revision Relations

**Pattern**: Link revisions to original thoughts.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_relations",
  arguments: {
    relations: [{
      from: "step#<reasoningId>#<revisedNumber>",
      to: "step#<reasoningId>#<originalNumber>",
      relationType: "REVISES"
    }]
  }
});
```

### Branch Relations

**Pattern**: Link branches to their parent thoughts.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_relations",
  arguments: {
    relations: [{
      from: "step#<reasoningId>#<branchNumber>",
      to: "step#<reasoningId>#<parentNumber>",
      relationType: "BRANCHES_FROM"
    }]
  }
});
```

### Evidence Relations

**Pattern**: Link reasoning to supporting evidence.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_relations",
  arguments: {
    relations: [
      // References to external evidence
      {
        from: "step#<reasoningId>#<stepNumber>",
        to: "doc#<source>",
        relationType: "REFERENCES"
      },
      // Validation of hypotheses
      {
        from: "step#<reasoningId>#<stepNumber>",
        to: "err#<error_type>",
        relationType: "FALSIFIES"
      },
      // Links to fixes
      {
        from: "reasoning#<runId>#<sha8>",
        to: "fix#<strategy>",
        relationType: "PRODUCES"
      }
    ]
  }
});
```

### Pattern Relations

**Pattern**: Link chains to their Sequential Thinking patterns.

```javascript
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_relations",
  arguments: {
    relations: [{
      from: "reasoning#<runId>#<sha8>",
      to: "pattern#P2",  // Could be a pattern entity
      relationType: "USES"
    }]
  }
});
```

## Post-Flight Consolidation

### Merge Duplicate Chains

**Pattern**: Consolidate similar reasoning chains.

```javascript
// Find similar chains
const similarChains = await use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {
    query: "type:ReasoningChain goal:<similar_goal>",
    limit: 5
  }
});

// If similar outcomes, merge observations
if (similarChains.length > 1) {
  await use_mcp_tool({
    server_name: "memory",
    tool_name: "add_observations",
    arguments: {
      observations: [{
        entityName: similarChains[0].name,
        contents: similarChains.slice(1).flatMap(chain =>
          chain.observations.map(obs => ({
            ...obs,
            type: "reasoning.consolidated",
            data: { ...obs.data, consolidatedFrom: chain.name }
          }))
        )
      }]
    }
  });
}
```

### Update Success Rates

**Pattern**: Track pattern effectiveness over time.

```javascript
// After chain completion, update pattern success metrics
await use_mcp_tool({
  server_name: "memory",
  tool_name: "add_observations",
  arguments: {
    observations: [{
      entityName: "pattern#P2",
      contents: [{
        type: "pattern.effectiveness",
        ts: new Date().toISOString(),
        data: {
          totalApplications: <count + 1>,
          successfulApplications: <success_count + (outcome === 'verified_successful' ? 1 : 0)>,
          averageConfidence: <updated_average>,
          commonDomains: ["<domains>"]
        }
      }]
    }]
  }
});
```

## Degradation Handling

### Memory MCP Unavailable

**Pattern**: Continue reasoning with local state, queue writes.

```javascript
class ReasoningQueue {
  constructor() {
    this.queue = [];
  }

  // Queue memory operations for later replay
  async queue(operation, data) {
    this.queue.push({
      operation,
      data,
      timestamp: new Date().toISOString(),
      retryCount: 0
    });
  }

  // Attempt to replay queued operations
  async replay() {
    const remaining = [];
    for (const item of this.queue) {
      try {
        await use_mcp_tool({
          server_name: "memory",
          tool_name: item.operation,
          arguments: item.data
        });
      } catch (error) {
        item.retryCount++;
        if (item.retryCount < 3) {
          remaining.push(item);
        }
      }
    }
    this.queue = remaining;
  }
}

// Usage in reasoning mode
const memoryQueue = new ReasoningQueue();

// When memory operation fails
try {
  await createReasoningEntity(chainData);
} catch (error) {
  await memoryQueue.queue('create_entities', {
    entities: [chainEntity]
  });
}
```

### Partial Chain Recovery

**Pattern**: Save incomplete chains for resumption.

```javascript
// Save partial progress
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_entities",
  arguments: {
    entities: [{
      name: `reasoning_partial#${chainId}`,
      entityType: "ReasoningPartial",
      observations: [{
        type: "reasoning.partial",
        data: {
          currentStep: chain.currentStep,
          completedSteps: chain.steps,
          partialDecision: chain.partialDecision,
          canResume: true
        }
      }]
    }]
  }
});
```

## Query Optimization

### Pre-computed Aggregates

**Pattern**: Cache frequently accessed reasoning patterns.

```javascript
// Create aggregate entities for quick access
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_entities",
  arguments: {
    entities: [{
      name: "aggregate#reasoning#debugging#success_rate",
      entityType: "ReasoningAggregate",
      observations: [{
        type: "aggregate.reasoning",
        data: {
          pattern: "P2",
          domain: "debugging",
          totalChains: 150,
          successRate: 0.87,
          averageSteps: 5.2,
          commonEvidenceTypes: ["command_output", "log_analysis", "test_results"]
        }
      }]
    }]
  }
});
```

### Indexed Search Patterns

**Pattern**: Use indexed fields for fast retrieval.

```javascript
// Search with indexed fields
const fastResults = await use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {
    query: "type:ReasoningChain pattern:P2 outcome:verified_successful",
    sortBy: "ts",
    order: "desc",
    limit: 5
  }
});
```

## Audit Trail Maintenance

### Chain Provenance

**Pattern**: Maintain complete audit trail of reasoning evolution.

```javascript
// Record chain metadata
await use_mcp_tool({
  server_name: "memory",
  tool_name: "add_observations",
  arguments: {
    observations: [{
      entityName: "reasoning#<id>",
      contents: [{
        type: "reasoning.provenance",
        data: {
          createdBy: "sequential-thinking@v1.0",
          createdAt: new Date().toISOString(),
          sourcePattern: "P2",
          evidenceSources: ["memory_historical", "tool_outputs", "code_analysis"],
          validationStatus: "evidence_backed",
          reproducibilityScore: 0.95
        }
      }]
    }]
  }
});
```

### Learning Feedback Loop

**Pattern**: Enable continuous improvement of reasoning patterns.

```javascript
// After chain completion, analyze effectiveness
const effectivenessAnalysis = analyzeChainEffectiveness(chain);

await use_mcp_tool({
  server_name: "memory",
  tool_name: "add_observations",
  arguments: {
    observations: [{
      entityName: "pattern#P2",
      contents: [{
        type: "pattern.learning",
        data: {
          chainId: chain.id,
          effectiveness: effectivenessAnalysis.score,
          improvementAreas: effectivenessAnalysis.suggestions,
          patternStrengths: effectivenessAnalysis.strengths
        }
      }]
    }]
  }
});
```

This comprehensive I/O specification ensures Sequential Thinking integrates seamlessly with the Memory MCP, creating a persistent, queryable, and continuously improving reasoning system.