csv_str = """Short Name,Medium Name,Long Name,Category,Font Color,Order,Synonyms,Clustal Substitution,Comment,<BackgroundColor>Hydrophobicity-KD,<BackgroundColor>Hydrophobicity-HW,<BackgroundColor>ChemicalStructure,<BackgroundColor>ChouFasman,<Data>Kyte-Doolittle,<Data>Hopp-Woods,<BackgroundColor>Clustal,<Data>logp (crippen),<Data>mr,<Data>TPSArea,<Data>kappa1,<Data>kappa2,<Data>kappa3,<Data>SArea,<Data>MW,Smiles
G,Gly,Glycine,neutral,black,1,G;Gly;GLY;Glycine,G,,"RGB(116,116,139)","RGB(120,120,136)","RGB(0,255,255)",green,-0.4,0,yellow,-0.856,15.1184,43.09,0.43129,2.63,1.63,31.7466,57.0515,C(C(=O)[r])N[r]
A,Ala,Alanine,neutral,black,2,A;Ala;ALA;Alanine,A,,"RGB(179,179,77)","RGB(139,139,116)","RGB(0,255,255)",red,1.8,-0.5,white,-0.4675,19.7134,43.09,0.539918,1.90548,3.63,40.9215,71.0782,C[C@@H](C(=O)[r])N[r]
dA,dAla,D-Alanine,neutral,red,2.1,dAla;dA,A,,"RGB(179,179,77)","RGB(139,139,116)","RGB(0,255,255)",red,1.8,-0.5,white,-0.4675,19.7134,43.09,0.539918,1.90548,3.63,40.9215,71.0782,C[C@H](C(=O)[r])N[r]
V,Val,Valine,aliphatic,black,3,V;Val;VAL;Valine,V,,"RGB(9,9,247)","RGB(179,179,76)","RGB(0,255,255)",blue,4.2,-1.5,green,0.1686,28.8774,43.09,0.759881,2.74564,2.34048,59.2712,99.1316,[r]C([C@@H](N[r])C(C)C)=O
dV,dVal,D-Valine,aliphatic,red,3.1,dV;dVal,V,,"RGB(9,9,247)","RGB(179,179,76)","RGB(0,255,255)",blue,4.2,-1.5,green,0.1686,28.8774,43.09,0.759881,2.74564,2.34048,59.2712,99.1316,[r]C([C@H](N[r])C(C)C)=O"""


svg_str = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="305" height="352">
<g id="unmapped">
<g id="lines" style="stroke:rgb(138,0,0);stroke-width:2">
 <line x1="265" y1="350" x2="276" y2="330" />
 <line x1="276" y1="330" x2="266" y2="313" />
 <line x1="266" y1="298" x2="276" y2="280" />
 <line x1="276" y1="283" x2="290" y2="283" />
 <line x1="276" y1="278" x2="290" y2="278" />
 <line x1="276" y1="280" x2="265" y2="263" />
 <line x1="253" y1="256" x2="233" y2="256" />
 <line x1="265" y1="248" x2="275" y2="231" />
 <line x1="233" y1="256" x2="218" y2="231" />
 <line x1="218" y1="231" x2="228" y2="213" />
 <line x1="240" y1="206" x2="261" y2="206" />
 <line x1="228" y1="199" x2="217" y2="181" />
 <line x1="261" y1="206" x2="275" y2="231" />
 <line x1="220" y1="183" x2="227" y2="170" />
 <line x1="215" y1="180" x2="222" y2="168" />
 <line x1="217" y1="181" x2="189" y2="182" />
 <line x1="189" y1="182" x2="175" y2="207" />
 <line x1="189" y1="182" x2="178" y2="164" />
 <line x1="175" y1="207" x2="146" y2="207" />
 <line x1="146" y1="207" x2="132" y2="232" />
 <line x1="130" y1="233" x2="137" y2="246" />
 <line x1="134" y1="231" x2="141" y2="243" />
 <line x1="132" y1="232" x2="117" y2="232" />
 <line x1="166" y1="157" x2="145" y2="157" />
 <line x1="143" y1="156" x2="136" y2="169" />
 <line x1="148" y1="158" x2="141" y2="171" />
 <line x1="145" y1="157" x2="131" y2="132" />
 <line x1="131" y1="132" x2="145" y2="108" />
 <line x1="128" y1="128" x2="140" y2="107" />
 <line x1="131" y1="132" x2="111" y2="133" />
 <line x1="145" y1="108" x2="130" y2="83" />
 <line x1="130" y1="83" x2="102" y2="83" />
 <line x1="128" y1="88" x2="104" y2="88" />
 <line x1="130" y1="83" x2="140" y2="65" />
 <line x1="102" y1="83" x2="88" y2="108" />
 <line x1="88" y1="108" x2="98" y2="126" />
 <line x1="93" y1="107" x2="101" y2="122" />
 <line x1="88" y1="108" x2="59" y2="108" />
 <line x1="59" y1="108" x2="45" y2="133" />
 <line x1="54" y1="108" x2="41" y2="129" />
 <line x1="59" y1="108" x2="44" y2="84" />
 <line x1="45" y1="133" x2="16" y2="134" />
 <line x1="16" y1="134" x2="2" y2="109" />
 <line x1="19" y1="129" x2="7" y2="108" />
 <line x1="2" y1="109" x2="16" y2="84" />
 <line x1="16" y1="84" x2="44" y2="84" />
 <line x1="18" y1="89" x2="42" y2="89" />
 <line x1="153" y1="58" x2="173" y2="58" />
 <line x1="140" y1="51" x2="130" y2="33" />
 <line x1="173" y1="58" x2="187" y2="33" />
 <line x1="187" y1="33" x2="177" y2="15" />
 <line x1="164" y1="8" x2="144" y2="8" />
 <line x1="144" y1="8" x2="130" y2="33" />
</g>
<g id="letters" fill="rgb(138,0,0)" text-anchor="start" font-family="Arial" text-rendering="geometricPrecision">
<text x="256" y="311" font-size="14">O</text>
<text x="293" y="286" font-size="14">O</text>
<text x="255" y="262" font-size="14">N</text>
<text x="226" y="212" font-size="14">N</text>
<text x="223" y="167" font-size="14">O</text>
<text x="138" y="258" font-size="14">O</text>
<text x="103" y="238" font-size="14">O</text>
<text x="94" y="238" font-size="14">H</text>
<text x="168" y="163" font-size="14">N</text>
<text x="168" y="150" font-size="14">H</text>
<text x="128" y="183" font-size="14">O</text>
<text x="96" y="139" font-size="14">N</text>
<text x="139" y="64" font-size="14">N</text>
<text x="167" y="14" font-size="14">O</text>
</g>
</g>
<g id="mapped">
<g id="lines" style="stroke:rgb(0,0,138);stroke-width:2">
</g>
<g id="letters" fill="rgb(0,0,138)" text-anchor="start" font-family="Arial" text-rendering="geometricPrecision">
</g>
</g>
</svg>"""

db_path_name = "/home/mark/chatbot/db/Molecules.db"
db_virus_knowledgebase = "/home/mark/chatbot/db/Viruses.db"

action_tag = "action:"
query_tag = "query:"
tokenized_query_tag = "tokenized_query:"
svg_tag = "load svg"
csv_tag = "load csv"
histogram_tag = "histogram:"
scatter_tag = "scatterplot:"


# Get column names from "MOLPROPS" and "MOLDATA"
#  regex out (case insensitive compare) : could match multiple
#       'logp'-> 'logP_rdkit'
#       'HBA', 'Hydrogen Bond Acceptor', 'H-Bond Acceptor', HBond Acceptor', 'Acceptors'->'HBA'
#       'TPSA', 'PSA', 'Polar Surface'-> 'TPSA_rdkit'
#       'HBD', 'Hydrogen Bond Donar', 'HBond Donar', 'H-Bond Donar', 'Donar', 'Doner' -> 'HBD'
#       'Surface Area', 'SA' -> 'SArea_rdkit'
#       'fCSP3', 'fracCsp3','Fraction Csp3', 'number csp3 carbons' ->fracCSP3_rdkit
#       'Number of Spiroatoms', 'Number of spiro-atoms', 'spiroatoms', 'spiro-atoms', 'Spiro-atom-count' -> 'SpiroAtoms_rdkit'
#       'Number of BridgeHeadAtoms', Bridgehead count', 'bridgehead atoms' -> 'BridgeHeadAtoms_rdkit'
#       'RotBond', 'RotatableBond', 'Rotatable' -> 'Rotatable_bonds'
#       'MW','Molecular Weight', 'MolWeight', 'mass' -> 'MW'
#
#       ignore others for now

keyword_replacements = {
    "LOGP": "LOGP_RDKIT",
    "HBA": "HBA",
    "HYDROGEN BOND ACCEPTOR": "HBA",
    "H-BOND ACCEPTOR": "HBA",
    "HBOND ACCEPTOR": "HBA",
    "ACCEPTORS": "HBA",
    "TPSA": "TPSA_RDKIT",
    "PSA": "TPSA_RDKIT",
    "POLAR SURFACE": "TPSA_RDKIT",
    "HBD": "HBD",
    "HYDROGEN BOND DONAR": "HBD",
    "HBOND DONAR": "HBD",
    "H-BOND DONAR": "HBD",
    "DONAR": "HBD",
    "DONER": "HBD",
    "SURFACE AREA": "SAREA_RDKIT",
    "SAREA": "SAREA_RDKIT",
    "SA": "SAREA_RDKIT",
    "FCSP3": "FRACCSP3_RDKIT",
    "FRACCSP3": "FRACCSP3_RDKIT",
    "FRACTION CSP3": "FRACCSP3_RDKIT",
    "NUMBER CSP3 CARBONS": "FRACCSP3_RDKIT",
    "NUMBER OF SPIROATOMS": "SPIROATOMS_RDKIT",
    "NUMBER OF SPIRO-ATOMS": "SPIROATOMS_RDKIT",
    "SPIROATOMS": "SPIROATOMS_RDKIT",
    "SPIROATOMS": "SPIROATOMS_RDKIT",
    "SPIRO-ATOMS": "SPIROATOMS_RDKIT",
    "SPIRO-ATOM-COUNT": "SPIROATOMS_RDKIT",
    "BRIDGEHEADATOMS": "BRIDGEHEADATOMS_RDKIT",
    "NUMBER OF BRIDGEHEADATOMS": "BRIDGEHEADATOMS_RDKIT",
    "BRIDGEHEAD COUNT": "BRIDGEHEADATOMS_RDKIT",
    "BRIDGEHEAD ATOMS": "BRIDGEHEADATOMS_RDKIT",
    "ROTBOND": "ROTATABLE_BONDS",
    "ROTATABLEBOND": "ROTATABLE_BONDS",
    "ROTATABLE": "ROTATABLE_BONDS",
    "MASS": "MW",
    "MOLECULAR WEIGHT": "MW",
    "MOLWEIGHT": "MW",
    "MW": "MW",
}


"""
  utter_nlu_fallback:
  - text: "nlu_fallback"

  utter_test_fcn:
  - text: "test_fcn"

  utter_help:
  - text: "help"

  utter_help2:
  - text: "help2"

  utter_help3:
  - text: "help3"

  utter_help4:
  - text: "help4"

  utter_help5:
  - text: "help5"

  utter_help_properties:
  - text: "help_properties"

  utter_help_recommend_rgroups:
  - text: "help_recommend_rgroups"

  utter_who_r_u:
  - text: "who_r_u"

  utter_who_creator:
  - text: "who_creator"

  utter_what_language:
  - text: "what_language"

  utter_tell_tech_details:
  - text: "tell_tech_details"

  utter_load_sdf_file:
  - text: "load_sdf_file"

  utter_load_cddvault:
  - text: "load_cddvault"

  utter_load_mols_postgres:
  - text: "load_mols_postgres"

  utter_load_mols_sqlite:
  - text: "load_mols_sqlite"

  utter_load_smiles:
  - text: "load_smiles"

  utter_load_mols:
  - text: "load_mols"

  utter_load_chembl_by_id:
  - text: "load_chembl_by_id"

  utter_load_api:
  - text: "load_api"

  utter_add_scaffold:
  - text: "add_scaffold"

  utter_load_scaffold:
  - text: "load_scaffold"

  utter_draw_scaffold:
  - text: "draw_scaffold"

  utter_paste_scaffold:
  - text: "paste_scaffold"

  utter_append_csv_columns:
  - text: "append_csv_columns"

  utter_molecule_count:
  - text: "molecule_count"

  utter_list_properties:
  - text: "list_properties"

  utter_list_data:
  - text: "list_data"

  utter_data_minimum:
  - text: "data_minimum"

  utter_data_maximum:
  - text: "data_maximum"

  utter_select_model_column:
  - text: "select_model_column"

  utter_calc_properties:
  - text: "calc_properties"

  utter_calc_explicit_properties:
  - text: "calc_explicit_properties"

  utter_show_scaffold:
  - text: "show_scaffold"

  utter_show_most_active:
  - text: "show_most_active"

  utter_show_least_active:
  - text: "show_least_active"

  utter_reload_data:
  - text: "reload_data"

  utter_bin_data:
  - text: "bin_data"

  utter_scatter_xy:
  - text: "scatter_xy"

  utter_heatmap_column:
  - text: "heatmap_column"

  utter_clear_data:
  - text: "clear_data"

  utter_test_svg:
  - text: "test_svg"

  utter_test_CSV:
  - text: "test_CSV"

  utter_perform_r_analysis:
  - text: "perform_r_analysis"

  utter_show_least_potent_rgroup:
  - text: "show_least_potent_rgroup"

  utter_show_most_potent_rgroup:
  - text: "show_most_potent_rgroup"

  utter_recommend_rgroups:
  - text: "recommend_rgroups"

  utter_recommend_biosteres:
  - text: "recommend_biosteres"

  utter_sar_by_catalog:
  - text: "sar_by_catalog"

  utter_search_sure_chembl:
  - text: "search_sure_chembl"

  utter_search_chemb_mols:
  - text: "search_chemb_mols"

  utter_find_scaffolds:
  - text: "find_scaffolds"
"""
actions = {
    "nlu_fallback": "did not understand",
    "test_fcn": "test_fcn",
    "help": "This is the help",
    "help2": "utter_help2",
    "help3": "utter_help3",
    "help4": "utter_help4",
    "help5": "utter_help5",
    "help_properties": "utter_help_properties",
    "help_recommend_rgroups": "utter_help_recommend_rgroups",
    "who_r_u": "utter_who_r_u",
    "who_creator": "utter_who_creator",
    "what_language": "utter_what_language",
    "tell_tech_details": "utter_tell_tech_details",
    "load_sdf_file": "utter_load_sdf_file",
    "load_cddvault": "utter_load_cddvault",
    "load_mols_postgres": "utter_load_mols_postgres",
    "load_mols_sqlite": "utter_load_mols_sqlite",
    "load_smiles": "utter_load_smiles",
    "load_mols": "utter_load_mols",
    "load_chembl_by_id": "utter_load_chembl_by_id",
    "load_api": "utter_load_api",
    "add_scaffold": "utter_add_scaffold",
    "load_scaffold": "utter_load_scaffold",
    "draw_scaffold": "utter_draw_scaffold",
    "paste_scaffold": "utter_paste_scaffold",
    "append_csv_columns": "utter_append_csv_columns",
    "molecule_count": "utter_molecule_count",
    "list_properties": "utter_list_properties",
    "list_data": "utter_list_data",
    "data_minimum": f"{tokenized_query_tag} SELECT MIN($TOKEN$) FROM MOLPROPS;",
    "data_maximum": f"{tokenized_query_tag} SELECT MAX($TOKEN$) FROM MOLPROPS;",
    "select_model_column": "utter_select_model_column",
    "calc_properties": "utter_calc_properties",
    "calc_explicit_properties": "utter_calc_explicit_properties",
    "show_scaffold": "utter_show_scaffold",
    "show_most_active": "utter_show_most_active",
    "show_least_active": "utter_show_least_active",
    "reload_data": "utter_reload_data",
    "bin_data": f"{histogram_tag} select distinct cast($TOKEN$ / 1 as int)  as Bin, count(ID) as Frequency from MOLPROPS GROUP by Bin;",
    "scatter_xy": f"{scatter_tag} select logp_rdkit, sarea_rdkit from MOLPROPS limit 10000;",
    "heatmap_column": "utter_heatmap_column",
    "clear_data": "utter_clear_data",
    "test_svg": "action: action_test_svg",
    "test_CSV": "action: action_test_CSV",
    "perform_r_analysis": "utter_perform_r_analysis",
    "show_least_potent_rgroup": "utter_show_least_potent_rgroup",
    "show_most_potent_rgroup": "utter_show_most_potent_rgroup",
    "recommend_rgroups": "utter_recommend_rgroups",
    "recommend_biosteres": "utter_recommend_biosteres",
    "sar_by_catalog": "utter_sar_by_catalog",
    "search_sure_chembl": "utter_search_sure_chembl",
    "search_chemb_mols": "utter_search_chemb_mols",
    "find_scaffolds": "find scaffolds",
}
