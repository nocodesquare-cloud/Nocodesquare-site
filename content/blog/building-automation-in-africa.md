{
  "title": "Building automation in Africa: what the tutorials leave out",
  "dek": "Most tutorials assume steady internet, card payments and English-speaking customers. Here is how to build for the market you actually work in.",
  "cat": "Building in Africa",
  "date": "2026-11-05",
  "order": 7,
  "cover": "",
  "sources": []
}
Most automation tutorials are made for somewhere else. They assume stable connections, international cards and customers who fill in forms correctly. A system that works in that demo can fall apart in Lagos or Kampala.

## Assume the connection will fail

Networks drop and services time out. A cloud automation keeps running, but the people and systems around it may not respond, so plan for that:

- **Set up retries** so a failed step tries again before it gives up.
- **Add failure alerts** so a person knows when something has stopped.
- **Never lose the data.** Save the incoming record first, then process it. If a later step fails, you can run it again.
- **Avoid doing things twice.** A retry should not charge or message someone a second time. Check whether a step already happened.

## Budget for currency

Many tools bill in dollars or euros, while your client earns in naira, cedis or shillings. A cost that looks fine today can look very different after an exchange-rate move. Quote with a buffer, state which currency each tool bills in, and agree who carries that risk. Virtual dollar cards can also fail on some services, so test payment before you commit a client to a tool.

## Meet customers where they are

A beautifully built web form may lose to a simple WhatsApp conversation or a phone call. Start with the channel customers already use, even if it is less tidy to automate.

## Plan for local payments

Many customers pay by bank transfer, mobile money or USSD, and not by card. Providers such as Paystack and Flutterwave can notify your automation by webhook when a payment succeeds. Bank transfers often need a matching step, because the amount or the reference may not be exact. Decide what happens when they do not match, and send those cases to a person.

## Handle messy, multilingual data

People mix languages and spell the same name in many ways. Phone numbers appear with and without country codes. Clean this up early: store numbers in one format, and test any AI step on real local messages.

## Take data protection seriously

Nigeria has its Data Protection Act of 2023, Kenya has its Data Protection Act of 2019, and other countries have their own laws. Collect only what you need, know which tools hold the data, and get proper advice for sensitive work. This also helps you win bigger clients, who will ask.

## The opportunity

These constraints are also your advantage. Someone who understands how business really works here can build things that a tool made elsewhere will never handle properly.
