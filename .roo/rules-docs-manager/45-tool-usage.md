# .roo/rules-docs-manager/40-tool-usage.md
> Specific tool usage instructions and patterns for documentation management tasks.

## Primary Analysis Tools

### `codebase_search` - Finding Documentation Sources
**Purpose:** Locate code elements that need documentation or verify existing documentation accuracy.

**When to use:**
- Identifying undocumented functions, classes, or APIs
- Finding code examples for documentation
- Verifying documentation matches implementation
- Discovering related code for comprehensive documentation

**Best practices:**
- Use specific keywords from function names, class names, or error messages
- Combine with file type filters for targeted searches
- Search for TODO/FIXME comments indicating documentation needs
- Look for existing documentation files to understand current coverage

**Example usage:**
```javascript
// Search for API functions that might need documentation
codebase_search("export.*function|export.*class", "*.ts,*.tsx")

// Find existing documentation files
codebase_search("README|API|docs", "*.md")
```

### `read_file` - Code Analysis for Documentation
**Purpose:** Examine source code to extract accurate information for documentation.

**When to use:**
- Analyzing function signatures and parameters
- Understanding class structures and relationships
- Extracting code examples and usage patterns
- Verifying implementation details against documentation

**Best practices:**
- Read interface/type definitions first for API documentation
- Focus on public methods and exported functions
- Note parameter types, return types, and error conditions
- Look for existing comments that can be enhanced

**Example patterns:**
```javascript
// Read interface definitions for API docs
read_file("src/interfaces/User.ts")

// Examine implementation for usage examples
read_file("src/services/UserService.ts")
```

### `search_files` - Documentation Quality Checks
**Purpose:** Find patterns in documentation or code that indicate documentation issues.

**When to use:**
- Finding outdated documentation references
- Identifying inconsistent terminology
- Locating broken links or references
- Checking for documentation coverage gaps

**Best practices:**
- Use regex patterns to find specific documentation issues
- Search for common outdated patterns (old version numbers, deprecated APIs)
- Look for TODO comments related to documentation
- Check for consistent naming across documentation files

**Example patterns:**
```regex
# Find potentially outdated version references
search_files("v\d+\.\d+", "*.md")

# Locate broken relative links
search_files("\[.*\]\(\.\./\.\./.*\)", "*.md")

# Find functions without JSDoc comments
search_files("^(export )?function \w+\(", "*.ts,*.tsx")
```

## Documentation Generation Tools

### `apply_diff` - Documentation Updates
**Purpose:** Modify existing documentation files with accurate, up-to-date information.

**When to use:**
- Updating API documentation with new parameters or return types
- Correcting outdated examples or usage instructions
- Adding missing documentation sections
- Fixing documentation formatting or structure

**Best practices:**
- Always read the full file first to understand context
- Make minimal, targeted changes to avoid introducing errors
- Preserve existing formatting and style conventions
- Include line numbers for precise targeting

**Example usage:**
```javascript
// Update function documentation with new parameter
apply_diff("docs/api.md", {
  search: "### oldFunction(param1)\n\nDescription of old function.",
  replace: "### oldFunction(param1, param2)\n\nDescription of old function with new parameter.\n\n**Parameters:**\n- `param1` (string): Original parameter\n- `param2` (number): New parameter added in v2.0"
})
```

### `write_to_file` - New Documentation Creation
**Purpose:** Create new documentation files from scratch.

**When to use:**
- Generating API reference documentation
- Creating user guides or tutorials
- Writing architecture documentation
- Producing release notes or changelogs

**Best practices:**
- Use established templates and patterns
- Follow project documentation conventions
- Include all necessary sections (examples, parameters, error handling)
- Ensure proper file naming and location

**Example structure:**
```javascript
write_to_file("docs/new-feature.md", `# New Feature Documentation

## Overview
Description of the new feature and its benefits.

## Usage
\`\`\`javascript
// Code example showing how to use the feature
const result = newFeature(options);
\`\`\`

## API Reference
Complete API documentation...

## Migration Guide
If applicable, migration instructions from old versions.
`)
```

## Validation and Quality Assurance Tools

### `execute_command` - Documentation Validation
**Purpose:** Run tools to validate documentation quality and accuracy.

**When to use:**
- Checking documentation formatting and links
- Running documentation linters
- Building documentation sites to verify rendering
- Executing code examples to verify they work

**Best practices:**
- Use documentation-specific linters (markdownlint, remark)
- Run link checkers to find broken references
- Build documentation to catch rendering issues
- Test code examples in isolated environments

**Example commands:**
```bash
# Lint markdown files
execute_command("markdownlint docs/*.md")

# Check for broken links
execute_command("find docs -name '*.md' -exec markdown-link-check {} \;")

# Build documentation site
execute_command("cd docs && mkdocs build")

# Test code examples (if applicable)
execute_command("node -e \"// Test documentation examples\"")
```

### `list_files` - Documentation Inventory
**Purpose:** Survey existing documentation to understand coverage and organization.

**When to use:**
- Assessing current documentation state
- Planning documentation improvements
- Identifying missing documentation areas
- Organizing documentation restructuring

**Best practices:**
- Use recursive listing for full documentation tree
- Filter by file extensions (.md, .rst, .adoc)
- Look for patterns in file naming and organization
- Compare against code structure for coverage gaps

**Example usage:**
```javascript
// List all documentation files
list_files("docs", { recursive: true })

// Find API documentation specifically
list_files("docs/api", { recursive: true })
```

## Integration with Memory MCP

### Documentation Error Tracking
**Purpose:** Track and learn from documentation issues for continuous improvement.

**When to use:**
- After discovering documentation inaccuracies
- When documentation generation fails
- After receiving user feedback on documentation
- When fixing documentation bugs

**Memory integration:**
```javascript
// Capture documentation failure
error.capture({
  kind: "DocFailure",
  message: "API documentation missing new parameter",
  detector: "manual-review",
  normalizedKey: "api-doc-incomplete"
})

// Query for similar issues
search_nodes("type:Error normalizedKey:api-doc-incomplete")

// Record successful fix
fix.apply({
  strategy: "add-missing-parameter-docs",
  changes: ["Updated API docs with new parameter"],
  result: "applied"
})
```

### Documentation Source Tracking
**Purpose:** Maintain provenance of documentation sources and updates.

**When to use:**
- After generating new documentation
- When updating existing documentation
- After verifying documentation accuracy
- When archiving documentation sources

**Memory integration:**
```javascript
// Record documentation source
doc.note({
  url: "https://github.com/org/repo/blob/main/src/api.ts",
  title: "API Implementation Source",
  site: "GitHub",
  author: "Development Team",
  accessed_at: "2023-10-15T10:30:00Z",
  excerpt: "export function apiFunction(param1: string, param2: number)"
})

// Link fix to documentation
fix.apply({
  strategy: "update-api-docs",
  changes: ["Added param2 documentation"],
  result: "applied"
})
// Then create relationship: Fix DERIVED_FROM Doc
```

## Workflow Integration Patterns

### Documentation Generation Workflow
1. **Analyze code:** Use `codebase_search` and `read_file` to understand implementation
2. **Extract information:** Identify functions, parameters, return types, examples
3. **Generate content:** Use templates and patterns from common-patterns.md
4. **Validate accuracy:** Cross-reference with code and run examples
5. **Apply updates:** Use `apply_diff` for existing docs, `write_to_file` for new docs
6. **Quality check:** Run linters and link checkers
7. **Record success:** Log to Memory MCP with `fix.apply` and `doc.note`

### Documentation Maintenance Workflow
1. **Monitor changes:** Watch for code changes that affect documentation
2. **Identify impacts:** Use `search_files` to find affected documentation
3. **Update content:** Apply necessary changes with `apply_diff`
4. **Verify completeness:** Check that all affected areas are updated
5. **Test validation:** Run documentation tests and builds
6. **Track updates:** Record changes in Memory MCP for future reference

### Error Recovery Workflow
1. **Detect failure:** Identify documentation issues through validation or user feedback
2. **Analyze cause:** Use Memory MCP to find similar past issues
3. **Apply fix:** Use proven solutions from memory or develop new approach
4. **Verify fix:** Test that documentation is now accurate and complete
5. **Record learning:** Store fix in Memory MCP for future use
6. **Prevent recurrence:** Update processes to catch similar issues early