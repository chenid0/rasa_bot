# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import sqlite3
import re
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


db_path_name = '/home/mark/chatbot/db/Molecules.db';
db_virus_knowledgebase = '/home/mark/chatbot/db/Viruses.db';

# SELECT MOLID FROM MOLECULES EXCEPT SELECT MOLID FROM MARKING WHERE MARK = "good"

# action: action_help
# action: action_load_mols_sdf
# action: action_load_mols_cddvault
# action: action_load_mols_postgres
# action: action_set_model_column
# action: action_heat_map_column
# action: action_count_mols
# action: action_r_analysis
# action: action_reload_data
# action: action_show_scaffold
# action: action_most_active
# action: action_least_active
# action: action_load_scaffold
# action: action_draw_scaffold
# action: action_paste_scaffold
# action: action_help_properties
# action: action_calc_properties
# action: action_explicit_property

# action: action_least_potent_rgroup
# action: action_most_potent_rgroup
# action: action_recommend_rgroups
# action: action_recommend_bioisosteres
# action: action_help_recommend_rgroups




# globals: persistent variables : how do we remember these? db? per user per project
g_current_scaffold = "";            # table:rowid [SCAFFOLDS:SCAFID]
g_calc_properties = set();          # [logP, MW, rotB, TPSA]
g_display_cols_in_order = [];       # col names to display table:col [MOLECULES:MOLID, MOLDATA:EXTERNALKEY, MOLDATA:IC50, MOLDATA:Ki, MOLPROPS:logP, MOLPROPS:MW ]
g_rename_cols = [];                 # rename ori name:new name  [measured Ki(n) for xyza: Ki(nM), LOGP_RDKIT, logP]
g_heatmap_cols = [];                # heatmap to col name:range:color/range:color/range:color [Ki(n):0->1000]
g_activity_col = "";                # activity or model column 

g_history_calls = [];               #list in order of calls e.g. "action_load_mols_sdf: filename", "add_scaffold: mol", ...



#_______________________________________________________________________________________________________________
class LoadMolsFromSDF(Action):
    def name(self) -> Text:
        return "action_load_mols_sdf"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<open browserui> running: action_load_mols_sdf");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class LoadMolsCDD(Action):
    def name(self) -> Text:
        return "action_load_mols_cddvault"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<open cddvaultui> running: action_load_mols_cddvault");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class LoadMolsPostgres(Action):
    def name(self) -> Text:
        return "action_load_mols_postgres"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<open postgresui> running: action_load_mols_postgres");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class SetActivityColumn(Action):
    def name(self) -> Text:
        return "action_set_model_column"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<column selectorui>running: action_set_model_column");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class HeatMapColumn(Action):
    def name(self) -> Text:
        return "action_heat_map_column"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_heat_map_column");

        return []
#__________________________________________________________________________________________________


#__________________________________________________________________________________________________
# Count all molecules in MOLECULES table (unique set)____________________________________________________________
# trigger this with count molecules
# !!Note this one fails .. seems simple enough
class CountMols(Action): 
    
    def name(self) -> Text:
        return "action_count_mols";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sql = 'SELECT COUNT(ID) AS Count FROM MOLECULES;';

        dispatcher.utter_message(text=sql);
        return[];
        dispatcher.utter_message(text=sql);

        try:          
            conn = sqlite3.connect(db_path_name);
            cursor = conn.cursor();
            cursor.execute(sql);
            results = cursor.fetchall();

            for row in results:
                count = row[0];
                message = "unique molecules: " + f"{count}";
                dispatcher.utter_message(text=message);

            conn.close();

        except Exception as e:
            # handle the error gracefully
            error_message = "I'm sorry, there was a problem processing your request.";
            dispatcher.utter_message(text=error_message);

        return [];
#_______________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class PerformRGroupAnalysis(Action):
    def name(self) -> Text:
        return "action_r_analysis"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_r_analysis");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class ReloadData(Action):
    def name(self) -> Text:
        return "action_reload_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_reload_data");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class ShowCurrentScaffold(Action):
    def name(self) -> Text:
        return "action_show_scaffold"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_show_scaffold");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class ShowMostActiveCompound(Action):
    def name(self) -> Text:
        return "action_most_active"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_most_active");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class ShowLeastActiveCompound(Action):
    def name(self) -> Text:
        return "action_least_active"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_least_active");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class LoadScaffoldFromFile(Action):
    def name(self) -> Text:
        return "action_load_scaffold"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<open file browser ui> running: action_load_scaffold");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class DrawScaffold(Action):
    def name(self) -> Text:
        return "action_draw_scaffold"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<open mol sketcher ui> : open javascrip molecule drawer");
        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class PasteScaffold(Action):
    def name(self) -> Text:
        return "action_paste_scaffold"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_paste_scaffold");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class GenericHelp(Action):
    def name(self) -> Text:
        return "action_help"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   

        help = "This is a tool to study Structure Activity Relationships.\n Type in smiple/concise commands to make it operate:\n";
        help += "\tload molecule\tload smiles\tload molecules from cddvault\n";
        help += "\tload scaffold\tdraw scaffold\tshow current scaffold\n";
        help += "\tset activity column\theatmap column\n";
        help += "\tshow most active molecule\tshow least active molecules\n";
        help += "\tperfrom SAR analysis\n";

        dispatcher.utter_message(text = help);

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class HelpProperties(Action):
    def name(self) -> Text:
        return "action_help_properties"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
           
        help = "The properties that can be calculated:\n";
        help += "\tlogP (rdkit based on Crippen)\n";
        help += "\tpolar surface area (TPSA based on Ertl)\n";
        help += "\tsolvent accessible surface area (rdkit)\n";
        help += "\tHydrogen bond donars and acceptors (HBD, HBA)\n";
        help += "\tMolecular weight (MW)\n";
        help += "try: \'open property UI\', \'calc HBA\', \'calc HBD\' ...\n";
        dispatcher.utter_message(text = help);

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class CalcProperties(Action):
    def name(self) -> Text:
        return "action_calc_properties"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<PropertyUI>: open Property calculation UI and wait");

        return []
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class CalcExplicitProperties(Action):
    def name(self) -> Text:
        return "action_explicit_property"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        calc_list = set();
        user_input = tracker.latest_message.get('text');
        user_input = user_input.lower();

        if re.search("logp", user_input):
            calc_list.add("logp");
        if re.search("hba", user_input):
            calc_list.add("hba");
        if re.search("acceptors", user_input):
            calc_list.add("hba");        
        if re.search("hbd", user_input):
            calc_list.add("hbd");
        if re.search("donors", user_input):    
             calc_list.add("hbd");   
        if re.search("donars", user_input):    
             calc_list.add("hbd");                      
        if re.search("tpsa", user_input):
            calc_list.add("tpsa");
        if re.search("polar surface", user_input):
            calc_list.add("tpsa");      
        if re.search("polar sa", user_input):
            calc_list.add("tpsa");            
        if re.search("sasa", user_input):
            calc_list.add("sasa");
        if re.search("solvent accessible surface", user_input):
            calc_list.add("sasa");
        if re.search("surface area", user_input):
            calc_list.add("sasa");        
        if re.search("rotb", user_input):
            calc_list.add("rotb");
        if re.search("rot bonds", user_input):
            calc_list.add("rotb");
        if re.search("rotatable bonds", user_input):
            calc_list.add("rotbonds");
        if re.search("rotb", user_input):
            calc_list.add("rotb");
        if re.search("mw", user_input):
            calc_list.add("mw");
        if re.search("molweight", user_input):
            calc_list.add("mw");
        if re.search("molecular weight", user_input):
            calc_list.add("mw");
        if re.search("mass", user_input):
            calc_list.add("mw");        
        

        output_str = "calculating ";
        for s in calc_list:
            output_str += s;
            output_str += ",";

        if len(calc_list) == 0:
            output_str = "I do not recognize that property";

        dispatcher.utter_message(text = output_str);
        #calc properties
        return [];
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class FindLeastPotentRGroup(Action):
    def name(self) -> Text:
        return "action_least_potent_rgroup";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_least_potent_rgroup");
        return [];
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class FindMostPotentRGroup(Action):
    def name(self) -> Text:
        return "action_most_potent_rgroup";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_most_potent_rgroup");
        return [];
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class RecommendRGroups(Action):
    def name(self) -> Text:
        return "action_recommend_rgroups";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_recommend_rgroups");
        return [];
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class FindBioisosteres(Action):
    def name(self) -> Text:
        return "action_recommend_bioisosteres";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_recommend_bioisosteres");
        return [];
#__________________________________________________________________________________________________

#_______________________________________________________________________________________________________________
class HelpRecommendRGroups(Action):
    def name(self) -> Text:
        return "action_help_recommend_rgroups";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "running: action_help_recommend_rgroups");
        return [];



#__________________________________________________________________________________________________
svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"305\" height=\"352\">\
<g id=\"unmapped\">\
<g id=\"lines\" style=\"stroke:rgb(138,0,0);stroke-width:2\">\
 <line x1=\"265\" y1=\"350\" x2=\"276\" y2=\"330\" />\
 <line x1=\"276\" y1=\"330\" x2=\"266\" y2=\"313\" />\
 <line x1=\"266\" y1=\"298\" x2=\"276\" y2=\"280\" />\
 <line x1=\"276\" y1=\"283\" x2=\"290\" y2=\"283\" />\
 <line x1=\"276\" y1=\"278\" x2=\"290\" y2=\"278\" />\
 <line x1=\"276\" y1=\"280\" x2=\"265\" y2=\"263\" />\
 <line x1=\"253\" y1=\"256\" x2=\"233\" y2=\"256\" />\
 <line x1=\"265\" y1=\"248\" x2=\"275\" y2=\"231\" />\
 <line x1=\"233\" y1=\"256\" x2=\"218\" y2=\"231\" />\
 <line x1=\"218\" y1=\"231\" x2=\"228\" y2=\"213\" />\
 <line x1=\"240\" y1=\"206\" x2=\"261\" y2=\"206\" />\
 <line x1=\"228\" y1=\"199\" x2=\"217\" y2=\"181\" />\
 <line x1=\"261\" y1=\"206\" x2=\"275\" y2=\"231\" />\
 <line x1=\"220\" y1=\"183\" x2=\"227\" y2=\"170\" />\
 <line x1=\"215\" y1=\"180\" x2=\"222\" y2=\"168\" />\
 <line x1=\"217\" y1=\"181\" x2=\"189\" y2=\"182\" />\
 <line x1=\"189\" y1=\"182\" x2=\"175\" y2=\"207\" />\
 <line x1=\"189\" y1=\"182\" x2=\"178\" y2=\"164\" />\
 <line x1=\"175\" y1=\"207\" x2=\"146\" y2=\"207\" />\
 <line x1=\"146\" y1=\"207\" x2=\"132\" y2=\"232\" />\
 <line x1=\"130\" y1=\"233\" x2=\"137\" y2=\"246\" />\
 <line x1=\"134\" y1=\"231\" x2=\"141\" y2=\"243\" />\
 <line x1=\"132\" y1=\"232\" x2=\"117\" y2=\"232\" />\
 <line x1=\"166\" y1=\"157\" x2=\"145\" y2=\"157\" />\
 <line x1=\"143\" y1=\"156\" x2=\"136\" y2=\"169\" />\
 <line x1=\"148\" y1=\"158\" x2=\"141\" y2=\"171\" />\
 <line x1=\"145\" y1=\"157\" x2=\"131\" y2=\"132\" />\
 <line x1=\"131\" y1=\"132\" x2=\"145\" y2=\"108\" />\
 <line x1=\"128\" y1=\"128\" x2=\"140\" y2=\"107\" />\
 <line x1=\"131\" y1=\"132\" x2=\"111\" y2=\"133\" />\
 <line x1=\"145\" y1=\"108\" x2=\"130\" y2=\"83\" />\
 <line x1=\"130\" y1=\"83\" x2=\"102\" y2=\"83\" />\
 <line x1=\"128\" y1=\"88\" x2=\"104\" y2=\"88\" />\
 <line x1=\"130\" y1=\"83\" x2=\"140\" y2=\"65\" />\
 <line x1=\"102\" y1=\"83\" x2=\"88\" y2=\"108\" />\
 <line x1=\"88\" y1=\"108\" x2=\"98\" y2=\"126\" />\
 <line x1=\"93\" y1=\"107\" x2=\"101\" y2=\"122\" />\
 <line x1=\"88\" y1=\"108\" x2=\"59\" y2=\"108\" />\
 <line x1=\"59\" y1=\"108\" x2=\"45\" y2=\"133\" />\
 <line x1=\"54\" y1=\"108\" x2=\"41\" y2=\"129\" />\
 <line x1=\"59\" y1=\"108\" x2=\"44\" y2=\"84\" />\
 <line x1=\"45\" y1=\"133\" x2=\"16\" y2=\"134\" />\
 <line x1=\"16\" y1=\"134\" x2=\"2\" y2=\"109\" />\
 <line x1=\"19\" y1=\"129\" x2=\"7\" y2=\"108\" />\
 <line x1=\"2\" y1=\"109\" x2=\"16\" y2=\"84\" />\
 <line x1=\"16\" y1=\"84\" x2=\"44\" y2=\"84\" />\
 <line x1=\"18\" y1=\"89\" x2=\"42\" y2=\"89\" />\
 <line x1=\"153\" y1=\"58\" x2=\"173\" y2=\"58\" />\
 <line x1=\"140\" y1=\"51\" x2=\"130\" y2=\"33\" />\
 <line x1=\"173\" y1=\"58\" x2=\"187\" y2=\"33\" />\
 <line x1=\"187\" y1=\"33\" x2=\"177\" y2=\"15\" />\
 <line x1=\"164\" y1=\"8\" x2=\"144\" y2=\"8\" />\
 <line x1=\"144\" y1=\"8\" x2=\"130\" y2=\"33\" />\
</g>\
<g id=\"letters\" fill=\"rgb(138,0,0)\" text-anchor=\"start\" font-family=\"Arial\" text-rendering=\"geometricPrecision\">\
<text x=\"256\" y=\"311\" font-size=\"14\">O</text>\
<text x=\"293\" y=\"286\" font-size=\"14\">O</text>\
<text x=\"255\" y=\"262\" font-size=\"14\">N</text>\
<text x=\"226\" y=\"212\" font-size=\"14\">N</text>\
<text x=\"223\" y=\"167\" font-size=\"14\">O</text>\
<text x=\"138\" y=\"258\" font-size=\"14\">O</text>\
<text x=\"103\" y=\"238\" font-size=\"14\">O</text>\
<text x=\"94\" y=\"238\" font-size=\"14\">H</text>\
<text x=\"168\" y=\"163\" font-size=\"14\">N</text>\
<text x=\"168\" y=\"150\" font-size=\"14\">H</text>\
<text x=\"128\" y=\"183\" font-size=\"14\">O</text>\
<text x=\"96\" y=\"139\" font-size=\"14\">N</text>\
<text x=\"139\" y=\"64\" font-size=\"14\">N</text>\
<text x=\"167\" y=\"14\" font-size=\"14\">O</text>\
</g>\
</g>\
<g id=\"mapped\">\
<g id=\"lines\" style=\"stroke:rgb(0,0,138);stroke-width:2\">\
</g>\
<g id=\"letters\" fill=\"rgb(0,0,138)\" text-anchor=\"start\" font-family=\"Arial\" text-rendering=\"geometricPrecision\">\
</g>\
</g>\
</svg>";

class TestSVG(Action):
    def name(self) -> Text:
        return "action_test_svg";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = svg);
        return [];
    
#__________________________________________________________________________________________________________________________    
csv = "Short Name,Medium Name,Long Name,Category,Font Color,Order,Synonyms,Clustal Substitution,Comment,<BackgroundColor>Hydrophobicity-KD,<BackgroundColor>Hydrophobicity-HW,<BackgroundColor>ChemicalStructure,<BackgroundColor>ChouFasman,<Data>Kyte-Doolittle,<Data>Hopp-Woods,<BackgroundColor>Clustal,<Data>logp (crippen),<Data>mr,<Data>TPSArea,<Data>kappa1,<Data>kappa2,<Data>kappa3,<Data>SArea,<Data>MW,Smiles\r \
G,Gly,Glycine,neutral,black,1,G;Gly;GLY;Glycine,G,,\"RGB(116,116,139)\",\"RGB(120,120,136)\",\"RGB(0,255,255)\",green,-0.4,0,yellow,-0.856,15.1184,43.09,0.43129,2.63,1.63,31.7466,57.0515,C(C(=O)[r])N[r]\r \
A,Ala,Alanine,neutral,black,2,A;Ala;ALA;Alanine,A,,\"RGB(179,179,77)\",\"RGB(139,139,116)\",\"RGB(0,255,255)\",red,1.8,-0.5,white,-0.4675,19.7134,43.09,0.539918,1.90548,3.63,40.9215,71.0782,C[C@@H](C(=O)[r])N[r]\r \
dA,dAla,D-Alanine,neutral,red,2.1,dAla;dA,A,,\"RGB(179,179,77)\",\"RGB(139,139,116)\",\"RGB(0,255,255)\",red,1.8,-0.5,white,-0.4675,19.7134,43.09,0.539918,1.90548,3.63,40.9215,71.0782,C[C@H](C(=O)[r])N[r]\r \
V,Val,Valine,aliphatic,black,3,V;Val;VAL;Valine,V,,\"RGB(9,9,247)\",\"RGB(179,179,76)\",\"RGB(0,255,255)\",blue,4.2,-1.5,green,0.1686,28.8774,43.09,0.759881,2.74564,2.34048,59.2712,99.1316,[r]C([C@@H](N[r])C(C)C)=O\r \
dV,dVal,D-Valine,aliphatic,red,3.1,dV;dVal,V,,\"RGB(9,9,247)\",\"RGB(179,179,76)\",\"RGB(0,255,255)\",blue,4.2,-1.5,green,0.1686,28.8774,43.09,0.759881,2.74564,2.34048,59.2712,99.1316,[r]C([C@H](N[r])C(C)C)=O\r ";
class TestCSV(Action):
    def name(self) -> Text:
        return "action_test_csv";

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = csv);
        return [];

