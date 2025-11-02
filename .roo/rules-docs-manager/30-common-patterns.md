# .roo/rules-docs-manager/30-common-patterns.md
> Reusable documentation patterns, templates, and code examples for consistent documentation generation.

## Documentation Templates

### API Function Documentation Template
```markdown
## `functionName(parameters)`

**Description:** Brief description of what the function does and its primary purpose.

**Parameters:**
- `param1` (Type): Description of parameter purpose and constraints
- `param2` (Type, optional): Description with default value if applicable

**Returns:** ReturnType - Description of return value and possible values

**Throws:**
- `ErrorType`: When this error occurs and what it means
- `AnotherError`: Additional error conditions

**Example:**
```javascript
const result = functionName('value', { option: true });
// Returns: expected result
```

**Since:** v1.2.0
**Deprecated:** Use `newFunctionName()` instead (since v2.0.0)
```

### Class Documentation Template
```markdown
## ClassName

**Description:** Overview of the class purpose and responsibilities.

**Constructor:**
```javascript
new ClassName(options)
```

**Properties:**
- `property1` (Type): Description of property purpose
- `property2` (Type, readonly): Description with access constraints

**Methods:**
- [`method1()`](#method1) - Brief method description
- [`method2()`](#method2) - Brief method description

**Example:**
```javascript
const instance = new ClassName({ config: 'value' });
instance.method1();
```

**Extends:** ParentClass
**Implements:** Interface1, Interface2
```

### Configuration Documentation Template
```markdown
## Configuration Options

Configure the system using the following options in `config.json`:

```json
{
  "option1": "default_value",
  "option2": 42,
  "option3": {
    "nested": "value"
  }
}
```

### Option Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | string | `"default"` | Description of option1 purpose |
| `option2` | number | `42` | Description of option2 with valid ranges |
| `option3.nested` | string | `"value"` | Description of nested configuration |

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENV_VAR1` | Yes | - | Required environment variable description |
| `ENV_VAR2` | No | `"default"` | Optional environment variable |
```

## Code Comment Patterns

### Function Header Comments
```javascript
/**
 * Calculates the total price including tax and discounts
 * @param {number} basePrice - The base price before tax/discounts
 * @param {number} taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param {number[]} discounts - Array of discount percentages as decimals
 * @returns {number} The final price after applying tax and discounts
 * @throws {Error} If basePrice is negative or taxRate is invalid
 * @example
 * calculatePrice(100, 0.08, [0.1, 0.05]) // Returns 87.6
 */
function calculatePrice(basePrice, taxRate, discounts) {
  // Implementation
}
```

### Class Property Comments
```javascript
class ShoppingCart {
  /**
   * Items currently in the cart
   * @type {CartItem[]}
   * @private
   */
  #items = [];

  /**
   * Total price before tax
   * @type {number}
   * @readonly
   */
  get subtotal() {
    return this.#items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

### Complex Algorithm Comments
```javascript
/**
 * Implements the Knuth-Morris-Pratt string search algorithm
 * Time complexity: O(n + m) where n is text length, m is pattern length
 * Space complexity: O(m) for the failure function
 *
 * The algorithm preprocesses the pattern to create a failure function that
 * indicates where to continue searching when a mismatch occurs, avoiding
 * redundant comparisons.
 */
function kmpSearch(text, pattern) {
  // Build failure function - tracks prefix/suffix matches
  const failure = buildFailureFunction(pattern);

  let i = 0; // text index
  let j = 0; // pattern index

  while (i < text.length) {
    if (text[i] === pattern[j]) {
      i++;
      j++;
      if (j === pattern.length) {
        return i - j; // Found match
      }
    } else if (j > 0) {
      j = failure[j - 1]; // Use failure function to skip
    } else {
      i++;
    }
  }

  return -1; // No match found
}
```

## README Patterns

### Project README Structure
```markdown
# Project Name

Brief description of what the project does and its main purpose.

## Features

- Feature 1: Description of key capability
- Feature 2: Description of another capability
- Feature 3: Description of additional functionality

## Installation

```bash
npm install project-name
# or
yarn add project-name
```

## Quick Start

```javascript
import { mainFunction } from 'project-name';

const result = mainFunction('input');
// Do something with result
```

## API Reference

See [API Documentation](./docs/api.md) for complete API reference.

## Configuration

See [Configuration Guide](./docs/configuration.md) for setup options.

## Contributing

See [Contributing Guide](./CONTRIBUTING.md) for development setup.

## License

MIT - see [LICENSE](./LICENSE) file for details.
```

### API Documentation README
```markdown
# API Documentation

This document describes the available APIs for integrating with the system.

## Authentication

All API requests require authentication via Bearer token:

```
Authorization: Bearer <your-api-token>
```

## Endpoints

### GET /api/v1/resources

Retrieve a list of resources.

**Query Parameters:**
- `limit` (number, optional): Maximum number of results (default: 20, max: 100)
- `offset` (number, optional): Number of results to skip (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": "123",
      "name": "Resource Name",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 0
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing authentication
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Server error

### POST /api/v1/resources

Create a new resource.

**Request Body:**
```json
{
  "name": "New Resource",
  "description": "Optional description"
}
```

**Response:** `201 Created`
```json
{
  "id": "456",
  "name": "New Resource",
  "description": "Optional description",
  "created_at": "2023-01-01T00:00:00Z"
}
```
```

## Error Handling

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "specific field that caused the error"
    }
  }
}
```

## Rate Limiting

API requests are limited to 1000 requests per hour per API token.
Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1638360000
```
```

## Changelog Patterns

### Version Release Format
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description
- Another new feature

### Changed
- Modified behavior description
- Updated API endpoint

### Deprecated
- Deprecated feature notice

### Removed
- Removed feature description

### Fixed
- Bug fix description
- Another bug fix

### Security
- Security improvement description

## [1.2.0] - 2023-10-15

### Added
- Added support for custom themes
- New configuration option for timeouts

### Fixed
- Fixed memory leak in long-running processes
- Corrected error handling in edge cases

## [1.1.0] - 2023-09-01

### Added
- Initial public API release
- Basic authentication support

### Changed
- Improved error messages for better debugging

---

## Version History

- **1.2.0** (2023-10-15): Theme support and bug fixes
- **1.1.0** (2023-09-01): Public API and authentication
- **1.0.0** (2023-08-01): Initial release
```

## Troubleshooting Documentation Patterns

### Common Issues Section
```markdown
## Troubleshooting

### Issue: "Connection timeout"

**Symptoms:**
- Requests fail with timeout errors
- Slow response times
- Intermittent connectivity

**Causes:**
- Network connectivity issues
- Server overload
- Incorrect timeout configuration

**Solutions:**

1. **Check network connectivity:**
   ```bash
   ping api.example.com
   ```

2. **Verify configuration:**
   ```javascript
   const config = {
     timeout: 30000, // Increase timeout to 30 seconds
     retries: 3
   };
   ```

3. **Monitor server status:**
   Check status page at https://status.example.com

### Issue: "Authentication failed"

**Symptoms:**
- 401 Unauthorized responses
- Access denied to protected resources

**Causes:**
- Expired API token
- Incorrect token format
- Insufficient permissions

**Solutions:**

1. **Regenerate API token:**
   ```bash
   curl -X POST https://api.example.com/auth/token \
     -H "Content-Type: application/json" \
     -d '{"username": "your-username", "password": "your-password"}'
   ```

2. **Verify token format:**
   Ensure token is included as: `Authorization: Bearer <token>`

3. **Check permissions:**
   Contact administrator to verify account permissions