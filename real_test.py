import os
from openai_multi_client import OpenAIMultiClient


def test():
    if 'OPENAI_API_KEY' not in os.environ:
        raise Exception("Please set the OPENAI_API_KEY environment variable to run this test")
    api = OpenAIMultiClient(endpoint="chats", data_template={"model": "gpt-3.5-turbo"})

    def make_requests():
        for pid in range(9):
            pid = pid + 1
            print(f"Requesting {pid}")
            api.request(data={
                "messages": [{"role": "user", "content": f"Can you tell me what is {pid} * {pid}?"}]
            }, metadata={'id': pid})

    api.run_request_function(make_requests)

    print('*' * 20)
    i = 0
    failed = 0
    for result in api:
        i += 1
        if result.failed:
            failed += 1
            print(f"Failed {result.metadata['id']}")
        else:
            print(f"Got response for {result.metadata['id']}:", result.response['choices'][0]['message']['content'])

    print('*' * 20)
    print(f"Total failed: {failed}")
    print('*' * 20)


if __name__ == '__main__':
    test()
