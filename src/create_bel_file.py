import re
import argparse
import pandas as pd

from pathlib import Path


BEL_HEADER = """##################################################################################
# Document Properties
##################################################################################
SET DOCUMENT Authors = "xxx"
SET DOCUMENT ContactInfo = "Dhruv Chetanbhai Rathod"
SET DOCUMENT Copyright = "Copyright © 2023 Fraunhofer Institute SCAI, All rights reserved."
SET DOCUMENT Description = "HemeKG"

SET DOCUMENT Licenses = "MIT License"
SET DOCUMENT Name = "{}"
SET DOCUMENT Version = "1.0.0"

###################################################################################
# Definitions Section

DEFINE NAMESPACE CHEBI AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/chebi/chebi-20230925.belns"
DEFINE NAMESPACE DO AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/disease-ontology/disease-ontology-20200407.belns"
DEFINE NAMESPACE MESHD AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/mesh-diseases/mesh-diseases-20190128.belns"
DEFINE NAMESPACE HGNC AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/hgnc/hgnc-20230925.belns"
DEFINE NAMESPACE GO AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/go/go-20180109.belns"
DEFINE NAMESPACE GOBP AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/go-biological-process/go-biological-process-20190128.belns"
DEFINE NAMESPACE MESHPP AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/mesh-processes/mesh-processes-20190128.belns"
DEFINE NAMESPACE MESH AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/mesh/mesh-names-20181007.belns"
DEFINE NAMESPACE MGI AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/mgi-mouse-genes/mgi-20230925.belns"
DEFINE NAMESPACE RGD AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/rgd-rat-genes/rgd-20230925.belns"
DEFINE NAMESPACE INTERPRO AS URL "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/interpro/interpro-20170731.belns"
DEFINE NAMESPACE MIRBASE AS URL "https://raw.githubusercontent.com/pharmacome/terminology/c328ad964c08967a0417a887510b97b965a62fa5/external/mirbase-names.belns"
DEFINE NAMESPACE CONSO AS URL "https://raw.githubusercontent.com/pharmacome/conso/master/export/conso.belns"
DEFINE NAMESPACE FPLX AS URL "https://raw.githubusercontent.com/sorgerlab/famplex/e8ae9926ff95266032cb74f77973c84939bffbeb/export/famplex.belns"
DEFINE NAMESPACE PFAM AS URL "https://raw.githubusercontent.com/pharmacome/terminology/8ccfed235e418e4c8aa576f9a5ef0f838e794c7f/external/pfam-names.belns"
DEFINE NAMESPACE HGNCGENEFAMILY AS URL "https://raw.githubusercontent.com/pharmacome/terminology/73688d6dc24e309fca59a1340dc9ee971e9f3baa/external/hgnc.genefamily-names.belns"
DEFINE NAMESPACE PUBCHEM AS PATTERN "^\d+$"
DEFINE NAMESPACE CL AS PATTERN "^\d+$"

DEFINE ANNOTATION Score AS PATTERN "0.\d+"
DEFINE ANNOTATION DataSource AS LIST {{"manual-curation"}}

# Namespaces defined with regular expressions
# -------------------------------------------

DEFINE NAMESPACE PKG        AS PATTERN ".*"

##################################################################################

# Statements Section


"""

rel_map = {
    "positive_correlation": "pos",
    "is_a": "isA",
    "correlation": "association",
}

def create_bel_body(df_fp: Path) -> str:
    """Create the body of the BEL file by parsing the text-2-graph excel file."""
    # Compile body of BEL file
    bel_body = ""
    id_reg = r"\w+ ! "
    t2g_df = pd.read_excel(df_fp, names=["Subject", "Relation", 
                                     "Object", "Score", 
                                     "EvidenceSentence", "Journal", "PubMedID"])

    t2g_df = t2g_df.astype(str)
    
    for row in t2g_df.itertuples(index=False):
        #print(row)
        subj, rel, obj, score, evid, journal, pmid = row
        new_entry = ""

        # Fix IDs
        subj = re.sub(id_reg, "", subj)
        print("obj is", subj)
        obj = re.sub(id_reg, "", obj)

        # Fix GO namespaces
        subj = subj.replace("(go:", "(GO:")
        obj = obj.replace("(go:", "(GO:")

        # Fix '"' in evidence line
        evid = evid.replace('\"', '\\"')

        if rel in rel_map:
            rel = rel_map[rel]

        if pmid == pmid:  # Check not NaN
            new_entry += f'SET Citation = {{"PubMed", "{pmid}"}}\n'

        new_entry += f"""SET DataSource = "manual-curation"
SET Support = "{evid}"
{subj} {rel} {obj}\n\n"""

        bel_body += new_entry
        # new_row = {"subject": subj, "relation": rel, "object": obj, "pmid": pmid, "evidence": evid}
       
    return bel_body


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    import os
    cwd = os.getcwd()
    parser.add_argument("text_2_graph_file_path", help="file path to text to graph excel file")
    parser.add_argument("bel_file_path", help="file path which to write the BEL file to")
    text_2_graph_file_path = "curated_bel_files.xlsx"
    bel_file_path = "curated_bel_file.bel"
    args = parser.parse_args()

    t2g_fp = Path(args.text_2_graph_file_path)
    bel_fp = Path(args.bel_file_path)

    bel_file_body = create_bel_body(df_fp=t2g_fp)
    bel_content = BEL_HEADER.format("manual-curation") + bel_file_body

    with open(bel_fp, "w", encoding="utf-8") as bel_file:
        bel_file.write(bel_content)
