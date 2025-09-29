import json
import pandas as pd
import logging
from openai import OpenAI
from datetime import datetime
import os
from utils.calc_kappa import calcu_kappa_subfacet

repeat_count = 1  
dataname = 'IDS'
input_folder = f'./data/{dataname}' # the path to the dataset folder
output_json_folder = f'./result/{dataname}' # the path to the result folder

openai_api_key = "your_api_key"

client = OpenAI(api_key = openai_api_key)

current_date = datetime.now().strftime("%y%m%d_%H:%M")
log_file_name = f"{current_date}.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"./log/{dataname}/{log_file_name}")
logger.addHandler(file_handler)

for run_idx in range(repeat_count):
    idx = run_idx+2
    print(f"\n=== Run {idx} ===\n")
    current_date = datetime.now().strftime("%y%m%d_%H%M")

    for file_name in os.listdir(input_folder):
        print(file_name)
        # file_name = 'xxxx.csv'
        if file_name.endswith(".csv"):
            print(f"processing: {file_name}")
            full_path = os.path.join(input_folder, file_name)
            df = pd.read_csv(full_path)   
            conv_data = df.values.tolist()

            context = ""
            # the current prompt_fix is tailored to our task. To get the best result, modification of the prompt to fit the context or the data is recommended.
            prompt_fix = '''
            Task Description: You are a teacher who is assessing the students' collaborative competency. To do so, you have to determine which category each utterance falls into. For each utterance, first generate who the addressee is. Second, generate the intention of each utterance. Then, find the category that best fits the intention. Follow the instructions in "Categories" strictly.

            Given Situation: A small group of students collaborate to solve 3 data visualization tasks. The exercises are guided by an agent named “OPEBot”. In completing three tasks, each student is assigned by the bot to one of three roles: driver, navigator, or researcher. At the end of each task, OPEBot asks the students questions and students answer the question.

            Categories:
            (x): none of above. these are the cases including greetings, wrap-up, responding to the bot, or other cases which do not fall into other categories such as utterances not related to problem solving, talk about whether something looks good, requesting others to do something, talk about progress or whether to move on to the next step, or talk about technical issues.
                - For utterances before the OPEbot starts the task or after the OPEbot ends the task should be (x).
                - Saying Drama, Comedy, Romance, Actions, or Thriller with no context should be (x).
            (-): OPEbot's utterance
            (a): these are the cases where a student proposes or improve specific solution related to the data visualiation task, or talks about givens and constraints of the tasks. 
                - propose or improve specific solution: these are the cases where a student proposes solutions to the given problem, or build up on current solution. Methodological approach such as suggesting to review or understand the situation should be labeled as (x). If the solution has a question mark or is in interrogative sentence, label as (b). If the addressee is OPEBot, label as (x). Note that the utterances that can be answers to the bot's question should be labeled as (x). 
                - talks about givens and constraints of a specific task: these are the cases where a student talks about the information given by OPEBot such as roles or jupyter file such as a description of certain functions. This does not include the progress.
            (b): these are the cases where a student confirms understanding by asking questions / paraphrasing, or intrude others
                - confirms understanding by asking questions/paraphrasing: the utterances should be directly related to solving the given problem. these are the cases where a student ask questions about other's opinions, or propose a solution with a question mark or is in interrogative sentence. Asking about current task state should be labeled as (x). Talking about the progress or the process should be labeled as (x). Note that technical issues should be categorized as (x). This does not include answering to others in order to confirm. 
            (c): these are the cases where student respond when spoken to by others, makes an attempt after discussion, be rude to others, or provide reason to support a solution.
                - respond when spoken to by others: these are the cases where a student responds to questions or agree to a proposed solution. If the response does not contain any information nor directed to them, label as (x). If the addressee is OPEBot, label as (x).
                - makes an attempt after discussion: these are the cases where a student makes or asks an attempt after discussion. Some examples can be executing a code.
                - provides reasons to support/refute a potential solution: these are the cases where students provide reasons for a proposed solution. Some examples can be a sentence with “since” or “because”.
            (d): these are the cases where student talks about results or brings up giving up a challenge.
                - talks about results: these are the cases where a student talks about task execution results, expected result or errors. However, if such result is about technical issue, the label should be (x).
            (e): these are the cases where a student is not focused on tasks and assigned roles, or engage in off-topic conversation. Be very strict on using this label.
                - These does not include student's answers to the OPEBot or repeating others.
                - Some examples of not being focused on tasks are asking others what step they are on.
                - Engage in off-topic conversation: There should be a specific topic that is not related to problem-solving. This does not include abbreviation such as 'lol', or 'ikr'. Amusement or greeting should be labeled as (x).
            (f): these are the cases where a student asks others for suggestion, provide help, compliment or encourages others.
                - Asks if others have suggestions: these are the cases where a student ask for others’ opinions. However, if the utterance is about the solution or establishing common ground, the label should be (d). If a student suggest something to others, label as (x).
                - Asks to take action before anyone on the team asks for help: these are the cases where a student asks if others need help preemptively. If s student request others to do something, label as (x).
                - Compliments or encourages others: these are the cases where a student encourage others. Some examples a student can say are “great”, “sweet”, “nice”, “cool”, or “awesome”. This does not include “thanks”

            Use cases:
            The speaker is proposing an answer: If the answer has a question mark or is in interrogative sentence, label as (b). If the addressee is the OPEBot, label as (x). In other cases, label as (a).
            The speaker is replying to others: If the speaker is talking about answers, label as (a). If the speaker is answering to a question directed to them, label as (c). If the speaker is agreeing to others’ utterance which are not a question or an answer, label as (x). If the addressee is the OPEBot, label as (x).
            The speaker is talking about result: If the addressee is the OPEBot, label as (x). If the speaker is talking about technical issues, label as (x). If else, label as (d).
            The speaker is asking questions: If the speaker is asking for suggestion, label as (f). If the speaker is asking a question about the given problem of solution, label as (b).

            Generate the output in the following dictionary format:
            {
                "utt": "<Utterance of the speaker>",
                "speaker": "<Speaker>",
                "intention": "<Speaker's intention>",
                "addressee": "<Addressee of the utterance>",
                "category": "<Category>"
            }
            '''
            prompt = prompt_fix
            result = []
            for i, line in enumerate(conv_data):
                if i > 5: 
                    context_data = conv_data[i-5:i]
                else:
                    context_data = conv_data[:i]
                
                for c in context_data:
                    context = context + f"{c[1]}: \"{c[4]}\"\n"

                if context_data:
                    prompt = prompt + f"context:\n{context}\n"

                user_prompt = f"{line[1]} says \"{line[4]}\"\n"
                user_prompt = user_prompt + f"what category does {line[1]}\'s intention falls into?" 
                
                logger.info(prompt)
                logger.info(user_prompt)
                response = client.chat.completions.create(  
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0
                )
                logger.info(response.choices[0].message.content)
                temp_result = response.choices[0].message.content

                dict_flag = 0
                while dict_flag == 0:
                    try:
                        # print(temp_result)
                        if '```json' in temp_result:
                            temp_result = temp_result.split('```json')[1].replace('```','')
                        print(temp_result)
                        temp_result = eval(temp_result)
                        if isinstance(temp_result, dict) and "category" in temp_result.keys():
                            dict_flag = 1
                    except:
                        # print("***** something went wrong *****")
                        # print(temp_result)
                        # print(eval(temp_result))
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            max_tokens=1000,
                            temperature=0
                        )
                        temp_result = response.choices[0].message.content
                        logger.info(response.choices[0].message.content)
                temp_result["idx"] = i
                result.append(temp_result) 
     
                logger.info(response)
                logger.info(response.choices[0].message.content)
               
                context = ""
                prompt = prompt_fix
            
        print(f"Length of df: {len(df)}")
        print(f"Length of result: {len(result)}")
        pred = [lab["category"].split(')')[0].strip('(').strip(')') for lab in result] 
        df["pred"] = pred 
        df.to_csv(f'{output_json_folder}/run{idx}_{file_name}', index=False)

        base_name = file_name.replace(".csv", "")
        json_output_name = f'{output_json_folder}/{current_date}_run{idx}_{base_name}.json'
        with open(json_output_name, 'w+') as f:
            json.dump(result, f)
        # kappa = calcu_kappa_subfacet(df[["Indicator"]].values, df[["pred"]].values) 
        # print(kappa)


        # file_name = f'./result/{current_date}_{file_name}_{kappa:.4f}.json'


    
