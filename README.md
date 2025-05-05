# SentineLLM

**SentineLLM** is a tool allowing you to test the robustness of the most popular LLMs (Claude,deepseek,Mistral,ChatGPT) against jailbreaking attacks.

## What is a jailbreak attack ?

As the name suggests, a *Jail* **Break** attack consists in freeing an LLM (Large Language Model) from its constraints. 

In other words, it consists in making a model produce content that it is not supposed to produce. This can include (but is not limited to) dangerous, threatening, sexual and, more generally, unethical content. For example: the recipe for a Molotov cocktail, a ransomware written in Python or a Nazi speech.

## The tool

Several jailbreaking methods have been implemented to extend the tool's defensive spectrum:

- **PAIR**
    - via logical appealing
    - via impersonation
- **Crescendo**
    - Single Turn
    - Multi Turn
- **Obfuscation**
    - Character level
    - Context level
    - Structure level
- **DAN (Do Anything Now)**
    - Direct
    - Reciprocal

*A short description of each methods is provided at the end of this document.*

## Installation

### Prerequisites

Make sure you have the following installed on your system:

- [Git](https://git-scm.com/)
- [Python 3.x](https://www.python.org/) (or other required environment)
- (Optional) [pipenv](https://pipenv.pypa.io/en/latest/) or `venv` for virtual environments

### 🔧 Clone the Repository

Clone this GitHub repository to your local machine:

```bash
git clone https://github.com/mephisto65/SentineLLM
cd SentineLLM

pip install -r requirements.txt

python3 main.py --victim-model <MODEL> --api-key-v <PATH> --jailbreak-type <TYPE>
```
## ⚙️ Command-Line Arguments

| Argument             | Required | Type    | Description                                                                                   | Example                                   |
|----------------------|----------|---------|-----------------------------------------------------------------------------------------------|-------------------------------------------|
| `--api-key-v`        | Yes      | `str`   | Path to your API key for **Victim Model** (`.key` file)                                       | `--api-key-v path/to/victim.key`          |
| `--api-key-a`        | No       | `str`   | Path to your API key for **Attacker Model** (`.key` file)                                     | `--api-key-a path/to/attacker.key`        |
| `--api-key-j`        | No       | `str`   | Path to your API key for **Judge Model** (`.key` file)                                        | `--api-key-j path/to/judge.key`           |
| `--victim-model`     | Yes      | `str`   | Victim model to attack (`OpenAI`, `Mistral`, `deepseek`, `Claude`, `Other`)                  | `--victim-model OpenAI`                   |
| `--attacker-model`   | No       | `str`   | Attacker model to use                                                                         | `--attacker-model Mistral`                |
| `--judge-model`      | No       | `str`   | Judge model to evaluate results                                                               | `--judge-model Claude`                    |
| `--jailbreak-type`   | Yes      | `str`   | Jailbreak method: `PAIR`, `Crescendo`, `Obfuscation`, or `DAN`                                | `--jailbreak-type PAIR`                   |
| `--baseline`         | No       | `str`   | Malicious prompt used as baseline                                                             | `--baseline "How to make a molotov"`      |
| `--output`           | No       | `str`   | Path to output file where results will be saved (csv)                                               | `--output results.csv`                   |
| `--target-str`       | No       | `str`   | Target string (use case dependent)                                                            | `--target-str "Sure ! Here is..."`             |

### Jailbreak-Specific Arguments

#### If `--jailbreak-type` is `PAIR`:

| Argument         | Type    | Description                                  | Example                             |
|------------------|---------|----------------------------------------------|-------------------------------------|
| `--pair-iter`    | `int`   | Number of PAIR iterations (default: `20`)    | `--pair-iter 10`                    |
| `--subtype`      | `str`   | Attack mode: `impersonation` or `logical_appealing` (default: `logical_appealing`) | `--subtype impersonation`           |

#### If `--jailbreak-type` is `Crescendo`:

| Argument     | Type    | Description                        | Example                      |
|--------------|---------|------------------------------------|------------------------------|
| `--subtype`  | `str`   | Turn mode: `single` or `multi-turn` (default: `single`) | `--subtype multi-turn` |

#### If `--jailbreak-type` is `Obfuscation`:

| Argument     | Type    | Description                        | Example                                    |
|--------------|---------|------------------------------------|--------------------------------------------|
| `--subtype`  | `str`   | Obfuscation methods (comma-separated): `character`, `context`, `structure` | `--subtype character,context`             |
| `--encode`   | `str`   | Encoding method: `base64`, `rot13`, `morse` (default: `base64`) | `--encode rot13`               |

#### If `--jailbreak-type` is `DAN`:

| Argument     | Type    | Description                        | Example                        |
|--------------|---------|------------------------------------|--------------------------------|
| `--subtype`  | `str`   | Mode: `reciprocal` or `direct` (default: `direct`) | `--subtype reciprocal` |

---

### 🧪 Example

```bash
python3 main.py \
  --api-key-v path/to/victim.key \
  --victim-model OpenAI \
  --jailbreak-type PAIR \
  --pair-iter 15 \
  --subtype impersonation
```

## Results

The **Results** section in this code focuses on collecting, analyzing, and generating reports regarding the success of the attacks performed on the "victim" model. This section includes several features that allow tracking the progress of the attack, analyzing the feedback from the judges, and generating a detailed report of the outcomes.

### Associated Attributes for Results

1. **`score`**: This score is used to evaluate the quality of the attack based on feedback from the "judge" model. If the score is above or equal to a certain threshold (e.g., 7), it indicates that the attack was successful.

2. **`nb_message`**: The number of messages exchanged during the attack, which helps track the intensity and duration of the interaction.

3. **`successful_prompts`**: A list of prompts that successfully bypassed the victim model's restrictions, indicating successful attack attempts.

4. **`successful_victim_answers`**: A list of answers from the victim model that were successfully generated as a result of the attack.

### Methods Related to Results

- **`get_judge_feedback`**: This method interacts with the judge model to analyze the feedback and return a score for the given attack prompt and the victim’s response. It tracks the success of the attack based on the score received from the judge.
  
- **`generate_report`**: This method generates a CSV report containing the attack details
  
  The report is saved as a CSV file and provides a structured view of the attack's performance.

### Report Structure

The generated report contains the following columns:

1. **Attack Type**: The type of jailbreak attack performed.
2. **Subtype**: The specific subtype of the attack.
3. **Victim Model**: The model being attacked.
4. **Judge Model**: The model acting as a judge, providing feedback on the attack.
5. **Attacker Model**: The model used to create the attack.
6. **Baseline Prompt**: The initial prompt used in the attack.
7. **Target String**: The string the attacker aims to achieve with the attack.
8. **Mean of Score**: The average score achieved during the attack, representing its overall success.
9. **Successful Prompts**: A list of prompts that successfully bypassed the victim model.
10. **Successful Victim Answers**: The answers provided by the victim that indicate a successful bypass.
11. **Number of Messages**: The total number of messages exchanged during the attack.


## 🔓 Jailbreak Types

| Type         | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `PAIR`       | An iterative attack strategy that uses prompts designed to impersonate or logically persuade the victim model into violating its safety guardrails. Often involves multiple prompt refinements. |
| `Crescendo`  | A step-by-step jailbreak that builds up gradually, either in a single message or over multiple turns, to bypass content filters through progressive escalation. |
| `Obfuscation`| Hides malicious intent using indirect phrasing or encoding techniques (e.g., base64, ROT13) to confuse the moderation system while preserving meaning. |
| `DAN`        | "Do Anything Now" jailbreaks attempt to trick the model into simulating a persona that ignores ethical or policy constraints. Variants include direct roleplay or reciprocal prompt structures. |

## 🧑‍⚖️ Judge Model

The **Judge Model** (`--judge-model`) is used to evaluate whether the attack on the victim model has successfully bypassed its safety restrictions.

### 🔍 Role of the Judge

The judge model acts as a **third-party evaluator**. Here's how it typically works in the process:

1. **Input**:
   - The **attack prompt** (the malicious input designed to bypass the model's safeguards).
   - The **response** generated by the victim model.
   - Optionally, a **baseline prompt** to compare against.

2. **Analysis**:
   - The judge model analyzes whether the victim model’s response contains any **forbidden content** or fails to adhere to safety guidelines (e.g., promoting violence, hate speech, or other prohibited topics).
   - It checks if the victim model has been manipulated into violating its constraints.

3. **Output**:
   - The judge will either confirm that the response was **safe** or indicate if the victim model has **broken its guardrails**.
   - The judge model may also assist in determining the **severity** or **nature** of the violation.

## Current Limitation

At this moment, the process of adding new prompts to the `prompt.json` file requires manual intervention. While tools like `write.py` may be available in the future to automate this process, for now, users need to directly edit the JSON file to include new prompts.

#### Steps for Adding a New Prompt

1. **Open the `prompt.json` File**:
   Use any text editor (e.g., VSCode, Sublime Text, or even Notepad) to open the `prompt.json` file. This file contains all the prompts and responses in a structured format.

2. **Locate the Prompts Section**:
   The `prompt.json` file is likely structured in a JSON array or dictionary that holds the various prompts and their associated responses. You'll need to find the section where the prompts are stored.


## 📚 Bibliography

Here are some of the sources and references that helped in the development of this tool:

1. **The State of Attacks on GenAI** – A report from Pillar Security discussing the state of attacks on generative AI.
   - [Pillar Security Report](https://45700826.fs1.hubspotusercontent-na1.net/hubfs/45700826/The%20State%20of%20Attacks%20on%20GenAI%20-%20Pillar%20Security.pdf)

2. **How to Jailbreak LLMs One Step at a Time** – A blog post discussing methods of jailbreaking large language models.
   - [Confident AI Blog](https://www.confident-ai.com/blog/how-to-jailbreak-llms-one-step-at-a-time)

3. **Understanding LLMs from Scratch Using Middle School Math** – An article explaining large language models (LLMs) in an accessible way.
   - [Towards Data Science](https://towardsdatascience.com/understanding-llms-from-scratch-using-middle-school-math-e602d27ec876?s=09)

4. **Crescendo: A Multiturn Jailbreak** – Information on the Crescendo multiturn jailbreak strategy.
   - [Crescendo Jailbreak](https://crescendo-the-multiturn-jailbreak.github.io/)

5. **Jailbreaking Generative AI Web Products** – A report from Palo Alto Networks about jailbreaking generative AI products.
   - [Palo Alto Networks](https://unit42.paloaltonetworks.com/jailbreaking-generative-ai-web-products/)

6. **LLM Jailbreaking Taxonomy** – A detailed paper discussing the taxonomy of LLM jailbreaking techniques.
   - [Innodata LLM Jailbreaking](https://innodata.com/llm-jailbreaking-taxonomy/)

7. **Anthropic's Guide on Mitigating Jailbreaks** – Documentation on how Anthropic strengthens guardrails to mitigate jailbreaks.
   - [Anthropic Documentation](https://docs.anthropic.com/fr/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)

8. **Constitutional Classifiers** – A blog from Anthropic discussing methods for increasing model safety.
   - [Constitutional Classifiers](https://www.anthropic.com/news/constitutional-classifiers)

9. **Jailbreak ChatGPT: DAN, Prompt Injection, and Other Techniques** – A blog post discussing techniques to jailbreak ChatGPT.
   - [Jedha Blog](https://www.jedha.co/formation-ia/comment-jailbreak-chatgpt-dan-prompt-injection-et-autres-techniques)

10. **Find and Mitigate an LLM Jailbreak** – A blog post on how to find and mitigate jailbreaks in LLMs.
    - [Mindgard AI Blog](https://mindgard.ai/blog/find-and-mitigate-an-llm-jailbreak)

11. **Jailbreaking LLMs GitHub Repository** – A GitHub repository with tools and resources sfor jailbreaking LLMs.
    - [Patrick R. Chao's Jailbreaking LLMs](https://github.com/patrickrchao/JailbreakingLLMs)

12. **Jailbreak LLMs Repository** – A GitHub repository with various jailbreak methods and examples.
    - [Verazuo Jailbreak LLMs](https://github.com/verazuo/jailbreak_llms/tree/main)

13. **Jailbreaking Generative AI Models Paper** – A research paper discussing jailbreaks in generative AI models.
    - [arXiv Jailbreaking Paper](https://arxiv.org/html/2406.08754v2)

## Disclaimer

The content and activities described in this document, including jailbreak techniques and attacks on language models, are purely for educational and research purposes. The intention is to explore the boundaries and limitations of artificial intelligence systems to better understand their vulnerabilities and improve their security.

- **Ethical Use**: This information should not be used for malicious purposes or to exploit vulnerabilities in any system without permission. Engaging in unauthorized attacks or exploiting vulnerabilities in AI systems is illegal and unethical.
  
- **Legal Compliance**: Ensure that any testing or experimentation involving AI systems, especially in the context of jailbreak techniques, complies with applicable laws, terms of service, and ethical guidelines. Always seek consent from the appropriate parties before conducting any form of testing on a system or model.

- **Security Considerations**: Any techniques or methods described here should be viewed as a means to enhance AI safety and security. Researchers and developers are encouraged to use this knowledge to build more resilient and secure models that prevent unintended exploits.

By engaging with the content in this document, you acknowledge and agree to use the information responsibly and within the confines of applicable laws and ethical standards.
