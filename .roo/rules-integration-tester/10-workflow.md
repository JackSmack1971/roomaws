# .roo/rules-integration-tester/10-workflow.md
> Comprehensive workflow for integration test development, debugging, and maintenance.

## Phase 0: Memory Consultation (MANDATORY - DO NOT SKIP)

**Objective**: Leverage historical knowledge before attempting solutions.

**Steps**:
1. **Extract task signature**:
   - For errors: Normalize error message (strip hashes/paths/versions)
   - For tasks: Extract key entities (component names, file paths, error types)

2. **Query memory**:
   ```javascript
   use_mcp_tool({
     server_name: "memory",
     tool_name: "search_nodes",
     arguments: { query: "type:Error|Fix <signature>" }
   })
   ```

3. **Analyze results**:
   - **If hits found**: Review top 3 fixes/docs
   - **If no hits**: Flag as "novel case" for future learning
   - **If MCP unavailable**: Log degraded mode warning

4. **Document consultation**:
```
✓ Memory consulted: [N results | No matches | MCP unavailable]
✓ Top recommendation: [fix#<id> with strategy X | None applicable]
✓ Evidence: [doc#<id> from <source> | Local knowledge only]
```

5. **Validate consultation execution**:
   - **MANDATORY GATE**: Verify memory consultation was actually executed (not skipped)
   - **MCP Failure Handling**: If MCP unavailable, warn user and proceed in degraded mode with local knowledge only
   - **Skipped Query Handling**: If consultation was bypassed, STOP immediately and require explicit user confirmation to proceed
   - **Degraded Operation Warning**: Display clear user notification: "⚠️ Operating in degraded mode - memory consultation unavailable. Proceeding with local knowledge only."

**CRITICAL EXECUTION GATE**: Do not proceed to Intake & Requirements Analysis without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

## Intake & Requirements Analysis

1) **Identify test objective**: Determine if this is new test creation, existing test repair, utility development, or failure debugging
2) **Gather context**: Collect user stories, acceptance criteria, system requirements, and integration points
3) **Define scope**: Establish test boundaries, success criteria, and quality gates
4) **Assess complexity**: Evaluate technical challenges, dependencies, and testing approach needed

## Test Planning & Design Phase

1) **Requirements decomposition**: Break down user requirements into testable scenarios and acceptance criteria
2) **Integration point analysis**: Identify all systems, APIs, and components that need to be tested together
3) **Test scenario identification**: Define happy path, edge cases, error conditions, and failure modes
4) **Data and fixture planning**: Design test data, mock objects, and environment configurations
5) **Success criteria definition**: Establish measurable outcomes and validation approaches

## Environment & Infrastructure Setup

1) **Test environment assessment**: Evaluate available testing infrastructure and capabilities
2) **Dependency identification**: Catalog all systems, services, and tools required for testing
3) **Configuration management**: Set up environment variables, connection strings, and test configurations
4) **Resource provisioning**: Ensure test databases, message queues, and external services are available
5) **Security considerations**: Configure authentication, authorization, and secure data handling

## Test Architecture Design

1) **Test structure planning**: Design test suites, test classes, and test method organization
2) **Fixture and data management**: Plan test data creation, cleanup, and isolation strategies
3) **Mock and stub design**: Identify external dependencies to mock and design mock behaviors
4) **Assertion strategy**: Define validation approaches and expected outcomes
5) **Reporting framework**: Plan test result collection, formatting, and communication

## Implementation Phase

1) **Incremental development**: Build tests step-by-step, starting with basic functionality
2) **Test framework utilization**: Leverage appropriate testing frameworks and libraries
3) **Helper and utility creation**: Develop reusable test utilities and helper functions
4) **Error handling implementation**: Add proper exception handling and error reporting
5) **Logging and debugging**: Implement comprehensive logging for test execution tracking

## Test Execution & Validation

1) **Isolated test execution**: Run individual tests to verify basic functionality
2) **Integration verification**: Execute end-to-end scenarios across integrated components
3) **Performance validation**: Ensure tests complete within acceptable time limits
4) **Resource cleanup**: Verify proper cleanup of test data and system state
5) **Cross-browser/device testing**: Validate behavior across different environments when applicable

## Debugging & Troubleshooting

1) **Failure analysis**: Examine test failures to identify root causes and failure patterns
2) **Environment issues**: Check for configuration problems, resource constraints, or timing issues
3) **Data consistency**: Verify test data integrity and isolation between test runs
4) **Race conditions**: Identify and resolve timing-related test failures
5) **External dependencies**: Debug issues with third-party services or APIs

## Quality Assurance & Refinement

1) **Code review**: Conduct peer review of test implementation and design
2) **Test coverage analysis**: Evaluate how well tests cover requirements and edge cases
3) **Maintainability assessment**: Ensure tests are readable, documented, and maintainable
4) **Performance optimization**: Optimize test execution time and resource usage
5) **Documentation completion**: Document test purpose, setup requirements, and execution procedures

## Maintenance & Evolution

1) **Regression detection**: Monitor for test failures indicating code changes or system issues
2) **Test updates**: Modify tests to reflect changes in system behavior or requirements
3) **Performance monitoring**: Track test execution times and identify performance degradation
4) **Flaky test management**: Address intermittent test failures and improve reliability
5) **Test suite health**: Maintain overall test suite quality and effectiveness

## Memory Integration Points

1) **Test execution logging**: Record test runs with performance metrics and failure details
2) **Failure pattern tracking**: Store recurring test failures and their resolution approaches
3) **Test improvement logging**: Document successful test enhancements and optimization strategies
4) **Knowledge preservation**: Maintain searchable history of test development challenges and solutions
5) **Pattern recognition**: Identify common testing problems and proven resolution approaches

---

## Final Phase: Knowledge Capture (MANDATORY - DO NOT SKIP)

**Objective**: Persist learnings for future runs.

**Steps**:
1. **Create observation envelopes** (see `40-memory-io.md` for schemas):
   - `command.exec` for key operations
   - `error.capture` for failures
   - `fix.apply` for resolutions
   - `doc.note` for research sources

2. **Write to memory**:
   ```javascript
   use_mcp_tool({ server_name: "memory", tool_name: "create_entities", ... })
   use_mcp_tool({ server_name: "memory", tool_name: "add_observations", ... })
   use_mcp_tool({ server_name: "memory", tool_name: "create_relations", ... })
   ```

3. **Validate persistence**:
   ```
   ✓ Entities created: [run#..., cmd#..., fix#...]
   ✓ Relations linked: [EXECUTES, RESOLVES, DERIVED_FROM, PERFORMED_BY, TOUCHES]
   ✓ Memory persistence confirmed
   ```

**If memory write fails**: Log structured event with `{ operation, data, timestamp }` for later replay when MCP recovers.
