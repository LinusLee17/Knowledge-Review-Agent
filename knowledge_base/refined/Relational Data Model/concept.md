---
concept_name: "Relational Data Model"
canonical_key: "relational data model"
concept_type: "model"
domain: "Data Science"
topic: "Data Management"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 2
last_updated_timestamp: "2026-07-14T17:35:38.329961+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Relational Data Model

## Classification
- domain: Data Science
- topic: Data Management
- type: model
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: relational database, relational model

## Contributing Courses
- BT2102

## Definition
The relational data model represents data as relations, commonly implemented as tables, with rows for records and columns for attributes. Keys and integrity rules describe how tables relate and which values are valid.

## Why it Matters
Relational Data Model provides a formal way to support Analytics, Reporting, Transactional Systems under stated assumptions.

## Core Intuition
Think of tables joined by keys, with each table representing one kind of thing or relationship.

## How it Works
1. Represent entities and relationships as tables.
2. Use keys to identify rows and connect related tables.
3. Apply integrity constraints and query the relations with relational operations or SQL.

## Key Components
- Relations or tables
- Rows and attributes
- Primary and foreign keys
- Integrity constraints
- Relational operations

## Common Mistakes
- Using duplicated fields instead of representing relationships with keys.
- Confusing a primary key with a foreign key.
- Ignoring nullability and integrity constraints when interpreting joins.

## Real-world Applications
- Analytics
- Reporting
- Transactional Systems

## Interview Questions
- What problem does Relational Data Model solve, and what is its output?
- Explain Relational Data Model using one concrete input-to-decision example.
- What assumptions must hold before using Relational Data Model?
- Which trade-off decides whether to use Relational Data Model instead of an alternative?
- How does Relational Data Model compare with Database Normalization?

## Related Concepts
- Database Normalization
- Functional Dependency
- SQL

## Connections
- Depends on: Data Model and Database
- Used in: Transactional Systems, Reporting, and Analytics
- Related: SQL, Functional Dependency, and Database Normalization
- Broader topic: Data Management

## Prerequisites
- Data Model
- Database

## Slide-derived Evidence
- BT2102 | p7 | [BT2102-01-DatabaseAndDataModel.pdf](../data/raw/BT2102/BT2102-01-DatabaseAndDataModel.pdf#page=7) — Relational Data Model THE RELATIONAL DATA MODEL IS BASED ON THE CONCEPT OF MATHEMATICAL RELATIONS AND WHERE DATA AND ◦ Relational Data Model
- BT2102 | p2 | [BT2102-02-TheRelationalDataModel.pdf](../data/raw/BT2102/BT2102-02-TheRelationalDataModel.pdf#page=2) — Relational Data Model THE RELATIONAL DATA MODEL IS BASED ON THE CONCEPT OF MATHEMATICAL RELATIONS AND WHERE DATA AND Relational Data Model branchNo street City postCode Branch B005 22 Deer Rd London SW1 4EH B007 16 Argyll St Aberdeen AB2 3SU B003 163 Main St Glasgow G11 9QX B004 32 Manse Rd Bristol BS99 1NZ B002 56 Clover Dr London NW106EU staffNo fName lName position sex DOB salary branchNo Staff SL21 John White Manager M 1-Oct-45 30000 B005 SG37 Ann Beech Assistant F 10-Nov-60 12000 B003 SG14 David Ford Supervisor M 24-Mar-58 18000 B003 SA9 Mary Howe Assistant F 19-Feb-70 9000 B007 SG5 Susan Brand Manager F 3-Jun-40 24000 B003 SL41 Julie Lee Assistant F 13-Jun-65 9000 B005 THE RELATIONAL DATA MODEL IS BASED ON THE CONCEPT OF MATHEMATICAL RELATIONS AND WHERE DATA AND RELATIONSHIPS ARE REPRESENTED AS TABLES, EACH OF WHICH HAS A NUMBER OF COLUMNS WITH A UNIQUE NAME.

## Provenance
- BT2102 | p7 | [BT2102-01-DatabaseAndDataModel.pdf](../data/raw/BT2102/BT2102-01-DatabaseAndDataModel.pdf#page=7) — Relational Data Model THE RELATIONAL DATA MODEL IS BASED ON THE CONCEPT OF MATHEMATICAL RELATIONS AND WHERE DATA AND ◦ Relational Data Model
- BT2102 | p2 | [BT2102-02-TheRelationalDataModel.pdf](../data/raw/BT2102/BT2102-02-TheRelationalDataModel.pdf#page=2) — Relational Data Model THE RELATIONAL DATA MODEL IS BASED ON THE CONCEPT OF MATHEMATICAL RELATIONS AND WHERE DATA AND Relational Data Model branchNo street City postCode Branch B005 22 Deer Rd London SW1 4EH B007 16 Argyll St Aberdeen AB2 3SU B003 163 Main St Glasgow G11 9QX B004 32 Manse Rd Bristol BS99 1NZ B002 56 Clover Dr London NW106EU staffNo fName lName position sex DOB salary branchNo Staff SL21 John White Manager M 1-Oct-45 30000 B005 SG37 Ann Beech Assistant F 10-Nov-60 12000 B003 SG14 David Ford Supervisor M 24-Mar-58 18000 B003 SA9 Mary Howe Assistant F 19-Feb-70 9000 B007 SG5 Susan Brand Manager F 3-Jun-40 24000 B003 SL41 Julie Lee Assistant F 13-Jun-65 9000 B005 THE RELATIONAL DATA MODEL IS BASED ON THE CONCEPT OF MATHEMATICAL RELATIONS AND WHERE DATA AND RELATIONSHIPS ARE REPRESENTED AS TABLES, EACH OF WHICH HAS A NUMBER OF COLUMNS WITH A UNIQUE NAME.

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.853
- evidence strength: 0.84
- definition quality: 0.78
- interview relevance: 0.98
- version: 2
- last updated: 2026-07-14T17:35:38.329961+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- no meaningful equation or formal relationship extracted
- assumptions not extracted
- trade-offs or limitations not extracted
