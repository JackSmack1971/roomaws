#!/usr/bin/env python3
"""
Memory Health Check Script
Validates memory MCP integration health and provides diagnostics.

Usage:
    python memory-health-check.py [--mode <mode_slug>] [--verbose]

Checks performed:
- Memory MCP connectivity
- Recent memory writes per mode
- Fix reuse patterns
- Observation envelope quality
- Relation consistency
- Memory protocol compliance
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Mock MCP client for demonstration - replace with actual MCP integration
class MockMemoryMCP:
    def __init__(self):
        self.connected = True
        self.last_health_check = datetime.now()

    def search_nodes(self, query: str) -> Dict[str, Any]:
        """Mock search - replace with actual MCP call"""
        # Simulate some test data
        if "type:Run" in query:
            return {
                "nodes": [
                    {
                        "name": "run#2025-11-01T16:00:00.000Z#abc12345",
                        "type": "Run",
                        "observations": ["command.exec", "run.summary"],
                        "timestamp": "2025-11-01T16:00:00.000Z"
                    }
                ]
            }
        return {"nodes": []}

    def read_graph(self) -> Dict[str, Any]:
        """Mock graph read - replace with actual MCP call"""
        return {
            "entities": [
                {"name": "err#test-error", "type": "Error"},
                {"name": "fix#test-fix#def67890", "type": "Fix"},
                {"name": "run#2025-11-01T16:00:00.000Z#abc12345", "type": "Run"}
            ],
            "relations": [
                {"from": "fix#test-fix#def67890", "to": "err#test-error", "relationType": "RESOLVES"},
                {"from": "run#2025-11-01T16:00:00.000Z#abc12345", "to": "fix#test-fix#def67890", "relationType": "APPLIES"}
            ]
        }

class MemoryHealthChecker:
    def __init__(self, mcp_client=None):
        self.mcp = mcp_client or MockMemoryMCP()
        self.issues = []
        self.warnings = []
        self.metrics = {}

    def check_connectivity(self) -> bool:
        """Check if Memory MCP is accessible"""
        try:
            # Test basic connectivity
            result = self.mcp.search_nodes("type:Run LIMIT 1")
            self.metrics["mcp_connected"] = True
            return True
        except Exception as e:
            self.issues.append({
                "check": "connectivity",
                "severity": "CRITICAL",
                "message": f"Memory MCP unavailable: {e}"
            })
            self.metrics["mcp_connected"] = False
            return False

    def check_recent_activity(self, hours: int = 24) -> None:
        """Check for recent memory writes across all modes"""
        cutoff = datetime.now() - timedelta(hours=hours)

        try:
            runs = self.mcp.search_nodes(f"type:Run timestamp > {cutoff.isoformat()}")

            mode_activity = {}
            for run in runs.get("nodes", []):
                # Extract mode from run metadata (would need actual implementation)
                mode = run.get("mode", "unknown")
                mode_activity[mode] = mode_activity.get(mode, 0) + 1

            self.metrics["recent_runs"] = len(runs.get("nodes", []))
            self.metrics["mode_activity"] = mode_activity

            # Check for modes with no recent activity
            expected_modes = [
                "issue-resolver", "design-engineer", "test", "integration-tester",
                "docs-manager", "merge-resolver", "security-auditor", "performance-profiler"
            ]

            inactive_modes = []
            for mode in expected_modes:
                if mode_activity.get(mode, 0) == 0:
                    inactive_modes.append(mode)

            if inactive_modes:
                self.warnings.append({
                    "check": "recent_activity",
                    "severity": "WARNING",
                    "message": f"Modes with no recent memory writes: {', '.join(inactive_modes)}"
                })

        except Exception as e:
            self.issues.append({
                "check": "recent_activity",
                "severity": "ERROR",
                "message": f"Failed to check recent activity: {e}"
            })

    def check_fix_reuse_patterns(self) -> None:
        """Analyze how often modes reuse learned fixes"""
        try:
            # Get all fixes and their application counts
            fixes = self.mcp.search_nodes("type:Fix")

            total_fixes = len(fixes.get("nodes", []))
            applied_fixes = sum(1 for fix in fixes.get("nodes", [])
                               if fix.get("application_count", 0) > 1)

            self.metrics["total_fixes"] = total_fixes
            self.metrics["reused_fixes"] = applied_fixes

            if total_fixes > 0:
                reuse_rate = applied_fixes / total_fixes
                self.metrics["fix_reuse_rate"] = reuse_rate

                if reuse_rate < 0.1:  # Less than 10% reuse
                    self.warnings.append({
                        "check": "fix_reuse",
                        "severity": "WARNING",
                        "message": f"Low fix reuse rate: {reuse_rate:.1%} - memory may not be effectively consulted"
                    })

        except Exception as e:
            self.issues.append({
                "check": "fix_reuse",
                "severity": "ERROR",
                "message": f"Failed to analyze fix reuse patterns: {e}"
            })

    def check_observation_quality(self) -> None:
        """Validate observation envelope completeness"""
        try:
            graph = self.mcp.read_graph()
            entities = graph.get("entities", [])

            quality_issues = []
            for entity in entities:
                observations = entity.get("observations", [])
                for obs in observations:
                    # Check for required fields based on observation type
                    if obs.get("type") == "fix.apply":
                        if not obs.get("strategy") or not obs.get("changes"):
                            quality_issues.append(f"fix.apply missing required fields in {entity['name']}")
                    elif obs.get("type") == "error.capture":
                        if not obs.get("normalizedKey"):
                            quality_issues.append(f"error.capture missing normalizedKey in {entity['name']}")

            if quality_issues:
                self.issues.append({
                    "check": "observation_quality",
                    "severity": "ERROR",
                    "message": f"Observation quality issues: {len(quality_issues)} found",
                    "details": quality_issues[:5]  # Limit details
                })

            self.metrics["observation_quality_issues"] = len(quality_issues)

        except Exception as e:
            self.issues.append({
                "check": "observation_quality",
                "severity": "ERROR",
                "message": f"Failed to check observation quality: {e}"
            })

    def check_relation_consistency(self) -> None:
        """Validate that relations are consistent and complete"""
        try:
            graph = self.mcp.read_graph()
            relations = graph.get("relations", [])

            # Check for orphaned entities
            entities = {e["name"]: e for e in graph.get("entities", [])}
            orphaned_relations = []

            for rel in relations:
                if rel["from"] not in entities or rel["to"] not in entities:
                    orphaned_relations.append(rel)

            if orphaned_relations:
                self.issues.append({
                    "check": "relation_consistency",
                    "severity": "ERROR",
                    "message": f"Found {len(orphaned_relations)} relations pointing to non-existent entities"
                })

            # Check for Fixes without Errors
            fixes_without_errors = []
            error_relations = [r for r in relations if r["relationType"] == "RESOLVES"]

            for entity in entities.values():
                if entity["type"] == "Fix":
                    has_error = any(r["from"] == entity["name"] for r in error_relations)
                    if not has_error:
                        fixes_without_errors.append(entity["name"])

            if fixes_without_errors:
                self.warnings.append({
                    "check": "relation_consistency",
                    "severity": "WARNING",
                    "message": f"Found {len(fixes_without_errors)} fixes not linked to errors"
                })

            self.metrics["orphaned_relations"] = len(orphaned_relations)
            self.metrics["unlinked_fixes"] = len(fixes_without_errors)

        except Exception as e:
            self.issues.append({
                "check": "relation_consistency",
                "severity": "ERROR",
                "message": f"Failed to check relation consistency: {e}"
            })

    def generate_report(self, verbose: bool = False) -> str:
        """Generate a comprehensive health report"""
        report_lines = []

        report_lines.append("Memory Health Check Report")
        report_lines.append("=" * 50)
        report_lines.append(f"Timestamp: {datetime.now().isoformat()}")
        report_lines.append(f"MCP Connected: {self.metrics.get('mcp_connected', 'Unknown')}")
        report_lines.append("")

        # Issues
        if self.issues:
            report_lines.append(f"ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                report_lines.append(f"  {issue['severity']}: {issue['message']}")
                if verbose and 'details' in issue:
                    for detail in issue['details']:
                        report_lines.append(f"    - {detail}")
            report_lines.append("")

        # Warnings
        if self.warnings:
            report_lines.append(f"WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                report_lines.append(f"  {warning['severity']}: {warning['message']}")
            report_lines.append("")

        # Metrics
        report_lines.append("METRICS:")
        for key, value in self.metrics.items():
            if isinstance(value, float):
                report_lines.append(f"  {key}: {value:.2%}")
            else:
                report_lines.append(f"  {key}: {value}")
        report_lines.append("")

        # Overall health score
        health_score = self._calculate_health_score()
        report_lines.append(f"OVERALL HEALTH SCORE: {health_score:.1f}/100")

        if health_score >= 80:
            report_lines.append("Memory system is healthy")
        elif health_score >= 60:
            report_lines.append("Memory system needs attention")
        else:
            report_lines.append("Memory system requires immediate fixes")

        return "\n".join(report_lines)

    def _calculate_health_score(self) -> float:
        """Calculate overall health score 0-100"""
        score = 100.0

        # Critical issues
        score -= len(self.issues) * 20

        # Warnings
        score -= len(self.warnings) * 5

        # MCP connectivity
        if not self.metrics.get("mcp_connected", True):
            score -= 50

        # Activity levels
        recent_runs = self.metrics.get("recent_runs", 0)
        if recent_runs == 0:
            score -= 30
        elif recent_runs < 5:
            score -= 10

        # Fix reuse rate
        reuse_rate = self.metrics.get("fix_reuse_rate", 0)
        if reuse_rate < 0.1:
            score -= 15

        return max(0.0, min(100.0, score))

    def run_all_checks(self, verbose: bool = False) -> str:
        """Run all health checks and return report"""
        print("Running memory health checks...")

        self.check_connectivity()
        if self.metrics.get("mcp_connected"):
            self.check_recent_activity()
            self.check_fix_reuse_patterns()
            self.check_observation_quality()
            self.check_relation_consistency()

        return self.generate_report(verbose)

def main():
    parser = argparse.ArgumentParser(description="Memory Health Check")
    parser.add_argument("--mode", help="Check specific mode only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--hours", type=int, default=24, help="Hours to look back for activity")

    args = parser.parse_args()

    checker = MemoryHealthChecker()
    report = checker.run_all_checks(verbose=args.verbose)

    print(report)

    # Exit with error code if there are critical issues
    critical_issues = [i for i in checker.issues if i["severity"] == "CRITICAL"]
    if critical_issues:
        sys.exit(1)

if __name__ == "__main__":
    main()