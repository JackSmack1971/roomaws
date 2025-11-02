# .roo/rules-performance-profiler/50-examples.md
> Critical examples for complex performance profiling scenarios.

## Example 1: Memory Leak Detection in React App

### Scenario
A React application shows increasing memory usage over time, leading to performance degradation.

### Profiling Steps
1. **Initial Assessment**: Run Lighthouse memory audit
   ```bash
   lighthouse https://example.com --output=json --only-audits=total-byte-weight,unused-javascript,unused-css-rules
   ```

2. **Memory Profiling**: Use Chrome DevTools to capture heap snapshots
   - Navigate to application
   - Open DevTools > Memory tab
   - Take initial heap snapshot
   - Perform user interactions (navigate, create content)
   - Force garbage collection
   - Take second heap snapshot
   - Compare snapshots to identify retained objects

3. **Root Cause Analysis**: Identify common leak patterns
   - Event listeners not cleaned up
   - Timers/intervals not cleared
   - Component state holding references
   - Third-party library leaks

### Optimization Implementation
```javascript
// Before: Memory leak in useEffect
useEffect(() => {
  const handleResize = () => setWindowSize(getWindowSize());
  window.addEventListener('resize', handleResize);
  // Missing cleanup!
}, []);

// After: Proper cleanup
useEffect(() => {
  const handleResize = () => setWindowSize(getWindowSize());
  window.addEventListener('resize', handleResize);

  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

### Memory MCP Integration
- Persist `warning.capture` for detected leaks
- Link to `fix.apply` with cleanup implementation
- Reference documentation on React memory management

## Example 2: API Performance Regression Investigation

### Scenario
API response times increased by 200ms after recent deployment, affecting user experience.

### Profiling Steps
1. **Load Testing Baseline**: Establish performance baseline
   ```bash
   k6 run --vus 50 --duration 60s baseline-test.js
   ```

2. **Identify Bottleneck**: Profile different layers
   - Application server (Node.js pprof)
   - Database queries (slow query log)
   - External API calls (response time monitoring)
   - Network latency (traceroute, ping)

3. **Database Analysis**: Check for N+1 queries or missing indexes
   ```sql
   -- Enable PostgreSQL query analysis
   EXPLAIN ANALYZE SELECT * FROM users WHERE created_at > '2024-01-01';

   -- Check for missing indexes
   SELECT schemaname, tablename, attname, n_distinct, correlation
   FROM pg_stats
   WHERE schemaname = 'public' AND n_distinct > 1000
   ORDER BY n_distinct DESC;
   ```

### Optimization Implementation
```javascript
// Before: N+1 query problem
const users = await User.findAll();
const posts = await Promise.all(
  users.map(user => Post.findAll({ where: { userId: user.id } }))
);

// After: Single query with joins
const usersWithPosts = await User.findAll({
  include: [{
    model: Post,
    where: { createdAt: { [Op.gt]: '2024-01-01' } }
  }]
});
```

### Memory MCP Integration
- Record `command.exec` for profiling runs
- Persist `warning.capture` for regression detection
- Link `fix.apply` to optimization changes
- Reference database optimization best practices

## Example 3: Frontend Bundle Size Optimization

### Scenario
JavaScript bundle size grew to 5MB, causing slow initial page loads.

### Profiling Steps
1. **Bundle Analysis**: Use webpack-bundle-analyzer
   ```bash
   npm install --save-dev webpack-bundle-analyzer
   npx webpack-bundle-analyzer dist/static/js/*.js
   ```

2. **Dependency Audit**: Identify large/unused dependencies
   ```bash
   npx webpack-bundle-analyzer dist/static/js/*.js --mode static
   npm audit --audit-level moderate
   ```

3. **Code Splitting Analysis**: Check for optimization opportunities
   - Route-based splitting
   - Component lazy loading
   - Vendor library separation

### Optimization Implementation
```javascript
// Before: Large single bundle
import React from 'react';
import HeavyLibrary from 'heavy-library'; // 2MB
import Dashboard from './components/Dashboard'; // Complex component

// After: Code splitting with React.lazy
import React, { Suspense, lazy } from 'react';

const HeavyLibrary = lazy(() => import('heavy-library'));
const Dashboard = lazy(() => import('./components/Dashboard'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyLibrary />
      <Dashboard />
    </Suspense>
  );
}
```

### Memory MCP Integration
- Persist bundle size metrics in `command.exec`
- Record optimization recommendations
- Link to webpack documentation for code splitting

## Example 4: Database Connection Pool Exhaustion

### Scenario
Application experiencing intermittent slowdowns and connection timeouts under load.

### Profiling Steps
1. **Connection Monitoring**: Track database connections
   ```sql
   -- PostgreSQL connection monitoring
   SELECT count(*) as connection_count,
          state,
          wait_event_type,
          wait_event
   FROM pg_stat_activity
   GROUP BY state, wait_event_type, wait_event;
   ```

2. **Pool Configuration Analysis**: Check connection pool settings
   - Maximum connections
   - Idle timeout
   - Connection lifetime
   - Queue behavior

3. **Load Testing**: Simulate connection pool exhaustion
   ```javascript
   // k6 script to test connection limits
   export let options = {
     stages: [
       { duration: '1m', target: 100 },
       { duration: '2m', target: 100 },
     ],
   };

   export default function () {
     let response = http.get('https://api.example.com/db-heavy-endpoint');
     check(response, {
       'status is 200': (r) => r.status === 200,
       'response time < 1000ms': (r) => r.timings.duration < 1000,
     });
   }
   ```

### Optimization Implementation
```javascript
// Before: Default pool settings
const pool = new Pool({
  host: 'localhost',
  database: 'myapp',
  // Using defaults - may be too low for high traffic
});

// After: Optimized pool configuration
const pool = new Pool({
  host: 'localhost',
  database: 'myapp',
  max: 20,              // Increase max connections
  min: 5,               // Maintain minimum connections
  idleTimeoutMillis: 30000,  // Close idle connections after 30s
  connectionTimeoutMillis: 2000,  // Fail fast on connection issues
  allowExitOnIdle: true, // Allow pool to close when idle
});
```

### Memory MCP Integration
- Record connection pool metrics
- Persist timeout warnings
- Link to database connection pooling best practices

## Example 5: Image Optimization Pipeline

### Scenario
Web page loading slowly due to unoptimized images, high LCP scores.

### Profiling Steps
1. **Image Audit**: Analyze image sizes and formats
   ```bash
   # Use lighthouse for image audit
   lighthouse https://example.com --only-audits=unminified-css,unminified-javascript,unused-css-rules,unused-javascript,modern-image-formats
   ```

2. **Format Analysis**: Check for optimization opportunities
   - Convert to WebP/AVIF
   - Resize to appropriate dimensions
   - Compress without quality loss
   - Implement lazy loading

3. **CDN Configuration**: Verify image delivery optimization
   - Proper caching headers
   - CDN compression
   - Responsive images

### Optimization Implementation
```html
<!-- Before: Unoptimized images -->
<img src="/images/hero.jpg" alt="Hero image" style="width: 100%; height: auto;">

<!-- After: Optimized with modern formats and responsive loading -->
<picture>
  <source srcset="/images/hero.avif" type="image/avif">
  <source srcset="/images/hero.webp" type="image/webp">
  <img src="/images/hero.jpg"
       alt="Hero image"
       loading="lazy"
       decoding="async"
       style="width: 100%; height: auto;">
</picture>
```

```javascript
// Implement responsive images with srcset
import { useState, useEffect } from 'react';

function OptimizedImage({ src, alt, width, height }) {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    // Generate responsive image URLs
    const responsiveSrc = generateResponsiveSrc(src, width);
    setImageSrc(responsiveSrc);
  }, [src, width]);

  return (
    <img
      src={imageSrc}
      alt={alt}
      width={width}
      height={height}
      loading="lazy"
      decoding="async"
    />
  );
}
```

### Memory MCP Integration
- Record image size metrics from Lighthouse
- Persist optimization recommendations
- Link to WebP/AVIF migration guides
- Track LCP improvements over time