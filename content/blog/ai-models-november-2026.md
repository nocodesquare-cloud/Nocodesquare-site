{
"title": "The AI models worth knowing right now (Updated)",
  "dek": "A plain snapshot of the current line-ups from OpenAI, Google and Anthropic, and how to choose between them for automation work.",
  "cat": "New models",
  "date": "2026-11-05",
  "order": 3,
  "cover": "",
  "sources": [
    {
      "title": "OpenAI model list",
      "url": "https://developers.openai.com/api/docs/models"
    },
    {
      "title": "Gemini API changelog",
      "url": "https://aistudio.google.com/docs/changelog"
    }
  ]
}
This list goes out of date quickly, so treat it as a snapshot from November 2026 and check each company's own page before you build on it.

## OpenAI

- **GPT-6 Astra.** Its most capable model, for complex reasoning, coding and demanding work.
- **GPT-6.1 Sol.** Close to Astra on complex work, at a lower cost.
- **GPT-6.1 Terra.** Fast and efficient, aimed at visual reasoning, computer use and natural writing.
- **GPT-6 Luna.** Its most efficient model, for focused, high-volume tasks where cost matters.

## Google

- **Gemini 4 Argon.** The most capable model in Google's recent changelog, built for complex coding, agent, maths and science tasks. It became generally available on October 13, 2026.
- **Gemini 3.8 Flash.** Described as Google's most intelligent Flash model.
- **Gemini 3.8 Flash TTS and Flash-Lite TTS.** Text-to-speech models, which are useful for voice work.

One thing to act on: from December 1, 2026, Google will route API requests for Gemini 2.5 Pro and 2.5 Flash to newer models. If you have an automation still using either one, test it now.

## Anthropic

Anthropic's current Claude models are Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5. Check Anthropic's documentation for what each is best suited to and what it costs.

## How to choose for automation

The newest and strongest model is rarely the right default. Most workflow steps are small jobs, like sorting a message or pulling a date from an email.

1. **Start with the cheapest model that might work.** Move up only when it actually fails.
2. **Test on your own messy data.** Use 20 or 30 real examples, including Pidgin, Sheng, typos and whatever else your customers really send. Published rankings will not tell you how a model handles that.
3. **Mix models in one system.** Use a low-cost model for high-volume sorting and a stronger one for the rare hard cases.
4. **Work out the cost per job.** Multiply that by your monthly volume before you promise anyone a price.
5. **Expect models to retire.** Keep the model name in one easy-to-change setting, and re-test whenever you switch.
