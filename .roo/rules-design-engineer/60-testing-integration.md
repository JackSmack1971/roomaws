# .roo/rules-design-engineer/50-testing-integration.md
> Storybook integration, visual regression testing, and component testing requirements for UI components.

## Storybook Integration
- **Story organization**: Group stories by component and variant.
- **Controls addon**: Use Storybook controls for interactive prop exploration.
- **Documentation**: Auto-generate docs from TypeScript interfaces.
- **Themes**: Support light/dark theme switching in stories.
- **Responsive testing**: Include viewport addon for responsive testing.

## Component Testing
- **Unit tests**: Test component logic and prop handling.
- **Integration tests**: Test component interactions and data flow.
- **Accessibility tests**: Automated a11y checks with axe-core.
- **Snapshot tests**: Visual regression testing with Chromatic or similar.

## Visual Regression Testing
- **Baseline images**: Establish visual baselines for all component states.
- **Cross-browser**: Test across supported browsers and devices.
- **Responsive variants**: Capture screenshots at all breakpoints.
- **Theme variants**: Test both light and dark themes.

## Testing Patterns
- **Arrange-Act-Assert**: Structure tests clearly.
- **Mock data**: Use consistent mock data across tests.
- **Test utilities**: Create reusable testing utilities.
- **Coverage goals**: Aim for >90% component coverage.

## CI/CD Integration
- **Automated runs**: Run tests on every PR and merge.
- **Failure handling**: Block merges on test failures.
- **Review process**: Require manual review of visual changes.
- **Performance budgets**: Monitor component performance metrics.

## Quality Gates
- **Code review**: Require review of component changes.
- **Design review**: Validate against design specifications.
- **Accessibility audit**: Pass automated and manual a11y checks.
- **Performance check**: Meet performance budgets and metrics.

## Documentation Requirements
- **Usage examples**: Comprehensive Storybook documentation.
- **API reference**: Auto-generated from TypeScript types.
- **Migration guides**: Document breaking changes.
- **Changelog**: Track component updates and fixes.

## Tool Configuration
- **Storybook config**: Consistent addon and configuration setup.
- **Test runners**: Jest/Vitest configuration for component testing.
- **Build tools**: Optimized builds for Storybook deployment.
- **Linting**: ESLint rules specific to component development.