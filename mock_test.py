import asyncio
from openai_multi_client import OpenAIMultiClient, Payload, OpenAIMultiOrderedClient


def test(ordered):
    async def mock(payload: Payload):
        import random

        rand_wait_time = random.random()
        await asyncio.sleep(rand_wait_time)
        rand_fail = random.random()
        if rand_fail < 0.3:
            raise Exception("Mocked exception")
        return {"response": f"mocked {payload.metadata.get('id')}"}

    if ordered:
        api = OpenAIMultiOrderedClient(custom_api=mock, max_retries=3, retry_multiplier=2)
    else:
        api = OpenAIMultiClient(custom_api=mock, max_retries=3, retry_multiplier=2)

    def put_data():
        for pid in range(100):
            pid = pid + 1
            print(f"Requesting {pid}")
            api.request({"prompt": f"This is test {pid}"}, metadata={'id': pid},
                        endpoint="completions")

    api.run_request_function(put_data)

    print('*' * 20)
    i = 0
    failed = 0
    for response in api:
        i += 1
        if response.failed:
            failed += 1
            print(f"Failed {response.metadata.get('id')}: {i}/100")
        else:
            print(f"Got response {response.metadata.get('id')}: {i}/100")


    print('*' * 20)
    print(f"Total failed: {failed}/100")
    print('*' * 20)


if __name__ == '__main__':
    test(ordered=False)
    test(ordered=True)
