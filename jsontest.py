import json
test = '''{"FAQs": [
    {
        "question": "What is the current weather situation in the area?",
        "answer": "There is a Red Flag Warning in effect from 8 AM to 6 PM on Sunday, October 27, 2024."
    },
    {
        "question": "What are the expected conditions for the Red Flag Warning?",
        "answer": "The warning is due to breezy and dry conditions with winds gusting up to 35 mph and relative humidity values falling between 20 and 30 percent."
    },
    {
        "question": "Which areas are affected by the Red Flag Warning?",
        "answer": "The affected areas include Fire Weather Zone 023 Central Lakes, Fire Weather Zone 024 Lake Sunapee and Monadnocks, Fire Weather Zone 025 Merrimack Valley, and Fire Weather Zone 026 Seacoast."
    },
    {
        "question": "What are the expected impacts of the Red Flag Warning?",
        "answer": "Any fire that develops will catch and spread quickly. Outdoor burning is not recommended."
    },
    {
        "question": "What should I do during the Red Flag Warning?",
        "answer": "Prepare for extreme fire behavior and consult with local fire officials before engaging in any open burning activities. Always comply with all applicable laws and regulations, and never leave an open fire unattended or extinguish campfires completely before leaving."
    },
    {
        "question": "When does the Red Flag Warning end?",
        "answer": "The Red Flag Warning ends at 6 PM on Sunday, October 27, 2024."
    }
]}'''

test = json.loads(test)
for qaPair in test['FAQs']:
    print(qaPair['question'])
    print(qaPair['answer'])