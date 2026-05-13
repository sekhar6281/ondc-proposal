import asyncio
import edge_tts

EN_VOICE = "en-IN-PrabhatNeural"
TE_VOICE = "te-IN-MohanNeural"

scripts = {
    "en_01": "AP Commerce Stack is Andhra Pradesh's own digital commerce platform — where every order placed, every rupee earned, and every data point generated belongs to the state, not to a private company. Proposed by Zian Technologies LLP, Visakhapatnam — built to make the CM's vision of One Entrepreneur Per One Family a measurable, funded reality.",
    "te_01": "AP కామర్స్ స్టాక్ అనేది ఆంధ్రప్రదేశ్ సొంత డిజిటల్ వాణిజ్య వేదిక — ఇక్కడ జరిగే ప్రతి ఆర్డర్, సంపాదించిన ప్రతి రూపాయి, తయారైన ప్రతి డేటా రాష్ట్రానిదే, ఏ ప్రైవేట్ కంపెనీదీ కాదు. జియాన్ టెక్నాలజీస్ LLP, విశాఖపట్నం సమర్పించింది — సీఎం ఒక్కో కుటుంబానికి ఒక్కో వ్యాపారవేత్త అనే దార్శనికతను నిజంగా అమలు చేయడానికి.",
}

async def generate(key, text):
    voice = EN_VOICE if key.startswith("en") else TE_VOICE
    out = f"audio/{key}.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out)
    print(f"Generated: {out}")

async def main():
    for key, text in scripts.items():
        await generate(key, text)

if __name__ == "__main__":
    asyncio.run(main())
