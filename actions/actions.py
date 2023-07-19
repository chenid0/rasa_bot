# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions




from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher



#_______________________________________________________________________________________________________________
class LoadMolsFromSDF(Action):
    def name(self) -> Text:
        return "action_load_mols_sdf"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        dispatcher.utter_message(text = "<open browserui> running: action_load_mols_sdf");

        return []
#__________________________________________________________________________________________________
