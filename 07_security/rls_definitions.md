# CertiAce — Row-Level Security Definitions

## Semantic Model: CertiAce_Model

### RLS Roles

| Role Name | DAX Filter | Assigned Security Group |
|-----------|-----------|------------------------|
| `Role_RegMgr_NortheastUS` | `DimStores[Region] = "Northeast US"` | SG_RegMgr_Northeast_US |
| `Role_RegMgr_SoutheastUS` | `DimStores[Region] = "Southeast US"` | SG_RegMgr_Southeast_US |
| `Role_RegMgr_UKIreland` | `DimStores[Region] = "UK & Ireland"` | SG_RegMgr_UK_and_Ireland |
| `Role_Executives` | `TRUE()` (no filter) | SG_Executives |
| *(one role per region)* | | |

### Dynamic RLS Implementation

```dax
// Applied on DimStores table
// Reads region from security group membership via USERPRINCIPALNAME()

[Region] = 
VAR CurrentUser = USERPRINCIPALNAME()
VAR UserRegion = 
    LOOKUPVALUE(
        SecurityGroups[Region],
        SecurityGroups[UserEmail], CurrentUser,
        "NONE"
    )
RETURN
    IF(UserRegion = "ALL", TRUE(), DimStores[Region] = UserRegion)
```

## Object-Level Security (OLS)

Columns hidden from `SG_Analysts` role:
- `DimSuppliers[ContractValue]`
- `DimSuppliers[PricingCategory]`
- `FactDeliveries[UnitCost]`

Applied via Tabular Editor or XMLA endpoint TMSL script.
