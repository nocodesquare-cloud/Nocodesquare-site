{
  "title": "Voice AI in African languages: where things stand",
  "dek": "Many customers would rather talk than type. Here is how voice agents work, who is building for African languages, and what to test.",
  "cat": "Building in Africa",
  "date": "2026-11-05",
  "order": 5,
  "cover": "",
  "sources": [
    {
      "title": "YarnGPT on GitHub",
      "url": "https://github.com/saheedniyi02/yarngpt"
    },
    {
      "title": "Princeton Africa World: Lelapa AI launches InkubaLM",
      "url": "https://africaworld.princeton.edu/news/2024/lelapa-ai-launches-africa%E2%80%99s-first-ai-large-language-model"
    },
    {
      "title": "ITWeb Africa: Africa's languages are becoming the next AI battleground",
      "url": "https://itweb.africa/article/africas-languages-are-becoming-the-next-ai-battleground/KA3Ww7dzdaVqrydZ"
    }
  ]
}
Across much of Africa, a phone call is still the most natural way to get something done. That makes voice AI especially interesting here. It also makes it harder, because most models were not trained on the way people here speak.

## How a voice agent works

A voice agent is a relay race with three runners:

1. **It listens.** Speech-to-text turns the caller's words into text.
2. **It thinks.** A language model decides what to say or do next, such as checking a calendar.
3. **It speaks.** Text-to-speech turns the reply into a voice.

Platforms such as Retell AI and VAPI manage this relay, so you can focus on the conversation and on connecting it to your other systems. Every runner adds delay, and long pauses are what make a call feel robotic.

## Who is working on African languages

- **YarnGPT** is an open-source text-to-speech model that generates Nigerian-accented English.
- **Lelapa AI** built InkubaLM, a language model covering Swahili, Yoruba, isiXhosa, Hausa and isiZulu.
- **Intron**, a Nigerian startup, has reportedly expanded its Sahara voice model to 57 languages, including 23 African ones.

This space moves quickly, and a claim on a website does not guarantee a good result on your calls. Test for yourself.

## What to test before you trust it

- **Mixed speech.** People switch between English, Pidgin, Yoruba or Sheng in one sentence. Test that, not textbook phrases.
- **Real phone lines.** Background noise and poor connections are normal. Studio-quality samples will flatter any model.
- **Names, numbers and addresses.** Small errors here cause the biggest problems, so have the agent read important details back.
- **Whether people accept it.** A voice can be accurate and still feel wrong. Let real customers listen.

## Build it responsibly

Tell callers they are speaking with an AI, follow local rules on recording and data, and always give people a way to reach a human. This matters most in sensitive conversations such as debt or health.

A good first project is one narrow job, such as confirming appointments in one language. Get that working well before you add more.
