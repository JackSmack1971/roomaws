# .roo/rules-test/20-coverage-policy.md
> Coverage requirements and enforcement for Test mode. Ensures code quality through measurable test coverage with Vitest/Istanbul integration.

## Coverage Policy

- Never commit changes that decrease overall coverage below 80%
- New features require >= 85% line coverage
- Bug fixes must add regression tests
- Run `pnpm test:coverage` before marking tests complete
- Document why if unable to cover edge cases

## Coverage Requirements

### Acceptable Coverage Metrics
- **Line Coverage**: Minimum 80% overall; 85% for new features
- **Branch Coverage**: Minimum 75% overall; aim for 80% on critical paths
- **Function Coverage**: Minimum 85% overall; 90% for exported/public functions
- **Statement Coverage**: Minimum 80% overall; align with line coverage

### When Coverage Can Be Lower
- **Edge Cases**: Error handling paths, deprecated code, or platform-specific code (e.g., Windows-only paths) may have lower coverage if testing is impractical
- **Error Handling**: Exception paths that require specific conditions (e.g., network failures, disk full) can be excluded if mocked alternatives exist
- **Third-Party Code**: Wrapper functions around external libraries may have reduced requirements if the library itself is tested
- **Performance Code**: Hot paths optimized for speed may prioritize branch coverage over exhaustive line coverage

### Coverage Tooling Integration
- **Primary Tool**: Use Istanbul/c8 via Vitest's built-in coverage (`vitest --coverage`)
- **Configuration**: Ensure `vitest.config.ts` includes coverage settings with thresholds:
  ```typescript
  export default defineConfig({
    test: {
      coverage: {
        provider: 'c8',
        reporter: ['text', 'json', 'html'],
        thresholds: {
          global: {
            lines: 80,
            branches: 75,
            functions: 85,
            statements: 80
          }
        },
        exclude: [
          'node_modules/',
          'dist/',
          '**/*.d.ts',
          '**/*.config.*',
          'src/utils/safeWriteJson.ts' // exempt per rules-code
        ]
      }
    }
  })
  ```
- **Reporting**: Generate HTML reports for review; JSON for CI integration
- **CI Integration**: Fail builds if thresholds not met; use `pnpm test:coverage --run` in pipelines

### Coverage Change Requirements
- **No Decreases**: All changes must maintain or improve overall coverage percentages
- **Baseline Checks**: Compare against main branch coverage before merging
- **Incremental Improvements**: Aim to increase coverage with each PR, even if minimally
- **Exceptions**: Document and approve coverage decreases only for justified reasons (e.g., removing dead code)

### Handling Hard-to-Test Code
- **Mocks and Stubs**: Use Vitest's mocking capabilities for external dependencies, network calls, or file system operations
- **Integration Tests**: For complex interactions, supplement unit tests with integration tests that achieve higher coverage
- **Test Utilities**: Create builders/factories for complex object construction to enable thorough testing
- **Manual Testing Notes**: For truly untestable code (e.g., hardware-specific), document manual testing procedures and link to integration test coverage
- **Refactoring for Testability**: Prefer dependency injection and small, pure functions to improve testability

## Workflow Integration

- **Pre-Commit Hook**: Run coverage checks before commits to prevent regressions
- **PR Reviews**: Include coverage reports in pull request comments; require reviewer approval for coverage changes
- **Memory Integration**: Persist coverage metrics as `run.summary` observations with coverage deltas and failure reasons if thresholds not met
- **Fix Application**: When applying fixes, ensure new tests maintain or improve coverage; link coverage improvements to `fix.apply` observations

## Enforcement

- **Automatic Checks**: Use `vitest --coverage --run` in test scripts to enforce thresholds
- **Manual Overrides**: Require explicit documentation and approval for any coverage exceptions
- **Continuous Monitoring**: Track coverage trends over time via memory graph queries for historical analysis