import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-06-01-preview"

API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
assert API_KEY, "ERROR: Azure OpenAI Key is missing"
openai.api_key = API_KEY

RESOURCE_ENDPOINT = os.getenv("OPENAI_API_BASE", "").strip()
assert RESOURCE_ENDPOINT, "ERROR: Azure OpenAI Endpoint is missing"
assert "openai.azure.com" in RESOURCE_ENDPOINT.lower(), "ERROR: Azure OpenAI Endpoint should be in the form: \n\n\t<your unique endpoint identifier>.openai.azure.com"
openai.api_base = RESOURCE_ENDPOINT

model = "gpt-35-turbo"
deployment_default = "gpt-35-turbo-16k"
deployment_gpt4 = "gpt-4"


def request(text_prompt: str):
    return openai.ChatCompletion.create(
        engine=model,
        max_tokens=60,
        messages=[
            {"role": "user", "content": text_prompt},
        ]
    )


def get_parking_summary(data):
    messages = [
        {
            "role": "system",
            "content": """
                You are assistant of parking service. You only response result as json.
                Please do not include ```json ``` either.
                
                Dataset contains content, score, provider_name, and name in csv format.                
                content is a subjective expression, score is a user evaluation score, and provider_name is the parking lot name.
                
                Group by provider_name, then extract words from content and summarize frequently used keywords.
                Extract only meaningful words from other users when using the parking lot.
                You need to analyze whether the content is positive or negative.
                Provide positive words as positive_keywords and words with negative meaning as negative_keywords.                
                Please provide a maximum of 5 each positive/negative word.                
                
                The json example is:
                [
                    {                        
                        "provider_name": "주차장",                        
                        "positive_keywords": ["넓다"]
                        "negative_keywords": ["좁다", "비싸다"]
                    }
                ]                            
            """
        },
        {
            "role": "user",
            "content": ("""
                아래 csv 데이터에서 다른 사용자에게 의미있는 요약 정보 알려줘.
                %s
            """) % (data.to_string)
        }
    ]

    response = openai.ChatCompletion.create(
        deployment_id=deployment_gpt4,
        messages=messages,
        temperature=0,
        max_tokens=4096
    )

    # print(response)
    print(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]


def get_parking_suggest(model_name: str = ""):
    messages = [
        {
            "role": "system",
            "content": """
                You are assistant of parking service. You only response result as json.
                Dataset contains content, score, provider_name, and name.

                First filter data by name matches input model name.

                Then you suggest provider_name from filterd dataset by positive content and higher score.
                The score is from 1 to 5 and 5 is max.
                And the suggestion is effected by content more.

                And find most positive content from filtered dataset as reason.

                Expansive is negative.

                The json example is
                {
                    "model_name": "카니발",
                    "provider_name": "주차장",
                    "reason": "넓다"
                }

                If you cannot found the provider_name sample:
                {
                    "model_name": "카니발",
                    "provider_name": null,
                    "reason": "데이터가 없음"
                }
            """
        },
        {
            "role": "user",
            "content": ("""
                아래 데이터에서 %s인 차량이 제일 선호하는 주차장 1개만 그리고 이유를 알려줘
                %s
            """) % (model_name, model_name)
        }
    ]

    response = openai.ChatCompletion.create(
        deployment_id=deployment_default,
        messages=messages,
        temperature=0,
        max_tokens=10000
    )

    # print(response)
    # print(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]
