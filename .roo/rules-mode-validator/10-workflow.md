# .roo/rules-mode-validator/10-workflow.md
> Canonical workflow from validation request intake → comprehensive validation → detailed reporting.

## Intake & Preparation

1) **Identify validation scope**: Determine what needs validation (single mode, all modes, specific aspects)
2) **Gather context**: Review current .roomodes configuration and existing validation results
3) **Set validation parameters**: Choose validation depth (basic schema vs comprehensive analysis)
4) **Prepare environment**: Ensure all validation tools and dependencies are available

## Schema Validation Phase

1) **YAML syntax check**: Validate .roomodes file is well-formed YAML
2) **Schema compliance**: Verify all required fields are present and correctly typed
3) **Field validation**: Check slug format, name conventions, and field constraints
4) **Cross-reference checks**: Ensure referenced files and tools exist

## Permission Analysis Phase

1) **FileRegex pattern validation**: Test regex patterns against sample file paths
2) **Security boundary checks**: Verify patterns don't allow access to forbidden directories
3) **Permission consistency**: Ensure edit permissions align with mode responsibilities
4) **Single tuple verification**: Confirm each mode uses exactly one edit tuple

## Rules Directory Validation

1) **Directory structure check**: Verify all required rule files exist
2) **File completeness assessment**: Check each rule file has substantial content
3) **Content consistency**: Ensure rules align with .roomodes configuration
4) **Memory integration verification**: Confirm hivemind contract compliance

## Functional Testing Phase

1) **Mode loading test**: Attempt to load each mode configuration
2) **Tool availability check**: Verify all declared tools are accessible
3) **File access testing**: Test fileRegex patterns against actual repository structure
4) **Integration validation**: Check mode interactions and handoffs work correctly

## Comprehensive Analysis Phase

1) **Completeness scoring**: Evaluate rule file coverage against quality matrix
2) **Cohesion assessment**: Check for contradictions between configuration and rules
3) **Best practice compliance**: Verify adherence to established patterns
4) **Performance impact analysis**: Assess validation overhead and optimization opportunities

## Reporting & Recommendations

1) **Generate detailed report**: Create comprehensive validation results with severity levels
2) **Prioritize issues**: Rank findings by impact and ease of resolution
3) **Provide actionable fixes**: Suggest specific changes with examples
4) **Document exceptions**: Note any acceptable deviations with justification

## Remediation Support

1) **Automated fixes**: Apply safe, automated corrections where possible
2) **Guided remediation**: Provide step-by-step instructions for manual fixes
3) **Validation verification**: Re-run validation after fixes to confirm resolution
4) **Regression prevention**: Update validation rules to prevent similar issues

## Continuous Improvement

1) **Pattern analysis**: Identify common issues across modes for systemic fixes
2) **Validation enhancement**: Update validation suite based on findings
3) **Documentation updates**: Improve validation documentation with lessons learned
4) **Process refinement**: Optimize validation workflow for efficiency

## Memory Integration Points

1) **Validation logging**: Emit `command.exec` with comprehensive results and metrics
2) **Error tracking**: Persist `error.capture` for validation failures with detailed context
3) **Fix documentation**: Record `fix.apply` for successful automated corrections
4) **Knowledge preservation**: Store `doc.note` for validation findings and patterns
5) **Pattern learning**: Link validation issues to proven resolution strategies