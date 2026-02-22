# Deciphering Porphyrias and Associated Comorbidities Through Knowledge Graph Integration

Porphyria is a group of rare, mostly genetic disorders of heme biosynthesis that lead to the accumulation of porphyrin precursors and/or porphyrins, causing acute neurovisceral attacks, cutaneous photosensitivity, or both, depending on the enzyme defect and tissue of overproduction. These diseases carry a substantial burden of chronic comorbidities beyond classic attacks or cutaneous symptoms, yet information about comorbidities across porphyria subtypes is often discrete and fragmented.

Using modern computational approaches to map physiological/pathophysiological knowledge together with the biochemical characteristics of porphyria, this repository provides a consolidative knowledge graph of porphyria comorbidities. The Porphyria Knowledge Graph (PorphKG) highlights genetic, molecular, and protein-level factors that serve as key links between porphyria and other diseases (including metabolic disorders), and exposes shared clinical aspects and intersections across associated conditions. This comprehensive map is intended to support clinicians and researchers in understanding disease complexity, facilitating diagnosis, and informing treatment strategies.

---

## What’s in this repository

- `data/`  
  Contains artifacts for the project, including a Neo4j database dump (`neo4j_v4.dump`) that can be loaded directly to recreate the knowledge graph.

- `src/`  
  Scripts used for building, processing, and/or validating components of the knowledge graph.

- `analysis/`  
  Notebooks and analyses for exploration and validation.

---

## Quick start (recommended): Restore the graph in Neo4j from the dump

You can recreate the knowledge graph by loading the provided Neo4j dump file:

- Dump file: `neo4j_v4.dump`
- Intended Neo4j major version: **Neo4j 4.x** (because the dump is for v4)

> Note: Neo4j dumps are generally not forward-compatible across major versions.  
> If you are on Neo4j 5.x, you may need to use a Neo4j 4.x instance to load the dump first.

### Option A: Neo4j local install (Neo4j 4.x)

1. Stop Neo4j (the load is an offline operation).
2. Load the dump into a database (example database name: `neo4j`):

```bash
neo4j-admin load --from=neo4j_v4.dump --database=neo4j --force
```

3. Start Neo4j again.
4. Open Neo4j Browser and run quick checks (see below).



If you prefer not to load the dump (or want to validate/reproduce steps), use the contents of:

- `src/` for processing / reconstruction steps
- `analysis/` for notebooks and validation workflows


---

## License

MIT License. See `LICENSE`.

---

## Citation

If you use PorphKG in academic work, please cite the corresponding manuscript (if applicable) and reference this repository.
