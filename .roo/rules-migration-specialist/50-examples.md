# 50-examples.md
> Critical examples for complex migrations: framework upgrades, database schema changes, and API migrations.

## Framework Upgrade Examples

### React 17 to 18 Migration

#### Step 1: Dependency Updates
```json
// package.json changes
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0"
  }
}
```

#### Step 2: Root Render Migration
```typescript
// Before (React 17)
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));

// After (React 18)
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<App />);
```

#### Step 3: Feature Flag Implementation
```typescript
// Feature flag for gradual rollout
const useNewReact = process.env.REACT_VERSION === '18';

function App() {
  if (useNewReact) {
    return <NewApp />;
  }
  return <LegacyApp />;
}
```

### Angular Migration Example

#### Module to Standalone Components
```typescript
// Before: Module-based
@NgModule({
  declarations: [UserComponent],
  imports: [CommonModule, FormsModule],
  exports: [UserComponent]
})
export class UserModule { }

// After: Standalone component
@Component({
  selector: 'app-user',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `...`
})
export class UserComponent { }
```

## Database Schema Migration Examples

### PostgreSQL Schema Evolution

#### Adding Nullable Column
```sql
-- Migration: Add profile_picture column
ALTER TABLE users ADD COLUMN profile_picture_url TEXT;

-- Data migration (optional)
UPDATE users SET profile_picture_url = DEFAULT_PROFILE_URL
WHERE profile_picture_url IS NULL;

-- Add constraint later
ALTER TABLE users ALTER COLUMN profile_picture_url SET NOT NULL;
```

#### Table Partitioning Migration
```sql
-- Create partitioned table
CREATE TABLE events (
  id SERIAL,
  event_type TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  data JSONB
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02 PARTITION OF events
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Migrate existing data
INSERT INTO events SELECT * FROM old_events;
```

### MongoDB Schema Migration

#### Field Renaming with Rollback
```javascript
// Migration script
db.users.updateMany(
  { oldField: { $exists: true } },
  [
    {
      $set: {
        newField: "$oldField",
        migratedAt: new Date()
      }
    },
    {
      $unset: "oldField"
    }
  ]
);

// Rollback script
db.users.updateMany(
  { newField: { $exists: true }, migratedAt: { $exists: true } },
  [
    {
      $set: {
        oldField: "$newField"
      }
    },
    {
      $unset: ["newField", "migratedAt"]
    }
  ]
);
```

## API Migration Examples

### REST to GraphQL Migration

#### Dual API Implementation
```typescript
// REST endpoint (legacy)
app.get('/api/users/:id', async (req, res) => {
  const user = await userService.getUser(req.params.id);
  res.json(user);
});

// GraphQL schema (new)
const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    user(id: ID!): User
  }
`;

// Feature flag routing
app.use('/graphql', (req, res, next) => {
  if (process.env.ENABLE_GRAPHQL === 'true') {
    return graphqlHandler(req, res, next);
  }
  res.status(404).json({ error: 'GraphQL not enabled' });
});
```

#### Version Header Routing
```typescript
app.use('/api', (req, res, next) => {
  const version = req.headers['api-version'] || 'v1';

  if (version === 'v2') {
    return v2Router(req, res, next);
  }

  return v1Router(req, res, next);
});
```

### Microservice Split Migration

#### Service Extraction Pattern
```typescript
// Before: Monolithic user service
class UserService {
  async getUser(id) {
    // Get user data
    const user = await db.users.findById(id);

    // Get user orders (tight coupling)
    const orders = await db.orders.find({ userId: id });

    return { ...user, orders };
  }
}

// After: Separate services with async communication
class UserService {
  constructor(orderServiceClient) {
    this.orderServiceClient = orderServiceClient;
  }

  async getUser(id) {
    const user = await db.users.findById(id);

    // Async call to order service
    const orders = await this.orderServiceClient.getUserOrders(id);

    return { ...user, orders };
  }
}
```

## Complex Multi-Step Migration

### Legacy System Modernization

#### Phase 1: Data Export
```bash
#!/bin/bash
# Export legacy data to JSON
mongoexport --db legacy --collection users --out users.json --jsonArray
mongoexport --db legacy --collection orders --out orders.json --jsonArray
```

#### Phase 2: Schema Transformation
```javascript
// Transform legacy schema to new format
const transformedUsers = legacyUsers.map(user => ({
  id: user._id,
  email: user.email_address, // Field rename
  profile: {
    firstName: user.first_name,
    lastName: user.last_name,
    phone: user.phone_number
  },
  createdAt: new Date(user.registration_date),
  status: user.active ? 'active' : 'inactive'
}));
```

#### Phase 3: Incremental Import
```javascript
// Import in batches with progress tracking
const batchSize = 1000;
for (let i = 0; i < transformedUsers.length; i += batchSize) {
  const batch = transformedUsers.slice(i, i + batchSize);

  await newUserService.bulkCreate(batch);

  console.log(`Imported ${i + batch.length} of ${transformedUsers.length} users`);

  // Checkpoint for resumability
  await saveMigrationCheckpoint(i + batch.length);
}
```

#### Phase 4: Validation and Switchover
```javascript
// Data consistency validation
async function validateMigration() {
  const legacyCount = await legacyDb.users.count();
  const newCount = await newDb.users.count();

  if (legacyCount !== newCount) {
    throw new Error(`Count mismatch: ${legacyCount} vs ${newCount}`);
  }

  // Spot check random records
  const sampleIds = await legacyDb.users.find().limit(100).toArray();
  for (const legacyUser of sampleIds) {
    const newUser = await newDb.users.findById(legacyUser._id);
    if (!newUser) {
      throw new Error(`User ${legacyUser._id} not migrated`);
    }
  }
}

// Feature flag cutover
process.env.LEGACY_SYSTEM_ENABLED = 'false';
process.env.NEW_SYSTEM_ENABLED = 'true';