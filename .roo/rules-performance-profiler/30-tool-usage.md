# .roo/rules-performance-profiler/30-tool-usage.md
> Detailed tool usage patterns and examples for performance profiling tools.

## Tool Usage Patterns

### Lighthouse Integration
- **Primary Use**: Web performance audits, Core Web Vitals measurement
- **When to Use**: Initial performance assessment, regression detection, optimization validation
- **Integration Pattern**:
  1. Run lighthouse with JSON output
  2. Parse results for CWV metrics
  3. Compare against thresholds
  4. Generate optimization recommendations

### k6 Load Testing
- **Primary Use**: API/backend load testing, stress testing
- **When to Use**: Capacity planning, performance regression testing, scalability validation
- **Integration Pattern**:
  1. Define test scenarios in k6 script
  2. Run with controlled load parameters
  3. Analyze throughput, latency, error rates
  4. Identify performance bottlenecks

### Chrome DevTools Protocol
- **Primary Use**: Real-time performance profiling, memory analysis
- **When to Use**: Debugging performance issues, memory leak detection
- **Integration Pattern**:
  1. Use puppeteer or similar for automation
  2. Collect performance traces
  3. Analyze flamegraphs and timelines
  4. Identify optimization opportunities

### Application-Specific Profilers
- **Node.js**: Use `--inspect` flag with Chrome DevTools or clinic.js
- **Python**: Use cProfile, line_profiler, or py-spy
- **Go**: Use pprof with net/http/pprof
- **Java**: Use VisualVM or async-profiler

## Detailed Tool Usage Examples

### Lighthouse CI Integration
```bash
# Install lighthouse globally
npm install -g lighthouse

# Run performance audit
lighthouse https://example.com \
  --output=json \
  --output-path=./lighthouse-results.json \
  --preset=desktop \
  --only-categories=performance \
  --chrome-flags="--headless --disable-gpu --no-sandbox"

# Parse results in script
node -e "
const results = require('./lighthouse-results.json');
const score = results.categories.performance.score * 100;
const lcp = results.audits['largest-contentful-paint'].numericValue;
console.log(\`Performance Score: \${score}%, LCP: \${lcp}ms\`);
"
```

### k6 Script for API Load Testing
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.1'],    // Error rate should be below 10%
  },
};

export default function () {
  let response = http.get('https://api.example.com/users');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### Memory Profiling with Chrome DevTools
```javascript
const puppeteer = require('puppeteer');

async function profileMemory() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Start memory profiling
  await page.tracing.start({ path: 'trace.json', categories: ['memory'] });

  // Navigate and interact
  await page.goto('https://example.com');
  await page.waitForTimeout(5000); // Simulate user interaction

  // Stop tracing
  await page.tracing.stop();

  // Take heap snapshot
  const heapSnapshot = await page.evaluate(() => {
    return new Promise((resolve) => {
      // Trigger garbage collection
      if (window.gc) window.gc();

      // Get memory info
      const memInfo = performance.memory;
      resolve({
        used: memInfo.usedJSHeapSize,
        total: memInfo.totalJSHeapSize,
        limit: memInfo.jsHeapSizeLimit
      });
    });
  });

  console.log('Memory Usage:', heapSnapshot);
  await browser.close();
}

profileMemory();
```

### Flamegraph Generation (Node.js)
```bash
# Install clinic
npm install -g clinic

# Profile application
clinic doctor -- node app.js

# Or use 0x for flamegraphs
npm install -g 0x
0x app.js

# Generate flamegraph from perf data
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
```

### Database Query Profiling
```sql
-- PostgreSQL: Enable query logging
ALTER DATABASE mydb SET log_statement = 'all';
ALTER DATABASE mydb SET log_duration = on;

-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1; -- Log queries > 1 second

-- MongoDB: Enable profiling
db.setProfilingLevel(2, { slowms: 100 }); -- Profile all queries > 100ms
db.system.profile.find().sort({ ts: -1 }).limit(5);
```

## Tool Selection Guidelines

### For Web Applications
1. **Lighthouse**: Always first - comprehensive audit
2. **WebPageTest**: Compare different environments
3. **Chrome DevTools**: Deep dive into specific issues

### For APIs
1. **k6/wrk/autocannon**: Load testing
2. **New Relic/AppDynamics**: Production monitoring
3. **APM tools**: Application performance monitoring

### For Backend Services
1. **Language-specific profilers**: CPU/memory analysis
2. **APM tools**: Distributed tracing
3. **Database profilers**: Query optimization

### For Mobile Apps
1. **Android Profiler**: Memory/CPU/network
2. **Xcode Instruments**: iOS performance
3. **Flipper**: React Native debugging

## Automation Patterns

### CI/CD Integration
- Run Lighthouse on every PR
- Automated regression detection
- Performance budgets enforcement
- Historical trend tracking

### Monitoring Setup
- Real user monitoring (RUM)
- Synthetic monitoring
- Alert thresholds
- Dashboard creation

### Benchmark Automation
- Consistent environment setup
- Automated result collection
- Statistical analysis
- Report generation