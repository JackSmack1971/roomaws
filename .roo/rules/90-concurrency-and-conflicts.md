# 90-concurrency-and-conflicts.md
> Concurrency and Conflict Resolution: Write ordering, conflict detection, and resolution strategies for cross-mode race conditions in the memory graph to prevent data corruption and ensure consistency.

## Overview

The memory graph is a shared resource accessed by multiple modes simultaneously. Without proper concurrency control, race conditions can lead to:

- Duplicate entity creation with conflicting data
- Inconsistent relation states
- Lost observations due to concurrent writes
- Broken graph traversals from partial updates
- Incorrect fix recommendations based on stale data

This document defines strategies for write ordering, conflict detection, and resolution to maintain graph consistency across concurrent mode operations.

## Write Ordering Strategies

### Optimistic Concurrency Control

#### Version-Based Writes
All entities include version metadata for optimistic locking:

```typescript
interface VersionedEntity {
  name: string;
  entityType: string;
  version: number; // Monotonically increasing
  lastModified: string; // ISO8601 timestamp
  observations: string[];
}
```

#### Write Ordering Protocol
1. **Read Current Version**: Always fetch current entity version before modification
2. **Apply Changes**: Make changes to local copy
3. **Conditional Write**: Write back only if version matches current
4. **Retry on Conflict**: If version mismatch, re-read and retry

```typescript
async function optimisticUpdate(entityName: string, updateFn: (entity: any) => any) {
  const maxRetries = 3;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      // Read current entity with version
      const current = await readEntityWithVersion(entityName);

      // Apply update function
      const updated = updateFn(current);

      // Attempt conditional write
      const success = await conditionalWrite(entityName, updated, current.version);

      if (success) {
        return updated;
      }

      // Version conflict - retry after brief delay
      await delay(Math.pow(2, attempt) * 100); // Exponential backoff
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
    }
  }
}
```

### Pessimistic Locking

#### Entity-Level Locks
For high-contention entities, use explicit locking:

```typescript
async function withEntityLock(entityName: string, operation: () => Promise<any>) {
  const lockId = await acquireLock(entityName, 'exclusive', 30000); // 30s timeout

  try {
    const result = await operation();
    return result;
  } finally {
    await releaseLock(lockId);
  }
}
```

#### Lock Hierarchy
Define lock ordering to prevent deadlocks:
1. Entity locks (alphabetical by name)
2. Relation locks (source-target ordering)
3. Observation locks (entity-based)

### Batch Write Ordering

#### Transactional Batches
Group related writes into atomic transactions:

```typescript
interface MemoryTransaction {
  operations: Array<{
    type: 'create_entity' | 'add_observation' | 'create_relation';
    data: any;
  }>;
  isolation: 'read_committed' | 'serializable';
}

async function executeTransaction(transaction: MemoryTransaction) {
  // Validate transaction consistency
  validateTransaction(transaction);

  // Execute all operations atomically
  const results = await atomicBatchWrite(transaction.operations);

  // Update entity versions
  await updateVersions(results);

  return results;
}
```

## Conflict Detection Mechanisms

### Version Conflict Detection

#### Entity Version Checking
```typescript
async function detectVersionConflict(entityName: string, expectedVersion: number) {
  const current = await readEntityVersion(entityName);

  if (current !== expectedVersion) {
    return {
      conflict: true,
      currentVersion: current,
      expectedVersion,
      timestamp: new Date().toISOString()
    };
  }

  return { conflict: false };
}
```

#### Relation Consistency Checks
Verify relation integrity after concurrent operations:

```typescript
async function validateRelationConsistency(relation: Relation) {
  const sourceExists = await entityExists(relation.from);
  const targetExists = await entityExists(relation.to);

  if (!sourceExists || !targetExists) {
    return {
      valid: false,
      error: 'Relation references non-existent entity',
      missingEntities: [
        !sourceExists ? relation.from : null,
        !targetExists ? relation.to : null
      ].filter(Boolean)
    };
  }

  return { valid: true };
}
```

### Semantic Conflict Detection

#### Observation Conflicts
Detect conflicting observations on the same entity:

```typescript
function detectObservationConflicts(existing: string[], newObs: string[]) {
  const conflicts = [];

  for (const newObservation of newObs) {
    const newData = JSON.parse(newObservation);

    for (const existingObservation of existing) {
      const existingData = JSON.parse(existingObservation);

      if (isConflictingObservation(existingData, newData)) {
        conflicts.push({
          type: 'observation_conflict',
          existing: existingData,
          new: newData,
          reason: determineConflictReason(existingData, newData)
        });
      }
    }
  }

  return conflicts;
}

function isConflictingObservation(existing: any, newObs: any) {
  // Same type and conflicting data
  if (existing.type === newObs.type) {
    switch (existing.type) {
      case 'fix.apply':
        return existing.result !== newObs.result; // Different outcomes
      case 'error.capture':
        return existing.normalizedKey === newObs.normalizedKey &&
               existing.message !== newObs.message; // Same error, different message
      default:
        return false;
    }
  }

  return false;
}
```

#### Entity Type Conflicts
Detect when different modes create entities with conflicting types:

```typescript
function detectEntityTypeConflict(entityName: string, attemptedType: string) {
  const existingType = getEntityType(entityName);

  if (existingType && existingType !== attemptedType) {
    return {
      conflict: true,
      existingType,
      attemptedType,
      resolution: 'use_existing' // Always prefer existing type
    };
  }

  return { conflict: false };
}
```

## Resolution Strategies

### Automatic Resolution

#### Last-Writer-Wins
For non-conflicting updates, accept the most recent write:

```typescript
async function resolveLastWriterWins(conflicts: Conflict[]) {
  const resolutions = [];

  for (const conflict of conflicts) {
    const lastWrite = await getLastWriteTimestamp(conflict.entityName);

    resolutions.push({
      entity: conflict.entityName,
      strategy: 'last_writer_wins',
      winner: lastWrite.mode,
      timestamp: lastWrite.timestamp
    });
  }

  return resolutions;
}
```

#### Merge Strategies
For compatible changes, merge them:

```typescript
async function mergeCompatibleChanges(entityName: string, changes: Change[]) {
  const merged = { ...changes[0] };

  for (const change of changes.slice(1)) {
    merged.observations = [...new Set([...merged.observations, ...change.observations])];
    merged.relations = mergeRelations(merged.relations, change.relations);
  }

  return merged;
}

function mergeRelations(existing: Relation[], newRelations: Relation[]) {
  const merged = [...existing];

  for (const newRel of newRelations) {
    const existingRel = merged.find(r =>
      r.from === newRel.from &&
      r.to === newRel.to &&
      r.relationType === newRel.relationType
    );

    if (!existingRel) {
      merged.push(newRel);
    }
  }

  return merged;
}
```

### Manual Resolution

#### Conflict Escalation
For complex conflicts, escalate to human review:

```typescript
async function escalateConflict(conflict: Conflict) {
  // Log detailed conflict information
  await logConflictDetails(conflict);

  // Notify relevant modes
  await notifyModes(conflict.involvedModes, {
    type: 'conflict_escalation',
    conflict,
    resolution_required: true
  });

  // Create conflict resolution task
  await createConflictResolutionTask(conflict);
}
```

#### Conflict Resolution Workflow
1. **Detection**: Conflict detected during write attempt
2. **Analysis**: Determine conflict type and severity
3. **Escalation**: If automatic resolution fails, notify human operator
4. **Resolution**: Apply human-guided resolution
5. **Recording**: Log resolution for future learning

### Cross-Mode Coordination

#### Mode Communication Protocol
Modes coordinate via shared conflict resolution channels:

```typescript
interface ModeCommunication {
  modeId: string;
  messageType: 'conflict_detected' | 'resolution_proposed' | 'resolution_accepted';
  conflictId: string;
  data: any;
}

async function broadcastConflict(modeId: string, conflict: Conflict) {
  const message: ModeCommunication = {
    modeId,
    messageType: 'conflict_detected',
    conflictId: conflict.id,
    data: conflict
  };

  await broadcastToModes(message);
}
```

#### Conflict Ownership
Assign conflict ownership based on mode hierarchy:

```typescript
const MODE_HIERARCHY = {
  'orchestrator': 1,      // Highest priority
  'issue-resolver': 2,
  'merge-resolver': 3,
  'design-engineer': 4,
  'test': 5,
  'integration-tester': 6,
  'docs-manager': 7,
  'translate': 8,
  'security-auditor': 9,
  'performance-profiler': 10,
  'migration-specialist': 11,
  'mode-writer': 12     // Lowest priority
};

function determineConflictOwner(conflict: Conflict) {
  const involvedModes = conflict.involvedModes;
  const sorted = involvedModes.sort((a, b) =>
    MODE_HIERARCHY[a] - MODE_HIERARCHY[b]
  );

  return sorted[0]; // Highest priority mode owns resolution
}
```

## Implementation Requirements

### For All Modes

1. **Version Awareness**: Always read entity versions before writing
2. **Optimistic Locking**: Implement retry logic for version conflicts
3. **Conflict Detection**: Check for conflicts before and after writes
4. **Resolution Integration**: Support automatic and manual resolution strategies
5. **Communication**: Participate in cross-mode conflict resolution

### Memory MCP Extensions

1. **Version Management**: Maintain entity versions and timestamps
2. **Conditional Writes**: Support version-based conditional operations
3. **Conflict Detection**: Built-in conflict detection and notification
4. **Lock Management**: Provide entity-level locking primitives
5. **Transaction Support**: Atomic batch operations with rollback

### Monitoring and Alerting

#### Conflict Metrics
Track conflict rates and resolution effectiveness:

```typescript
interface ConflictMetrics {
  totalConflicts: number;
  resolvedAutomatically: number;
  escalatedManually: number;
  averageResolutionTime: number;
  conflictsByType: Record<string, number>;
  conflictsByMode: Record<string, number>;
}
```

#### Alert Thresholds
- Automatic resolution rate < 90% → Investigate
- Average resolution time > 30 seconds → Performance issue
- Conflicts per minute > 10 → High contention warning

## Testing and Validation

### Concurrency Test Suite

```typescript
describe('Memory Graph Concurrency', () => {
  test('optimistic locking prevents lost updates', async () => {
    // Simulate concurrent updates to same entity
    const entityName = 'test-entity';

    const update1 = optimisticUpdate(entityName, (entity) => ({
      ...entity,
      observations: [...entity.observations, 'update1']
    }));

    const update2 = optimisticUpdate(entityName, (entity) => ({
      ...entity,
      observations: [...entity.observations, 'update2']
    }));

    const results = await Promise.all([update1, update2]);

    // Both updates should succeed without data loss
    expect(results).toHaveLength(2);
    const finalEntity = await readEntity(entityName);
    expect(finalEntity.observations).toContain('update1');
    expect(finalEntity.observations).toContain('update2');
  });

  test('conflict detection identifies version mismatches', async () => {
    const entityName = 'version-test';

    // Read entity
    const entity = await readEntityWithVersion(entityName);
    const originalVersion = entity.version;

    // Simulate concurrent modification
    await directUpdate(entityName, { version: originalVersion + 1 });

    // Attempt update with stale version
    const conflict = await detectVersionConflict(entityName, originalVersion);

    expect(conflict.conflict).toBe(true);
    expect(conflict.currentVersion).toBe(originalVersion + 1);
  });

  test('cross-mode conflict resolution works', async () => {
    // Simulate issue-resolver and test mode conflicting on fix entity
    const fixId = 'fix#test-conflict';

    const resolverUpdate = createFixEntity(fixId, 'resolver-outcome');
    const testUpdate = createFixEntity(fixId, 'test-outcome');

    // Both attempt to create same entity
    await Promise.allSettled([resolverUpdate, testUpdate]);

    // Verify proper resolution (higher priority mode wins)
    const finalEntity = await readEntity(fixId);
    expect(finalEntity.createdBy).toBe('issue-resolver'); // Higher priority
  });
});
```

### Load Testing

#### High-Concurrency Scenarios
- 10+ modes writing simultaneously
- Entity creation bursts
- Relation graph updates
- Observation spam scenarios

#### Performance Benchmarks
- Conflict detection latency < 100ms
- Resolution time < 5 seconds for automatic cases
- Memory usage under high contention

## Success Metrics

- **Conflict Rate**: < 5% of total write operations result in conflicts
- **Automatic Resolution Rate**: > 95% of conflicts resolved automatically
- **Average Resolution Time**: < 10 seconds for automatic resolution
- **Data Loss Incidents**: 0 instances of lost updates or corrupted entities
- **Cross-Mode Coordination**: All modes successfully coordinate during conflicts

This framework ensures the memory graph remains consistent and reliable even under high concurrency and cross-mode race conditions, maintaining the integrity of the shared knowledge base.