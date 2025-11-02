# .roo/rules-docs-manager/20-best-practices.md
> Best practices for documentation management, quality standards, and maintenance procedures.

## Documentation Quality Standards

### Content Accuracy
- **Verify against code**: Always cross-reference documentation with actual implementation
- **Test examples**: Ensure code examples compile and run correctly
- **Update on changes**: Monitor code changes that affect documented behavior
- **Version alignment**: Keep documentation synchronized with code versions

### Structure and Organization
- **Clear hierarchy**: Use consistent heading levels and logical section organization
- **Navigation aids**: Include table of contents, cross-references, and search-friendly structure
- **Progressive disclosure**: Start with high-level overviews, provide details on demand
- **Modular design**: Break complex documentation into focused, reusable sections

### Writing Standards
- **Active voice**: Use active voice for clarity and directness
- **Consistent terminology**: Maintain consistent naming and technical terms throughout
- **Audience awareness**: Write for the appropriate technical level of target readers
- **Concise expression**: Be comprehensive but avoid unnecessary verbosity

## Code Documentation Practices

### API Documentation
- **Complete signatures**: Document all parameters, return types, and exceptions
- **Usage examples**: Provide practical examples for common use cases
- **Edge cases**: Document limitations, constraints, and error conditions
- **Version information**: Note when APIs were introduced or deprecated

### Inline Comments
- **Purpose explanation**: Explain why code exists, not just what it does
- **Complexity justification**: Comment on non-obvious algorithms or business logic
- **Assumption documentation**: Note important assumptions or preconditions
- **TODO/FIXME tracking**: Use standardized markers for future improvements

## Documentation Maintenance

### Update Triggers
- **Code changes**: Review documentation when modifying public interfaces
- **Bug fixes**: Update documentation to reflect corrected behavior
- **Feature additions**: Document new capabilities and usage patterns
- **Deprecation notices**: Clearly mark deprecated features and migration paths

### Review Processes
- **Peer review**: Have documentation reviewed by subject matter experts
- **User feedback**: Incorporate feedback from documentation users
- **Automated checks**: Use tools to verify documentation accuracy and completeness
- **Regular audits**: Schedule periodic reviews of documentation quality

## Tool and Process Integration

### Documentation Generation
- **Automated extraction**: Use tools to extract API documentation from code
- **Template consistency**: Apply consistent templates across similar documentation
- **Version control**: Keep documentation in version control with code
- **Build integration**: Include documentation validation in CI/CD pipelines

### Quality Assurance
- **Link checking**: Verify all internal and external links are functional
- **Format validation**: Ensure consistent formatting and style adherence
- **Accessibility**: Follow accessibility guidelines for web-based documentation
- **Search optimization**: Structure content for effective search and discovery

## Common Pitfalls to Avoid

### Accuracy Issues
- **Stale content**: Documentation that doesn't reflect current implementation
- **Incomplete coverage**: Missing documentation for important features
- **Inconsistent information**: Contradictions between different documentation sources
- **Unclear examples**: Code examples that don't work or are misleading

### Structural Problems
- **Poor organization**: Hard-to-navigate or illogically structured content
- **Missing context**: Documentation lacking necessary background information
- **Over-complication**: Unnecessarily complex explanations for simple concepts
- **Under-documentation**: Insufficient detail for complex or critical features

### Maintenance Challenges
- **No update process**: Lack of clear procedures for keeping documentation current
- **Ownership gaps**: Unclear responsibility for different documentation areas
- **Tool fragmentation**: Using incompatible tools that create maintenance overhead
- **Quality neglect**: Allowing documentation quality to degrade over time

## Documentation Types and Standards

### API Reference Documentation
- Function/method signatures with complete parameter descriptions
- Return value specifications and error conditions
- Usage examples with expected outputs
- Version compatibility and deprecation information

### User Guides and Tutorials
- Step-by-step instructions for common tasks
- Prerequisites and system requirements
- Troubleshooting sections for common issues
- Screenshots or diagrams where helpful

### Architecture and Design Documents
- System component relationships and data flows
- Design decision rationales and trade-offs
- Performance characteristics and limitations
- Future evolution plans and extensibility points

### Release Notes and Changelogs
- Clear categorization of changes (features, fixes, breaking changes)
- Migration guides for breaking changes
- Known issues and workarounds
- Future roadmap highlights