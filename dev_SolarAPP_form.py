import os
import networkx as nx
from elm.base import ApiBase
from elm.tree import DecisionTree
from sklearn import tree
from dotenv import load_dotenv

# Load API key from environment variable
# ADD KEY HERE
load_dotenv()

def Equipment_Inverter(**kwargs):
    G = nx.DiGraph(**kwargs)
    G.graph["api"] = ApiBase(model="gpt-4o")

    formatting_instructions = (
        "\n\nProvide only the selected option as your first sentence."
        "\n\nThen, in a short paragraph, explain how you determined your answer based on the diagram or text."
        "\nCite specific language, components, or design elements that support your choice."
        "\nOnly choose one manufacturer exactly as it appears in the optionslist, in case there is a list."
        "\nIf there is no list, provide your own answer, but always the short answer first and then the explanation on a separate paragraph"
    )

    ApiBase.MODEL_ROLE = "You are an expert on analyzing Single Line Diagrams (SLD) of residential solar installations."

    G.add_node(
        "intro_inverter_type",
        prompt=(
            "I have provided you with a diagram (see attached). I want you to professionally analyze it"
            "and answer the following questions."
            "Use only clear evidence from the diagram and do not make assumptions."
            "Store your answers internally and provide them as a single JSON file at the end of the decision tree."
            "What is the architecture type used for all inverters in this project?\n"
            "Choose only one of the following options based on the ordinance text:\n"
            "- String Inverter without DC-DC Converters\n"
            "- String Inverter with DC-DC Converters\n"
            "- Microinverters\n"
            "- AC Modules"
            + formatting_instructions
        ),
    )
    # Microinverter branch.
    manufacturer_list_json = [
        "Enphase Energy Inc.",
        "ABB",
        "SMA America",
        "SolarEdge Technologies",
        "Fronius USA",
        "OutBack Power",
        "Huawei",
        "Delta Electronics",
        "Chilicon Power",
        "other"
    ]

    G.add_node("micro_mfr1", prompt=(
        "Inverter 1 Manufacturer.\n"
        "Choose from the following list:\n\n"
        + '\n'.join(f"- {m}" for m in manufacturer_list_json)
        + formatting_instructions
    ))

    G.add_node("micro_model1", prompt=(
        "Inverter 1 Model Number.\nPlease state the full model number as listed on the diagram or specification."
        + formatting_instructions
    ))

    G.add_node("micro_ocpd1", prompt=(
        "What is the maximum overcurrent protection device (OCPD) rating allowed on Inverter 1 (Amps)?"
        + formatting_instructions
    ))

    G.add_node("micro_interconnect1", prompt=(
        "Where will Inverter 1 be interconnected to the premises wiring and utility power?\n"
        "Select one of the following options:\n"
        "- Main Service Panel\n"
        "- Service Feeders\n"
        "- Backup Loads Panel"
        + formatting_instructions
    ))
    # Other branches, not developed yet. 
    # G.add_node("string_node", prompt="Answer detailed follow-up questions for String Inverter without DC-DC Converters." + formatting_instructions)
    # G.add_node("dc_dc_node", prompt="Answer detailed follow-up questions for String Inverter with DC-DC Converters." + formatting_instructions)
    # G.add_node("ac_module_node", prompt="Answer detailed follow-up questions for AC Modules." + formatting_instructions)

    # Branch dividers. Only including microinverters for now. 
    G.add_edge("inverter_type", "micro_node", condition=lambda x: x.strip().lower().startswith("microinverters"))
    # G.add_edge("inverter_type", "string_node", condition=lambda x: x.strip().lower().startswith("string inverter without dc"))
    # G.add_edge("inverter_type", "dc_dc_node", condition=lambda x: x.strip().lower().startswith("string inverter with dc"))
    # G.add_edge("inverter_type", "ac_module_node", condition=lambda x: x.strip().lower().startswith("ac modules"))

    G.add_edge("micro_node", "micro_mfr1")
    G.add_edge("micro_mfr1", "micro_model1")
    G.add_edge("micro_model1", "micro_ocpd1")
    G.add_edge("micro_ocpd1", "micro_interconnect1")
    G.add_edge("micro_interconnect1", "final")
    G.add_node("final", prompt="Please output all collected answers as a single JSON file." + formatting_instructions)
    # Can I do this?? Am I not relying too much on the model's memory? Shouldnt I store the answers while provided? 

    # G.add_edge("string_node", "final")
    # G.add_edge("dc_dc_node", "final")
    # G.add_edge("ac_module_node", "final")

    return G

def main():
    G = Equipment_Inverter()
    tree = DecisionTree(G)
    # result = tree.run()
    # print(result)
    out = tree.run("intro_inverter_type") # Make sure we are starting at that node. 
    print(tree.all_messages_txt)

if __name__ == "__main__":
    main()

