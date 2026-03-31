import json
import collections
import string
import re
from rouge_score import rouge_scorer
import numpy as np
from transformers import AutoTokenizer


from openai import OpenAI
import os

#global client
client = OpenAI(
	api_key=os.getenv("OPENAI_API_KEY"),
	base_url=os.getenv("OPENAI_BASE_URL")
)


#global model name
MODEL_NAME = "kimi-k2.5"
tokenizer = AutoTokenizer.from_pretrained("moonshotai/Kimi-K2.5")

#global eval dataset path
eval_dataset_path = "2wikimqa_200_samples_from_blend.json"



def normalize_question(question):
    if not question.endswith("?"):
        question = question + "?"

    return question[0].lower() + question[1:]

def parse_generation(s):
    s = s.lstrip('\n').split('\n')[0]
    if s.startswith("Yes") or s.startswith("yes"):
        s = "Yes"
    elif (s.split()[0]).startswith("No") or (s.split()[0]).startswith("no"):
        s = "No"
    return s

def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))



def build_fewshot_prompt(example):
    q = "\n\n"+example["question"]
    doc_prompts = [f"{ctx['text']}" for ctx in example["ctxs"]]
    q_prompt = f"{q}"
    return doc_prompts, q_prompt

def compute_f1(a_pred, a_gold, tokenizer):
    a_pred = parse_generation(a_pred)
    gold_toks = tokenizer.encode(normalize_answer(a_gold))
    pred_toks = tokenizer.encode(normalize_answer(a_pred))
    common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
    num_same = sum(common.values())
    if len(gold_toks) == 0 or len(pred_toks) == 0:
        # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
        return int(gold_toks == pred_toks)
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(pred_toks)
    recall = 1.0 * num_same / len(gold_toks)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

def compute_rl(pred, gold):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rougeL = scorer.score(gold, pred)['rougeL'].fmeasure
    return rougeL




def get_completion(prompt):
    completion = client.chat.completions.create(
        model=MODEL_NAME,  
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': prompt}],
        max_completion_tokens=20,  # newer parameter (recommended), old version is max_tokens
    )
    return completion.choices[0].message.content


def main():
    try:
        with open(eval_dataset_path) as f:
            eval_dataset = json.load(f)
        print(f"Dataset loaded successfully with {len(eval_dataset)} samples")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        exit(1)

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

    prefix_prompt = "Answer the question based on the given passages. Only give me the answer and do not output any other words.\n\nThe following are given passages.\n"
    query_prompt = f"\n\nAnswer the question based on the given passages. Answer the question within 5 words. Do NOT repeat the question or output any other words. Question: "

    f1_list =[]
    rl_list =[]
    #max_ctx_len = 4096-196

    for idx, ex in enumerate(eval_dataset):
        print(f"Processing sample {idx+1} of {len(eval_dataset)}")

        question = ex["question"]
        question = normalize_question(question)
        answers = ex["answers"][0][0]

        ctxs = ex["ctxs"]
        print(f"Question: {question}")
        print(f"Contexts: {ctxs}")
        print(f"Answers: {answers}")

        context=""
        for ctx in ctxs:
            context += f"{ctx['title']}\n\n{ctx['text']}\n\n"
        

        #we use longbench's prompt template for 2WikiMQA
        prompt = f"Answer the question based on the given passages. Only give me the answer and do not output any other words.\nThe following are given passages.\n{context}\nQuestion: {question} Answer:"

        response = get_completion(prompt)
        print(f"Response: {response}")

        f1 = compute_f1(response, answers, tokenizer)
        print(f"F1: {f1}")
        f1_list.append(f1)

        rl = compute_rl(response, answers)
        print(f"RL: {rl}")
        rl_list.append(rl)
        
    print("---------------Result Summary---------------------")
    print(f"F1: {np.mean(f1_list)}")
    print(f"RL: {np.mean(rl_list)}")

if __name__ == "__main__":
    main()