# Minimum Test Contract

Implement at least the following checks:

1. production feature set excludes `duration`;
2. production feature set excludes current-campaign-only variables;
3. train timestamps precede test timestamps;
4. preprocessing is fitted only on training data;
5. gains table reconciles with saved test predictions;
6. top-k sets are nested;
7. lift equals top-k conversion divided by population conversion;
8. incremental conversions equal observed minus random expectation;
9. target mapping is deterministic;
10. all configured artifacts are generated.
