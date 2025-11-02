# .roo/rules-performance-profiler/20-best-practices.md
> Best practices for performance profiling: tool selection, flamegraph interpretation, benchmark reproducibility, and Core Web Vitals thresholds.

## Profiling Tool Command Patterns

### Lighthouse (Web Performance)
- **Desktop**: `lighthouse https://example.com --output=json --output-path=./report.json --preset=desktop --only-categories=performance,accessibility,best-practices,seo`
- **Mobile**: `lighthouse https://example.com --output=json --output-path=./report.json --preset=mobile --form-factor=mobile --screenEmulation.mobile --throttling.cpuSlowdownMultiplier=4`
- **CI/CD**: `lighthouse https://example.com --output=json --output-path=./report.json --budget-path=./budget.json --fail-on-error`

### k6 (Load Testing)
- **Basic Load**: `k6 run --vus 10 --duration 30s script.js`
- **Ramp Up**: `k6 run --vus 1 --duration 10s --stage 10s:10,30s:20,1m:0 script.js`
- **Cloud**: `k6 cloud script.js --tag testid=performance-baseline`

### wrk (HTTP Benchmarking)
- **Basic**: `wrk -t12 -c400 -d30s https://example.com/api/endpoint`
- **Custom Headers**: `wrk -t12 -c400 -d30s -H "Authorization: Bearer token" https://example.com/api/endpoint`
- **Scripted**: `wrk -t12 -c400 -d30s -s post.lua https://example.com/api/endpoint`

### autocannon (Node.js HTTP Load)
- **Basic**: `autocannon -c 100 -d 10 -R 1000 https://example.com`
- **JSON POST**: `autocannon -c 100 -d 10 -m POST -H 'Content-Type: application/json' -b '{"key":"value"}' https://example.com/api`
- **Progress**: `autocannon -c 100 -d 10 --progress https://example.com`

## Flamegraph Interpretation Guidelines

### CPU Flamegraphs
- **Width**: Represents CPU time; wider bars = more time spent
- **Height**: Call stack depth; bottom = entry point, top = current function
- **Color**: Usually random (not meaningful); focus on width
- **Key Patterns**:
  - Wide top bars: Hot functions consuming most CPU
  - Plateaus: Functions called many times (loops)
  - Icicles: Deep call stacks (recursion or complex flows)

### Memory Flamegraphs
- **Width**: Memory allocation size
- **Color Coding**: Often by allocation type (heap, stack)
- **Identify Leaks**: Look for growing memory over time in repeated profiles
- **Garbage Collection**: Spikes indicate GC pressure

### Reading Tips
- Start from top: Find widest bars (bottlenecks)
- Drill down: Click bars to zoom into sub-trees
- Compare profiles: Before/after optimizations
- Focus on application code: Ignore system/library noise

## Benchmark Reproducibility Checklist

### Environment Consistency
- [ ] Same hardware specs (CPU, RAM, disk)
- [ ] Identical OS and kernel versions
- [ ] Fixed network conditions (latency, bandwidth)
- [ ] Consistent system load (no background processes)
- [ ] Same Node.js/Python/Go runtime versions

### Application Setup
- [ ] Clean database state (fresh data or known seed)
- [ ] Consistent cache state (warm/cold as needed)
- [ ] Same configuration values
- [ ] Identical build artifacts (no dev vs prod differences)

### Test Parameters
- [ ] Fixed random seeds for reproducible results
- [ ] Consistent user load patterns (not random)
- [ ] Same test duration and ramp-up periods
- [ ] Controlled concurrent users/threads

### Measurement Standards
- [ ] Multiple runs (3-5) with statistical analysis
- [ ] Discard first run (warm-up effects)
- [ ] Measure 95th/99th percentiles, not just averages
- [ ] Include error rates and timeouts

## Core Web Vitals Threshold Matrix

### Largest Contentful Paint (LCP)
| Rating | Threshold | Impact |
|--------|-----------|--------|
| Good | < 2.5s | Fast loading |
| Needs Improvement | 2.5s - 4.0s | Moderate delay |
| Poor | > 4.0s | Slow loading |

### First Input Delay (FID)
| Rating | Threshold | Impact |
|--------|-----------|--------|
| Good | < 100ms | Responsive |
| Needs Improvement | 100ms - 300ms | Noticeable delay |
| Poor | > 300ms | Sluggish |

### Cumulative Layout Shift (CLS)
| Rating | Threshold | Impact |
|--------|-----------|--------|
| Good | < 0.1 | Stable layout |
| Needs Improvement | 0.1 - 0.25 | Moderate shifts |
| Poor | > 0.25 | Jarring shifts |

### Additional Metrics
- **First Contentful Paint (FCP)**: < 1.8s (Good), 1.8s-3.0s (Needs Work), >3.0s (Poor)
- **Time to Interactive (TTI)**: < 3.8s (Good), 3.8s-7.3s (Needs Work), >7.3s (Poor)
- **Total Blocking Time (TBT)**: < 200ms (Good), 200ms-600ms (Needs Work), >600ms (Poor)

### Monitoring Thresholds
- **Regression Alert**: >10% degradation in any CWV metric
- **Budget Limits**: Set per-page budgets in lighthouse budget.json
- **Trend Analysis**: Track metrics over time, not single snapshots