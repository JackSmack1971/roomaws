# .roo/rules-docs-manager/50-examples.md
> Complete workflow examples demonstrating documentation management from start to finish.

## Example 1: API Documentation Update

### Scenario
A new parameter `timeout` was added to the `fetchData()` function, but the API documentation wasn't updated.

### Workflow Execution

**Step 1: Intake & Analysis**
- Task: Update API documentation for `fetchData()` function
- Keywords extracted: fetchData, timeout, API documentation
- Code search: `codebase_search("function fetchData", "*.ts")`

**Step 2: Code Examination**
```javascript
// Found in src/api/client.ts
/**
 * Fetches data from the API endpoint
 * @param {string} url - The API endpoint URL
 * @param {object} options - Request options
 * @returns {Promise<object>} The response data
 */
export async function fetchData(url, options = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), options.timeout || 5000);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}
```

**Step 3: Documentation Gap Analysis**
- Current docs: Missing `timeout` parameter in JSDoc
- Missing: Parameter description, type information, default value
- Missing: Error handling documentation for timeout scenarios

**Step 4: Documentation Update**
```javascript
apply_diff("src/api/client.ts", {
  search: `/**
 * Fetches data from the API endpoint
 * @param {string} url - The API endpoint URL
 * @param {object} options - Request options
 * @returns {Promise<object>} The response data
 */`,
  replace: `/**
 * Fetches data from the API endpoint with timeout support
 * @param {string} url - The API endpoint URL
 * @param {object} options - Request options
 * @param {number} [options.timeout=5000] - Request timeout in milliseconds
 * @returns {Promise<object>} The response data
 * @throws {Error} When request times out or network error occurs
 * @example
 * // Basic usage
 * const data = await fetchData('/api/users');
 *
 * // With custom timeout
 * const data = await fetchData('/api/users', { timeout: 10000 });
 */`
})
```

**Step 5: Verification**
- Run code to ensure JSDoc is syntactically correct
- Check that examples execute without errors
- Verify parameter descriptions are complete and accurate

**Step 6: Memory Logging**
```javascript
fix.apply({
  strategy: "update-jsdoc-with-missing-parameter",
  changes: ["Added timeout parameter documentation with examples"],
  result: "applied"
})
```

## Example 2: README Generation for New Package

### Scenario
A new npm package `data-validator` needs a comprehensive README.md file.

### Workflow Execution

**Step 1: Intake & Analysis**
- Task: Create README for new `data-validator` package
- Keywords: validation, data, npm package, API
- Code analysis: `read_file("src/index.ts")` to understand public API

**Step 2: API Analysis**
```javascript
// src/index.ts
export { validateEmail } from './validators/email';
export { validatePhone } from './validators/phone';
export { validateCreditCard } from './validators/credit-card';
export { ValidationError } from './errors';
export type { ValidationResult } from './types';
```

**Step 3: Feature Extraction**
- Core validators: email, phone, credit card
- Error handling: ValidationError class
- Type safety: TypeScript types for results
- Usage patterns: Individual validators vs batch validation

**Step 4: README Creation**
```markdown
write_to_file("README.md", `# Data Validator

A lightweight, type-safe data validation library for JavaScript and TypeScript applications.

## Features

- ✅ Email validation with common provider support
- ✅ Phone number validation for international formats
- ✅ Credit card validation with type detection
- ✅ TypeScript support with full type safety
- ✅ Custom error messages and validation rules
- ✅ Zero dependencies, small bundle size

## Installation

\`\`\`bash
npm install data-validator
# or
yarn add data-validator
\`\`\`

## Quick Start

\`\`\`javascript
import { validateEmail, validatePhone, ValidationError } from 'data-validator';

try {
  // Validate email
  const emailResult = validateEmail('user@example.com');
  console.log(emailResult.isValid); // true

  // Validate phone
  const phoneResult = validatePhone('+1-555-123-4567');
  console.log(phoneResult.isValid); // true

} catch (error) {
  if (error instanceof ValidationError) {
    console.log('Validation failed:', error.message);
  }
}
\`\`\`

## API Reference

### Validators

#### \`validateEmail(email: string): ValidationResult\`

Validates email address format and common domain patterns.

**Parameters:**
- \`email\` (string): Email address to validate

**Returns:** \`ValidationResult\` with \`isValid\` boolean and optional error message

**Example:**
\`\`\`javascript
const result = validateEmail('invalid-email');
console.log(result.isValid); // false
console.log(result.error); // "Invalid email format"
\`\`\`

#### \`validatePhone(phone: string): ValidationResult\`

Validates phone number format for international numbers.

**Parameters:**
- \`phone\` (string): Phone number to validate (supports various formats)

**Returns:** \`ValidationResult\` with validation status

#### \`validateCreditCard(cardNumber: string): ValidationResult\`

Validates credit card numbers and identifies card type.

**Parameters:**
- \`cardNumber\` (string): Credit card number (digits only or with spaces/dashes)

**Returns:** \`ValidationResult\` with card type information

### Error Handling

\`\`\`javascript
import { ValidationError } from 'data-validator';

try {
  validateEmail('invalid');
} catch (error) {
  if (error instanceof ValidationError) {
    // Handle validation error
    console.log(error.field); // Field that failed validation
    console.log(error.rule); // Validation rule that failed
  }
}
\`\`\`

### Types

\`\`\`typescript
interface ValidationResult {
  isValid: boolean;
  error?: string;
  details?: {
    cardType?: string; // For credit card validation
    countryCode?: string; // For phone validation
  };
}
\`\`\`

## Advanced Usage

### Custom Validation Rules

\`\`\`javascript
import { validateEmail } from 'data-validator';

// Basic validation
const result = validateEmail('user@company.com');

// With custom options (future feature)
const result = validateEmail('user@company.com', {
  allowLocal: true,
  checkDNS: false
});
\`\`\`

### Batch Validation

\`\`\`javascript
import { validateEmail, validatePhone } from 'data-validator';

const validations = [
  validateEmail('user@example.com'),
  validatePhone('+1-555-123-4567'),
  validateEmail('invalid-email') // Will be invalid
];

const allValid = validations.every(v => v.isValid);
const errors = validations.filter(v => !v.isValid);
\`\`\`

## Error Messages

The library provides clear, user-friendly error messages:

- "Invalid email format"
- "Phone number must include country code"
- "Credit card number is invalid"
- "Unsupported credit card type"

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup and contribution guidelines.

## License

MIT - see [LICENSE](./LICENSE) file for details.
`)
```

**Step 5: Quality Validation**
- Run `markdownlint README.md` to check formatting
- Test code examples manually
- Verify all links and references are correct
- Get peer review from team members

**Step 6: Publication**
- Commit README.md to repository
- Update package.json description if needed
- Publish to npm if ready for release

## Example 3: Troubleshooting Documentation

### Scenario
Users are reporting timeout issues with the API client, but troubleshooting docs are inadequate.

### Workflow Execution

**Step 1: Issue Analysis**
- User reports: "API calls timeout after 5 seconds"
- Code review: Default timeout is 5000ms, but no documentation on how to configure
- Search existing docs: `search_files("timeout", "*.md")` - finds minimal references

**Step 2: Root Cause Identification**
- Missing configuration documentation
- No troubleshooting section for timeout issues
- Examples don't show timeout configuration

**Step 3: Troubleshooting Section Creation**
```markdown
write_to_file("docs/troubleshooting.md", `# Troubleshooting

## Common Issues

### API Request Timeouts

**Symptoms:**
- Requests fail with "AbortError" or timeout messages
- Slow API response times
- Intermittent connectivity issues

**Causes:**
- Default 5-second timeout is too short for slow networks
- Large payloads requiring more time
- Server-side processing delays

**Solutions:**

#### 1. Increase Timeout Configuration

\`\`\`javascript
import { ApiClient } from 'api-client';

// Increase timeout to 30 seconds
const client = new ApiClient({
  timeout: 30000, // 30 seconds
  retries: 2
});

// Or per-request timeout
const data = await client.get('/slow-endpoint', {
  timeout: 60000 // 1 minute for specific slow requests
});
\`\`\`

#### 2. Implement Retry Logic

\`\`\`javascript
const client = new ApiClient({
  timeout: 10000,
  retries: 3,
  retryDelay: 1000 // 1 second between retries
});
\`\`\`

#### 3. Check Network Connectivity

\`\`\`bash
# Test basic connectivity
ping api.example.com

# Test API endpoint
curl -m 10 https://api.example.com/health
\`\`\`

#### 4. Monitor Request Performance

\`\`\`javascript
const start = Date.now();
try {
  const data = await client.get('/endpoint');
  console.log(\`Request took \${Date.now() - start}ms\`);
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request timed out after 5 seconds');
  }
}
\`\`\`

### Authentication Errors

**Symptoms:**
- 401 Unauthorized responses
- "Invalid token" error messages

**Causes:**
- Expired API tokens
- Incorrect token format
- Missing authentication headers

**Solutions:**

#### Token Refresh

\`\`\`javascript
class AuthenticatedClient extends ApiClient {
  async request(method, url, options = {}) {
    try {
      return await super.request(method, url, options);
    } catch (error) {
      if (error.status === 401) {
        // Token expired, refresh and retry
        await this.refreshToken();
        return await super.request(method, url, options);
      }
      throw error;
    }
  }
}
\`\`\`

#### Token Validation

\`\`\`javascript
// Check token before making requests
const client = new ApiClient();

if (!client.isTokenValid()) {
  await client.authenticate();
}

// Now make authenticated requests
const data = await client.get('/protected-endpoint');
\`\`\`

### Rate Limiting

**Symptoms:**
- 429 Too Many Requests responses
- Requests work intermittently

**Solutions:**

#### Implement Backoff Strategy

\`\`\`javascript
class ResilientClient extends ApiClient {
  async request(method, url, options = {}) {
    let attempt = 0;
    const maxAttempts = 5;

    while (attempt < maxAttempts) {
      try {
        return await super.request(method, url, options);
      } catch (error) {
        if (error.status === 429) {
          // Exponential backoff
          const delay = Math.pow(2, attempt) * 1000;
          await new Promise(resolve => setTimeout(resolve, delay));
          attempt++;
        } else {
          throw error;
        }
      }
    }
    throw new Error('Max retry attempts exceeded');
  }
}
\`\`\`

## Diagnostic Tools

### Connection Test Script

\`\`\`javascript
// diagnostic.js
const { ApiClient } = require('api-client');

async function diagnose() {
  const client = new ApiClient();

  console.log('Testing API connectivity...');

  // Test 1: Basic connectivity
  try {
    const health = await client.get('/health', { timeout: 5000 });
    console.log('✅ Health check passed');
  } catch (error) {
    console.log('❌ Health check failed:', error.message);
  }

  // Test 2: Authentication
  try {
    const auth = await client.get('/auth/test');
    console.log('✅ Authentication check passed');
  } catch (error) {
    console.log('❌ Authentication check failed:', error.message);
  }

  // Test 3: Timeout handling
  try {
    const slow = await client.get('/slow-endpoint', { timeout: 1000 });
    console.log('✅ Timeout test passed');
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('✅ Timeout correctly triggered');
    } else {
      console.log('❌ Unexpected error:', error.message);
    }
  }
}

diagnose();
\`\`\`

Run diagnostics:
\`\`\`bash
node diagnostic.js
\`\`\`

## Getting Help

If these solutions don't resolve your issue:

1. Check the [GitHub Issues](https://github.com/org/repo/issues) for similar problems
2. Create a new issue with:
   - Your environment (Node.js version, OS)
   - Full error message and stack trace
   - Code sample that reproduces the issue
   - API client configuration
3. Include diagnostic script output when reporting issues
`)
```

**Step 4: Integration with Existing Docs**
- Update main README to reference troubleshooting guide
- Add troubleshooting links to API documentation
- Cross-reference related sections

**Step 5: Testing & Validation**
- Test all code examples manually
- Verify diagnostic script works
- Get user feedback on clarity and completeness

## Example 4: Architecture Documentation Update

### Scenario
System architecture changed with addition of caching layer, but docs weren't updated.

### Workflow Execution

**Step 1: Change Detection**
- Code review shows new Redis caching layer added
- Architecture diagrams need updating
- API behavior changed (cache headers, performance characteristics)

**Step 2: Impact Analysis**
- Which documentation needs updating: API docs, architecture docs, deployment docs
- What changed: Response times, cache behavior, error handling
- Who needs to know: Developers, DevOps, stakeholders

**Step 3: Documentation Updates**

**API Documentation Update:**
```javascript
apply_diff("docs/api.md", {
  search: `## Performance

Response times vary based on data complexity and server load.`,
  replace: `## Performance

Response times vary based on data complexity, server load, and cache status.

### Caching Behavior

- **First request**: 200-500ms (cache miss, data fetched from database)
- **Subsequent requests**: 50-100ms (cache hit, data served from Redis)
- **Cache TTL**: 300 seconds (5 minutes)
- **Cache invalidation**: Automatic on data updates

### Cache Headers

Responses include cache status headers:

\`\`\`http
X-Cache-Status: HIT
X-Cache-TTL: 240
Age: 60
\`\`\`

**Header values:**
- \`X-Cache-Status\`: \`HIT\`, \`MISS\`, or \`EXPIRED\`
- \`X-Cache-TTL\`: Seconds remaining before cache expires
- \`Age\`: Seconds since cache was populated
`
})
```

**Architecture Documentation Update:**
```markdown
write_to_file("docs/architecture.md", `# System Architecture

## Overview

The system implements a layered architecture with caching for improved performance.

\`\`\`mermaid
graph TB
    A[Client] --> B[API Gateway]
    B --> C[Load Balancer]
    C --> D[Application Server]
    D --> E[Redis Cache]
    D --> F[Database]

    E -.->|Cache Miss| F
    E -->|Cache Hit| D
\`\`\`

## Components

### API Gateway
- Routes requests to appropriate services
- Handles authentication and rate limiting
- Provides unified API interface

### Application Server
- Implements business logic
- Manages data validation and processing
- Coordinates with cache and database

### Redis Cache
- **Type**: In-memory data structure store
- **Purpose**: Reduce database load and improve response times
- **TTL**: 5 minutes for most data
- **Invalidation**: Write-through cache updates

### Database
- **Type**: PostgreSQL relational database
- **Purpose**: Persistent data storage
- **Access**: Through application server only

## Data Flow

### Read Operations

1. **Cache Check**: Application server checks Redis for requested data
2. **Cache Hit**: Return cached data with cache headers
3. **Cache Miss**: Query database, store result in cache, return data

### Write Operations

1. **Database Update**: Write changes to database
2. **Cache Invalidation**: Remove or update related cache entries
3. **Response**: Return success confirmation

## Performance Characteristics

| Operation | Cache Hit | Cache Miss | Database Only |
|-----------|-----------|------------|---------------|
| Simple Query | ~50ms | ~200ms | ~300ms |
| Complex Query | ~100ms | ~500ms | ~800ms |
| Write Operation | ~150ms | ~150ms | ~150ms |

## Caching Strategy

### Cache Keys
- \`user:{id}\`: User profile data
- \`posts:{userId}:{page}\`: Paginated post lists
- \`stats:{type}\`: Aggregated statistics

### Cache Invalidation Patterns
- **Direct**: Delete specific keys on updates
- **Pattern**: Delete all keys matching pattern
- **Time-based**: Let cache expire naturally

### Cache Warming
- Pre-populate frequently accessed data on startup
- Warm cache during low-traffic periods
- Monitor cache hit rates and adjust warming strategy

## Monitoring

### Cache Metrics
- Hit rate (> 80% target)
- Memory usage (< 80% of allocated)
- Eviction rate (should be low)
- Response time degradation

### Alerts
- Cache hit rate below 70%
- Redis memory usage above 90%
- Cache warming failures
- Database connection pool exhaustion
`)
```

**Step 4: Deployment Documentation**
```markdown
apply_diff("docs/deployment.md", {
  search: `## Infrastructure Requirements

- Application server
- Database server
- Load balancer`,
  replace: `## Infrastructure Requirements

- Application server
- Database server
- Redis cache server
- Load balancer

## Redis Configuration

### Development
\`\`\`yaml
redis:
  host: localhost
  port: 6379
  password: ""  # No password for dev
  db: 0
\`\`\`

### Production
\`\`\`yaml
redis:
  host: redis-cluster.example.com
  port: 6379
  password: \${REDIS_PASSWORD}
  db: 0
  cluster: true
  tls: true
\`\`\`

### Environment Variables
\`\`\`
REDIS_URL=redis://username:password@host:port/db
REDIS_TLS=true  # For production clusters
REDIS_CLUSTER=true  # Enable cluster mode
\`\`\`
`
})
```

**Step 5: Validation & Testing**
- Verify architecture diagrams render correctly
- Test cache behavior with actual requests
- Validate performance claims with benchmarks
- Get architecture review from technical leads

**Step 6: Communication**
- Update team with architecture changes
- Provide migration guide for deployment changes
- Schedule knowledge sharing session for complex changes