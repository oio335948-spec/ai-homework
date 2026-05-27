import os, json, requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("Қоршаған ортада OPENAI_API_KEY орнатылмаған")

CHAT_URL = f"{BASE_URL}/chat/completions"

SYSTEM_PROMPT = (
    "Сен — Қазақстандағы 9-сынып оқушыларын математикадан (Алгебра және Геометрия) мемлекеттік бітіру емтиханына (ГОС) дайындауға мамандандырылған ИИ-репетиторсың.\n"
    "Сенің мақсатың — оқушыларға дайын жауапты бере салаймай, есептің шығарылу жолын түсінуге көмектесу.\n"
    "Жауап беру ережелері:\n"
    "1. Сұрақ қай тілде қойылса, сол тілде (Қазақша немесе Орысша) жауап бер.\n"
    "2. Егер пайдаланушы есепті шығарып беруді сұраса, шешімін 3-4 түсінікті қадамға бөл. Қолданылатын формулалар мен теоремаларды міндетті түрде көрсет.\n"
    "3. Әр шешімнің соңына '💡 Внимание (Маңызды):' деген бөлім қосып, оқушыларға осы тақырыпта емтиханда жиі жіберетін қателіктері туралы ескерт (мысалы, ММЖ (ОДЗ) немесе мүшелерді көшіргендегі таңбалар туралы).\n"
    "4. Түсінікті математикалық жазбаны қолдан (мысалы, x^2, sqrt(x))."
)

def ask_llm(question: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.2
    }
    try:
        resp = requests.post(
            CHAT_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload),
            timeout=60
        )
        resp.raise_for_status()
        obj = json.loads(resp.text)
        return obj["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Сұраныс қатесі: {e}"

def main():
    print("🧮 Математикадан мемлекеттік емтиханға (ГОС) дайындау боты іске қосылды. Есепті енгіз (немесе шығу үшін /exit деп жаз):")
    while True:
        try:
            q = input("\nСен: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nБоттан шығу...")
            break
        if not q:
            continue
        if q.lower() in ("/exit", "exit", "quit"):
            print("Боттан шығу...")
            break
        print(f"\nБот:\n{ask_llm(q)}")

if __name__ == "__main__":
    main()