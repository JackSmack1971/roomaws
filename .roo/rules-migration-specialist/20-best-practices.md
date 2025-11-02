# 20-best-practices.md
> Best practices for migration-specialist mode: strangler fig patterns, feature flags, rollback procedures, and validation rules.

## Strangler Fig Pattern Implementation

### Overview
The Strangler Fig pattern involves gradually replacing old system components with new ones while maintaining functionality. This minimizes risk during large migrations.

### Implementation Examples

#### API Endpoint Migration
```typescript
// Legacy API endpoint
app.get('/api/v1/users', legacyUserHandler);

// New API endpoint (initially disabled)
app.get('/api/v2/users', newUserHandler);

// Feature flag-controlled routing
app.get('/users', (req, res) => {
  if (process.env.USE_NEW_API === 'true') {
    return newUserHandler(req, res);
  }
  return legacyUserHandler(req, res);
});
```

#### Database Schema Migration
```sql
-- Add new column alongside old one
ALTER TABLE users ADD COLUMN email_new VARCHAR(255);

-- Migrate data incrementally
UPDATE users SET email_new = email WHERE email_new IS NULL LIMIT 1000;

-- Switch reads to new column via feature flag
SELECT CASE
  WHEN @use_new_schema THEN email_new
  ELSE email
END as email FROM users;
```

### Cutover Strategies

#### Blue-Green Deployment
- Deploy new system alongside old
- Route traffic gradually (0% → 25% → 50% → 100%)
- Monitor metrics at each stage
- Rollback by switching traffic back

#### Canary Releases
- Deploy to small subset of users first
- Monitor error rates and performance
- Gradually increase traffic percentage
- Use feature flags for user segmentation

#### Feature Flag Cutover
```javascript
// Feature flag service integration
const featureFlags = require('feature-flag-service');

async function getUserData(userId) {
  const useNewApi = await featureFlags.isEnabled('new-api', userId);

  if (useNewApi) {
    return newApiClient.getUser(userId);
  } else {
    return legacyApiClient.getUser(userId);
  }
}
```

## Rollback Procedure Templates

### Immediate Rollback (< 5 minutes)
1. **Feature Flag Reversal**: Set feature flag to false
2. **Traffic Switch**: Route 100% to old system
3. **Cache Invalidation**: Clear any cached new-system data
4. **Verification**: Confirm old system is handling all requests

### Data Rollback (5-30 minutes)
1. **Stop Migration**: Halt any ongoing data migration scripts
2. **Backup Restore**: Restore from pre-migration backup
3. **Schema Revert**: Run down migration scripts
4. **Application Restart**: Restart services with old configuration

### Full System Rollback (> 30 minutes)
1. **Traffic Cutover**: Route all traffic to backup/old environment
2. **Database Failover**: Switch to backup database instance
3. **Code Deployment**: Deploy previous version
4. **Data Synchronization**: Sync any missed data from new to old system

## Migration Checkpoint Validation Rules

### Pre-Migration Validation
- [ ] All automated tests passing
- [ ] Performance benchmarks established
- [ ] Rollback procedures documented and tested
- [ ] Monitoring dashboards configured
- [ ] Stakeholder communication plan in place

### During Migration Validation
- [ ] Error rates below threshold (< 1%)
- [ ] Response times within SLA
- [ ] Data consistency checks passing
- [ ] Feature flag rollout gradual and controlled
- [ ] User feedback monitoring active

### Post-Migration Validation
- [ ] All functionality verified in production
- [ ] Performance meets or exceeds baseline
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [ ] Team training completed

### Automated Validation Scripts
```bash
#!/bin/bash
# Migration health check script

echo "Running migration validation checks..."

# Check error rates
ERROR_RATE=$(curl -s "monitoring-api/errors?period=5m" | jq '.rate')
if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
  echo "ERROR: Error rate too high: $ERROR_RATE"
  exit 1
fi

# Check response times
RESPONSE_TIME=$(curl -s "monitoring-api/response-time?period=5m" | jq '.p95')
if (( $(echo "$RESPONSE_TIME > 200" | bc -l) )); then
  echo "ERROR: Response time too high: ${RESPONSE_TIME}ms"
  exit 1
fi

# Data consistency check
DATA_DIFF=$(run-data-consistency-check.sh)
if [ "$DATA_DIFF" -gt 0 ]; then
  echo "ERROR: Data inconsistency detected: $DATA_DIFF records"
  exit 1
fi

echo "All validation checks passed!"