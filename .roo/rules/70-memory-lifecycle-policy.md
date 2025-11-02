# 70-memory-lifecycle-policy.md
> Memory Lifecycle Policy: Retention periods, consolidation rules, and archive processes to prevent unbounded memory graph growth and performance degradation.

## Overview

The memory graph grows continuously through daily operations. Without lifecycle management, this leads to:
- Performance degradation from large graph traversals
- Storage bloat from redundant observations
- Query timeouts on complex searches
- Increased operational costs

This policy defines automated lifecycle management to maintain optimal graph size and performance while preserving valuable historical knowledge.

## Retention Periods

### Entity-Specific Retention Rules

#### Run Entities (`run#<ISO8601>#<fp8>`)
- **Active Retention**: 90 days - Recent runs for debugging and pattern analysis
- **Archive Retention**: 1 year - Move to cold storage for trend analysis
- **Delete After**: 2 years - Remove unless referenced by unresolved issues

#### Command Entities (`cmd#<canonical-cmd>#<fp8>`)
- **Active Retention**: 180 days - Command patterns and success rates
- **Archive Retention**: 2 years - Historical command usage
- **Delete After**: 5 years - Remove unless high-frequency or problematic

#### Error/Warning Entities (`err#<normalizedKey>`, `warn#<normalizedKey>`)
- **Active Retention**: Indefinite - Core error patterns never deleted
- **Consolidation**: Merge duplicate normalizedKeys, keep most recent 10 observations
- **Archive**: Move observations older than 1 year to compressed storage

#### Fix Entities (`fix#<issueName>#<sha8>`)
- **Active Retention**: Indefinite - Successful fixes preserved
- **Consolidation**: Merge identical fixes, track success rates across time
- **Archive**: Move fix outcomes older than 6 months to summary statistics

#### Dependency Entities (`dep#<name>@<version>`)
- **Active Retention**: Indefinite - Dependency knowledge base
- **Consolidation**: Merge version ranges, track compatibility patterns
- **Archive**: Move unused dependencies after 2 years of no references

#### Doc Entities (`doc#<sha256(url)>`)
- **Active Retention**: Indefinite - Documentation sources
- **Consolidation**: Merge duplicate URLs, update metadata
- **Archive**: Move access logs older than 1 year

#### Mode/Tool/File/Concept Entities
- **Active Retention**: Indefinite - Taxonomy entities
- **Consolidation**: Merge duplicates, maintain canonical names
- **Archive**: Never archived - Core graph structure

### Observation-Specific Retention

#### command.exec Observations
- **Retention**: 90 days active, 1 year archive
- **Consolidation**: Summarize into command success rates

#### error.capture/warning.capture Observations
- **Retention**: 1 year active, 2 years archive
- **Consolidation**: Roll up into error frequency statistics

#### fix.apply/fix.outcome Observations
- **Retention**: Indefinite active (on Fix entities)
- **Consolidation**: Aggregate into success rate metrics

#### doc.note Observations
- **Retention**: Indefinite active
- **Consolidation**: Update with latest access metadata

## Consolidation Rules

### Duplicate Detection and Merging

#### Entity Consolidation
```javascript
// Detect and merge duplicate entities
async function consolidateEntities(entityType) {
  const duplicates = await findDuplicates(entityType);

  for (const dupGroup of duplicates) {
    const canonical = selectCanonicalEntity(dupGroup);
    const others = dupGroup.filter(e => e !== canonical);

    // Move all relations to canonical entity
    await migrateRelations(others, canonical);

    // Merge observations
    await mergeObservations(others, canonical);

    // Delete duplicate entities
    await deleteEntities(others);
  }
}
```

#### Observation Consolidation
```javascript
// Roll up observations into summary statistics
async function consolidateObservations(entityName, type) {
  const observations = await getObservations(entityName, type);

  if (observations.length > 10) {
    const summary = createSummaryStatistic(observations);
    const toArchive = observations.slice(0, -10); // Keep 10 most recent

    await archiveObservations(toArchive);
    await addSummaryObservation(entityName, summary);
  }
}
```

### Pattern-Based Consolidation

#### Error Pattern Aggregation
- Group similar errors by normalizedKey stems
- Maintain frequency counts and resolution success rates
- Archive individual instances, keep aggregates

#### Fix Effectiveness Tracking
- Track success rates: `verified_successful / total_applications`
- Consolidate similar fixes by strategy similarity
- Maintain top-performing fixes, archive less effective ones

#### Command Pattern Analysis
- Group commands by canonical form
- Track execution success rates and performance metrics
- Consolidate similar command variations

## Archive Processes

### Archive Triggers

#### Time-Based Archiving
```javascript
// Archive entities older than retention period
async function timeBasedArchive() {
  const now = new Date();

  for (const [entityType, rules] of retentionRules) {
    const cutoffDate = new Date(now);
    cutoffDate.setDate(now.getDate() - rules.archiveAfterDays);

    const toArchive = await findEntitiesOlderThan(entityType, cutoffDate);
    await moveToArchive(toArchive, entityType);
  }
}
```

#### Size-Based Archiving
```javascript
// Archive when graph size exceeds thresholds
async function sizeBasedArchive() {
  const graphStats = await getGraphStatistics();

  if (graphStats.nodeCount > MAX_ACTIVE_NODES) {
    const toArchive = await selectLeastRecentlyUsed(MAX_ARCHIVE_BATCH);
    await moveToArchive(toArchive, 'size-based');
  }
}
```

### Archive Storage Strategy

#### Cold Storage Structure
```
archive/
├── entities/
│   ├── runs/          # Archived run entities
│   ├── commands/      # Archived command entities
│   ├── errors/        # Archived error entities
│   └── fixes/         # Archived fix entities
├── observations/
│   ├── command-exec/  # Archived command executions
│   ├── error-capture/ # Archived error captures
│   └── fix-apply/     # Archived fix applications
└── summaries/
    ├── monthly/       # Monthly summary statistics
    └── quarterly/     # Quarterly trend analysis
```

#### Compression and Indexing
- **Compression**: Use LZ4 for fast compression/decompression
- **Indexing**: Maintain inverted indexes for archived data
- **Metadata**: Store archive metadata for quick searches

### Archive Retrieval

#### On-Demand Restoration
```javascript
// Restore archived entities when needed
async function restoreFromArchive(entityNames) {
  const archived = await findInArchive(entityNames);

  // Check access patterns before restoration
  if (shouldRestore(archived)) {
    await moveFromArchive(archived, 'active');
    return archived;
  }

  return null; // Keep archived if not frequently accessed
}
```

#### Summary-Based Queries
```javascript
// Query archived data through summaries
async function queryArchivedData(query) {
  // First check active graph
  const activeResults = await searchActiveGraph(query);

  // If insufficient, check archive summaries
  if (activeResults.length < MIN_RESULTS) {
    const summaryResults = await searchArchiveSummaries(query);
    return combineResults(activeResults, summaryResults);
  }

  return activeResults;
}
```

## Automated Lifecycle Management

### Daily Maintenance Tasks

#### Cleanup Job (Daily, 02:00 UTC)
```javascript
async function dailyCleanup() {
  console.log('Starting daily memory lifecycle cleanup');

  // 1. Consolidate duplicates
  await consolidateAllDuplicates();

  // 2. Archive expired entities
  await timeBasedArchive();

  // 3. Update summary statistics
  await refreshSummaryStatistics();

  // 4. Optimize graph structure
  await optimizeGraphIndexes();

  console.log('Daily cleanup completed');
}
```

#### Weekly Maintenance Tasks (Sunday, 03:00 UTC)
```javascript
async function weeklyMaintenance() {
  console.log('Starting weekly memory maintenance');

  // 1. Deep consolidation
  await deepConsolidation();

  // 2. Archive size-based cleanup
  await sizeBasedArchive();

  // 3. Integrity checks
  await validateGraphIntegrity();

  // 4. Performance optimization
  await rebuildIndexes();

  console.log('Weekly maintenance completed');
}
```

#### Monthly Maintenance Tasks (1st of month, 04:00 UTC)
```javascript
async function monthlyMaintenance() {
  console.log('Starting monthly memory maintenance');

  // 1. Generate trend reports
  await generateTrendReports();

  // 2. Archive quarterly summaries
  await archiveQuarterlySummaries();

  // 3. Clean up orphaned relations
  await cleanupOrphanedRelations();

  // 4. Update retention policies
  await reviewRetentionPolicies();

  console.log('Monthly maintenance completed');
}
```

### Monitoring and Alerts

#### Performance Metrics
- Graph size (nodes, relations, observations)
- Query performance (P95 response times)
- Archive retrieval frequency
- Consolidation effectiveness

#### Alert Thresholds
- Graph size > 80% of capacity → Trigger size-based archiving
- Query P95 > 5 seconds → Trigger index optimization
- Archive retrieval rate > 100/day → Consider warming frequently accessed data
- Consolidation failure rate > 5% → Manual review required

### Manual Intervention Points

#### Emergency Cleanup
When automated processes fail or graph performance degrades significantly:

1. **Immediate Actions**:
   - Pause new writes to prevent further growth
   - Enable emergency archiving with aggressive thresholds
   - Notify administrators of degraded performance

2. **Recovery Process**:
   - Analyze growth patterns to identify root causes
   - Implement targeted cleanup rules
   - Gradually restore normal operations
   - Update policies to prevent recurrence

#### Policy Updates
Retention periods and consolidation rules should be reviewed quarterly:

- Analyze access patterns and query performance
- Adjust retention periods based on business needs
- Update consolidation algorithms based on data patterns
- Implement new archive strategies as needed

## Implementation Requirements

### For All Modes
- Respect lifecycle policies when creating new entities
- Use consolidation-aware entity creation (check for duplicates)
- Support archive-aware queries (fall back to summaries)

### Memory MCP Extensions
- Add lifecycle management endpoints
- Implement automatic archiving triggers
- Provide consolidation utilities
- Support archive retrieval APIs

### Monitoring Integration
- Export lifecycle metrics to monitoring systems
- Implement alerting for policy violations
- Track cleanup job success/failure rates
- Monitor archive access patterns

## Success Metrics

- **Graph Size Stability**: Maintain < 70% of capacity under normal load
- **Query Performance**: P95 < 2 seconds for common queries
- **Archive Hit Rate**: > 90% of archived data requests served from summaries
- **Cleanup Effectiveness**: > 95% duplicate consolidation rate
- **Operational Overhead**: < 5% of total system resources for lifecycle management

This policy ensures the memory graph remains performant and valuable while preventing unbounded growth through systematic lifecycle management.