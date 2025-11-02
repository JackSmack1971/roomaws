# .roo/rules-performance-profiler/60-common-mistakes.md
> Common pitfalls in performance profiling and how to avoid them.

## Profiling Environment Issues

### Mistake: Profiling Production Systems
**Problem**: Running profiling tools on production can impact user experience and skew results.
**Impact**: Service degradation, inaccurate measurements, potential data loss.
**Solution**:
- Use staging environments that mirror production
- Implement feature flags for profiling in production
- Use read-only profiling tools that don't affect performance

### Mistake: Inconsistent Test Environments
**Problem**: Different hardware, network conditions, or system loads between test runs.
**Impact**: Unreliable benchmarks, false regressions, wasted optimization efforts.
**Solution**:
- Document environment specifications (CPU, RAM, network)
- Use containerized environments (Docker) for consistency
- Run tests during low-traffic periods
- Control background processes and system load

### Mistake: Ignoring Warm-up Effects
**Problem**: Measuring performance immediately after startup without allowing systems to warm up.
**Impact**: Artificially slow measurements, JIT compilation not optimized.
**Solution**:
- Allow 1-2 minute warm-up period before measurements
- Pre-load commonly accessed data
- Run multiple iterations and discard initial results

## Measurement Errors

### Mistake: Focusing Only on Averages
**Problem**: Using only mean response times, ignoring outliers and percentiles.
**Impact**: Missing performance issues affecting real users (long tail).
**Solution**:
- Measure 95th and 99th percentiles
- Track standard deviation
- Use distribution analysis (histograms, box plots)
- Consider user experience metrics over raw performance

### Mistake: Micro-benchmarking Without Context
**Problem**: Optimizing small code snippets without considering system-wide impact.
**Impact**: Improvements that don't translate to real-world performance gains.
**Solution**:
- Profile entire user journeys, not isolated functions
- Use realistic data sets and usage patterns
- Measure end-to-end performance impact
- Consider caching, network, and I/O effects

### Mistake: Not Accounting for Caching Effects
**Problem**: Measurements vary wildly between cold and warm cache states.
**Impact**: Inconsistent results, unrealistic performance expectations.
**Solution**:
- Clearly document cache state (cold/warm/hot)
- Test both cache states when relevant
- Implement proper cache warming procedures
- Monitor cache hit rates in measurements

## Tool Usage Pitfalls

### Mistake: Over-relying on Single Tools
**Problem**: Using only one profiling tool, missing issues detectable by others.
**Impact**: Incomplete performance analysis, missed optimization opportunities.
**Solution**:
- Use multiple complementary tools (Lighthouse + DevTools + APM)
- Cross-validate findings between tools
- Understand each tool's strengths and limitations
- Combine synthetic and real user monitoring

### Mistake: Ignoring Tool Overhead
**Problem**: Profiling tools themselves slow down the application being measured.
**Impact**: Measurements don't reflect real performance.
**Solution**:
- Use low-overhead profiling when possible
- Account for profiling overhead in measurements
- Compare profiled vs non-profiled runs
- Use sampling profilers over instrumenting profilers

### Mistake: Not Updating Profiling Tools
**Problem**: Using outdated versions of profiling tools with known bugs or limitations.
**Impact**: Inaccurate results, missed modern performance features.
**Solution**:
- Keep tools updated to latest versions
- Check for known issues in tool changelogs
- Validate tool behavior with known benchmarks
- Use tool-specific best practices

## Analysis Mistakes

### Mistake: Confusing Correlation with Causation
**Problem**: Assuming that metrics changing together are causally related.
**Impact**: Optimizing the wrong things, introducing unnecessary complexity.
**Solution**:
- Use controlled experiments (A/B testing)
- Isolate variables when possible
- Use statistical significance testing
- Look for confounding factors

### Mistake: Ignoring Statistical Significance
**Problem**: Treating small performance differences as meaningful without statistical validation.
**Impact**: Over-optimizing minor issues, missing major bottlenecks.
**Solution**:
- Run sufficient sample sizes (minimum 30 runs)
- Calculate confidence intervals
- Use statistical tests (t-tests, ANOVA)
- Focus on changes >5-10% for significance

### Mistake: Not Considering Business Impact
**Problem**: Optimizing technical metrics without considering user experience or business value.
**Impact**: Improvements that don't matter to users or business goals.
**Solution**:
- Map performance metrics to business KPIs
- Prioritize based on user impact (Core Web Vitals)
- Consider cost-benefit of optimizations
- Focus on bottlenecks affecting most users

## Optimization Pitfalls

### Mistake: Premature Optimization
**Problem**: Optimizing code before identifying real bottlenecks.
**Impact**: Wasted effort on non-critical paths, complex code.
**Solution**:
- Profile first, optimize second
- Focus on top 20% of performance issues (Pareto principle)
- Use data-driven optimization decisions
- Avoid "optimizing for optimization's sake"

### Mistake: Breaking Functionality for Performance
**Problem**: Performance optimizations that introduce bugs or reduce functionality.
**Impact**: Broken features, security vulnerabilities, maintenance issues.
**Solution**:
- Maintain comprehensive test suites
- Use gradual optimization approaches
- Validate optimizations don't break functionality
- Have rollback plans for failed optimizations

### Mistake: Ignoring Maintenance Overhead
**Problem**: Optimizations that make code harder to maintain or understand.
**Impact**: Technical debt, slower future development, bugs.
**Solution**:
- Balance performance gains against maintenance costs
- Document complex optimizations
- Use established patterns over clever hacks
- Consider long-term maintainability

## Memory and Resource Issues

### Mistake: Memory Leak Misdiagnosis
**Problem**: Attributing memory growth to leaks when it's normal heap expansion.
**Impact**: Unnecessary "fixes" that hurt performance.
**Solution**:
- Understand normal memory patterns for your application
- Use proper heap dump analysis
- Monitor memory over extended periods
- Consider garbage collection behavior

### Mistake: Ignoring Garbage Collection Pressure
**Problem**: Not accounting for GC pauses in performance measurements.
**Impact**: Missing major performance bottlenecks.
**Solution**:
- Measure GC pause times separately
- Use GC logs for analysis
- Consider GC tuning for high-throughput applications
- Monitor GC metrics in production

### Mistake: Resource Contention Ignored
**Problem**: Multiple processes competing for CPU, memory, or I/O resources.
**Impact**: Inaccurate performance measurements.
**Solution**:
- Isolate profiling runs from other processes
- Monitor system resource usage during profiling
- Use dedicated profiling environments
- Account for resource contention in analysis

## Reporting and Communication Issues

### Mistake: Poor Metric Communication
**Problem**: Using technical jargon without explaining impact to stakeholders.
**Impact**: Lack of buy-in for performance initiatives.
**Solution**:
- Translate technical metrics to business impact
- Use clear visualizations (charts, graphs)
- Provide context and baselines
- Focus on user experience improvements

### Mistake: Not Tracking Trends Over Time
**Problem**: Looking at single measurements without historical context.
**Impact**: Missing gradual performance degradation.
**Solution**:
- Implement performance dashboards
- Set up automated regression detection
- Track metrics over releases and time
- Use statistical process control

### Mistake: Ignoring External Factors
**Problem**: Attributing performance issues to code when caused by external factors.
**Impact**: Blaming wrong teams, ineffective fixes.
**Solution**:
- Check network conditions, third-party services
- Monitor infrastructure performance
- Consider CDN, database, and API performance
- Use distributed tracing for complex systems