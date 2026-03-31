import json
import collections
import string
import re
import asyncio
import csv
from rouge_score import rouge_scorer
import numpy as np


from openai import AsyncOpenAI
import os

#global client
aclient = AsyncOpenAI(
	api_key=os.getenv("OPENAI_API_KEY"),
	base_url=os.getenv("OPENAI_BASE_URL")
)


#global model name
MODEL_NAME = "kimi-k2.5"
DISABLE_THINKING = os.getenv("DISABLE_THINKING", "1") == "1"

#global eval dataset path
eval_dataset_path = "data/2wikimqa_200_samples_from_blend.json"
save_results_path = f"results/{MODEL_NAME}.csv"


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

def compute_f1(a_pred, a_gold):
    if a_pred is None or len(a_pred) == 0:
        print(f"WARNING:a_pred is None or empty for response: {a_pred}")
        return 0, 0, 0

    if a_gold is None or len(a_gold) == 0:
        print(f"WARNING:a_gold is None or empty for response: {a_gold}")
        return 0, 0, 0

    a_pred = parse_generation(a_pred)
    normalized_prediction = normalize_answer(a_pred)
    normalized_ground_truth = normalize_answer(a_gold)

    if normalized_prediction in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return 0, 0, 0
    if normalized_ground_truth in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return 0, 0, 0

    #here each word is a token
    #I do not think we should involve an external LLM tokenizer to compute the F1 score
    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    common = collections.Counter(prediction_tokens) & collections.Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0, 0, 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, precision, recall

def compute_rl(pred, gold):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rougeL = scorer.score(gold, pred)['rougeL'].fmeasure
    return rougeL



async def get_response_async(prompt):
    request_kwargs = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_completion_tokens": 20,
    }
    if DISABLE_THINKING:
        request_kwargs["extra_body"] = {"thinking": {"type": "disabled"}}

    completion = await aclient.chat.completions.create(**request_kwargs)

    print("="*50+"completion as json"+"="*50)
    print(completion.model_dump_json())

    print("="*55+"response"+"="*55)
    print(completion.choices[0].message.content)

    return completion.choices[0].message.content


async def get_responses_batched_async(prompts, max_concurrency=4):
    semaphore = asyncio.Semaphore(max_concurrency)
    responses = [None] * len(prompts)

    async def _run_one(idx, prompt):
        async with semaphore:
            responses[idx] = await get_response_async(prompt)

    await asyncio.gather(*[_run_one(idx, prompt) for idx, prompt in enumerate(prompts)])
    return responses


async def main():
    try:
        with open(eval_dataset_path) as f:
            eval_dataset = json.load(f)
        print(f"Dataset loaded successfully with {len(eval_dataset)} samples from {eval_dataset_path}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        exit(1)
    

    with open(save_results_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "question", "answers", "response", "f1", "precision", "recall", "rl"])

    #CacheBlend Prompt
    #prefix_prompt = "Answer the question based on the given passages. Only give me the answer and do not output any other words.\n\nThe following are given passages.\n"
    #query_prompt = f"\n\nAnswer the question based on the given passages. Answer the question within 5 words. Do NOT repeat the question or output any other words. Question: "

    f1_list =[]
    rl_list =[]
    precision_list =[]
    recall_list =[]
    #max_ctx_len = 4096-196

    MAX_SAMPLES = int(os.getenv("MAX_SAMPLES", "200"))
    REQUEST_BATCH_SIZE = int(os.getenv("REQUEST_BATCH_SIZE", "20"))

    selected_samples = eval_dataset[:MAX_SAMPLES]
    for batch_start in range(0, len(selected_samples), REQUEST_BATCH_SIZE):
        batch = selected_samples[batch_start : batch_start + REQUEST_BATCH_SIZE]

        prompts = []
        questions = []
        answers_list = []
        sample_indices = []

        for i, ex in enumerate(batch):
            idx = batch_start + i
            print(f"Processing sample {idx+1} of {len(selected_samples)}")

            question = normalize_question(ex["question"])
            answers = ex["answers"][0][0]
            ctxs = ex["ctxs"]

            print(f"Question: {question}")
            print(f"Answers: {answers}")

            context = ""
            for ctx in ctxs:
                context += f"{ctx['title']}\n\n{ctx['text']}\n\n"

            print(f"Context: {len(ctxs)} chunks with total {len(context)} characters")

            #we use longbench's prompt template for 2WikiMQA
            prompt = f"Answer the question based on the given passages. Only give me the answer and do not output any other words.\nThe following are given passages.\n{context}\nAnswer the question based on the given passages. Only give me the answer and do not output any other words.\nQuestion: {question} Answer:"
            print(f"Prompt(short): {prompt[:500]}\n......\n{prompt[-500:]}")

            prompts.append(prompt)
            questions.append(question)
            answers_list.append(answers)
            sample_indices.append(idx + 1)

        if os.getenv("DEBUG_MODE", "1") == "1":
            responses = ["yes"] * len(prompts)
        else:
            responses = await get_responses_batched_async(
                prompts, max_concurrency=REQUEST_BATCH_SIZE
            )

        for i, response in enumerate(responses):
            question = questions[i]
            answers = answers_list[i]
            sample_idx = sample_indices[i]

            print(f"Response: {response}")

            f1, precision, recall = compute_f1(response, answers)
            print(f"F1: {f1}, Precision: {precision}, Recall: {recall}")
            f1_list.append(f1)
            precision_list.append(precision)
            recall_list.append(recall)
            rl = compute_rl(response, answers)
            print(f"RL: {rl}")
            rl_list.append(rl)

            with open(save_results_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([sample_idx, question, answers, response, f1, precision, recall, rl])
        
    print("---------------Result Summary---------------------")
    avg_f1 = np.mean(f1_list)
    avg_precision = np.mean(precision_list)
    avg_recall = np.mean(recall_list)
    avg_rl = np.mean(rl_list)
    with open(save_results_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["", "", "", "", avg_f1, avg_precision, avg_recall, avg_rl])
    print(f"F1: {avg_f1}")
    print(f"Precision: {avg_precision}")
    print(f"Recall: {avg_recall}")
    print(f"RL: {avg_rl}")
    print("----------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(main())