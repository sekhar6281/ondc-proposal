import asyncio
import edge_tts

EN_VOICE = "en-IN-PrabhatNeural"
TE_VOICE = "te-IN-MohanNeural"

scripts = {
    "en_01": "AP Commerce Stack is Andhra Pradesh's own digital commerce platform — where every order placed, every rupee earned, and every data point generated belongs to the state, not to a private company. Proposed by Zian Technologies LLP, Visakhapatnam — built to make the CM's vision of One Entrepreneur Per One Family a measurable, funded reality.",
    "te_01": "AP కామర్స్ స్టాక్ అనేది ఆంధ్రప్రదేశ్ సొంత డిజిటల్ వాణిజ్య వేదిక — ఇక్కడ జరిగే ప్రతి ఆర్డర్, సంపాదించిన ప్రతి రూపాయి, తయారైన ప్రతి డేటా రాష్ట్రానిదే, ఏ ప్రైవేట్ కంపెనీదీ కాదు. జియాన్ టెక్నాలజీస్ LLP, విశాఖపట్నం సమర్పించింది — సీఎం ఒక్కో కుటుంబానికి ఒక్కో వ్యాపారవేత్త అనే దార్శనికతను నిజంగా అమలు చేయడానికి.",
    "en_02": "Every single day, Swiggy, Amazon, and Flipkart collect 18–35% commission from AP's own consumers and MSMEs — and the state of Andhra Pradesh receives zero rupees from transactions happening on its own soil. AP built the market, AP has the people — Zian Technologies LLP is here to make sure AP finally keeps the money too.",
    "te_02": "రోజూ Swiggy, Amazon, Flipkart లు AP వినియోగదారుల నుండి 18–35% కమీషన్ తీసుకుంటున్నాయి — AP సొంత భూమిపై జరిగే లావాదేవీల నుండి రాష్ట్రానికి ఒక్క రూపాయి కూడా రావట్లేదు. AP మార్కెట్ సృష్టించింది, AP దగ్గర జనం ఉన్నారు — ఆ డబ్బు కూడా AP కే చెందేలా చేయడానికి జియాన్ టెక్నాలజీస్ LLP ఇక్కడ ఉంది.",
    "en_03": "ONDC is already processing 14 lakh transactions daily across India — and not a single South Indian state has claimed Network Participant status yet, leaving that first-mover advantage open for AP to take today. Zian Technologies LLP has the technical readiness and ONDC expertise to make AP that first mover — immediately.",
    "te_03": "ONDC ఇప్పటికే భారతదేశంలో రోజుకు 14 లక్షల లావాదేవీలు నిర్వహిస్తోంది — ఇంకా ఒక్క దక్షిణ భారత రాష్ట్రం కూడా నెట్‌వర్క్ పార్టిసిపెంట్ హోదా తీసుకోలేదు, ఆ అవకాశం AP కోసం నేటికీ తెరుచుకునే ఉంది. జియాన్ టెక్నాలజీస్ LLP సాంకేతిక సంసిద్ధత మరియు ONDC నైపుణ్యంతో AP ని వెంటనే ఆ స్థానంలో నిలపగలదు.",
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
