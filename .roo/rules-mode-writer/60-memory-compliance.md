# 60-memory-compliance.md
> Runtime validation and degraded operation handling for memory protocol compliance.

## Overview

This document provides runtime validation mechanisms and degraded operation patterns to ensure memory protocol compliance across all modes. It addresses the critical gaps identified in the memory integration testing report.

## Runtime Validation Framework

### Memory Protocol Checkpoint System

All modes must implement runtime checkpoints to validate memory protocol compliance:

```javascript
class MemoryProtocolValidator {
  constructor(modeSlug) {
    this.modeSlug = modeSlug;
    this.checkpoints = [];
    this.degradedMode = false;
  }

  // PRE-FLIGHT: Validate memory consultation
  async validatePreFlight() {
    const checkpoint = {
      phase: 'PRE-FLIGHT',
      timestamp: new Date().toISOString(),
      required: ['memory_search_executed', 'consultation_logged'],
      status: 'pending'
    };

    try {
      // Check if memory search was actually executed (not just documented)
      const searchExecuted = await this.verifyMemorySearch();
      const consultationLogged = await this.verifyConsultationLog();

      checkpoint.status = (searchExecuted && consultationLogged) ? 'passed' : 'failed';
      checkpoint.details = { searchExecuted, consultationLogged };
    } catch (error) {
      checkpoint.status = 'error';
      checkpoint.error = error.message;
    }

    this.checkpoints.push(checkpoint);
    return checkpoint;
  }

  // POST-FLIGHT: Validate memory writes
  async validatePostFlight() {
    const checkpoint = {
      phase: 'POST-FLIGHT',
      timestamp: new Date().toISOString(),
      required: ['entities_created', 'relations_established', 'confirmation_logged'],
      status: 'pending'
    };

    try {
      const entitiesCreated = await this.verifyEntityCreation();
      const relationsEstablished = await this.verifyRelationCreation();
      const confirmationLogged = await this.verifyConfirmationLog();

      checkpoint.status = (entitiesCreated && relationsEstablished && confirmationLogged) ? 'passed' : 'failed';
      checkpoint.details = { entitiesCreated, relationsEstablished, confirmationLogged };
    } catch (error) {
      checkpoint.status = 'error';
      checkpoint.error = error.message;
    }

    this.checkpoints.push(checkpoint);
    return checkpoint;
  }

  // Generate compliance report
  generateReport() {
    const passed = this.checkpoints.filter(cp => cp.status === 'passed').length;
    const total = this.checkpoints.length;
    const compliance = total > 0 ? (passed / total) * 100 : 0;

    return {
      mode: this.modeSlug,
      timestamp: new Date().toISOString(),
      compliance: `${compliance.toFixed(1)}%`,
      checkpoints: this.checkpoints,
      degradedMode: this.degradedMode,
      recommendations: this.generateRecommendations()
    };
  }
}
```

### Degraded Operation Handler

When Memory MCP is unavailable, modes must implement graceful degradation:

```javascript
class DegradedOperationHandler {
  constructor(modeSlug) {
    this.modeSlug = modeSlug;
    this.writeQueue = [];
    this.circuitBreaker = new CircuitBreaker();
    this.fallbackStrategies = this.initializeFallbackStrategies();
  }

  // Detect MCP unavailability
  async detectMcpFailure(operation, error) {
    const isMcpError = this.isMcpError(error);
    if (isMcpError) {
      this.circuitBreaker.recordFailure();
      await this.enterDegradedMode();
      return true;
    }
    return false;
  }

  // Enter degraded operation mode
  async enterDegradedMode() {
    this.degradedMode = true;

    // Log degraded mode entry
    console.warn(`⚠️ DEGRADED MODE: Memory MCP unavailable for ${this.modeSlug}`);
    console.warn(`⚠️ Operating with local context only`);
    console.warn(`⚠️ Memory writes will be queued for later replay`);

    // Initialize write queue
    this.writeQueue = [];

    // Set up recovery monitoring
    this.startRecoveryMonitor();
  }

  // Queue memory writes for later replay
  async queueMemoryWrite(operation, data) {
    const queuedItem = {
      operation,
      data,
      timestamp: new Date().toISOString(),
      retryCount: 0,
      mode: this.modeSlug
    };

    this.writeQueue.push(queuedItem);

    console.log(`📝 Queued memory write: ${operation} (${this.writeQueue.length} total)`);
  }

  // Attempt to replay queued writes
  async replayQueuedWrites() {
    if (this.writeQueue.length === 0) return;

    console.log(`🔄 Attempting to replay ${this.writeQueue.length} queued memory writes`);

    const remaining = [];
    for (const item of this.writeQueue) {
      try {
        await this.attemptMemoryWrite(item);
        console.log(`✓ Replayed: ${item.operation}`);
      } catch (error) {
        item.retryCount++;
        if (item.retryCount < 3) {
          remaining.push(item);
        } else {
          console.error(`✗ Permanently failed to replay: ${item.operation}`, error);
        }
      }
    }

    this.writeQueue = remaining;
    if (remaining.length > 0) {
      console.warn(`⚠️ ${remaining.length} memory writes still queued`);
    }
  }

  // Circuit breaker for consistent failures
  class CircuitBreaker {
    constructor() {
      this.failureCount = 0;
      this.lastFailureTime = null;
      this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    }

    recordFailure() {
      this.failureCount++;
      this.lastFailureTime = Date.now();

      if (this.failureCount >= 3) {
        this.state = 'OPEN';
        console.error('🚫 Circuit breaker OPEN: Memory MCP consistently failing');
      }
    }

    recordSuccess() {
      if (this.state === 'HALF_OPEN') {
        this.state = 'CLOSED';
        this.failureCount = 0;
        console.log('✅ Circuit breaker CLOSED: Memory MCP recovered');
      }
    }

    canAttempt() {
      if (this.state === 'CLOSED') return true;
      if (this.state === 'OPEN') {
        // Allow attempt after 5 minutes
        if (Date.now() - this.lastFailureTime > 300000) {
          this.state = 'HALF_OPEN';
          return true;
        }
        return false;
      }
      return this.state === 'HALF_OPEN';
    }
  }

  // Fallback strategies for reads
  initializeFallbackStrategies() {
    return {
      search_nodes: this.fallbackSearch,
      open_nodes: this.fallbackOpen,
      read_graph: this.fallbackReadGraph
    };
  }

  async fallbackSearch(query) {
    console.warn(`🔄 Using fallback search for query: ${query}`);
    // Return empty results with warning
    return {
      results: [],
      warning: 'Memory MCP unavailable - using fallback (empty results)',
      degraded: true
    };
  }

  async fallbackOpen(names) {
    console.warn(`🔄 Using fallback open for entities: ${names.join(', ')}`);
    return {
      entities: [],
      warning: 'Memory MCP unavailable - using fallback (empty entities)',
      degraded: true
    };
  }

  async fallbackReadGraph() {
    console.warn(`🔄 Using fallback read graph`);
    return {
      entities: [],
      relations: [],
      warning: 'Memory MCP unavailable - using fallback (empty graph)',
      degraded: true
    };
  }
}
```

## Implementation Requirements

### For All Modes

1. **Import Validation Framework**
   ```javascript
   // At the top of every mode's workflow
   const validator = new MemoryProtocolValidator(modeSlug);
   const degradedHandler = new DegradedOperationHandler(modeSlug);
   ```

2. **PRE-FLIGHT Validation**
   ```javascript
   // Before any memory operations
   await validator.validatePreFlight();
   ```

3. **Memory Operation Wrapping**
   ```javascript
   async function safeMemoryOperation(operation, data) {
     try {
       if (!degradedHandler.circuitBreaker.canAttempt()) {
         throw new Error('Circuit breaker open');
       }

       const result = await use_mcp_tool({
         server_name: "memory",
         tool_name: operation,
         arguments: data
       });

       degradedHandler.circuitBreaker.recordSuccess();
       return result;
     } catch (error) {
       if (await degradedHandler.detectMcpFailure(operation, error)) {
         // Queue for later replay
         await degradedHandler.queueMemoryWrite(operation, data);
         // Return fallback result
         return await degradedHandler.fallbackStrategies[operation]?.(data);
       }
       throw error;
     }
   }
   ```

4. **POST-FLIGHT Validation**
   ```javascript
   // After all operations complete
   await validator.validatePostFlight();

   // Generate and log compliance report
   const report = validator.generateReport();
   console.log('📊 Memory Protocol Compliance Report:', report);
   ```

5. **Completion Summary Enhancement**
   ```javascript
   // Include compliance status in all completion summaries
   const completionSummary = {
     result: "Task completed successfully",
     memoryCompliance: report.compliance,
     degradedMode: report.degradedMode,
     queuedWrites: degradedHandler.writeQueue.length,
     warnings: report.recommendations
   };
   ```

### Mode-Specific Adaptations

#### Issue-Resolver Mode
```javascript
// Enhanced error pattern matching with fallbacks
async function searchSimilarIssues(errorPattern) {
  try {
    return await safeMemoryOperation('search_nodes', {
      query: `type:Error ${errorPattern}`
    });
  } catch (error) {
    // Fallback: Use local pattern matching
    return await localErrorPatternSearch(errorPattern);
  }
}
```

#### Test Mode
```javascript
// Enhanced test pattern recall with fallbacks
async function recallTestPatterns(testType) {
  try {
    return await safeMemoryOperation('search_nodes', {
      query: `type:Fix test:${testType}`
    });
  } catch (error) {
    // Fallback: Use embedded test pattern library
    return embeddedTestPatterns[testType] || [];
  }
}
```

#### Design-Engineer Mode
```javascript
// Enhanced UI pattern recall with fallbacks
async function recallUiPatterns(componentType) {
  try {
    return await safeMemoryOperation('search_nodes', {
      query: `type:Fix component:${componentType}`
    });
  } catch (error) {
    // Fallback: Use design system documentation
    return await searchDesignSystemDocs(componentType);
  }
}
```

## Compliance Monitoring Dashboard

### Real-time Compliance Tracking

```javascript
class ComplianceDashboard {
  constructor() {
    this.modeReports = new Map();
    this.alerts = [];
  }

  // Collect compliance reports from all modes
  collectReport(modeSlug, report) {
    this.modeReports.set(modeSlug, report);

    // Check for critical issues
    if (report.compliance < 80) {
      this.alerts.push({
        level: 'CRITICAL',
        mode: modeSlug,
        message: `Memory protocol compliance below 80%: ${report.compliance}`,
        timestamp: new Date().toISOString()
      });
    }

    if (report.degradedMode) {
      this.alerts.push({
        level: 'WARNING',
        mode: modeSlug,
        message: `Operating in degraded mode - memory writes queued`,
        timestamp: new Date().toISOString()
      });
    }
  }

  // Generate system-wide compliance report
  generateSystemReport() {
    const modes = Array.from(this.modeReports.keys());
    const avgCompliance = modes.reduce((sum, mode) => {
      const report = this.modeReports.get(mode);
      return sum + parseFloat(report.compliance);
    }, 0) / modes.length;

    const degradedModes = modes.filter(mode =>
      this.modeReports.get(mode).degradedMode
    );

    return {
      timestamp: new Date().toISOString(),
      overallCompliance: `${avgCompliance.toFixed(1)}%`,
      totalModes: modes.length,
      degradedModes: degradedModes.length,
      activeAlerts: this.alerts.length,
      modeDetails: Object.fromEntries(this.modeReports),
      alerts: this.alerts.slice(-10) // Last 10 alerts
    };
  }
}
```

## Testing and Validation

### Compliance Test Suite

```javascript
// Automated tests for memory protocol compliance
describe('Memory Protocol Compliance', () => {
  test('PRE-FLIGHT validation executes actual memory searches', async () => {
    const validator = new MemoryProtocolValidator('test-mode');
    const checkpoint = await validator.validatePreFlight();

    expect(checkpoint.status).toBe('passed');
    expect(checkpoint.details.searchExecuted).toBe(true);
  });

  test('POST-FLIGHT validation verifies entity creation', async () => {
    const validator = new MemoryProtocolValidator('test-mode');
    const checkpoint = await validator.validatePostFlight();

    expect(checkpoint.status).toBe('passed');
    expect(checkpoint.details.entitiesCreated).toBe(true);
  });

  test('Degraded operation handler queues writes when MCP fails', async () => {
    const handler = new DegradedOperationHandler('test-mode');

    // Simulate MCP failure
    const mockError = new Error('MCP connection failed');
    const isFailure = await handler.detectMcpFailure('search_nodes', mockError);

    expect(isFailure).toBe(true);
    expect(handler.degradedMode).toBe(true);

    // Queue a write
    await handler.queueMemoryWrite('create_entities', { entities: [] });
    expect(handler.writeQueue.length).toBe(1);
  });

  test('Circuit breaker prevents cascading failures', async () => {
    const handler = new DegradedOperationHandler('test-mode');

    // Simulate multiple failures
    for (let i = 0; i < 3; i++) {
      await handler.detectMcpFailure('search_nodes', new Error('MCP error'));
    }

    expect(handler.circuitBreaker.state).toBe('OPEN');
    expect(handler.circuitBreaker.canAttempt()).toBe(false);
  });
});
```

## Migration Path

### Phase 1: Framework Implementation (Week 1)
- [ ] Create MemoryProtocolValidator class
- [ ] Create DegradedOperationHandler class
- [ ] Add ComplianceDashboard class
- [ ] Create 60-memory-compliance.md documentation

### Phase 2: Mode Integration (Week 2-3)
- [ ] Update issue-resolver mode with validation framework
- [ ] Update test mode with validation framework
- [ ] Update design-engineer mode with validation framework
- [ ] Update remaining modes with validation framework

### Phase 3: Testing and Monitoring (Week 4)
- [ ] Implement compliance test suite
- [ ] Add real-time monitoring dashboard
- [ ] Test degraded operation scenarios
- [ ] Validate circuit breaker functionality

### Phase 4: Production Deployment (Week 5)
- [ ] Deploy updated modes to production
- [ ] Monitor compliance metrics
- [ ] Establish alert thresholds
- [ ] Create incident response procedures

## Success Metrics

- **Memory Protocol Compliance**: >95% across all modes
- **Degraded Operation Recovery**: <5 minute mean time to recovery
- **False Positive Rate**: <1% for compliance alerts
- **Memory Write Queue**: <100 items during normal operation
- **Circuit Breaker Effectiveness**: >99% reduction in cascading failures

This framework addresses all critical gaps identified in the memory integration testing report and provides a robust, self-healing hivemind system.