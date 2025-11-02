# .roo/rules-integration-tester/40-common-mistakes.md
> What to avoid (converted from XML).

- Writing a whole test via a single write operation instead of incremental steps.
- Using BDD (`describe/it`) instead of TDD (`suite/test`).
- Missing `suiteSetup/suiteTeardown`; leaking files/tasks; interdependent tests.
- Assuming specific tools/messages; test **outcomes** instead.
- Wrong working directory; using `npm test` when script is `npm run test:run`.
- Over-short timeouts and fixed sleeps; no retry for flaky ops.
- Complex message parsing; not listening to terminal events.
- Hardcoded paths and invisible test data; uncleaned workspace artifacts.
