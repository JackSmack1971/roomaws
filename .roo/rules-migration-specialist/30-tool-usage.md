# 30-tool-usage.md
> Detailed tool usage patterns for migration tools: codemods, migration scripts, and feature flags.

## Codemod Tools

### jscodeshift Usage Patterns

#### Basic Transformation
```javascript
// transform.js
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // Find all require statements for old library
  const requires = root.find(j.CallExpression, {
    callee: { name: 'require' },
    arguments: [{ value: 'old-library' }]
  });

  // Replace with new library
  requires.replaceWith(() => {
    return j.callExpression(
      j.identifier('require'),
      [j.literal('new-library')]
    );
  });

  return root.toSource();
};
```

#### Running Codemods
```bash
# Dry run first
npx jscodeshift -t transform.js --dry src/

# Apply transformations
npx jscodeshift -t transform.js src/

# With parser options for TypeScript
npx jscodeshift -t transform.js --parser tsx src/
```

### AST Transformation Libraries

#### ts-morph for TypeScript
```typescript
import { Project } from 'ts-morph';

const project = new Project();
const sourceFile = project.addSourceFileAtPath('src/old-file.ts');

// Rename interface
const interfaceDecl = sourceFile.getInterface('OldInterface');
if (interfaceDecl) {
  interfaceDecl.rename('NewInterface');
}

// Update import statements
sourceFile.getImportDeclarations().forEach(imp => {
  if (imp.getModuleSpecifierValue() === 'old-package') {
    imp.setModuleSpecifier('new-package');
  }
});

sourceFile.save();
```

## Migration Scripts

### Database Migration Tools

#### Flyway Migration Script
```sql
-- V1__Create_initial_schema.sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- V2__Add_user_profile.sql
ALTER TABLE users ADD COLUMN profile_id BIGINT;
ALTER TABLE users ADD CONSTRAINT fk_user_profile
  FOREIGN KEY (profile_id) REFERENCES profiles(id);
```

#### Running Flyway
```bash
# Validate migrations
flyway validate

# Apply migrations
flyway migrate

# Generate baseline
flyway baseline
```

### Data Migration Scripts

#### Node.js Data Migration
```javascript
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function migrateUserEmails() {
  const client = await pool.connect();

  try {
    // Get users in batches
    let offset = 0;
    const batchSize = 1000;

    while (true) {
      const result = await client.query(
        'SELECT id, email FROM users ORDER BY id LIMIT $1 OFFSET $2',
        [batchSize, offset]
      );

      if (result.rows.length === 0) break;

      // Process batch
      for (const user of result.rows) {
        const newEmail = transformEmail(user.email);
        await client.query(
          'UPDATE users SET email = $1 WHERE id = $2',
          [newEmail, user.id]
        );
      }

      offset += batchSize;
      console.log(`Processed ${offset} users`);
    }

    console.log('Migration completed successfully');
  } catch (error) {
    console.error('Migration failed:', error);
    throw error;
  } finally {
    client.release();
  }
}
```

## Feature Flag Tools

### LaunchDarkly Integration

#### Feature Flag Service
```javascript
const LaunchDarkly = require('launchdarkly-node-server-sdk');

class FeatureFlagService {
  constructor() {
    this.client = LaunchDarkly.init(process.env.LD_SDK_KEY);
  }

  async isEnabled(flagKey, userId, defaultValue = false) {
    const user = {
      key: userId,
      anonymous: false
    };

    return await this.client.variation(flagKey, user, defaultValue);
  }

  async getVariation(flagKey, userId, defaultValue) {
    const user = {
      key: userId,
      anonymous: false
    };

    return await this.client.variation(flagKey, user, defaultValue);
  }
}
```

#### Feature Flag Rollout Script
```javascript
const featureFlags = new FeatureFlagService();

async function gradualRollout(flagKey, targetPercentage) {
  const rules = [
    {
      variation: true,
      weight: targetPercentage,
      rule: {
        attribute: 'userId',
        op: 'in',
        values: [] // Would populate with user IDs
      }
    }
  ];

  await featureFlags.updateFlagRules(flagKey, rules);
}
```

### Configuration-Based Feature Flags

#### Environment Variable Flags
```javascript
class ConfigFeatureFlags {
  constructor(config = {}) {
    this.config = { ...process.env, ...config };
  }

  isEnabled(flagKey, context = {}) {
    const value = this.config[flagKey.toUpperCase()];
    if (value === undefined) return false;

    // Support percentage rollouts
    if (value.includes('%')) {
      const percentage = parseInt(value);
      const hash = this.hashUser(context.userId || 'anonymous');
      return (hash % 100) < percentage;
    }

    return value === 'true' || value === '1';
  }

  hashUser(userId) {
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      const char = userId.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }
}
```

## Testing Migration Tools

### Migration Testing Framework
```javascript
class MigrationTester {
  constructor() {
    this.originalData = null;
    this.migratedData = null;
  }

  async setupTestData() {
    // Create test data in old format
    this.originalData = await this.createTestUsers(100);
  }

  async runMigration() {
    // Execute migration script
    await runMigrationScript();
    this.migratedData = await this.fetchMigratedUsers();
  }

  async validateMigration() {
    const issues = [];

    // Check data integrity
    if (this.originalData.length !== this.migratedData.length) {
      issues.push('Data count mismatch');
    }

    // Validate transformations
    for (const original of this.originalData) {
      const migrated = this.migratedData.find(u => u.id === original.id);
      if (!migrated) {
        issues.push(`User ${original.id} missing after migration`);
        continue;
      }

      if (migrated.email !== transformEmail(original.email)) {
        issues.push(`Email transformation failed for user ${original.id}`);
      }
    }

    return issues;
  }
}