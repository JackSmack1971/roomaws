# .roo/rules-mode-validator/20-best-practices.md
> Best practices for mode validation, quality standards, and systematic validation approaches.

## Validation Philosophy

### Comprehensive Coverage
- **Multi-layer validation**: Check schema, permissions, rules, and functionality
- **Progressive depth**: Start with basic checks, then drill down into complex issues
- **Cross-validation**: Verify consistency between .roomodes and rule files
- **Regression prevention**: Include checks that catch common configuration mistakes

### Automated First Approach
- **Safe automation**: Apply automated fixes for obvious, safe issues
- **Guided remediation**: Provide clear instructions for manual fixes
- **Validation loops**: Re-validate after fixes to ensure completeness
- **Feedback integration**: Learn from validation results to improve future checks

## Schema Validation Standards

### YAML Structure Requirements
- **Well-formed YAML**: Valid syntax with proper indentation and structure
- **Required fields**: All mandatory fields present with correct data types
- **Field constraints**: Values meet specified format requirements (e.g., slug patterns)
- **Reference integrity**: All referenced tools and files exist

### Mode Configuration Best Practices
- **Descriptive names**: Clear, descriptive mode names with relevant emojis
- **Unique slugs**: Globally unique identifiers following naming conventions
- **Complete descriptions**: Comprehensive roleDefinition and whenToUse fields
- **Appropriate tool groups**: Minimal necessary permissions following least privilege

## Permission Validation Standards

### FileRegex Pattern Quality
- **Precise patterns**: Target exactly the intended files, no more, no less
- **Security compliance**: Never allow access to sensitive directories
- **Anchored patterns**: Use ^ and $ to prevent partial matches
- **Testable patterns**: Patterns that can be verified against repository structure

### Permission Scope Guidelines
- **Single edit tuple**: Exactly one edit group per mode to avoid parser bugs
- **Minimal access**: Grant only necessary permissions for mode responsibilities
- **Clear descriptions**: Document what each permission allows and why it's needed
- **Regular audits**: Periodically review and justify permission scopes

## Rules Directory Standards

### File Completeness Requirements
- **All required files**: Complete set of numbered rule files (00- through 60+)
- **Substantial content**: Each file contains meaningful, actionable guidance
- **Consistent structure**: Follow established patterns and templates
- **Current information**: Rules reflect actual mode behavior and constraints

### Content Quality Standards
- **Actionable guidance**: Clear, step-by-step instructions users can follow
- **Comprehensive coverage**: Address common scenarios and edge cases
- **Evidence-based**: Justify recommendations with reasoning or examples
- **Maintainable**: Easy to update as mode behavior evolves

## Functional Validation Standards

### Tool Availability Checks
- **Accessible tools**: All declared tools can be invoked successfully
- **Proper configuration**: Tools work with provided parameters
- **Error handling**: Tools fail gracefully with helpful error messages
- **Performance**: Tools complete operations within reasonable time limits

### Mode Loading Verification
- **Clean loading**: Modes load without errors or warnings
- **Configuration application**: Mode settings are applied correctly
- **Integration compatibility**: Modes work with orchestrator and other modes
- **Runtime stability**: Modes remain stable during extended operation

## Reporting and Communication Standards

### Issue Classification System
- **Critical**: Blocks mode operation or creates security vulnerabilities
- **High**: Significant functionality impairment or user confusion
- **Medium**: Quality degradation or missing features
- **Low**: Minor improvements or documentation issues
- **Info**: Suggestions for optimization or best practice adoption

### Report Structure Requirements
- **Executive summary**: High-level overview of validation results
- **Detailed findings**: Specific issues with evidence and impact assessment
- **Prioritized recommendations**: Actionable fixes ranked by importance
- **Success metrics**: Quantitative measures of validation coverage and quality

## Validation Process Standards

### Systematic Approach
- **Structured phases**: Follow defined validation phases in order
- **Complete coverage**: Don't skip validation categories
- **Consistent criteria**: Apply same standards to all modes
- **Documentation**: Record validation process and decisions

### Quality Assurance
- **Peer review**: Have validation results reviewed by experienced team members
- **Automated verification**: Use tools to verify validation tool correctness
- **Regression testing**: Ensure fixes don't break other functionality
- **Continuous improvement**: Learn from validation results to improve processes

## Memory Integration Standards

### Error Tracking Excellence
- **Precise categorization**: Use specific, actionable error types
- **Complete context**: Include all relevant information for debugging
- **Normalized keys**: Consistent error identification across validations
- **Resolution linkage**: Connect errors to proven fix patterns

### Knowledge Preservation
- **Comprehensive logging**: Record all validation activities and outcomes
- **Pattern recognition**: Identify recurring issues for systemic fixes
- **Solution documentation**: Preserve successful resolution strategies
- **Continuous learning**: Build knowledge base for future validations

## Common Validation Pitfalls

### Schema Issues
- **Missing fields**: Required fields omitted from mode configuration
- **Type mismatches**: Incorrect data types for configuration values
- **Invalid references**: References to non-existent tools or files
- **Malformed patterns**: FileRegex patterns with syntax errors

### Permission Problems
- **Over-permissive access**: FileRegex patterns allowing unintended file access
- **Security bypasses**: Patterns that circumvent security boundaries
- **Multiple edit tuples**: Configuration causing parser bugs
- **Unclear scope**: Permissions that are too broad or poorly documented

### Rules Inconsistencies
- **Missing files**: Incomplete rules directory structure
- **Outdated content**: Rules not reflecting current mode behavior
- **Contradictory guidance**: Rules conflicting with each other or configuration
- **Incomplete coverage**: Rules missing important scenarios or edge cases

### Functional Failures
- **Tool unavailability**: Declared tools not accessible or properly configured
- **Loading errors**: Modes failing to load due to configuration issues
- **Integration problems**: Modes not working properly with orchestrator
- **Performance issues**: Validation or mode operation taking excessive time

## Continuous Improvement Practices

### Validation Enhancement
- **New check development**: Add checks for newly discovered issue patterns
- **Automation expansion**: Increase automated fix coverage over time
- **Performance optimization**: Improve validation speed and efficiency
- **User experience**: Make validation reports clearer and more actionable

### Process Refinement
- **Workflow optimization**: Streamline validation processes based on experience
- **Standard updates**: Update validation standards based on industry best practices
- **Tool evaluation**: Assess and improve validation tool effectiveness
- **Training development**: Create training materials for validation best practices

### Quality Metrics Tracking
- **Coverage metrics**: Track percentage of potential issues detected
- **Accuracy metrics**: Measure false positive and false negative rates
- **Efficiency metrics**: Monitor validation time and resource usage
- **Impact metrics**: Track how validation prevents production issues