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
    "en_04": "Just as NPCI owns UPI, Government of AP will own APCS — the state's digital commerce operating system built on ONDC, where AP controls the platform, the data, and the revenue, with Zian Technologies LLP building and running it as appointed TSP.",
    "te_04": "NPCI UPIని స్వంతం చేసుకున్నట్టే, AP ప్రభుత్వం APCSని స్వంతం చేసుకుంటుంది — ONDC పైన నిర్మించిన రాష్ట్ర డిజిటల్ వాణిజ్య వ్యవస్థ, ప్లాట్‌ఫారమ్, డేటా, ఆదాయం అన్నీ AP వే, జియాన్ టెక్నాలజీస్ LLP నియమిత TSPగా దాన్ని నిర్మించి నడుపుతుంది.",
    "en_05": "Eight verticals under one government-owned roof — food, grocery, tickets, services, GI crafts, agri, MSMEs, and D2C — every sector AP earns zero from today becomes a direct state revenue source tomorrow, all operated by Zian Technologies LLP.",
    "te_05": "ఒకే ప్రభుత్వ వేదిక కింద ఎనిమిది విభాగాలు — ఆహారం, కిరాణా, టికెట్లు, సేవలు, GI క్రాఫ్ట్స్, వ్యవసాయం, MSMEలు, D2C — ఈరోజు AP సున్నా సంపాదిస్తున్న ప్రతి రంగం రేపు నేరుగా రాష్ట్ర ఆదాయ వనరుగా మారుతుంది, అన్నీ జియాన్ టెక్నాలజీస్ LLP నిర్వహిస్తుంది.",
    "en_06": "Six income streams start flowing from Month 1 — transaction fees, advertising, GI certification, seller subscriptions, GST services, and government procurement — all to the state exchequer, every rate decided by Government of AP, no ceiling.",
    "te_06": "నెల 1 నుండే ఆరు ఆదాయ వనరులు మొదలవుతాయి — లావాదేవీ రుసుము, యాడ్స్, GI సర్టిఫికేషన్, విక్రేత సభ్యత్వాలు, GST సేవలు, ప్రభుత్వ కొనుగోలు — అన్నీ రాష్ట్ర ఖజానాకే, ప్రతి రేటు AP ప్రభుత్వమే నిర్ణయిస్తుంది, పరిమితి లేదు.",
    "en_07": "10,000 entrepreneurs in 3 pilot districts, 1 lakh across all 26 districts by Month 18, and 5 lakh families earning real digital income by Month 36 — Zian Technologies LLP delivers the CM's vision with a hard number and deadline on every phase.",
    "te_07": "3 పైలట్ జిల్లాలలో 10,000 వ్యాపారవేత్తలు, 18వ నెలలోగా 26 జిల్లాలలో 1 లక్ష, 36వ నెలలోగా 5 లక్షల కుటుంబాలకు నిజమైన డిజిటల్ ఆదాయం — జియాన్ టెక్నాలజీస్ LLP సీఎం దార్శనికతను ప్రతి దశకు స్పష్టమైన సంఖ్య మరియు గడువుతో అందిస్తుంది.",
    "en_08": "Zian Technologies LLP holds both roles — Nodal Agency remitting revenue to government within 7 working days, and TSP guaranteeing 99.5% uptime — all data and IP owned by GoAP, all rates set by GoAP, zero lock-in guaranteed.",
    "te_08": "జియాన్ టెక్నాలజీస్ LLP రెండు పాత్రలు నిర్వహిస్తుంది — 7 పని రోజులలో ప్రభుత్వానికి ఆదాయం చెల్లించే నోడల్ ఏజెన్సీ, మరియు 99.5% అప్‌టైమ్ హామీ ఇచ్చే TSP — అన్ని డేటా మరియు IP GoAP కే చెందుతాయి, అన్ని రేట్లు GoAP నిర్ణయిస్తుంది, జీరో లాక్-ఇన్.",
    "en_09": "Month 6 — platform live in 3 districts, first revenue to government. Month 18 — all 26 districts, 8 verticals, 1 lakh entrepreneurs. Month 30 — platform fully self-sustaining, zero ongoing cost to the state.",
    "te_09": "నెల 6 — 3 జిల్లాలలో ప్లాట్‌ఫారమ్ లైవ్, ప్రభుత్వానికి మొదటి ఆదాయం. నెల 18 — 26 జిల్లాలు, 8 విభాగాలు, 1 లక్ష వ్యాపారవేత్తలు. నెల 30 — ప్లాట్‌ఫారమ్ స్వయంగా నిలబడుతుంది, రాష్ట్రానికి నిరంతర ఖర్చు సున్నా.",
    "en_10": "PS IT&C chairs the council, government sets every fee rate, CAG audit goes to the legislature — Zian Technologies LLP operates under complete government oversight, all data in AP SDC, all IP owned by GoAP, zero vendor control.",
    "te_10": "PS IT&C పాలక మండలికి అధ్యక్షుడు, ప్రభుత్వం ప్రతి రేటు నిర్ణయిస్తుంది, CAG ఆడిట్ శాసనసభకు వెళ్తుంది — జియాన్ టెక్నాలజీస్ LLP పూర్తి ప్రభుత్వ పర్యవేక్షణ కింద పనిచేస్తుంది, డేటా AP SDCలో, IP అంతా GoAP కే చెందుతుంది.",
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
