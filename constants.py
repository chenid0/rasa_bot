
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
db_virus_knowledgebase = '/home/mark/chatbot/db/Viruses.db'

action_tag = "action:"
query_tag = "query:"
tokenized_query_tag = "tokenized_query:"
svg_tag = "load svg"
csv_tag = "load csv"
histogram_tag ="histogram:"
scatter_tag ="scatterplot:"


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
    "LOPP": "LOGP_RDKIT",
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