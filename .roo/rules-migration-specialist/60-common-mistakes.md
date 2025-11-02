# 60-common-mistakes.md
> Common migration pitfalls and how to avoid them.

## Planning Phase Mistakes

### Mistake: Underestimating Migration Scope
**Problem**: Treating migrations as simple version bumps without analyzing dependencies and impact.

**Symptoms**:
- Breaking changes discovered mid-migration
- Unexpected downstream effects
- Rollback becomes impossible

**Prevention**:
- Create comprehensive dependency graph
- Impact analysis for all affected systems
- Pilot migration on subset of data/features

**Example**:
```javascript
// Bad: Assuming simple upgrade
npm update react

// Good: Comprehensive analysis first
// 1. Check breaking changes in React changelog
// 2. Audit all components for deprecated APIs
// 3. Test with canary release
// 4. Plan rollback strategy
```

### Mistake: Ignoring Data Volume
**Problem**: Not accounting for large datasets causing performance issues during migration.

**Symptoms**:
- Migration scripts run for days
- Database locks cause downtime
- Memory exhaustion on migration workers

**Prevention**:
- Analyze data size and growth patterns
- Implement batching and resumable migrations
- Test with production-scale data subsets

## Execution Phase Mistakes

### Mistake: Big Bang Migration
**Problem**: Attempting to migrate everything at once without incremental rollout.

**Symptoms**:
- All-or-nothing failure scenarios
- Prolonged downtime windows
- High-risk rollback requirements

**Prevention**:
- Use strangler fig pattern for gradual migration
- Feature flags for phased rollouts
- Blue-green deployment strategies

### Mistake: Inadequate Testing
**Problem**: Insufficient testing of migration scripts and transformed data.

**Symptoms**:
- Data corruption after migration
- Application crashes with new schema
- Silent data loss

**Prevention**:
- Automated migration testing
- Data integrity validation scripts
- Shadow testing against production data

**Example Validation Script**:
```javascript
async function validateMigration() {
  // Count validation
  const oldCount = await oldDb.users.count();
  const newCount = await newDb.users.count();
  assert.equal(oldCount, newCount, 'User count mismatch');

  // Data integrity checks
  const samples = await oldDb.users.find().limit(100).toArray();
  for (const oldUser of samples) {
    const newUser = await newDb.users.findById(oldUser.id);
    assert(newUser, `User ${oldUser.id} missing`);

    // Field transformations
    assert.equal(
      transformEmail(oldUser.email),
      newUser.email,
      'Email transformation failed'
    );
  }
}
```

## Data Migration Mistakes

### Mistake: Lossy Data Transformations
**Problem**: Irreversible data transformations without backup.

**Symptoms**:
- Cannot rollback due to data loss
- Historical data becomes inaccessible
- Compliance violations

**Prevention**:
- Preserve original data during transformation
- Implement reversible migrations
- Archive original data before transformation

**Example Safe Transformation**:
```sql
-- Bad: Destructive update
UPDATE users SET email = LOWER(email);

-- Good: Preserve original
ALTER TABLE users ADD COLUMN email_new VARCHAR(255);
UPDATE users SET email_new = LOWER(email);
-- Later: DROP COLUMN email; ALTER TABLE users RENAME COLUMN email_new TO email;
```

### Mistake: Ignoring Referential Integrity
**Problem**: Breaking foreign key relationships during schema changes.

**Symptoms**:
- Orphaned records after migration
- Inconsistent data states
- Application errors on related data access

**Prevention**:
- Defer constraint checks during migration
- Migrate related data together
- Validate relationships post-migration

## Operational Mistakes

### Mistake: Poor Monitoring and Alerting
**Problem**: No visibility into migration progress and issues.

**Symptoms**:
- Unaware of migration failures
- Delayed response to issues
- Inability to track progress

**Prevention**:
- Comprehensive monitoring dashboards
- Real-time alerting on failure conditions
- Progress tracking and ETA calculations

### Mistake: Inadequate Rollback Planning
**Problem**: Rollback procedures not tested or too slow to execute.

**Symptoms**:
- Cannot rollback when issues arise
- Prolonged downtime during rollback
- Data loss during rollback attempts

**Prevention**:
- Test rollback procedures before migration
- Automate rollback scripts
- Maintain backup systems during migration

**Example Rollback Script**:
```bash
#!/bin/bash
# Automated rollback procedure

echo "Starting rollback..."

# Stop new system
kubectl scale deployment new-app --replicas=0

# Switch traffic back
kubectl apply -f ingress-legacy.yaml

# Restore database
pg_restore --clean --if-exists backup.sql

# Verify rollback
curl -f http://legacy-app/health || exit 1

echo "Rollback completed successfully"
```

## Team and Communication Mistakes

### Mistake: Poor Stakeholder Communication
**Problem**: Teams unaware of migration schedule and impact.

**Symptoms**:
- Unexpected service disruptions
- Resistance to migration changes
- Lack of support during issues

**Prevention**:
- Clear communication plan
- Regular status updates
- Escalation procedures documented

### Mistake: Insufficient Team Training
**Problem**: Teams unprepared to work with new system post-migration.

**Symptoms**:
- Operational issues after migration
- Slow incident response
- Rollback pressure from fear

**Prevention**:
- Training sessions before migration
- Documentation updates
- Support team preparation

## Technical Debt Mistakes

### Mistake: Accumulating Migration Debt
**Problem**: Leaving migration scaffolding in production code.

**Symptoms**:
- Dead code and feature flags remain
- Performance degradation from compatibility layers
- Maintenance burden increases

**Prevention**:
- Cleanup plans as part of migration
- Time-boxed removal of temporary code
- Automated cleanup scripts

**Example Cleanup Script**:
```javascript
// Remove feature flags after successful migration
const cleanupFlags = [
  'USE_NEW_API',
  'ENABLE_GRAPHQL',
  'LEGACY_DATABASE'
];

for (const flag of cleanupFlags) {
  if (process.env[flag] === 'true') {
    console.log(`Removing legacy flag: ${flag}`);
    // Remove from code and configuration
  }
}
```

### Mistake: Ignoring Performance Impact
**Problem**: Migration introduces performance regressions.

**Symptoms**:
- Slower response times
- Increased resource usage
- User experience degradation

**Prevention**:
- Performance testing during migration
- Benchmarking before and after
- Gradual rollout to catch issues early

## Recovery and Learning Mistakes

### Mistake: Not Learning from Failures
**Problem**: Repeating the same migration mistakes.

**Symptoms**:
- Similar issues in future migrations
- Lack of process improvement
- Team frustration

**Prevention**:
- Post-mortem analysis after migrations
- Documentation of lessons learned
- Process improvements based on experience

### Mistake: Inadequate Backup Strategy
**Problem**: Insufficient or untested backup procedures.

**Symptoms**:
- Cannot recover from migration failures
- Data loss incidents
- Prolonged recovery times

**Prevention**:
- Multiple backup strategies
- Test backup restoration regularly
- Offsite and immutable backups