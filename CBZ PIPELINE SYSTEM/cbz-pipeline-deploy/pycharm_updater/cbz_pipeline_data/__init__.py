"""
CBZ Bank Disbursement Pipeline — Test Data Package
===================================================
Provides fully enriched test data for all pipeline sections.

Usage:
    from cbz_pipeline_data import DB
    from cbz_pipeline_data import users, pipeline, disbursements  # etc.

Sections:
    DB.users            - 20 users across all roles
    DB.its              - 7 Indicative Term Sheet entries
    DB.pipeline         - 35 pipeline entries (CCC / EXCO / Board / Near / Ready)
    DB.tobacco          - 7 tobacco merchants
    DB.nonfunded        - 7 non-funded facilities
    DB.ntb              - 8 New-to-Bank clients
    DB.loc              - 5 Lines of Credit
    DB.disbursements    - 30 disbursements (Jan–Jun 2025)
    DB.tobacco_repayments   - Tobacco repayment schedule dict
    DB.tobacco_drawdowns    - Tobacco drawdown schedule dict
    DB.tobacco_disbursements - Tobacco disbursement list
    DB.nf_disbursements - Non-funded disbursements
    DB.finance          - 7 division-wide finance records
    DB.finance_by_role  - Finance records keyed by head username
    DB.audit            - 20 audit log entries
    DB.targets          - Monthly & annual disbursement targets
"""

from .data import DB
from .data import (
    users,
    its,
    pipeline,
    tobacco,
    nonfunded,
    ntb,
    loc,
    disbursements,
    tobacco_repayments,
    tobacco_drawdowns,
    tobacco_disbursements,
    nf_disbursements,
    finance,
    finance_by_role,
    audit,
    targets,
)

__all__ = [
    "DB",
    "users",
    "its",
    "pipeline",
    "tobacco",
    "nonfunded",
    "ntb",
    "loc",
    "disbursements",
    "tobacco_repayments",
    "tobacco_drawdowns",
    "tobacco_disbursements",
    "nf_disbursements",
    "finance",
    "finance_by_role",
    "audit",
    "targets",
]
