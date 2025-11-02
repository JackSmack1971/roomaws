# 40-tool-usage.md
> Specific usage instructions for the sequentialthinking MCP tool and integration with other tools.

## Sequential Thinking MCP Tool Usage

### Tool Contract
The `sequentialthinking` tool accepts a JSON object with the following stable fields:

```json
{
  "thought": "Natural-language step content (compact, ≤8 lines)",
  "thoughtNumber": 2,
  "totalThoughts": 4,
  "nextThoughtNeeded": true,
  "isRevision": false,
  "revisesThought": null,
  "branchFromThought": null,
  "branchId": null,
  "metadata": {
    "goal": "one-line objective",
    "evidenceRefs": ["ulid:obs_01", "url:source"],
    "constraints": ["time<=5m", "tokens<=2k"],
    "decision": null
  }
}
```

### Required Fields
- **thought**: The actual reasoning content
- **thoughtNumber**: Current step in sequence (starts at 1)
- **totalThoughts**: Estimated total steps (can be adjusted)
- **nextThoughtNeeded**: Whether to continue the chain

### Optional Control Fields
- **isRevision**: Set to `true` when correcting a previous thought
- **revisesThought**: Number of the thought being revised
- **branchFromThought**: Number of the thought this branches from
- **branchId**: Identifier for the branch (e.g., "option-a", "path-1")

### Metadata Fields
- **goal**: One-line objective for the entire chain
- **evidenceRefs**: References to observations, docs, or external sources
- **constraints**: Time, token, or other limits
- **decision**: Set in terminal thoughts with final conclusion

## Integration with Other Tools

### Memory MCP Integration

**Before Sequential Thinking**:
```javascript
// Query historical reasoning patterns
const history = await use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {
    query: "type:ReasoningChain pattern:<P1-P10> <task_domain>",
    limit: 3
  }
});
```

**During Sequential Thinking**:
```javascript
// After each step, persist observations
await use_mcp_tool({
  server_name: "memory",
  tool_name: "add_observations",
  arguments: {
    observations: [{
      entityName: "step#reasoning#<id>#<thoughtNumber>",
      contents: [JSON.stringify({
        type: "reasoning.step",
        ts: new Date().toISOString(),
        mode: "sequential-thinking@<version>",
        data: stepData
      })]
    }]
  }
});
```

**After Chain Completion**:
```javascript
// Create complete reasoning chain entity
await use_mcp_tool({
  server_name: "memory",
  tool_name: "create_entities",
  arguments: {
    entities: [{
      name: "reasoning#<runId>#<sha8(goal)>",
      entityType: "ReasoningChain",
      observations: [{
        type: "reasoning.chain",
        data: {
          goal: goal,
          pattern: pattern,
          totalSteps: finalStepCount,
          decision: finalDecision,
          outcome: "verified_successful"
        }
      }]
    }]
  }
});
```

### Read Tools Integration

**Code Analysis**:
```javascript
// Gather evidence for reasoning steps
const codeAnalysis = await read_file({
  path: "src/component.ts"
});

// Use in sequential thinking
sequentialthinking({
  thought: `Code analysis shows ${findings}. Hypothesis: ${interpretation}`,
  thoughtNumber: currentStep,
  metadata: {
    evidenceRefs: [`file:src/component.ts:L${lineNumber}`]
  }
});
```

**Search Tools**:
```javascript
// Search for patterns or documentation
const searchResults = await search_files({
  path: ".",
  regex: "error.*timeout",
  file_pattern: "*.ts"
});

// Incorporate into reasoning
sequentialthinking({
  thought: `Search found ${results.length} timeout-related patterns. Indicates ${pattern}`,
  metadata: {
    evidenceRefs: results.map(r => `search:timeout_pattern:${r.file}`)
  }
});
```

### Command Execution Integration

**Testing Hypotheses**:
```javascript
// Run tests to validate hypothesis
const testResult = await execute_command({
  command: "npm test -- --grep 'timeout'",
  cwd: projectRoot
});

// Evaluate in reasoning
sequentialthinking({
  thought: `Test ${testResult.exitCode === 0 ? 'passed' : 'failed'}: ${testResult.stdout}`,
  isRevision: testResult.exitCode !== 0,
  revisesThought: previousHypothesisStep,
  metadata: {
    evidenceRefs: [`cmd:test_timeout_${Date.now()}`]
  }
});
```

## Pattern-Specific Tool Combinations

### P2 (Hypothesis-Test Loop) Tool Flow

```javascript
// Step 1: Form hypothesis
sequentialthinking({
  thought: "Hypothesis: Memory leak in component. Test: Monitor heap usage",
  thoughtNumber: 1,
  metadata: { hypothesisState: "proposed" }
});

// Step 2: Gather evidence
const heapSnapshot = await execute_command({
  command: "node --inspect --expose-gc script.js",
});

// Step 3: Evaluate hypothesis
sequentialthinking({
  thought: `Evidence: Heap usage ${heapSnapshot.stdout}. Hypothesis ${evaluation}`,
  thoughtNumber: 2,
  isRevision: evaluation === "falsified",
  revisesThought: 1,
  metadata: {
    hypothesisState: evaluation,
    evidenceRefs: [`cmd:heap_snapshot_${Date.now()}`]
  }
});
```

### P4 (Research Sprint) Tool Flow

```javascript
// Step 1: Plan sources
sequentialthinking({
  thought: "Research sources: API docs, GitHub issues, Stack Overflow",
  thoughtNumber: 1,
  metadata: { sourcesPlanned: ["api_docs", "github_issues", "stackoverflow"] }
});

// Step 2: Execute research
const apiDocs = await use_mcp_tool({
  server_name: "exa",
  tool_name: "web_search_exa",
  arguments: { query: "API timeout configuration", numResults: 5 }
});

// Step 3: Synthesize
sequentialthinking({
  thought: `Synthesis: ${apiDocs.results.length} sources found. Key insights: ${insights}`,
  thoughtNumber: 3,
  metadata: {
    sourcesCompleted: ["api_docs"],
    evidenceRefs: apiDocs.results.map(r => `web:${r.url}`)
  }
});
```

### P9 (Evaluation Harness) Tool Flow

```javascript
// Step 1: Establish baseline
const baseline = await execute_command({
  command: "npm run benchmark",
});

// Step 2: Test candidate
sequentialthinking({
  thought: `Baseline: ${baseline.stdout}. Testing optimization candidate A`,
  thoughtNumber: 1,
  metadata: { baselineMetric: parseFloat(baseline.stdout) }
});

// Step 3: Measure improvement
const candidateResult = await execute_command({
  command: "npm run benchmark -- --optimization A",
});

// Step 4: Compare
sequentialthinking({
  thought: `Candidate A: ${candidateResult.stdout} (${calculateImprovement(baseline, candidateResult)}% improvement)`,
  thoughtNumber: 2,
  metadata: {
    candidate: "optimization_A",
    score: parseFloat(candidateResult.stdout),
    improvement: calculateImprovement(baseline, candidateResult)
  }
});
```

## Error Handling and Degradation

### MCP Tool Failures

**Sequential Thinking Unavailable**:
```javascript
// Fall back to structured reasoning without MCP
const reasoningStep = {
  thought: content,
  step: currentStep,
  evidence: gatheredEvidence,
  decision: isTerminal ? finalDecision : null
};

// Continue with local state management
localReasoningChain.push(reasoningStep);
```

**Memory MCP Unavailable**:
```javascript
// Continue reasoning, queue memory writes
sequentialthinking(stepData);

// Queue for later replay
memoryWriteQueue.push({
  operation: "add_observations",
  data: observationData,
  timestamp: new Date().toISOString()
});
```

### Tool Timeout Handling

**Long-Running Commands**:
```javascript
// Set timeouts for evidence gathering
const timeoutPromise = new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Tool timeout')), 30000)
);

try {
  const result = await Promise.race([
    execute_command({ command: longRunningCmd }),
    timeoutPromise
  ]);

  // Use result in reasoning
  sequentialthinking({
    thought: `Evidence gathered: ${result.stdout}`,
    metadata: { evidenceRefs: [`cmd:${cmdId}`] }
  });
} catch (error) {
  // Handle timeout in reasoning
  sequentialthinking({
    thought: "Evidence gathering timed out. Proceeding with available data",
    metadata: {
      constraints: ["evidence_timeout"],
      evidenceRefs: ["partial_data"]
    }
  });
}
```

## Performance Optimization

### Batch Operations
```javascript
// Group related evidence gathering
const evidenceBatch = await Promise.all([
  read_file({ path: "config.json" }),
  search_files({ path: ".", regex: "timeout", file_pattern: "*.ts" }),
  execute_command({ command: "npm run test:unit" })
]);

// Single reasoning step incorporating all evidence
sequentialthinking({
  thought: `Multi-source evidence: Config ${configInsights}, Search ${searchCount} matches, Tests ${testStatus}`,
  metadata: {
    evidenceRefs: [
      "file:config.json",
      "search:timeout:*.ts",
      `cmd:test_unit_${Date.now()}`
    ]
  }
});
```

### Incremental Persistence
```javascript
// Save progress without waiting for completion
async function saveReasoningProgress(chain) {
  const progressEntity = {
    name: `reasoning_progress#${chain.id}`,
    entityType: "ReasoningProgress",
    observations: [{
      type: "reasoning.progress",
      data: {
        currentStep: chain.currentStep,
        totalSteps: chain.totalSteps,
        partialDecision: chain.partialDecision,
        lastUpdated: new Date().toISOString()
      }
    }]
  };

  // Fire-and-forget persistence
  use_mcp_tool({
    server_name: "memory",
    tool_name: "create_entities",
    arguments: { entities: [progressEntity] }
  }).catch(err => console.warn('Progress save failed:', err));
}
```

## Quality Assurance

### Tool Output Validation
```javascript
function validateToolOutput(toolName, output) {
  const validators = {
    'read_file': (out) => out.content && out.content.length > 0,
    'search_files': (out) => Array.isArray(out.matches),
    'execute_command': (out) => typeof out.exitCode === 'number',
    'sequentialthinking': (out) => out.thought && typeof out.thoughtNumber === 'number'
  };

  return validators[toolName]?.(output) ?? true;
}

// Use in reasoning
if (!validateToolOutput('read_file', fileContent)) {
  sequentialthinking({
    thought: "Evidence gathering failed validation. Retrying with alternative approach",
    isRevision: true,
    revisesThought: evidenceStep,
    metadata: { evidenceQuality: "invalid" }
  });
}
```

### Chain Consistency Checks
```javascript
function validateReasoningChain(chain) {
  const issues = [];

  // Check step numbering
  const stepNumbers = chain.steps.map(s => s.thoughtNumber);
  if (!stepNumbers.every((n, i) => n === i + 1)) {
    issues.push('Step numbering inconsistent');
  }

  // Check revision references
  chain.steps.forEach(step => {
    if (step.isRevision && !step.revisesThought) {
      issues.push(`Step ${step.thoughtNumber} marked as revision but no revisesThought`);
    }
  });

  // Check branch consistency
  const branches = chain.steps.filter(s => s.branchId);
  branches.forEach(branch => {
    const parent = chain.steps.find(s => s.thoughtNumber === branch.branchFromThought);
    if (!parent) {
      issues.push(`Branch ${branch.branchId} references non-existent parent`);
    }
  });

  return issues;
}
```

This comprehensive tool usage guide ensures Sequential Thinking integrates effectively with all available tools while maintaining reasoning quality and system reliability.