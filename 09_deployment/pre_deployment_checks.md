# CertiAce — Pre-Deployment Checklist (Dev → Test → Prod)

## Before Promoting to Test

- [ ] All notebooks execute without errors in ws_retail_dev
- [ ] Bronze row counts match expected source volumes (± 0.1%)
- [ ] Silver deduplication log shows expected duplicate removal
- [ ] Gold star schema passes referential integrity checks
- [ ] DAX measures return expected values against sample data
- [ ] RLS filters verified for each regional role
- [ ] OLS confirmed — SG_Analysts cannot see pricing columns
- [ ] Sensitivity labels applied to all Gold datasets
- [ ] Datasets endorsed as "Certified" in Gold workspace
- [ ] Git commit pushed to feature branch with descriptive message

## Before Promoting to Prod

- [ ] All Test checks passed
- [ ] Impact analysis run — no downstream reports broken
- [ ] Incremental refresh policy configured on FactSales
- [ ] Direct Lake mode confirmed on large fact tables
- [ ] Deployment pipeline approval received from Fabric Admin
- [ ] Rollback plan documented
- [ ] Business sign-off obtained from analytics lead

## Impact Analysis Steps

1. Open semantic model in ws_retail_test
2. Navigate to View → Lineage view
3. Identify all dependent reports and dashboards
4. For schema changes: run `GET /datasets/{id}/datasources` via REST API
5. Notify report owners of changes at least 48 hours before prod deployment
