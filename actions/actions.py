# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import re
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from constants import query_tag, action_tag, svg_tag, csv_tag

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
g_current_scaffold = ""
# table:rowid [SCAFFOLDS:SCAFID]
g_calc_properties = set()
# [logP, MW, rotB, TPSA]
g_display_cols_in_order = []
# col names to display table:col [MOLECULES:MOLID, MOLDATA:EXTERNALKEY, MOLDATA:IC50, MOLDATA:Ki, MOLPROPS:logP, MOLPROPS:MW ]
g_rename_cols = []
# rename ori name:new name  [measured Ki(n) for xyza: Ki(nM), LOGP_RDKIT, logP]
g_heatmap_cols = []
# heatmap to col name:range:color/range:color/range:color [Ki(n):0->1000]
g_activity_col = ""
# activity or model column

g_history_calls = []
# list in order of calls e.g. "action_load_mols_sdf: filename", "add_scaffold: mol", ...


def utter_query(dispatcher, query):
    dispatcher.utter_message(text=f"\n{query_tag} {query}\n")
    dispatcher.utter_message(json_message={"query": query})
    dispatcher.utter_message(elements=[query,])


def utter_svg(dispatcher, svg):
    dispatcher.utter_message(text=f"\n{svg_tag} {svg}\n")


def utter_csv(dispatcher, csv):
    dispatcher.utter_message(text=f"\n{csv_tag} {csv}\n")


# _______________________________________________________________________________________________________________
class LoadMolsFromSDF(Action):
    def name(self) -> Text:
        return "action_load_mols_sdf"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="<open browserui> running: action_load_mols_sdf")

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class LoadMolsCDD(Action):
    def name(self) -> Text:
        return "action_load_mols_cddvault"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="<open cddvaultui> running: action_load_mols_cddvault"
        )

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class LoadMolsPostgres(Action):
    def name(self) -> Text:
        return "action_load_mols_postgres"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="<open postgresui> running: action_load_mols_postgres"
        )

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class SetActivityColumn(Action):
    def name(self) -> Text:
        return "action_set_model_column"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="<column selectorui>running: action_set_model_column"
        )

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class HeatMapColumn(Action):
    def name(self) -> Text:
        return "action_heat_map_column"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_heat_map_column")

        return []


# __________________________________________________________________________________________________
class CountMols(Action):
    def name(self) -> Text:
        return "action_count_mols"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        sql = "SELECT COUNT(ID) AS Count FROM MOLECULES;"
        dispatcher.utter_message(text=f"{query_tag} {sql}\n")
        return []


# _______________________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class PerformRGroupAnalysis(Action):
    def name(self) -> Text:
        return "action_r_analysis"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_r_analysis")

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class ReloadData(Action):
    def name(self) -> Text:
        return "action_reload_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_reload_data")

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class ShowCurrentScaffold(Action):
    def name(self) -> Text:
        return "action_show_scaffold"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_show_scaffold")

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class ShowMostActiveCompound(Action):
    def name(self) -> Text:
        return "action_most_active"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_most_active")

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class ShowLeastActiveCompound(Action):
    def name(self) -> Text:
        return "action_least_active"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_least_active")

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class LoadScaffoldFromFile(Action):
    def name(self) -> Text:
        return "action_load_scaffold"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="<open file browser ui> running: action_load_scaffold"
        )

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class DrawScaffold(Action):
    def name(self) -> Text:
        return "action_draw_scaffold"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="<open mol sketcher ui> : open javascrip molecule drawer"
        )
        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class PasteScaffold(Action):
    def name(self) -> Text:
        return "action_paste_scaffold"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_paste_scaffold")

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class GenericHelp(Action):
    def name(self) -> Text:
        return "action_help"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        help = "This is a tool to study Structure Activity Relationships.\n Type in smiple/concise commands to make it operate:\n"
        help += "\tload molecule\tload smiles\tload molecules from cddvault\n"
        help += "\tload scaffold\tdraw scaffold\tshow current scaffold\n"
        help += "\tset activity column\theatmap column\n"
        help += "\tshow most active molecule\tshow least active molecules\n"
        help += "\tperfrom SAR analysis\n"

        dispatcher.utter_message(text=help)

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class HelpProperties(Action):
    def name(self) -> Text:
        return "action_help_properties"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        help = "The properties that can be calculated:\n"
        help += "\tlogP (rdkit based on Crippen)\n"
        help += "\tpolar surface area (TPSA based on Ertl)\n"
        help += "\tsolvent accessible surface area (rdkit)\n"
        help += "\tHydrogen bond donars and acceptors (HBD, HBA)\n"
        help += "\tMolecular weight (MW)\n"
        help += "try: 'open property UI', 'calc HBA', 'calc HBD' ...\n"
        dispatcher.utter_message(text=help)

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class CalcProperties(Action):
    def name(self) -> Text:
        return "action_calc_properties"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="<PropertyUI>: open Property calculation UI and wait"
        )

        return []


# __________________________________________________________________________________________________


# _______________________________________________________________________________________________________________
class CalcExplicitProperties(Action):
    def name(self) -> Text:
        return "action_explicit_property"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        calc_list = set()
        user_input = tracker.latest_message.get("text")
        user_input = user_input.lower()

        if re.search("logp", user_input):
            calc_list.add("logp")
        if re.search("hba", user_input):
            calc_list.add("hba")
        if re.search("acceptors", user_input):
            calc_list.add("hba")
        if re.search("hbd", user_input):
            calc_list.add("hbd")
        if re.search("donors", user_input):
            calc_list.add("hbd")
        if re.search("donars", user_input):
            calc_list.add("hbd")
        if re.search("tpsa", user_input):
            calc_list.add("tpsa")
        if re.search("polar surface", user_input):
            calc_list.add("tpsa")
        if re.search("polar sa", user_input):
            calc_list.add("tpsa")
        if re.search("sasa", user_input):
            calc_list.add("sasa")
        if re.search("solvent accessible surface", user_input):
            calc_list.add("sasa")
        if re.search("surface area", user_input):
            calc_list.add("sasa")
        if re.search("rotb", user_input):
            calc_list.add("rotb")
        if re.search("rot bonds", user_input):
            calc_list.add("rotb")
        if re.search("rotatable bonds", user_input):
            calc_list.add("rotbonds")
        if re.search("rotb", user_input):
            calc_list.add("rotb")
        if re.search("mw", user_input):
            calc_list.add("mw")
        if re.search("molweight", user_input):
            calc_list.add("mw")
        if re.search("molecular weight", user_input):
            calc_list.add("mw")
        if re.search("mass", user_input):
            calc_list.add("mw")

        output_str = "calculating "
        for s in calc_list:
            output_str += s
            output_str += ","

        if len(calc_list) == 0:
            output_str = "I do not recognize that property"

        dispatcher.utter_message(text=output_str)
        # calc properties
        return []


# _______________________________________________________________________________________________________________
class FindLeastPotentRGroup(Action):
    def name(self) -> Text:
        return "action_least_potent_rgroup"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_least_potent_rgroup")
        return []


# _______________________________________________________________________________________________________________
class FindMostPotentRGroup(Action):
    def name(self) -> Text:
        return "action_most_potent_rgroup"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_most_potent_rgroup")
        return []



# _______________________________________________________________________________________________________________
class RecommendRGroups(Action):
    def name(self) -> Text:
        return "action_recommend_rgroups"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_recommend_rgroups")
        return []


# _______________________________________________________________________________________________________________
class FindBioisosteres(Action):
    def name(self) -> Text:
        return "action_recommend_bioisosteres"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_recommend_bioisosteres")
        return []


# _______________________________________________________________________________________________________________
class HelpRecommendRGroups(Action):
    def name(self) -> Text:
        return "action_help_recommend_rgroups"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_help_recommend_rgroups")
        return []


class TestSVG(Action):
    def name(self) -> Text:
        return "action_test_svg"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"action: {svg_tag}\n")
        return []


class TestCSV(Action):
    def name(self) -> Text:
        return "action_test_csv"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"action: {csv_tag}\n")
        return []


# _______________________________________________________________________________________________________________
class ListAvailProperties(Action):
    def name(self) -> Text:
        return "action_list_properties"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tablename = "MOLDATA"
        sql1 = "SELECT name, type FROM PRAGMA_TABLE_INFO('" + tablename + "');"
        # take only DOUBLE, FLOAT, INT and INTEGER fields        
        dispatcher.utter_message(text="running: action_list_properties")
        
        utter_query(dispatcher, sql1)
        return []


# _______________________________________________________________________________________________________________
class ListAvailData(Action):
    def name(self) -> Text:
        return "action_list_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tablename = "MOLPROPS"
        sql2 = "SELECT name, type FROM PRAGMA_TABLE_INFO('" + tablename + "');"
        # take only DOUBLE, FLOAT, INT and INTEGER fields
        dispatcher.utter_message(text="running: action_list_data")
        utter_query(dispatcher, sql2)
        return []


# _______________________________________________________________________________________________________________
class GetMinimumValue(Action):
    def name(self) -> Text:
        return "action_min_value"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
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

        # tablename1 = "MOLPROPS"; tablename2 = "MOLDATA";
        # for each column
        # sql2 = "SELECT MIN(" + column + ") FROM " + tablename + ";";
        dispatcher.utter_message(text="running: action_min_value")

        # we will export a molecule svg with it later on...

        return []


# _______________________________________________________________________________________________________________
class GetMaximumValue(Action):
    def name(self) -> Text:
        return "action_max_value"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
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

        tablename1 = "MOLPROPS"
        tablename2 = "MOLDATA"
        # for each column
        # sql2 = "SELECT MIN(" + column + ") FROM " + tablename + ";";

        # we will export a molecule svg with it later on...

        dispatcher.utter_message(text="running: action_max_value")
        return []


# action: action_historgram
# _______________________________________________________________________________________________________________
class CalculateHistogram(Action):
    def name(self) -> Text:
        return "action_historgram"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
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

        tablename1 = "MOLPROPS"
        tablename2 = "MOLDATA"
        # specific
        sql1 = "SELECT DISTINCT CAST(MW/100 As INT)*100 AS Bin, COUNT(*) AS Frequency FROM " + tablename1 + " GROUP BY Bin;"

        # generic: for each column
        #sql = "SELECT DISTINCT CAST(" + column + "/" + divide_val + " As INT)*" + divide_val + " AS Bin, COUNT(*) AS Frequency FROM " + tablename + " GROUP BY Bin;";

        # we can export a simple csv formatted table to text.
        #  we can add a svg or gif from the data..

        dispatcher.utter_message(text="running: action_historgram")
        utter_query(dispatcher, sql1)        
        return []
