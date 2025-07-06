import json
import time

import requests

# 서버 설정
BASE_URL = "https://langgraph-agent-v2.1xe7hspvt1x3.us-south.codeengine.appdomain.cloud"
# BASE_URL = "http://localhost:8080"
CHAT_ENDPOINT = f"{BASE_URL}/chat/completions"


def test_chat_completion_with_api_key():
    """API 키를 사용한 채팅 완성 테스트"""
    print("=== API 키를 사용한 테스트 ===")

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "test_api_key_123",  # 아무 키나 사용 가능
    }

    payload = {
        # "model": "meta-llama/llama-3-2-90b-vision-instruct",
        "messages": [
            {"role": "user", "content": "who is the president of South Korea?"}
        ],
        "stream": False,
    }

    try:
        response = requests.post(CHAT_ENDPOINT, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_chat_completion_with_bearer_token():
    """Bearer 토큰을 사용한 채팅 완성 테스트"""
    print("\n=== Bearer 토큰을 사용한 테스트 ===")

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer test_bearer_token_456",  # 아무 토큰이나 사용 가능
    }

    payload = {
        # "model": "meta-llama/llama-3-2-90b-vision-instruct",
        "messages": [
            {
                "role": "user",
                "content": "파이썬으로 'Hello World'를 출력하는 코드를 작성해주세요.",
            }
        ],
        "stream": False,
    }

    try:
        response = requests.post(CHAT_ENDPOINT, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_chat_completion_without_auth():
    """인증 없이 채팅 완성 테스트"""
    print("\n=== 인증 없이 테스트 ===")

    headers = {"Content-Type": "application/json"}

    payload = {
        # "model": "meta-llama/llama-3-2-90b-vision-instruct",
        "messages": [
            {"role": "user", "content": "인증 없이도 작동하는지 테스트해보겠습니다."}
        ],
        "stream": False,
    }

    try:
        response = requests.post(CHAT_ENDPOINT, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_chat_completion_with_thread_id():
    """Thread ID를 포함한 채팅 완성 테스트"""
    print("\n=== Thread ID를 포함한 테스트 ===")

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "test_api_key_789",
        "X-IBM-THREAD-ID": "test_thread_123",
    }

    payload = {
        # "model": "meta-llama/llama-3-2-90b-vision-instruct",
        "messages": [
            {"role": "user", "content": "이것은 특정 스레드에서의 대화입니다."}
        ],
        "stream": False,
        "extra_body": {"thread_id": "extra_thread_456"},
    }

    try:
        response = requests.post(CHAT_ENDPOINT, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_streaming_chat_completion():
    """스트리밍 채팅 완성 테스트"""
    print("\n=== 스트리밍 테스트 ===")

    headers = {"Content-Type": "application/json", "X-API-Key": "stream_test_key"}

    payload = {
        # "model": "meta-llama/llama-3-2-90b-vision-instruct",
        "messages": [
            {"role": "user", "content": "스트리밍으로 긴 답변을 생성해주세요."}
        ],
        "stream": True,
    }

    try:
        response = requests.post(
            CHAT_ENDPOINT, headers=headers, json=payload, stream=True
        )
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("스트리밍 응답:")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:]  # 'data: ' 제거
                        if data != "[DONE]":
                            try:
                                json_data = json.loads(data)
                                if "choices" in json_data and json_data["choices"]:
                                    content = (
                                        json_data["choices"][0]
                                        .get("delta", {})
                                        .get("content", "")
                                    )
                                    if content:
                                        print(content, end="", flush=True)
                            except json.JSONDecodeError:
                                pass
                        else:
                            print("\n[스트리밍 완료]")
                            break
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_invalid_payload():
    """잘못된 페이로드 테스트"""
    print("\n=== 잘못된 페이로드 테스트 ===")

    headers = {"Content-Type": "application/json", "X-API-Key": "test_key"}

    # messages가 없는 잘못된 페이로드
    payload = {"model": "meta-llama/llama-3-2-90b-vision-instruct", "stream": False}

    try:
        response = requests.post(CHAT_ENDPOINT, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code != 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_thread_id_conversation_memory():
    """Thread ID가 대화 기억에 영향을 주는지 테스트"""
    print("\n=== Thread ID 대화 기억 테스트 ===")

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "test_key",
        "X-IBM-THREAD-ID": "memory_test_thread",
    }

    # 첫 번째 메시지
    payload1 = {
        # "model": "meta-llama/llama-3-2-90b-vision-instruct",
        "messages": [
            {"role": "user", "content": "내 이름은 김철수입니다. 기억해주세요."}
        ],
        "stream": False,
    }

    try:
        response1 = requests.post(CHAT_ENDPOINT, headers=headers, json=payload1)
        print(f"첫 번째 요청 Status Code: {response1.status_code}")
        print(
            f"첫 번째 응답: {json.dumps(response1.json(), indent=2, ensure_ascii=False)}"
        )

        # 두 번째 메시지 (이름을 물어봄)
        payload2 = {
            # "model": "meta-llama/llama-3-2-90b-vision-instruct",
            "messages": [{"role": "user", "content": "내 이름이 뭐였죠?"}],
            "stream": False,
        }

        response2 = requests.post(CHAT_ENDPOINT, headers=headers, json=payload2)
        print(f"\n두 번째 요청 Status Code: {response2.status_code}")
        print(
            f"두 번째 응답: {json.dumps(response2.json(), indent=2, ensure_ascii=False)}"
        )

        # 세 번째 메시지 (이전 대화 포함)
        payload3 = {
            # "model": "meta-llama/llama-3-2-90b-vision-instruct",
            "messages": [
                {"role": "user", "content": "내 이름은 김철수입니다. 기억해주세요."},
                {"role": "assistant", "content": "네, 김철수님을 기억하겠습니다."},
                {"role": "user", "content": "내 이름이 뭐였죠?"},
            ],
            "stream": False,
        }

        response3 = requests.post(CHAT_ENDPOINT, headers=headers, json=payload3)
        print(f"\n세 번째 요청 Status Code: {response3.status_code}")
        print(
            f"세 번째 응답: {json.dumps(response3.json(), indent=2, ensure_ascii=False)}"
        )

        return (
            response1.status_code == 200
            and response2.status_code == 200
            and response3.status_code == 200
        )
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests():
    """모든 테스트 실행"""
    print("🚀 FastAPI 채팅 엔드포인트 테스트 시작")
    print("=" * 50)

    tests = [
        ("API 키 테스트", test_chat_completion_with_api_key),
        ("Bearer 토큰 테스트", test_chat_completion_with_bearer_token),
        ("인증 없이 테스트", test_chat_completion_without_auth),
        ("Thread ID 테스트", test_chat_completion_with_thread_id),
        ("스트리밍 테스트", test_streaming_chat_completion),
        ("잘못된 페이로드 테스트", test_invalid_payload),
        ("Thread ID 대화 기억 테스트", test_thread_id_conversation_memory),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name} 실행 중...")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 성공" if result else "❌ 실패"
            print(f"{test_name}: {status}")
        except Exception as e:
            print(f"{test_name}: ❌ 오류 발생 - {e}")
            results.append((test_name, False))

        time.sleep(1)  # 요청 간 간격

    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약:")
    for test_name, result in results:
        status = "✅ 성공" if result else "❌ 실패"
        print(f"  {test_name}: {status}")

    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    print(f"\n총 {total_count}개 테스트 중 {success_count}개 성공")


if __name__ == "__main__":
    # 서버가 실행 중인지 확인
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ 서버가 실행 중입니다!")
            run_all_tests()
        else:
            print("❌ 서버에 연결할 수 없습니다.")
    except requests.exceptions.ConnectionError:
        print("❌ 서버가 실행되지 않았습니다.")
        print("다음 명령어로 서버를 먼저 실행해주세요:")
        print("python app.py")
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
