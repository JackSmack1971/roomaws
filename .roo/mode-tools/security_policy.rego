package security

import data.roomodes.customModes

# Security baseline data
forbidden_patterns = {
    "auth_files": ".*(auth|authentication|credentials)/.*",
    "payment_files": ".*(payment|billing|checkout)/.*",
    "security_files": ".*(security|secrets)/.*",
    "admin_files": ".*(admin|superuser)/.*"
}

# Rule: Each mode must have exactly one edit tuple
single_edit_tuple {
    some mode
    customModes[mode]
    groups := customModes[mode].groups
    edit_count := count([g | g := groups[_]; g[0] == "edit"])
    edit_count == 1
}

# Rule: No mode can access forbidden patterns
no_forbidden_access {
    some mode
    customModes[mode]
    groups := customModes[mode].groups
    some group
    groups[group][0] == "edit"
    regex := groups[group][1].fileRegex

    # Check that regex doesn't match forbidden patterns
    not matches_forbidden(regex)
}

matches_forbidden(regex) {
    some pattern_name
    forbidden_patterns[pattern_name]
    pattern := forbidden_patterns[pattern_name]

    # Test against sample forbidden paths
    test_paths := [
        sprintf("src/%s/file.ts", [pattern_name]),
        sprintf("lib/%s-service.ts", [pattern_name])
    ]

    some test_path
    test_paths[test_path]
    regex_match(regex, test_path)
}

# Rule: Issue resolver cannot access critical infrastructure
issue_resolver_security {
    some mode
    customModes[mode].slug == "issue-resolver"
    groups := customModes[mode].groups

    # Must not match forbidden patterns
    not matches_forbidden(groups[_][1].fileRegex)
}

# Rule: Migration specialist limited to specific config files
migration_specialist_restricted {
    some mode
    customModes[mode].slug == "migration-specialist"
    groups := customModes[mode].groups
    some group
    groups[group][0] == "edit"
    regex := groups[group][1].fileRegex

    # Must only allow specific migration config files
    allowed_configs := [
        "migration-config.",
        "flyway.conf",
        "liquibase.properties"
    ]

    some config
    allowed_configs[config]
    contains(regex, config)
}

# Deny policies
deny[msg] {
    not single_edit_tuple
    msg := "Each mode must have exactly one edit tuple to avoid parser bugs"
}

deny[msg] {
    not no_forbidden_access
    msg := "Mode can access forbidden security-critical files"
}

deny[msg] {
    not issue_resolver_security
    msg := "Issue resolver can access critical infrastructure files"
}

deny[msg] {
    not migration_specialist_restricted
    msg := "Migration specialist has overly broad access to config files"
}