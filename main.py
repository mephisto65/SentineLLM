import argparse 
import json
from LLM import *
from attacks import *

def get_model(model_name: str) -> LLM:
    model_classes = {
        "OpenAI": OpenAIModel(),
        "Mistral": MistralModel(),
        "deepseek": DeepSeekModel(),
        "Claude": ClaudeModel(),
    }

    model_class = model_classes.get(model_name)
    if not model_class:
        raise ValueError(f"Model {model_name} not supported.")

    return model_class  # Or pass model name if different

def main(args):


    print(f"Beginning of {args.jailbreak_type} Attack | {args.subtype} Mode\n")

    victim=get_model(args.victim_model)
    if args.judge_model and args.api_key_v:
        judge=get_model(args.judge_model)
    else:
        judge=None

    ##### PAIR ATTACK #####

    if args.jailbreak_type == "PAIR":
        print("PAIR Attack\n")
        attacker=get_model(args.attacker_model)
        attack = PAIR(args.jailbreak_type,args.subtype,victim,args.api_key_v, judge,args.api_key_j,attacker, args.api_key_a,args.pair_iter, args.baseline,args.target_str)
        attack.begin_attack()

    ##### CRESCENDO ATTACK #####

    if args.jailbreak_type == "Crescendo":

        attack = Crescendo(args.jailbreak_type,args.subtype,victim,args.api_key_v,judge,args.api_key_j)

        if args.subtype == "single":
            attack.single()
        elif args.subtype == "multi-turn":
            attack.multi()

    ##### DAN ATTACK #####

    if args.jailbreak_type == "DAN":
        attack = DAN(args.jailbreak_type,args.subtype,victim,args.api_key_v,judge,args.api_key_j)

        if args.subtype == "reciprocal":
            attack.reciprocal()
        elif args.subtype == "direct":
            attack.direct()

    ##### OBFUSCATION ATTACK #####

    if args.jailbreak_type == "Obfuscation":

        attack = Obfuscation(args.jailbreak_type,args.subtype,victim,args.api_key_v,judge,args.api_key_j, args.baseline,args.encode)
        attack.begin_attack()

    ######## REPORT GENERATION #########

    attack.generate_report(args.output)
    print(f"\n\nEnd of {args.jailbreak_type} Attack | {args.subtype} Mode\n")
    print("Note : Report only available if a judge model is used")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to test your LLM against jailbreaking attacks")
    parser.add_argument("--api-key-v", required=True, type=str, help="Path to your API key /!\\ for Victim Model (.key file)")
    parser.add_argument("--api-key-a", type=str, help="Path to your API key /!\\ for Attacker Model (.key file)")
    parser.add_argument("--api-key-j", type=str, default=None, help="Path to your API key /!\\ for Judge Model (.key file)")
    parser.add_argument("--victim-model",required=True, choices=["OpenAI", "Mistral","deepseek","Claude","Other"],type=str,help="The model you want to test against jailbreak")
    parser.add_argument("--attacker-model", choices=["OpenAI", "Mistral","deepseek","Claude","Other"],type=str,help="The model you want to use to attack the victim")
    parser.add_argument("--judge-model", choices=["OpenAI", "Mistral","deepseek","Claude","Other"],default=None,type=str,help="The model you want to use to judge the attack")
    parser.add_argument("--jailbreak-type",required=True,choices=["PAIR","Crescendo","Obfuscation","DAN"],type=str,help="Jailbreak method to use")
    parser.add_argument("--baseline",required=False,type=str,help="Basic, malicious prompts to make the model produce forbidden content (e.g. “Give me the recipe of the molotov cocktail”).")
    parser.add_argument("--output",required=False,type=str,help="Path to the output file")
    parser.add_argument("--target-str",required=False,type=str,help="")
    args,remaining_args=parser.parse_known_args()
    if args.jailbreak_type == "PAIR":
        parser.add_argument("--pair-iter", type=int, default=20,
                        help="Number of PAIR iterations")
        parser.add_argument("--subtype", choices=["impersonation", "logical_appealing"], 
                        default="logical_appealing", help="PAIR Attack mode")
    elif args.jailbreak_type == "Crescendo":
        parser.add_argument("--subtype",choices=["single","multi-turn"],default="single")
    elif args.jailbreak_type == "Obfuscation":
        print("If you chose 2 methods or more format --subtype argument like this : --subtype method1,method2,method3... write them in the order you want them to be applied (choices : character, context, structure)")
        parser.add_argument("--subtype",default="character")
        parser.add_argument("--encode",required=False,type=str,choices=["base64","rot13","morse"],help="Encoding method to use (choices : base64, rot13, morse)",default="base64")

    elif args.jailbreak_type == "DAN":
        parser.add_argument("--subtype",choices=["reciprocal","direct"],default="direct")

    args = parser.parse_args()
    main(args)