"""Builds the multi-page Nocodesquare site into site/.
Styles and script live in assets/; page content lives below.
Run: python build_site.py
"""
import json, os, re, shutil

OUT = 'site'
os.makedirs(OUT, exist_ok=True)
if os.path.isdir(f'{OUT}/img'): shutil.rmtree(f'{OUT}/img')
shutil.copytree('img', f'{OUT}/img')

def sub(text, a, b):
    assert a in text, a
    return text.replace(a, b)

shutil.copy('assets/site.css', f'{OUT}/site.css')
shutil.copy('assets/site.js', f'{OUT}/site.js')
for icon in ('favicon.svg', 'favicon.ico', 'favicon-light.png', 'favicon-dark.png', 'apple-touch-icon.png'):
    shutil.copy(f'assets/{icon}', f'{OUT}/{icon}')

# ------------------------------------------------------------------ shared chrome
APPLY_LINK = 'apply.html'
YOUTUBE_URL = 'https://www.youtube.com/@Nocodesquare'   # every YouTube link on the site uses this
LINKEDIN_URL = 'https://www.linkedin.com/company/nocodesquare'
INSTAGRAM_URL = 'https://www.instagram.com/nocodesquare/'
# Newsletter sign-ups are POSTed here as JSON {email, page, source}. A Make.com, n8n or Zapier webhook works. Empty = the form says sign-ups aren't open yet.
NEWSLETTER_WEBHOOK = ''
YT_ATTRS = '' if YOUTUBE_URL == '#' else ' target="_blank" rel="noopener"'
NAV = [('index.html', 'Home'), ('community.html', 'Community'), ('cohort.html', 'Academy'), ('events.html', 'Events'), ('about.html', 'About')]
THEME_BOOT = '<script>try{var t=localStorage.getItem("ncs-theme");if(t)document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>\n'
FONTS = THEME_BOOT + '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wdth,wght@75..100,300..800&family=DM+Mono:wght@400;500&display=swap">\n<link rel="stylesheet" href="site.css">\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n<link rel="icon" href="favicon-light.png" sizes="64x64" type="image/png" media="(prefers-color-scheme: light)">\n<link rel="icon" href="favicon-dark.png" sizes="64x64" type="image/png" media="(prefers-color-scheme: dark)">\n<link rel="alternate icon" href="favicon.ico">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">'
MARK = '<svg class="mark" aria-hidden="true"><use href="#cube"/></svg>'
CUBE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="cube" viewBox="-43.3 -50 86.6 100">
    <polygon class="cube-t" points="0,-50 43.3,-25 0,0 -43.3,-25"/>
    <polygon class="cube-l" points="-43.3,-25 0,0 0,50 -43.3,25"/>
    <polygon class="cube-r" points="0,0 43.3,-25 43.3,25 0,50"/>
  </symbol>
  <symbol id="i-linkedin" viewBox="0 0 24 24">
    <rect x="2" y="2" width="20" height="20" rx="3.5" fill="currentColor"/>
    <g fill="var(--ground)"><circle cx="7.5" cy="7.4" r="1.55"/><rect x="6.2" y="10" width="2.6" height="8"/><path d="M11 10h2.5v1.2c.5-.8 1.4-1.4 2.6-1.4 2.2 0 3 1.4 3 3.6V18h-2.6v-4.1c0-1-.4-1.7-1.3-1.7-.9 0-1.6.7-1.6 1.7V18H11z"/></g>
  </symbol>
  <symbol id="i-youtube" viewBox="0 0 24 24">
    <rect x="1.500" y="4.500" width="21" height="15" rx="4.500" fill="currentColor"/>
    <path d="M10 8.700v6.600l5.600-3.300z" fill="var(--ground)"/>
  </symbol>
  <symbol id="i-instagram" viewBox="0 0 24 24">
    <rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2.200"/>
    <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2.200"/>
    <circle cx="17.200" cy="6.800" r="1.350" fill="currentColor"/>
  </symbol>
</svg>'''

def header(current):
    here = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{here if h == current else ""}>{t}</a>' for h, t in NAV)
    menu = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV + [('@@APPLY@@', 'Apply')])
    return f'''<header class="nav">
  <div class="nav-bar">
    <a class="logo" href="index.html" aria-label="Nocodesquare home">
      <svg aria-hidden="true"><use href="#cube"/></svg>
      <span class="wordmark"><b>NOCODE</b><span>SQUARE</span></span>
    </a>
    <nav class="nav-links" aria-label="Main">{links}</nav>
    <div class="nav-right">
      <button class="theme-btn" type="button" aria-label="Switch colour mode" title="Light or dark mode"><svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.500 14.600A8.500 8.500 0 0 1 9.400 3.500a8.500 8.500 0 1 0 11.100 11.100z"/></svg><svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.500" fill="currentColor"/><path stroke="currentColor" stroke-width="2.200" stroke-linecap="round" d="M12 2.500v2.500M12 19v2.500M2.500 12H5M19 12h2.500M5.300 5.300 7 7M17 17l1.700 1.700M5.300 18.700 7 17M17 7l1.700-1.700"/></svg></button>
      <div class="mode-switch in-bar" role="group" aria-label="Who is reading"><button type="button" data-mode="human" aria-pressed="true">Human</button><button type="button" data-mode="machine" aria-pressed="false">Machine</button></div>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
      <a class="nav-cta" href="@@APPLY@@">Apply</a>
    </div>
  </div>
  <nav class="menu" id="menu" aria-label="Menu" hidden><div class="mode-switch in-menu" role="group" aria-label="Who is reading"><button type="button" data-mode="human" aria-pressed="true">Human</button><button type="button" data-mode="machine" aria-pressed="false">Machine</button></div>{menu}</nav>
</header>'''

FOOTER = '''<footer>
  <section class="newsletter" aria-labelledby="nl-title">
    <div class="nl-copy">
      <p class="nl-kicker">The NCS newsletter</p>
      <h2 id="nl-title">AI, automation and no-code news, <i>in your inbox.</i></h2>
      <p>New AI models, tools worth learning, and what builders across Africa are shipping. Short, useful, and free.</p>
    </div>
    <form class="nl-form" data-endpoint="@@NL@@" novalidate>
      <label for="nl-email">Email address</label>
      <div class="nl-row">
        <input id="nl-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
        <button type="submit">Subscribe</button>
      </div>
      <p class="nl-msg" role="status" aria-live="polite"></p>
      <p class="nl-note">No spam. Unsubscribe any time.</p>
    </form>
  </section>
  <div class="sitemap">
    <div><b><a href="about.html">About</a></b><a href="blog-what-is-no-code.html">What is no-code?</a><a href="about.html#beliefs">What we believe</a></div>
    <div><b><a href="community.html">Community</a></b><a href="community.html#inside">What happens inside</a><a href="community.html#sessions">Sessions</a><a href="inside-the-build.html">Inside the Build</a><a href="freelance-corner.html">Freelance Corner</a><a href="show-and-tell.html">Show and Tell</a><a href="community.html#start">How to apply</a></div>
    <div><b><a href="cohort.html">Academy</a></b><a href="cohort.html">Cohort</a><a href="cohort-curriculum.html">Curriculum</a><a href="cohort.html#questions">Questions</a><a href="instructors.html">Meet your instructors</a><a href="academy-testimonials.html">Testimonials</a><a href="apply-cohort.html">Apply to the cohort</a></div>
    <div><b><a href="events.html">Events</a></b><a href="events.html">Coming soon</a></div>
    <div><b><a href="blog.html">Blog</a></b><a href="blog.html">All articles</a><a href="blog-what-is-no-code.html">What is no-code?</a><a href="blog-ai-models-november-2026.html">New AI models</a></div>
    <div><b><a href="merch.html">Merch</a></b><a href="merch.html">Shop</a><a href="cart.html">Your cart</a></div>
    <div><b><a href="@@APPLY@@">Apply</a></b><a href="join.html">Every way in</a><a href="@@YT@@"@@YTA@@>YouTube</a></div>
  </div>
  <div class="foot-links">
    <span>Lagos, Nigeria</span>
    <div class="socials">@@SOCIALS@@</div>
    <span><a class="agent-link" href="llms.txt">For AI agents</a> · © 2026 Nocodesquare</span>
  </div>
  <div class="ncs-mark" aria-hidden="true">NCS</div>
</footer>'''

def social(url, icon, name):
    ext = '' if url == '#' else ' target="_blank" rel="noopener"'
    return f'<a href="{url}"{ext} aria-label="Nocodesquare on {name}" title="{name}"><svg aria-hidden="true"><use href="#{icon}"/></svg></a>'
SOCIALS = social(LINKEDIN_URL, 'i-linkedin', 'LinkedIn') + social(YOUTUBE_URL, 'i-youtube', 'YouTube') + social(INSTAGRAM_URL, 'i-instagram', 'Instagram')
FOOTER = FOOTER.replace('@@NL@@', NEWSLETTER_WEBHOOK).replace('@@YT@@', YOUTUBE_URL).replace('@@YTA@@', YT_ATTRS).replace('@@SOCIALS@@', SOCIALS)

def crumb(*parts):
    out = [f'<a href="{h}">{t}</a>' if h else t for h, t in parts]
    return '<div class="crumb">' + out[0] + ''.join(f'<span>{p}</span>' for p in out[1:]) + '</div>'

def hero(scene, ground, cls, crumbs, title, lead, cta=''):
    c = f'<div class="cta-row">{cta}</div>' if cta else ''
    return f'''<section class="pagehero"><div class="frame">
    {MARK}
    {crumbs}
    <h1 class="big">{title}</h1>
    <p>{lead}</p>
    {c}
  </div></section>'''

def sheet(color, side, body, id_=''):
    i = f' id="{id_}"' if id_ else ''
    return f'''<section class="sheet"{i}>
    <div class="frame">
      <div class="head">{side}</div>
      <div class="body">{body}</div>
    </div>
  </section>'''

def nxt(href, label, title):
    return f'<a class="next" href="{href}"><span class="inner-next"><span class="tag">{label}</span><b>{title} →</b></span></a>'

def page(slug, title, current, body):
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{title} | Nocodesquare</title>
<link rel="alternate" type="text/markdown" href="{slug[:-5]}.md" title="Agent-readable version">
{FONTS}
</head>
<body data-md="@@MD@@">
{CUBE}
{header(current)}
<main>
  {body}
</main>
{FOOTER}
<script src="site.js"></script>
</body>
</html>
'''
    open(f'{OUT}/{slug}', 'w', encoding='utf-8').write(html.replace('@@APPLY@@', APPLY_LINK).replace('@@MD@@', slug[:-5] + '.md'))

def rows(items):
    return '<ul class="rows">' + ''.join(f'<li><a class="row" href="{h}"><h3 class="big sm">{t}<small>{d}</small></h3><span>{r} →</span></a></li>' for h, t, d, r in items) + '</ul>'

def steps(items):
    return '<ol class="steps">' + ''.join(f'<li><span class="n">{i+1:02d}</span><div><h3 class="big">{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(items)) + '</ol>'

COMB = '''<figure class="orb">
        <svg aria-hidden="true"><use href="#cube"/></svg>
        <img src="img/portrait.jpg" alt="Smiling woman in glasses seated in an office" loading="lazy">
      </figure>'''
COHORT_START = '2027-03-03T00:00:00+01:00'   # next cohort: 3 March 2027, start of day, West Africa Time
COUNTDOWN = f'''<div class="countdown" data-target="{COHORT_START}">
      <span class="tag">Next cohort starts March 3, 2027</span>
      <div class="clock" role="timer" aria-label="Time left until the next cohort starts">
        <div><b data-unit="days">--</b><span class="caps">Days</span></div>
        <div><b data-unit="hours">--</b><span class="caps">Hours</span></div>
        <div><b data-unit="minutes">--</b><span class="caps">Minutes</span></div>
        <div><b data-unit="seconds">--</b><span class="caps">Seconds</span></div>
      </div>
    </div>'''
HOME = ('index.html', 'Home')

# ------------------------------------------------------------------ builds (layer 3)
BUILDS = [
 ('build-voice-agent.html', 'Missed-call voice agent', 'A voice agent that calls people back when you miss them and books them in.', 'Retell AI / Make.com / Google Calendar', 'teal', 'teal',
  'Every missed call can be a lost customer. A small team can\'t always pick up, and most callers won\'t leave a voicemail or try again.',
  [('A call gets missed', 'The phone system reports the missed call and sends the number to Make.com through a webhook.'),
   ('The agent calls back', 'Make.com asks Retell AI to place the call. The agent says who it is calling for and asks how it can help.'),
   ('It checks the calendar', 'If the caller wants an appointment, the agent looks up open times in Google Calendar and offers a few.'),
   ('The booking is saved', 'The appointment goes on the calendar, and a summary of the call is sent to the team.')],
  ['Retell AI', 'Make.com', 'Google Calendar'],
  ['How a voice agent is given instructions', 'What a webhook is and when to use one', 'How to let an agent use your calendar']),
 ('build-lead-routing.html', 'Lead scoring and routing', 'Every form that comes in gets read, scored and sent to the right person.', 'Tally / Claude / Airtable', 'copper', 'copper',
  'When leads pile up in one inbox, the good ones wait as long as the bad ones. Someone has to read each one before anything can happen.',
  [('A form is submitted', 'Someone fills in a Tally form, and the answers are sent to the automation straight away.'),
   ('Claude reads it', 'Claude reads the answers against the rules you set and returns a score with a one-line reason.'),
   ('The record is saved', 'The lead, the score and the reason are saved in Airtable, so the team can see why it scored that way.'),
   ('The right person hears', 'Hot leads go straight to a salesperson. The rest go into a follow-up list.')],
  ['Tally', 'Claude', 'Airtable'],
  ['How to get structured answers from an AI model', 'How to use Airtable as a simple database', 'How to route work based on a score']),
 ('build-whatsapp-follow-up.html', 'WhatsApp sales follow-up', 'A follow-up sequence that keeps talking to leads until they answer or say no.', 'n8n / WhatsApp Cloud API / Airtable', 'slate', 'slate',
  'Most sales are lost to silence. People mean to reply, then forget, and nobody on the team has time to chase every conversation by hand.',
  [('A lead enters the list', 'A new lead appears in Airtable with their number and what they asked about.'),
   ('The first message goes out', 'n8n sends an approved WhatsApp template through the WhatsApp Cloud API.'),
   ('The system waits', 'If there is no reply after a set time, n8n sends the next message in the sequence.'),
   ('A reply stops everything', 'As soon as the lead responds, the sequence stops and a person takes over the conversation.')],
  ['n8n', 'WhatsApp Cloud API', 'Airtable'],
  ['How WhatsApp message templates work', 'How to build waits and branches in n8n', 'How to hand a conversation back to a person']),
 ('build-payment-reminders.html', 'Payment reminder calls', 'Polite, consistent reminder calls, with every outcome written back to your CRM.', 'VAPI / Webhooks / CRM', 'teal', 'teal',
  'Reminding people to pay is slow, uncomfortable and easy to put off. When it is done by hand, the results often never reach the records.',
  [('The due list is pulled', 'The automation gets everyone with a payment due from the CRM.'),
   ('The agent calls', 'VAPI places each call and reminds the customer of the amount and the date.'),
   ('The outcome is captured', 'The agent records what was said: paid, promised a date, disputed or no answer.'),
   ('The CRM is updated', 'A webhook writes the outcome back to the CRM, and disputes go to a person.')],
  ['VAPI', 'Webhooks', 'CRM'],
  ['How to pull structured outcomes from a call', 'How to write data back with a webhook', 'When an agent should hand over to a person']),
 ('build-receipt-extractor.html', 'Receipt extractor', 'Receipts sent by email get read and filed in a spreadsheet automatically.', 'Gmail / OpenAI / Google Sheets', 'copper', 'copper',
  'Receipts arrive in every format, and typing them into a spreadsheet is the kind of task that gets left until the end of the month.',
  [('A receipt arrives', 'The automation watches a Gmail label for new receipts and picks up the attachment.'),
   ('OpenAI reads it', 'An OpenAI model pulls out the vendor, date, amount and category.'),
   ('The data is checked', 'Anything missing or unclear gets flagged for a person instead of being guessed.'),
   ('The row is added', 'Clean results become a new row in Google Sheets, ready for the books.')],
  ['Gmail', 'OpenAI', 'Google Sheets'],
  ['How to read documents with an AI model', 'How to check AI output before saving it', 'How to trigger an automation from an email label']),
]
CLS = {'teal': 'teal', 'copper': 'copper', 'slate': 'slate'}
for i, b in enumerate(BUILDS):
    slug, title, line, stack, ground, cls, problem, st, tools, learn = b
    prev_b, next_b = BUILDS[(i - 1) % len(BUILDS)], BUILDS[(i + 1) % len(BUILDS)]
    body = hero('flow', ground, cls, crumb(HOME, ('community.html', 'Community'), ('inside-the-build.html', 'Inside the Build'), (None, title)), title, line, '<a class="slab t" href="@@APPLY@@">Build this with us</a>' if cls != 'teal' else '<a class="slab" href="@@APPLY@@">Build this with us</a>')
    body += sheet('light', '<span class="tag">The problem</span><h2 class="big">Why this <i>is worth building.</i></h2>', f'<p>{problem}</p><ul class="chips">' + ''.join(f'<li>{t}</li>' for t in tools) + '</ul>')
    body += sheet('light', '<span class="tag">How it works</span><h2 class="big">Step <i>by step.</i></h2>', steps(st))
    body += sheet(cls, '<span class="tag">What you\'d pick up</span><h2 class="big">Skills you <i>can reuse.</i></h2>', '<ul class="rows">' + ''.join(f'<li><div class="row" style="grid-template-columns:1fr"><h3 class="big sm">{l}</h3></div></li>' for l in learn) + '</ul>')
    body += f'<nav class="pager" aria-label="More builds"><a href="{prev_b[0]}"><span class="tag">Previous build</span><b>← {prev_b[1]}</b></a><a href="{next_b[0]}"><span class="tag">Next build</span><b>{next_b[1]} →</b></a></nav>'
    page(slug, title, 'community.html', body)

# ------------------------------------------------------------------ layer 2 and other layer 3 pages
page('about.html', 'About', 'about.html',
  hero('', '', '', crumb(HOME, (None, 'About')), 'Who <i>we are.</i>', 'Nocodesquare (NCS) is a community and learning platform for people who build with no-code, automation, and AI.')
  + f'''<article class="prose about-story">
      <p>We help beginners, freelancers, and business owners move from “I’ve heard of this” to “I’ve built this and someone is paying me for it.”</p>
      <p>Our members span Nigeria, Kenya, Cameroon, and beyond. Some are students, some are freelancers looking for their first international client, and some are founders who want to stop doing repetitive work by hand. What they share is a willingness to build, and we give them the tools, the teachers, and the people to build alongside.</p>
      <p>We’re not just focused on no-code tools and automation. We also focus on AI: how it works, how to build with it, and how to use it in real work, from AI agents and voice agents to connecting AI to your tools with MCP.</p>

      <h2 id="story">Our story</h2>
      <p>Nocodesquare started in August 2023 as Gig Guru Network, a small group of people helping each other find their footing in freelancing and automation. The community grew quickly, because people didn’t just want theory. They wanted to build, share what they’d built, and learn from each other.</p>
      <p>In December 2024 we rebranded to Nocodesquare to match what the community had become: a home for everything no-code and AI automation. Our founder, Ogunyemi Ayobami, known as “the AYB”, builds AI systems and teaches others to do the same.</p>
      <p>Since then we’ve:</p>
      <ul>
        <li>Run a 100-day Zapier webinar series, then launched the Nocode365 challenge, a commitment to show up with a live session every single day at 8 PM</li>
        <li>Trained cohorts of builders through our paid AI Automation Cohort</li>
        <li>Built a library of live sessions, tutorials, and handbooks that members use long after the session ends</li>
      </ul>

      <h2 id="what">What we do</h2>
      <h3>Learn: cohorts and courses</h3>
      <p>Our flagship <a href="cohort.html">AI Automation Cohort</a> is a 60-day, hands-on program covering Zapier, Make.com, Airtable, and GoHighLevel. It is taught by working practitioners and built around one idea: you learn by building real systems, not by watching slides.</p>
      <h3>Build: Inside the Build</h3>
      <p><a href="inside-the-build.html">Inside the Build</a> is our recurring live series where we open up the process and build in front of you. Recent sessions have covered AI agents and agentic loops, an AI-powered inbox manager that drafts replies in your own voice, and a deep dive into MCP (Model Context Protocol). You see the real workflow, the mistakes, and the fixes.</p>
      <h3>Earn: Freelancers’ Corner</h3>
      <p><a href="freelance-corner.html">Freelancers’ Corner</a> is a space for members turning these skills into income: finding clients, pricing work, positioning yourself, and delivering projects that lead to referrals.</p>
      <h3>Connect: the community</h3>
      <p>A members-only <a href="community.html">community</a> with a handbook, onboarding, member spotlights, and a culture of helping each other ship. You won’t be learning alone.</p>
      <h3>Watch: our YouTube channel</h3>
      <p>Free tutorials on automation, AI agents, and AI voice agents on <a href="{YOUTUBE_URL}" target="_blank" rel="noopener">our YouTube channel</a>, so anyone can start learning before they join.</p>

      <h2 id="beliefs">How we teach</h2>
      <p>We believe in a systems-first, build-as-you-learn approach.</p>
      <ol>
        <li><b>Start with the system, not the tool.</b> Tools change every year. Thinking in triggers, data, logic, and outcomes lasts.</li>
        <li><b>Build something real, early.</b> Every learner ships a working automation quickly, because confidence comes from results.</li>
        <li><b>Learn from people doing the work.</b> Our instructors build and sell automation solutions every day. They teach what works now.</li>
        <li><b>Stay current.</b> From classic workflow automation to AI agents, voice agents, and MCP, we teach where the industry is going.</li>
      </ol>

      <h2 id="learn">What you’ll learn</h2>
      <ul>
        <li>Workflow automation with Zapier and Make.com</li>
        <li>Databases and data systems with Airtable</li>
        <li>CRM and marketing automation with GoHighLevel</li>
        <li>AI agents and agentic workflows</li>
        <li>AI voice agents for business</li>
        <li>Connecting AI to your tools with MCP</li>
        <li>Freelancing, client acquisition, and building an automation business</li>
      </ul>

      <h2 id="who">Who it’s for</h2>
      <ul>
        <li><b>Beginners</b> who want a practical, high-income digital skill with no coding background</li>
        <li><b>Freelancers</b> who want to add automation and AI services and win better clients</li>
        <li><b>Founders and operators</b> who want to automate their own business</li>
        <li><b>Students and career-switchers</b> looking for a clear path into tech</li>
      </ul>

      <h2 id="vision">Where we’re going</h2>
      <p>Our vision is simple: make Nocodesquare the biggest home for no-code and AI builders in Africa, and one of the strongest in the world.</p>
      <ul>
        <li><b>Nocode Africa:</b> we’re planning what we intend to be the largest no-code event in Africa, hosted in Lagos</li>
        <li>A growing community of members who learn, ship, and earn together</li>
        <li>More cohorts, more courses, more opportunities, so a talented person anywhere on the continent has a clear path from learning to earning</li>
        <li>A pipeline of African talent that businesses around the world can trust to build their automation and AI systems</li>
      </ul>
      <p>We believe the next generation of great builders doesn’t need permission, a degree, or a Silicon Valley address. It needs access, guidance, and community. That is what we are building.</p>

      <div class="post-cta" id="join">
        <b>Ready to start building?</b>
        <div class="about-cta">
          <a class="slab" href="@@APPLY@@">Join the community</a>
          <a class="slab" href="cohort.html">Explore the cohort</a>
          <a class="slab" href="{YOUTUBE_URL}" target="_blank" rel="noopener">Watch on YouTube</a>
        </div>
      </div>
    </article>''')

SESSIONS = [
  ('inside-the-build.html', 'Inside the Build', 'Our educational session. We go deep on topics like building AI agents and using OpenCode.', 'Learn'),
  ('freelance-corner.html', 'Freelance Corner', 'Finding clients, using platforms like Upwork and Fiverr, cold email, and life as a no-code and AI freelancer.', 'Freelancing'),
  ('show-and-tell.html', 'Show and Tell', 'A member takes an hour to walk the whole community through how they built a project.', 'Member projects'),
]
page('community.html', 'Community', 'community.html',
  hero('crowd', 'teal', 'teal', crumb(HOME, (None, 'Community')), 'Nobody builds <i>alone here.</i>', 'The community is the heart of Nocodesquare. Members come to learn no-code tools, stay up to date with no-code and AI, connect with other builders and stay consistent.', '<a class="slab" href="@@APPLY@@">Apply to the community</a>')
  + sheet('light', '<span class="tag">Inside</span><h2 class="big">What <i>happens here.</i></h2>', '''<dl class="defs">
        <div><dt>Ask questions</dt><dd>Stuck on a scenario or an API call? Someone here has probably hit the same wall.</dd></div>
        <div><dt>Share your work</dt><dd>Show what you've built, finished or not, and see what other people are making.</dd></div>
        <div><dt>Get feedback</dt><dd>Hear from people who build too, before you put something in front of a client.</dd></div>
        <div><dt>Hear first</dt><dd>Members find out first about new cohorts, sessions and events.</dd></div>
      </dl>''', 'inside')
  + sheet('light', '<span class="tag">Sessions</span><h2 class="big">Three ways <i>to learn together.</i></h2>', '<p>Members learn from each other in three regular sessions. Show and Tell is the one we record and upload to our YouTube channel.</p>' + rows(SESSIONS) + '<a class="more" href="' + YOUTUBE_URL + '" target="_blank" rel="noopener">Watch Show and Tell on YouTube</a>', 'sessions')
  + f'''<section class="sheet community"><div class="frame">
      <div class="copy">
        <span class="tag">Who you'll meet</span>
        <h2 class="big">Builders <i>at every stage.</i></h2>
        <p>The community is for people already building with no-code and AI, whether for clients, a product or their own company.</p>
        <ul class="who">
          <li><b>Freelancers</b>Selling no-code and AI services</li>
          <li><b>Agency founders</b>Delivering for clients, solo or with a team</li>
          <li><b>SaaS founders</b>Building products with no-code and AI</li>
          <li><b>Operators</b>Automating the business they work in</li>
          <li><b>Educators</b>Teaching clients, businesses and teams</li>
        </ul>
      </div>
      {COMB}
    </div></section>'''
  + sheet('light', '<span class="tag">Applying</span><h2 class="big">How to <i>get in.</i></h2>', steps([('Record two Loom videos', 'Up to 5 minutes each: one about yourself and why the community matters to you, and one about a recent project you built. The form asks for the links, so have them ready.'), ('Fill in the form', 'Tell us where you are, your goal, how you work, the tools you use and how committed you are, and share your LinkedIn profile.'), ('We review it', 'The community is by application, so we read every one before anyone comes in.')]) + '<a class="slab" href="@@APPLY@@">Apply to the community</a>', 'start')
  + nxt('cohort.html', 'Want more structure?', 'The cohort'))

# Add a video here and it appears on the Show and Tell page: (YouTube id, title, description, length)
SHOW_VIDEOS = [
  ('h0ZOh1nWvbU', 'Building upKit', 'An AI-powered system for highly tailored proposals.', '1:35:57'),
]
def video_card(v):
    vid, title, desc, length = v
    return f'''<a class="video" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">
      <span class="thumb"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy"><i aria-hidden="true"></i><em>{length}</em></span>
      <span class="tag">Show and Tell</span>
      <b>{title}</b>
      <span class="video-desc">{desc}</span>
      <span class="more">Watch on YouTube →</span>
    </a>'''

page('inside-the-build.html', 'Inside the Build', 'community.html',
  hero('flow', 'light', 'light', crumb(HOME, ('community.html', 'Community'), (None, 'Inside the Build')), 'Inside <i>the Build.</i>', 'Our most educational session. We go deep on one topic at a time, so you leave understanding how it really works. It isn\'t recorded, so you need to be there.', '<a class="slab" href="@@APPLY@@">Apply to the community</a>')
  + sheet('light', '<span class="tag">Topics</span><h2 class="big">The kind of thing <i>we dig into.</i></h2>', '''<dl class="defs">
        <div><dt>Building AI agents</dt><dd>How agents work and how to build them yourself.</dd></div>
        <div><dt>Using OpenCode</dt><dd>Using OpenCode to build AI agents, as one example of the tools we explore.</dd></div>
      </dl>''')
  + '<section class="sheet" id="builds"><div class="frame"><div class="builds-head"><span class="tag">Examples</span><h2 class="big">Systems <i>to explore.</i></h2><p>Worked examples of the kind of automation members build. Open one to see the problem and how each step works.</p></div>'
  + rows([(b[0], b[1], b[2], b[3]) for b in BUILDS]) + '</div></section>'
  + nxt('freelance-corner.html', 'Next session', 'Freelance Corner'))

page('freelance-corner.html', 'Freelance Corner', 'community.html',
  hero('', '', '', crumb(HOME, ('community.html', 'Community'), (None, 'Freelance Corner')), 'Freelance <i>Corner.</i>', 'The session about making a living as a freelancer with no-code and AI tools, and everything freelancers go through along the way. It isn\'t recorded, so you need to be there.', '<a class="slab" href="@@APPLY@@">Apply to the community</a>')
  + sheet('light', '<span class="tag">What we talk about</span><h2 class="big">The real side <i>of freelancing.</i></h2>', '''<dl class="defs">
        <div><dt>Freelance platforms</dt><dd>How to use Upwork, Fiverr and other platforms to win work.</dd></div>
        <div><dt>Cold email</dt><dd>How to use cold email to get clients of your own.</dd></div>
        <div><dt>Best practices</dt><dd>What works for freelancers, shared by people doing the work.</dd></div>
        <div><dt>Life as a freelancer</dt><dd>What day-to-day life is really like when you freelance with no-code and AI.</dd></div>
      </dl>''')
  + nxt('show-and-tell.html', 'Next session', 'Show and Tell'))

page('show-and-tell.html', 'Show and Tell', 'community.html',
  hero('', '', '', crumb(HOME, ('community.html', 'Community'), (None, 'Show and Tell')), 'Show <i>and Tell.</i>', 'Every member gets the chance to show a project. For an hour, one builder walks the entire community through how they built it.', '<a class="slab" href="@@APPLY@@">Apply to the community</a>')
  + sheet('light', '<span class="tag">How it works</span><h2 class="big">One member. <i>One project.</i></h2>', steps([('Pick a project', 'A member chooses a project they have built.'), ('Create a presentation', 'They put together a presentation about that project.'), ('Walk everyone through it', 'For an hour, they show the community how they built it.')]))
  + sheet('light', '<span class="tag">Watch</span><h2 class="big">See a member <i>walk through it.</i></h2>', '<p>Show and Tell sessions are recorded and uploaded to our YouTube channel.</p><div class="videos">' + ''.join(video_card(v) for v in SHOW_VIDEOS) + '</div><a class="more" href="' + YOUTUBE_URL + '" target="_blank" rel="noopener">See our YouTube channel</a>')
  + nxt('community.html', 'Back to', 'The community'))

# Real testimonials go here: ('Quote', 'Name', 'What they do, country').
# While a list is empty its section shows clearly marked placeholders, so real quotes must go in before launch.
MEMBER_QUOTES = []
ACADEMY_QUOTES = []
def quote_cards(quotes, who):
    if quotes:
        cards = ''.join(f'<figure class="quote"><blockquote>{q}</blockquote><figcaption><b>{n}</b><span>{r}</span></figcaption></figure>' for q, n, r in quotes)
    else:
        cards = ''.join(f'<figure class="quote empty"><span class="tag">Placeholder</span><blockquote>A real quote from {who} goes here.</blockquote><figcaption><b>Name</b><span>What they do, country</span></figcaption></figure>' for _ in range(3))
    return f'<div class="quotes">{cards}</div>'

# A member's full story: gets a large card on the homepage and a page of its own.
MEMBER_STORIES = [{
  'slug': 'story-sekinat-ibrahim.html',
  'name': 'Sekinat Ibrahim',
  'first': 'Sekinat',
  'headline': 'You don’t need permission to start building.',
  'role': 'CEO, AVOZ AI',
  'photo': 'img/sekinat-ibrahim.jpg',
  'title': 'My Nocodesquare <i>experience.</i>',
  'excerpt': ['I came in with a science background in quality control microbiology, no coding experience, and no clear idea of how I’d build anything in tech.',
              'This year, that confidence took me somewhere I wouldn’t have predicted: I founded AVOZ AI, an AI automation agency.'],
  'story': [
    'Joining Nocodesquare changed how I see what’s possible with technology. I came in with a science background in quality control microbiology, no coding experience, and no clear idea of how I’d build anything in tech. Nocodesquare showed me I didn’t need either.',
    'What stands out most is the community itself. People here share what they know freely, ask honest questions, and celebrate each other’s wins, however small. Whenever I got stuck on a scenario, someone was ready to help me think it through. That support made me braver about building and trying things in public.',
    'This year, that confidence took me somewhere I wouldn’t have predicted: I founded AVOZ AI, an AI automation agency. What started as workflows I was learning to build became real solutions for real businesses, including AI voice agents, WhatsApp AI agents, CRM integrations, and lead generation pipelines. Today we serve clients locally and internationally, and it all started with the skills and encouragement I found here.',
    'Along the way, I also began teaching Make.com to other learners in NCS Academy. Teaching taught me more than anything else did. Explaining a concept to someone else forces you to understand it properly, and watching a student’s first automation run successfully never gets old.',
    'I’m still growing, and I’m still learning hands-on. I know I’ll find people here who will cheer me on, challenge me, and build alongside me.',
    'To everyone in Nocodesquare: thank you for the generosity, the late-night troubleshooting, and the reminder that you don’t need permission to start building. I’m proud to be part of this community.',
  ],
}, {
  'slug': 'story-nafeesat-aliu.html',
  'name': 'Nafeesat Aliu',
  'first': 'Nafeesat',
  'headline': 'Start as a beginner.',
  'role': 'Freelancer and Instructor at NCS',
  'photo': 'img/nafeesat-aliu.jpg',
  'title': 'My Nocodesquare journey: <i>from learning to giving back.</i>',
  'excerpt': ['It is a community where you can start as a beginner, discover your interests, develop valuable skills and eventually become someone who helps others find their footing too.',
              'Seeing people learn, build their confidence, develop their skills and begin creating things with the knowledge they acquire is one of the things that makes being part of this community meaningful to me.'],
  'story': [
    'My journey with Nocodesquare has been one of learning, discovery, growth and continuous impact. It is an experience I genuinely appreciate because Nocodesquare has played an important role in shaping my understanding of technology, particularly in the world of No-Code, AI and automation.',
    'When I started my journey with Nocodesquare, I was introduced to the fundamentals of No-Code tools, automation and the possibilities that technology makes available to us. Those early lessons gave me a foundation and opened my eyes to an entirely new world of opportunities. Some of the knowledge, skills and understanding I have today can be traced back to the exposure and learning I received through Nocodesquare.',
    'One of the biggest things I appreciate is how the community helped me see beyond just learning individual tools. It exposed me to the bigger picture of what is possible within the AI workspace. I began to understand how technology could be used to solve real-world problems, simplify business processes, improve productivity and create opportunities. It sparked a curiosity that has continued to push me to learn, explore, experiment and grow.',
    'But my experience with Nocodesquare has evolved beyond being a learner. Today, I am still actively part of the community, and one of the most fulfilling aspects of that journey is having the opportunity to contribute to the growth of others.',
    'Being able to mentor, teach, guide beginners, share knowledge and help other people understand concepts that once seemed unfamiliar to me has been incredibly rewarding. There is something special about being able to help someone take their first steps into a space that once felt new to you. Seeing people learn, build their confidence, develop their skills and begin creating things with the knowledge they acquire is one of the things that makes being part of this community meaningful to me.',
    'It has also taught me that growth is not just about how much knowledge you acquire for yourself, but also about how much of that knowledge you can share to help others progress. In the process of mentoring and teaching, I have continued to learn, improve my communication, strengthen my understanding and develop myself professionally.',
    'Beyond the technical knowledge, the people I’ve met through Nocodesquare have also made the experience special. I’ve connected with amazing, talented and forward-thinking individuals whose passion for learning, building and innovation continues to inspire me. The relationships, shared experiences and opportunities to collaborate have added tremendous value to my journey.',
    'What makes Nocodesquare particularly meaningful to me is that it represents continuous growth. It is a community where you can start as a beginner, discover your interests, develop valuable skills and eventually become someone who helps others find their footing too.',
    'I am grateful for the foundation Nocodesquare gave me, the opportunities to keep learning, the wonderful people I’ve met and, most importantly, the opportunity to contribute to the development of others.',
    'I am still part of this journey, still learning, still growing, still exploring the possibilities of AI and automation, and still committed to helping others grow along the way.',
    'For me, Nocodesquare is more than where I started learning. It is a community where I continue to evolve, contribute and grow while helping others discover what is possible for them too.',
    'And that, to me, is the real beauty of being part of Nocodesquare.',
  ],
}, {
  'slug': 'story-ayodele-marvelous.html',
  'name': 'Ayodele Marvelous',
  'first': 'Ayodele Marvelous',
  'headline': 'I am glad I started.',
  'role': 'Nocodesquare member since 2024',
  'photo': 'img/ayodele-marvelous.jpg',
  'title': 'My journey is <i>still ongoing.</i>',
  'excerpt': ['I have gradually learnt to look beyond the usual manual processes and think about how tasks can be simplified, improved, or automated.',
              'My exposure to no-code has broadened my thinking and introduced me to opportunities I might not have considered before.'],
  'story': [
    'My journey with Nocodesquare (NCS) started in 2024, and it has been a significant part of my personal learning and growth.',
    'When I first started exploring no-code, I had little understanding of how much could be achieved with technology without necessarily writing code. I was curious, eager to learn, and still trying to understand how everything connected. Over time, that curiosity developed into a deeper interest in automation and digital solutions.',
    'One of the biggest changes for me has been the way I approach problems. I have gradually learnt to look beyond the usual manual processes and think about how tasks can be simplified, improved, or automated. I have also become more curious about technology, more willing to explore unfamiliar tools, and more confident in my ability to learn something new.',
    'My experience with NCS has taught me that learning technology is not just about understanding tools; it is also about developing a problem-solving mindset, being patient with the learning process, and recognising opportunities where others might only see routine tasks.',
    'I am still learning and discovering new possibilities, but I can confidently say that my exposure to no-code has broadened my thinking and introduced me to opportunities I might not have considered before.',
    'I appreciate NCS for introducing me to this space and providing an avenue to learn, explore, and grow. I look forward to becoming more proficient, building practical solutions, and putting the knowledge I have acquired to meaningful use.',
    'For anyone interested in automation or no-code/low-code development, I believe NCS is a good place to begin exploring what is possible. My journey is still ongoing, but I am glad I started it.',
  ],
}, {
  'slug': 'story-odeyemi-oladimeji-daniel.html',
  'name': 'Odeyemi Oladimeji Daniel',
  'first': 'Odeyemi Oladimeji Daniel',
  'headline': '75% fewer API tokens.',
  'role': 'AI Automation Specialist, community member since February 2025',
  'photo': 'img/odeyemi-oladimeji-daniel.jpg',
  'title': 'Building AI systems <i>with professional rigour.</i>',
  'excerpt': ['By optimising how documents are chunked and retrieved instead of relying on broad context injection, I achieved a 75% reduction in API token usage.',
              'If you are serious about building scalable, production-grade systems with AI and no-code tools, the depth of knowledge and peer feedback inside Nocodesquare makes it well worth your time.'],
  'story': [
    'Before I joined Nocodesquare in February 2025, I was deeply immersed in metallurgical engineering, and alongside it I was building workflow automations and retrieval-augmented generation (RAG) systems with tools like n8n, Supabase and Airtable. I already had a strong grasp of backend integrations and AI tooling. What I was looking for was a focused peer group of builders pushing the boundaries of practical AI automation.',
    'I joined to sharpen my approach to building production-ready AI workflows, and to exchange insights with other serious practitioners who treat no-code and AI engineering with professional rigour.',
    'Since joining, I have designed and engineered an advanced customer support help desk on a RAG architecture, using n8n and a Supabase vector store. By optimising how raw documents are chunked and how vectors are retrieved, instead of relying on broad context injection, I achieved a 75% reduction in API token usage. The system also automates the whole support flow end to end: it classifies each client complaint, alerts the right team, and confirms the ticket to the customer on WhatsApp.',
    'What has helped me most is the community discussions and the shared problem-solving around complex workflow edge cases. They have been invaluable for testing architectural patterns and staying sharp on modern automation practices.',
    'If you are serious about building scalable, production-grade systems with AI and no-code tools, the depth of knowledge and peer feedback inside Nocodesquare makes it well worth your time.',
  ],
}, {
  'slug': 'story-glory-bobby-bassey.html',
  'name': 'Glory Bobby Bassey',
  'first': 'Glory',
  'headline': 'One tool, mastered.',
  'role': 'Marketing Automation Specialist, community member since May 2025',
  'photo': 'img/glory-bobby-bassey.jpg',
  'title': 'Picking one tool <i>and going deep.</i>',
  'excerpt': ['Before joining, I was struggling to identify which tool to niche down into. The community, and especially AYB, encouraged me to stick with GoHighLevel.',
              'There are a lot of communities out there, but finding one that holds your hand, supports you and walks the journey with you is something you should prioritise.'],
  'story': [
    'I was at the early stage of my automation journey when I came across a post by Sekinat about an automation community that met every day to learn. I was curious, so I reached out to find out more. I am a sucker for knowledge.',
    'What made me join was simple: it was a community of people in automation. I was fairly new to the field, and I wanted to be around people doing the same work so I could learn from their experience.',
    'My biggest struggle at the time was choosing a tool to niche down into. I knew I could not master every tool at once, not in a short period. The community, and especially the community leader, AYB, encouraged me to stick with GoHighLevel (GHL). So I did.',
    'We met every day of the week, and those sessions were where the ideas, the learning and the energy came from.',
    'Today I build solutions for my clients in GHL: chatbots that engage customers on social media, Voice AI agents that speak with customers, and lead-to-conversion systems that help my clients serve their customers seamlessly and scale their businesses. All of it is built on the one tool I chose to go deep on.',
    'This is one community I would recommend to anyone looking to grow in their career. There are a lot of communities out there, but finding one that holds your hand, supports you and walks that journey with you is something you should prioritise.',
  ],
}, {
  'slug': 'story-lauren-jude.html',
  'name': 'Lauren Jude',
  'first': 'Lauren',
  'headline': 'A full business, automated.',
  'role': 'Founder and Technical Lead, Automation Prime Africa. Community member since mid-2026',
  'photo': 'img/lauren-jude.jpg',
  'title': 'From shipping systems <i>to founding a company.</i>',
  'excerpt': ['When someone submits a booking, the system creates the records, emails the client, alerts the interpreter team on Telegram, and later sends the invoice. Nobody touches it.',
              'If you build and want to be around other people who build, join. Nocodesquare is not a course. It is a community of people actually executing in the real world.'],
  'story': [
    'Before I joined Nocodesquare, I had just finished the TS Academy AI Automation Phoenix Cohort. Before that, I was a frontend developer working with React and Node.js. So I came in with a solid foundation in n8n, Airtable, Supabase and AI-powered systems, and I had already built several automation systems in production.',
    'I had the technical skills. What I wanted was to be around other builders who were actually shipping real systems for real clients: people focused on execution, not tutorials. I wanted to see what others were building, get honest feedback on my own work, and stay connected to global opportunities. Nocodesquare\'s show and tell culture was exactly what I needed at that stage.',
    'Since joining, I have built Horizon Interpreters, the complete digital infrastructure for a UK-based interpreting startup. It connects qualified interpreters with clients who need telephone, video or face-to-face language support across 47 languages.',
    'The system covers everything the business needs to operate: a professional website with an online booking form, an Airtable backend for interpreters, bookings and clients, and three n8n workflows that automate the whole chain from booking to invoice. When someone books, the system creates the client and booking records, sends a branded confirmation email, and notifies the interpreter team on Telegram. A daily workflow sends appointment reminders. When a job is completed, another workflow calculates the charge from the service type and duration, and sends a professional invoice with the company\'s bank details and payment terms.',
    'It all runs on self-hosted n8n with custom-domain email, so the business looks fully professional from day one without paying for expensive enterprise software.',
    'Beyond individual builds, being part of Nocodesquare gave me the push to found Automation Prime Africa, a technology company that helps businesses automate their operations.',
    'The Friday and Saturday show and tell sessions are what keep me coming back. You see what other builders are shipping in real time, then present your own work to people who actually understand it. You cannot get that anywhere else. The Tuesday and Wednesday sessions are valuable too, but the show and tell culture is what makes Nocodesquare different from every other community I have seen.',
    'If you build and want to be around other people who build, join. Nocodesquare is not a course. It is a community of people actually executing in the real world and sharing what they learn along the way. The show and tell sessions alone are worth it, because you learn as much from seeing how others approach problems as you do from building yourself. Come ready to show your work and give feedback on others\', and you will get far more out of it than you expect.',
  ],
}]
def story_card(m):
    quote = ''.join(f'<p>{x}</p>' for x in m['excerpt'])
    return f"""<figure class="story-card">
      <a class="story-photo" href="{m['slug']}"><img src="{m['photo']}" alt="Portrait of {m['name']}" loading="lazy"></a>
      <div class="story-text">
        <h3 class="story-head">{m['headline']}</h3>
        <blockquote>{quote}</blockquote>
        <figcaption><b>{m['name']}</b><span>{m['role']}</span></figcaption>
        <a class="more" href="{m['slug']}">Read {m['first']}’s full story</a>
      </div>
    </figure>"""

APPLY_COHORT = '<a class="slab" href="apply-cohort.html">Apply to the cohort</a>'
# Cohort fee in each currency. Change the amounts here and the switch updates everywhere.
COHORT_FEE = [('Naira', '₦40,000'), ('Dollars', '$30'), ('Shillings', 'KSh 3,900')]
FEE_TEXT = '₦40,000, $30 or KSh 3,900'
FEE_TABS = '<div class="cur-tabs" role="group" aria-label="Show the fee in">' + ''.join(
    f'<button type="button" data-cur="{name}" data-fee="{amount}" aria-pressed="{"true" if i == 0 else "false"}">{name}</button>'
    for i, (name, amount) in enumerate(COHORT_FEE)) + '</div>'
page('cohort.html', 'Cohort', 'cohort.html',
  hero('cohort', 'copper', 'copper', crumb(HOME, (None, 'Cohort')), 'Become skilled in <i>AI automation.</i>', 'The AI Automation Cohort is a guided, live program where you learn by building working automation systems. No coding needed, and no experience with the tools required.', COUNTDOWN + APPLY_COHORT)
  + '''<section class="sheet"><div class="frame"><div class="stats">
      <div data-fee-switch><b data-fee-amount aria-live="polite">₦40,000</b><span class="caps">Cohort fee</span>''' + FEE_TABS + '''</div>
      <div class="on"><b>4-6 weeks</b><span class="caps">Guided learning and building</span></div>
      <div><b>Live</b><span class="caps">Sessions and assignments</span></div>
    </div></div></section>'''
  + sheet('light', '<span class="tag">What you get</span><h2 class="big">Learn it <i>by building it.</i></h2>', '''<dl class="defs">
        <div><dt>Live sessions</dt><dd>Learn with a group, with practical assignments along the way.</dd></div>
        <div><dt>Hands-on projects</dt><dd>Build real systems from end to end, not just follow along.</dd></div>
        <div><dt>Direct feedback</dt><dd>Get feedback on what you build from people who build these systems themselves.</dd></div>
        <div><dt>Private community</dt><dd>Get support and feedback from others in your cohort.</dd></div>
      </dl>''')
  + '<section class="sheet"><div class="frame"><div class="builds-head"><span class="tag">What you\'ll cover</span><h2 class="big">From foundations <i>to full systems.</i></h2><p>Zapier, Make.com, Airtable and GoHighLevel, plus how to design a workflow before you build it.</p></div>'
  + rows([('cohort-curriculum.html', 'See the full curriculum', 'All six topics in the program.', 'Curriculum'), ('instructors.html', 'Meet your instructors', 'The people who teach in the Academy and the tools they teach.', 'Instructors'), ('academy-testimonials.html', 'Hear from past students', 'What people who took the cohort say about it.', 'Testimonials')]) + '</div></section>'
  + '''<section class="sheet" id="try"><div class="frame"><div class="builds-head"><span class="tag">Try us first</span><h2 class="big">See how we teach <i>before you pay.</i></h2><p>The fee is non-refundable, so get a feel for us first. All of this is free to look through.</p></div>
    <div class="try-grid">
      <a class="try" href="show-and-tell.html"><span class="tag">Watch</span><b>A full session</b><span>See a member walk through a real build in a recorded Show and Tell.</span><span class="more">Watch Show and Tell →</span></a>
      <a class="try" href="blog.html"><span class="tag">Read</span><b>Our articles</b><span>Plain-language guides on no-code, automation and finding your first client.</span><span class="more">Go to the blog →</span></a>
      <a class="try" href="cohort-curriculum.html"><span class="tag">Check</span><b>The curriculum</b><span>Go through all six topics, so you know exactly what you’re paying for.</span><span class="more">See the curriculum →</span></a>
    </div></div></section>'''
  + sheet('light', '<span class="tag">Questions</span><h2 class="big">Before <i>you apply.</i></h2>', '''<dl class="defs">
        <div><dt>Do I need to know how to code?</dt><dd>No. No coding is needed, and you don't need experience with the tools.</dd></div>
        <div><dt>What do I need?</dt><dd>A PC or laptop is the minimum requirement, and you need to be able to commit the required hours each week.</dd></div>
        <div><dt>When does it start?</dt><dd>The next cohort starts on March 3, 2027. Slots are limited, and enrollment closes once they fill.</dd></div>
        <div><dt>Is the fee refundable?</dt><dd>No. The cohort fee is non-refundable, so please be sure you can take part fully.</dd></div>
      </dl>''', 'questions')
  + nxt('apply-cohort.html', 'Ready?', 'Apply to the cohort'))

TOPICS = [('AI and automation foundations', 'The core ideas behind AI and automation, and how they fit together.'), ('Automation with Zapier and Make.com', 'Connect your apps and build workflows that run by themselves.'), ('Airtable as a system hub', 'Use Airtable as the place where your system keeps and organises its data.'), ('Workflow design and systems thinking', 'Learn to plan how a whole process should work before you build it.'), ('GoHighLevel for CRM and automation', 'Manage contacts and automate follow-up with GoHighLevel.'), ('Complete, real systems', 'Bring it all together and build working systems from end to end.')]
page('cohort-curriculum.html', 'Cohort curriculum', 'cohort.html',
  hero('cohort', 'teal', 'teal', crumb(HOME, ('cohort.html', 'Academy'), (None, 'Curriculum')), 'What you\'ll <i>learn.</i>', 'Six topics, from the foundations to complete systems you build yourself.', COUNTDOWN + APPLY_COHORT)
  + sheet('light', '<span class="tag">The curriculum</span><h2 class="big">Six <i>topics.</i></h2>', steps(TOPICS))
  + nxt('cohort.html#questions', 'Still deciding?', 'Read the questions'))

page('academy-testimonials.html', 'Academy testimonials', 'cohort.html',
  hero('', '', '', crumb(HOME, ('cohort.html', 'Academy'), (None, 'Testimonials')), 'From people <i>who took the cohort.</i>', 'What past students of the Nocodesquare Academy say about the AI Automation Cohort.', APPLY_COHORT)
  + '<section class="sheet"><div class="frame">' + quote_cards(ACADEMY_QUOTES, 'a cohort student') + '</div></section>'
  + nxt('cohort.html', 'Want to know more?', 'See how the cohort works'))

for m in MEMBER_STORIES:
    page(m['slug'], m['name'], 'community.html',
      hero('', '', '', crumb(HOME, ('community.html', 'Community'), (None, m['name'])), m['title'], m['name'] + ', ' + m['role'])
      + '<section class="sheet"><div class="frame"><article class="story"><img src="' + m['photo'] + '" alt="Portrait of ' + m['name'] + '"><div class="story-body">'
      + ''.join(f'<p>{x}</p>' for x in m['story'])
      + '<p class="story-sign"><b>' + m['name'] + '</b><span>' + m['role'] + '</span></p></div></article></div></section>'
      + nxt('@@APPLY@@', 'Build with us', 'Apply to the community'))

page('events.html', 'Events', 'events.html',
  hero('crowd', 'copper', 'copper', crumb(HOME, (None, 'Events')), 'Events <i>coming soon.</i>', 'We\'re working on our events. Community members will be the first to hear when they\'re announced.', '<a class="slab" href="@@APPLY@@">Apply to the community</a>')
  + nxt('community.html', 'In the meantime', 'The community'))

TALLY_LOADER = """<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>"""
def tally_embed(form_id, title, extra=''):
    return f"""<iframe data-tally-src="https://tally.so/embed/{form_id}?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1{extra}" loading="lazy" width="100%" height="200" frameborder="0" marginheight="0" marginwidth="0" title="{title}"></iframe>
""" + TALLY_LOADER

page('apply.html', 'Apply to the community', 'community.html',
  hero('', '', '', crumb(HOME, ('community.html', 'Community'), (None, 'Apply')), 'Apply to <i>the community.</i>', 'The community is by application. Have your two Loom videos recorded before you start, because the form asks for the links.')
  + """<section class="sheet apply-sheet"><div class="frame">
    <dl class="defs">
      <div><dt>Video one</dt><dd>Up to 5 minutes about yourself and why the community matters to you.</dd></div>
      <div><dt>Video two</dt><dd>Up to 5 minutes about a recent project you built.</dd></div>
    </dl>
    <div class="form-panel">""" + tally_embed('q4olPO', 'Nocodesquare Membership Application Form') + """</div>
    <p class="form-fallback">Form not showing? <a href="https://tally.so/r/q4olPO" target="_blank" rel="noopener">Open it on its own page</a>.</p>
  </div></section>""")

page('apply-cohort.html', 'Apply to the cohort', 'cohort.html',
  hero('', '', '', crumb(HOME, ('cohort.html', 'Academy'), (None, 'Apply')), 'Apply to <i>the cohort.</i>', 'Fill in the form below. When you finish, you\'ll go to the payment page to secure your place.')
  + """<section class="sheet apply-sheet"><div class="frame">
    <dl class="defs">
      <div><dt>The fee</dt><dd data-fee-switch><span><b data-fee-amount aria-live="polite">₦40,000</b>, paid after this form. The payment is non-refundable.</span>""" + FEE_TABS + """</dd></div>
      <div><dt>What you need</dt><dd>A PC or laptop, and time to commit the required hours each week.</dd></div>
    </dl>
    <div class="form-panel">""" + tally_embed('pb0WzZ', 'Nocodesquare Paid Cohort', '&formEventsForwarding=1') + """</div>
    <p class="form-fallback">Form not showing? <a href="https://tally.so/r/pb0WzZ" target="_blank" rel="noopener">Open it on its own page</a>.</p>
  </div></section>""")

page('join.html', 'Apply', 'join.html',
  hero('africa', 'teal', 'teal', crumb(HOME, (None, 'Apply')), 'Pick your <i>way in.</i>', 'Already building? Apply to the community. Just starting? The cohort is the place to begin.')
  + '<section class="sheet light"><div class="frame">'
  + rows([('@@APPLY@@', 'Apply to the community', 'For people already building. You\'ll share your goal, your tools and two short Loom videos, so have those links ready.', 'Start here'), ('apply-cohort.html', 'Apply to the cohort', 'The next AI Automation Cohort starts on March 3, 2027. No coding or experience needed. ' + FEE_TEXT + '.', 'Cohort'), ('#', 'Get event updates', 'Hear about our events as soon as they\'re announced.', 'Events'), (YOUTUBE_URL, 'Subscribe on YouTube', 'Watch recordings of our Show and Tell sessions.', 'YouTube')]) + '</div></section>')

# ------------------------------------------------------------------ merch shop
# Prices are placeholders until confirmed. A product with photos uses them; the rest are drawn here until they have photos.
INK = ('Ink', '#1E1F26', '#F3F4F3', '#6A6D80')
WHITE = ('White', '#FAFAF8', '#1E1F26', '#393A47')
TEAL = ('Teal', '#5ECDCB', '#14282B', '#393A47')
COPPER = ('Copper', '#A86C48', '#FFFFFF', '#393A47')
NATURAL = ('Natural', '#E6DFCF', '#1E1F26', '#393A47')

def txt(lines, cx, y, size, gap=None, weight=800):
    gap = gap or size * .92
    return ''.join(f'<text x="{cx}" y="{y + i * gap}" text-anchor="middle" fill="var(--print)" style="font-family:var(--font);font-stretch:75%;font-weight:{weight};font-size:{size}px;letter-spacing:-.01em">{l}</text>' for i, l in enumerate(lines))

def logo(cx, y, cube, size):
    return (f'<use href="#cube" x="{cx - cube * .433}" y="{y}" width="{cube * .866}" height="{cube}"/>'
            f'<text x="{cx}" y="{y + cube + size * 1.15}" text-anchor="middle" fill="var(--print)" style="font-family:var(--font);font-stretch:100%;font-size:{size}px;letter-spacing:-.01em"><tspan font-weight="800">NOCODE</tspan><tspan font-weight="400">SQUARE</tspan></text>')

EDGE = 'stroke="rgba(0,0,0,.14)" stroke-width="1.5"'
FOLD = 'fill="none" stroke="rgba(0,0,0,.09)" stroke-width="2" stroke-linecap="round"'

def tee(art):
    return f'''<path fill="var(--garment)" {EDGE} d="M140 70 C155 86 245 86 260 70 L320 95 L367 165 L322 196 L300 166 L300 346 Q200 358 100 346 L100 166 L78 196 L33 165 L80 95 Z"/>
    <path fill="rgba(0,0,0,.2)" d="M140 70 C155 86 245 86 260 70 C245 100 155 100 140 70 Z"/>
    <path {FOLD} d="M100 166 C106 150 108 132 104 112 M300 166 C294 150 292 132 296 112 M125 340 C130 310 128 290 122 270 M278 340 C272 312 274 292 280 268"/>{art}'''

def hoodie(art):
    return f'''<path fill="var(--garment)" {EDGE} d="M135 92 C122 22 278 22 265 92 L265 114 L135 114 Z"/>
    <path fill="rgba(0,0,0,.28)" d="M152 90 C146 44 254 44 248 90 C226 104 174 104 152 90 Z"/>
    <path fill="var(--garment)" {EDGE} d="M135 84 C160 108 240 108 265 84 L318 106 L356 298 L320 310 L292 196 L292 354 Q200 366 108 354 L108 196 L80 310 L44 298 L82 106 Z"/>
    <path fill="rgba(0,0,0,.08)" d="M142 282 L258 282 L280 344 L120 344 Z"/>
    <path {FOLD} d="M186 104 L183 150 M214 104 L217 150 M142 282 L258 282"/>{art}'''

def cap(art):
    return f'''<path fill="var(--garment)" {EDGE} d="M96 250 C88 118 312 118 304 250 Z"/>
    <path fill="var(--garment)" {EDGE} d="M84 250 C140 232 260 232 316 250 C342 262 342 284 316 280 C256 268 144 268 84 280 C58 284 58 262 84 250 Z"/>
    <path fill="rgba(0,0,0,.16)" d="M84 280 C144 268 256 268 316 280 C342 284 342 262 316 250 C330 268 300 266 200 258 C100 266 70 268 84 250 C58 262 58 284 84 280 Z"/>
    <path {FOLD} d="M200 142 L200 236 M140 156 C126 180 120 208 120 240 M260 156 C274 180 280 208 280 240"/>{art}'''

def tote(art):
    return f'''<path fill="none" stroke="var(--garment)" stroke-width="13" d="M150 150 C150 40 250 40 250 150"/>
    <path fill="none" stroke="rgba(0,0,0,.14)" stroke-width="1.5" d="M143.500 150 C143.500 30 256.500 30 256.500 150"/>
    <path fill="var(--garment)" {EDGE} d="M102 140 L298 140 L312 358 L88 358 Z"/>
    <path {FOLD} d="M112 340 C118 300 116 270 110 240 M290 340 C284 300 286 270 292 240"/>{art}'''

def mug(art):
    return f'''<path fill="none" stroke="var(--garment)" stroke-width="20" d="M292 170 C352 164 352 268 292 262"/>
    <path fill="var(--garment)" {EDGE} d="M92 118 L296 118 L296 306 C296 334 92 334 92 306 Z"/>
    <ellipse cx="194" cy="118" rx="102" ry="20" fill="var(--garment)" {EDGE}/>
    <ellipse cx="194" cy="119" rx="90" ry="14" fill="rgba(0,0,0,.28)"/>{art}'''

def stickers(_):
    return '''<g transform="rotate(-9 130 140)"><rect x="62" y="72" width="136" height="136" rx="18" fill="#FFFFFF" stroke="rgba(0,0,0,.14)"/><use href="#cube" x="92" y="88" width="78" height="90"/></g>
    <g transform="rotate(7 265 150)"><rect x="196" y="96" width="172" height="104" rx="14" fill="#1E1F26"/><text x="282" y="143" text-anchor="middle" fill="#F3F4F3" style="font-family:var(--font);font-stretch:75%;font-weight:800;font-size:34px">I AM A</text><text x="282" y="180" text-anchor="middle" fill="#5ECDCB" style="font-family:var(--font);font-stretch:75%;font-weight:800;font-size:34px">BUILDER</text></g>
    <circle cx="136" cy="290" r="72" fill="#5ECDCB" stroke="rgba(0,0,0,.1)"/><text x="136" y="306" text-anchor="middle" fill="#14282B" style="font-family:var(--font);font-weight:800;font-size:46px;letter-spacing:-.04em">NCS</text>
    <g transform="rotate(-5 285 300)"><rect x="208" y="244" width="160" height="110" rx="14" fill="#A86C48"/><text x="288" y="292" text-anchor="middle" fill="#FFF" style="font-family:var(--font);font-stretch:75%;font-weight:800;font-size:24px">BUILT WITHOUT</text><text x="288" y="327" text-anchor="middle" fill="#FFF" style="font-family:var(--font);font-stretch:75%;font-weight:300;font-size:28px">CODE</text></g>'''

# Colours for products with real photos: (name, swatch colour)
NAVY_P, WHITE_P, AQUA_P, TEAL_P = ('Navy', '#1F2A4D'), ('White', '#FAFAF8'), ('Aqua', '#6FC9CF'), ('Teal', '#2F8E9E')
def shots(*names):
    return [f'img/merch/{n}.jpg' for n in names]

SIZES = ['S', 'M', 'L', 'XL', 'XXL']
PRODUCTS = [
  dict(id='cube-hoodie', name='Cube Hoodie', price=32000, usd=24, kes=3100, kind='Hoodie', sizes=SIZES,
       photos=[(WHITE_P, shots('hoodie-cube-white-worn', 'cap-wordmark-navy-worn')), (NAVY_P, shots('hoodie-cube-navy-worn'))],
       desc='A clean hoodie with one small embroidered cube on the chest and nothing else.'),
  dict(id='wordmark-cap', name='Wordmark Corduroy Cap', price=10000, usd=8, kes=1000, kind='Cap', sizes=['One size'],
       photos=[(NAVY_P, shots('cap-wordmark-navy-flat', 'cap-wordmark-navy-worn')), (WHITE_P, shots('cap-wordmark-white-flat')), (AQUA_P, shots('cap-wordmark-aqua-worn'))],
       desc='A corduroy cap with the Nocodesquare name embroidered across the front.'),
  dict(id='logo-cap', name='Logo Corduroy Cap', price=10000, usd=8, kes=1000, kind='Cap', sizes=['One size'],
       photos=[(NAVY_P, shots('cap-logo-navy-worn', 'cap-logo-navy-flat')), (TEAL_P, shots('cap-logo-teal-worn', 'cap-logo-teal-flat')), (AQUA_P, shots('cap-logo-aqua-worn'))],
       desc='A corduroy cap with the full logo embroidered on the front: the name and the cube together.'),
  dict(id='cube-cap', name='Cube Corduroy Cap', price=10000, usd=8, kes=1000, kind='Cap', sizes=['One size'],
       photos=[(NAVY_P, shots('cap-cube-navy-worn'))],
       desc='A corduroy cap with only the embroidered cube. For people who already know.'),
  dict(id='cube-tote', name='Cube Corduroy Tote', price=8000, usd=6, kes=800, kind='Tote', sizes=['One size'],
       photos=[(AQUA_P, shots('tote-cube-aqua')), (('Charcoal', '#4A4C57'), shots('tote-cube-charcoal')), (WHITE_P, shots('tote-cube-white'))],
       desc='A soft corduroy tote with long shoulder straps and one embroidered cube on the front.'),
  dict(id='cube-keychain', name='Cube Keychain', price=5000, usd=4, kes=500, kind='Keychain', sizes=['One size'],
       photos=[(('Copper and teal', '#A86C48'), shots('keychain-cube'))],
       desc='The logo cube as a solid keychain, with copper, teal and dark grey faces.'),
]

def naira(n):
    return f'₦{n:,}'

def prices(p):
    return f'<span data-prices data-naira="{naira(p["price"])}" data-dollars="${p["usd"]}" data-shillings="KSh {p["kes"]:,}">{naira(p["price"])}</span>'

# The same switch as the cohort fee. The visitor's choice carries across the whole site.
PRICE_TABS = '<div class="cur-tabs" role="group" aria-label="Show prices in">' + ''.join(
    f'<button type="button" data-cur="{name}" aria-pressed="{"true" if i == 0 else "false"}">{name}</button>'
    for i, name in enumerate(['Naira', 'Dollars', 'Shillings'])) + '</div>'

# The small version on each product card: symbols, so it fits a narrow card on a phone
def card_tabs(p):
    return f'<div class="cur-tabs" role="group" aria-label="Show the {p["name"]} price in">' + ''.join(
        f'<button type="button" data-cur="{name}" aria-label="{name}" aria-pressed="{"true" if i == 0 else "false"}">{mark}</button>'
        for i, (name, mark) in enumerate([('Naira', '₦'), ('Dollars', '$'), ('Shillings', 'KSh')])) + '</div>'

def mock(p, colour=None, label=True):
    if p.get('photos'):
        col, imgs = p['photos'][0]
        return f'<img class="mock" src="{imgs[0]}" alt="{p["name"]} in {col[0].lower()}" loading="lazy">'
    c = colour or p['colours'][0]
    aria = f'Drawing of the {p["name"]} in {c[0].lower()}' if p['draw'] is not stickers else 'Drawing of four Nocodesquare stickers'
    return f'<svg class="mock" viewBox="0 0 400 400" role="img" aria-label="{aria}" style="--garment:{c[1]};--print:{c[2]};--cube-right:{c[3]}">{p["draw"](p["art"])}</svg>'

def card(p):
    return f'<div class="product" data-cur-scope><a class="product-link" href="merch-{p["id"]}.html"><span class="tile">{mock(p)}</span><span class="pname">{p["name"]}</span></a><span class="pprice" aria-live="polite">{prices(p)}</span>{card_tabs(p)}</div>'

CARTLINK = '<a class="more cartlink" href="cart.html">Your cart (<span data-cart-count>0</span>)</a>'

page('merch.html', 'Merch', '',
  hero('', '', '', crumb(HOME, (None, 'Merch')), 'Wear what <i>you build.</i>', 'Caps, hoodies, totes and a keychain for people who build with no-code and AI.', CARTLINK)
  + '<section class="sheet"><div class="frame"><div class="shop-grid">' + ''.join(card(p) for p in PRODUCTS) + '</div></div></section>')

for i, p in enumerate(PRODUCTS):
    photos = p.get('photos')
    swatches = ''.join(
        f'<label class="swatch"><input type="radio" name="colour" value="{c[0]}"{" checked" if j == 0 else ""}><i style="background:{c[1]}"></i><span>{c[0]}</span></label>'
        for j, (c, _) in enumerate(photos)) if photos else ''.join(
        f'<label class="swatch"><input type="radio" name="colour" value="{c[0]}" data-garment="{c[1]}" data-print="{c[2]}" data-cube="{c[3]}"{" checked" if j == 0 else ""}><i style="background:{c[1]}"></i><span>{c[0]}</span></label>'
        for j, c in enumerate(p['colours']))
    if photos and len(photos) == 1:
        colour_field = f'<input type="hidden" name="colour" value="{photos[0][0][0]}">'
    elif not photos and p['draw'] is stickers:
        colour_field = '<input type="hidden" name="colour" value="Mixed">'
    else:
        colour_field = f'<fieldset class="opt"><legend class="tag">Colour</legend><div class="swatches">{swatches}</div></fieldset>'
    if len(p['sizes']) > 1:
        size_field = '<div class="opt"><label class="tag" for="size">Size</label><select id="size" name="size">' + ''.join(f'<option{" selected" if s == "M" else ""}>{s}</option>' for s in p['sizes']) + '</select></div>'
    else:
        size_field = '<input type="hidden" name="size" value="One size">'
    more = [PRODUCTS[(i + k) % len(PRODUCTS)] for k in (1, 2, 3, 4)]
    if photos:
        data = json.dumps({c[0]: imgs for c, imgs in photos}).replace('"', '&quot;')
        gallery = f'<div class="gallery" data-photos="{data}" data-name="{p["name"]}"><div class="tile big-tile">{mock(p).replace(" loading=" + chr(34) + "lazy" + chr(34), "")}</div><div class="thumbs"></div></div>'
    else:
        gallery = f'<div class="tile big-tile">{mock(p)}</div>'
    body = f"""<section class="sheet buy"><div class="frame">
    {crumb(HOME, ('merch.html', 'Merch'), (None, p['name']))}
    <div class="buy-grid">
      {gallery}
      <form class="buy-form" data-cur-scope data-id="{p['id']}" data-name="{p['name']}" data-price="{p['price']}" data-usd="{p['usd']}" data-kes="{p['kes']}" data-href="merch-{p['id']}.html">
        <span class="chip">{p['kind']}</span>
        <h1 class="big">{p['name']}</h1>
        <p class="pprice big-price" aria-live="polite">{prices(p)}</p>
        {PRICE_TABS}
        <p class="lead">{p['desc']}</p>
        {colour_field}
        {size_field}
        <div class="opt"><label class="tag" for="qty">Quantity</label><input id="qty" name="qty" type="number" min="1" max="50" value="1" inputmode="numeric"></div>
        <div class="buy-row"><button class="slab" type="submit">Add to cart</button>{CARTLINK}</div>
        <p class="added" role="status" hidden></p>
      </form>
    </div>
  </div></section>
  <section class="sheet"><div class="frame">
    <div class="head"><h2 class="big">More <i>to wear.</i></h2></div>
    <div class="shop-grid">{''.join(card(m) for m in more)}</div>
  </div></section>"""
    page(f'merch-{p["id"]}.html', p['name'], '', body)

page('cart.html', 'Your cart', '',
  hero('', '', '', crumb(HOME, ('merch.html', 'Merch'), (None, 'Your cart')), 'Your <i>cart.</i>', 'Check your items, then add your details to order.')
  + '''<section class="sheet"><div class="frame">
    <div class="cart-grid">
      <div class="cart-lines" id="cartLines"></div>
      <form class="cart-form" id="orderForm">
        <div class="cart-total"><span class="tag">Total</span><b id="cartTotal" data-prices aria-live="polite">₦0</b></div>
        ''' + PRICE_TABS + '''
        <p class="note">Delivery is confirmed with you after you order.</p>
        <div class="opt"><label class="tag" for="oName">Full name</label><input id="oName" name="name" required autocomplete="name"></div>
        <div class="opt"><label class="tag" for="oPhone">Phone or WhatsApp number</label><input id="oPhone" name="phone" type="tel" required autocomplete="tel"></div>
        <div class="opt"><label class="tag" for="oAddress">Delivery address</label><textarea id="oAddress" name="address" rows="3" required autocomplete="street-address"></textarea></div>
        <button class="slab" type="submit">Place order</button>
        <div class="order-result" id="orderResult" role="status" hidden></div>
      </form>
    </div>
  </div></section>''')

# ------------------------------------------------------------------ blog
BLOG_DATE = 'November 5, 2026'
S_OPENAI = ('OpenAI model list', 'https://developers.openai.com/api/docs/models')
S_GOOGLE = ('Gemini API changelog', 'https://aistudio.google.com/docs/changelog')
S_MAKE = ('Make pricing', 'https://www.make.com/en/pricing')
S_N8N = ('n8n pricing', 'https://n8n.io/pricing/')
S_META = ('Meta: WhatsApp Business Platform pricing', 'https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing')
S_DUBAWA = ('Dubawa fact check on the "₦14 per message" claim', 'https://dubawa.org/misleading-whatsapp-not-set-to-charge-nigerians-n14-per-message/')
S_YARN = ('YarnGPT on GitHub', 'https://github.com/saheedniyi02/yarngpt')
S_LELAPA = ('Princeton Africa World: Lelapa AI launches InkubaLM', 'https://africaworld.princeton.edu/news/2024/lelapa-ai-launches-africa%E2%80%99s-first-ai-large-language-model')
S_ITWEB = ("ITWeb Africa: Africa's languages are becoming the next AI battleground", 'https://itweb.africa/article/africas-languages-are-becoming-the-next-ai-battleground/KA3Ww7dzdaVqrydZ')

POSTS = [
 dict(slug='what-is-no-code', cat='Start here', title='What is no-code? A plain guide for African builders',
  dek='You can build real software without writing traditional code. Here is what that means and where to begin.', sources=[], body="""
<p>Think about building with LEGO. The pieces already exist, so your job is to decide what to make and how the pieces connect. No-code tools work the same way for software. You arrange ready-made parts on a screen, and the tool handles the code underneath.</p>
<h2>What people actually build</h2>
<p>No-code usually falls into three groups:</p>
<ul>
<li><b>Apps and websites.</b> Booking pages, customer portals and internal dashboards.</li>
<li><b>Databases.</b> Tools like Airtable look like spreadsheets but can run a whole operation.</li>
<li><b>Automations.</b> Work that runs by itself. Tools like Make, n8n and Zapier connect your other apps so information moves without anyone copying and pasting.</li>
</ul>
<h2>A small example</h2>
<p>Imagine a tailor in Ibadan who takes orders through a form. Every morning, someone copies each order into a sheet, then messages the customer to confirm. With an automation, a new form entry adds a row to the sheet and sends the confirmation immediately. Nobody has to touch it, and nothing gets forgotten.</p>
<h2>Is it "real" building?</h2>
<p>Yes. A customer does not care how the system was made. They care that their order was confirmed. You still have to think clearly about steps, data and what happens when something goes wrong. Those are the same skills developers use, and they are the hard part.</p>
<p>No-code does have limits. Very large systems, unusual features and tight performance needs can outgrow it. Many builders reach that point later and bring in a developer for that one piece. That is a good problem to have.</p>
<h2>Where to start</h2>
<ol>
<li><b>Pick one annoying task.</b> Choose something you repeat every week.</li>
<li><b>Write the steps down in plain words.</b> "When this happens, do that, then do this."</li>
<li><b>Build it in a free plan.</b> Make and n8n are both good places to begin.</li>
<li><b>Show someone.</b> Other builders will spot problems and shortcuts you missed.</li>
</ol>
"""),
 dict(slug='no-code-and-ai', cat='AI automation', title='No-code and AI: how they work together',
  dek='Automation follows rules. AI handles judgement. Most useful systems need both, and knowing where each belongs is the skill.', sources=[], body="""
<p>People often talk about no-code and AI as if they were the same thing. They do different jobs, and the best systems use each for what it does well.</p>
<p>A simple way to picture it: <b>automation is the hands, and AI is the judgement.</b> The automation moves information reliably from one place to another. The AI reads something messy and decides what it means.</p>
<h2>Where the rules stop working</h2>
<p>Take a delivery company in Nairobi that receives requests on WhatsApp. Customers write in every style imaginable: "pls pick up from Westlands 2pm", a voice note, or a long story with the address in the middle.</p>
<p>A rules-based automation cannot read that reliably. A language model can. It turns the message into clean fields such as pickup point, time and urgency. From there, the automation takes over: it creates the record, assigns a rider and sends a confirmation.</p>
<h2>Three jobs AI does well inside a workflow</h2>
<ul>
<li><b>Extract.</b> Pull details out of messages, receipts and documents.</li>
<li><b>Classify.</b> Decide whether this is a complaint, an order or a question, and route it.</li>
<li><b>Draft.</b> Write a first version of a reply for a person to approve, or send it directly when the risk is low.</li>
</ul>
<h2>Where people go wrong</h2>
<p>The common mistake is giving AI work that a simple rule could do. If you need to add 7.5% VAT, use a calculation. A model might get it right most of the time, but "most of the time" is not good enough for money. It also costs more and runs slower.</p>
<p>Use this test: <b>if you can write the rule down, write the rule. If a person would have to read and think, consider AI.</b></p>
<h2>Keep a person where it matters</h2>
<p>AI will sometimes be wrong while sounding completely sure. So check its output before it reaches anything important. Confirm that required fields are present, send low-confidence cases to a human, and keep a log so you can see what happened. For refunds, debt conversations or anything legal, a person should review the result.</p>
<h2>Start small</h2>
<p>Take an automation you already have and add one AI step where someone currently has to read and sort. Run it beside your current process for a week, compare the results, and only then let it run alone.</p>
"""),
 dict(slug='make-vs-n8n-vs-zapier', cat='Tools', title='Make, n8n or Zapier: which should you learn first?',
  dek='They do similar jobs but charge very differently. That difference matters more when you are paying in dollars or euros.', sources=[S_MAKE, S_N8N], body="""
<p>All three tools connect apps and run workflows. Once you understand one, the others come quickly, because triggers, actions and data mapping work much the same way. So the first choice matters less than people think. Cost is usually the deciding factor.</p>
<h2>How each one charges</h2>
<ul>
<li><b>Make</b> bills in credits, and most actions use one credit. Its free plan includes 1,000 credits a month.</li>
<li><b>n8n</b> cloud bills per workflow run, however many steps that run contains. On annual billing, its pricing page lists Starter at €20 a month for 2,500 runs and Pro at €50 a month for 10,000. There is also a self-hosted version available on GitHub, where you run it on your own server.</li>
<li><b>Zapier</b> bills per task, which roughly means each action that completes. It is known for being very easy to use and for connecting to a huge number of apps.</li>
</ul>
<h2>The same job on each tool</h2>
<p>Say your workflow has five steps and runs 1,000 times a month. On Make, that is about 5,000 credits. On Zapier, it is roughly 4,000 tasks, since the starting trigger does not count. On n8n, it is 1,000 runs.</p>
<p>Longer workflows make the gap wider. That is why n8n becomes attractive for complex systems, and why it is worth doing this sum before you promise a client a monthly cost.</p>
<h2>What we would tell a friend</h2>
<ul>
<li><b>Complete beginner:</b> start with Make. You can see the data moving through each step on a visual canvas, which makes learning much easier.</li>
<li><b>Comfortable with technical things, or building heavy workflows:</b> learn n8n. Self-hosting can keep costs down, but you become responsible for keeping the server running, updated and secure.</li>
<li><b>Connecting two popular apps quickly:</b> Zapier is often the fastest way to get it done.</li>
</ul>
<h2>Before you commit</h2>
<p>Pricing changes often, so check each tool's own pricing page rather than a blog post, including this one. Then work out the cost in naira or shillings for your real volume, and leave room for exchange-rate moves.</p>
"""),
 dict(slug='ai-models-november-2026', cat='New models', title='The AI models worth knowing right now',
  dek='A plain snapshot of the current line-ups from OpenAI, Google and Anthropic, and how to choose between them for automation work.', sources=[S_OPENAI, S_GOOGLE], body="""
<p>This list goes out of date quickly, so treat it as a snapshot from November 2026 and check each company's own page before you build on it.</p>
<h2>OpenAI</h2>
<ul>
<li><b>GPT-6 Astra.</b> Its most capable model, for complex reasoning, coding and demanding work.</li>
<li><b>GPT-6.1 Sol.</b> Close to Astra on complex work, at a lower cost.</li>
<li><b>GPT-6.1 Terra.</b> Fast and efficient, aimed at visual reasoning, computer use and natural writing.</li>
<li><b>GPT-6 Luna.</b> Its most efficient model, for focused, high-volume tasks where cost matters.</li>
</ul>
<h2>Google</h2>
<ul>
<li><b>Gemini 4 Argon.</b> The most capable model in Google's recent changelog, built for complex coding, agent, maths and science tasks. It became generally available on October 13, 2026.</li>
<li><b>Gemini 3.8 Flash.</b> Described as Google's most intelligent Flash model.</li>
<li><b>Gemini 3.8 Flash TTS and Flash-Lite TTS.</b> Text-to-speech models, which are useful for voice work.</li>
</ul>
<p>One thing to act on: from December 1, 2026, Google will route API requests for Gemini 2.5 Pro and 2.5 Flash to newer models. If you have an automation still using either one, test it now.</p>
<h2>Anthropic</h2>
<p>Anthropic's current Claude models are Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5. Check Anthropic's documentation for what each is best suited to and what it costs.</p>
<h2>How to choose for automation</h2>
<p>The newest and strongest model is rarely the right default. Most workflow steps are small jobs, like sorting a message or pulling a date from an email.</p>
<ol>
<li><b>Start with the cheapest model that might work.</b> Move up only when it actually fails.</li>
<li><b>Test on your own messy data.</b> Use 20 or 30 real examples, including Pidgin, Sheng, typos and whatever else your customers really send. Published rankings will not tell you how a model handles that.</li>
<li><b>Mix models in one system.</b> Use a low-cost model for high-volume sorting and a stronger one for the rare hard cases.</li>
<li><b>Work out the cost per job.</b> Multiply that by your monthly volume before you promise anyone a price.</li>
<li><b>Expect models to retire.</b> Keep the model name in one easy-to-change setting, and re-test whenever you switch.</li>
</ol>
"""),
 dict(slug='whatsapp-automation-costs', cat='Building in Africa', title='WhatsApp automation: what changed and what it costs',
  dek="Meta's pricing changed on October 1, 2026, including for replies to customers. Here is what builders need to know before they quote a client.", sources=[S_META, S_DUBAWA], body="""
<p>For many African businesses, WhatsApp is the main customer channel, so it is often the first thing clients ask you to automate. Pricing rules on the WhatsApp Business Platform changed recently, and an old tutorial may give you the wrong numbers.</p>
<h2>First, who pays</h2>
<p>This pricing applies to businesses using the platform. Meta does not charge for messages that users send to businesses. A claim that ordinary Nigerians would pay ₦14 a message was fact-checked as misleading.</p>
<h2>How billing works</h2>
<p>Since July 1, 2025, Meta has charged per delivered message, based on the message's category and the recipient's country. The main categories are:</p>
<ul>
<li><b>Marketing.</b> Template messages such as promotions and offers.</li>
<li><b>Utility.</b> Template messages about something already happening, such as an order update or a payment reminder.</li>
<li><b>Authentication.</b> Template messages such as one-time passwords.</li>
<li><b>Service.</b> Ordinary free-form replies, sent after a customer messages you.</li>
</ul>
<h2>What changed on October 1, 2026</h2>
<ul>
<li>Each business phone number now gets <b>1,000 free service messages a month</b>. Charges begin with message 1,001.</li>
<li><b>Utility templates sent during an open customer-service window are now charged</b> at published rates. They used to be free.</li>
<li>Businesses needed a payment method on file by September 30, 2026, or their service messages could stop being delivered.</li>
</ul>
<p>Nigeria has its own line on Meta's rate card. Rates can change at the start of a quarter, so take the current figure from Meta directly and avoid quoting a number from a social media post.</p>
<h2>What to do as a builder</h2>
<ol>
<li><b>Count messages by category.</b> "How many customers?" is the wrong question. Ask how many marketing, utility and service messages each one will receive.</li>
<li><b>Audit old automations.</b> A flow that sends order updates inside the service window may have become a new cost since October.</li>
<li><b>Send fewer, better messages.</b> Combine three status updates into one where you can.</li>
<li><b>Build in consent and an exit.</b> Only message people who opted in, make it easy to stop, and hand off to a person when someone needs one.</li>
<li><b>Put the cost in your proposal.</b> Make clear that WhatsApp charges are separate from your fee, so a client is not surprised later.</li>
</ol>
"""),
 dict(slug='voice-ai-african-languages', cat='Building in Africa', title='Voice AI in African languages: where things stand',
  dek='Many customers would rather talk than type. Here is how voice agents work, who is building for African languages, and what to test.', sources=[S_YARN, S_LELAPA, S_ITWEB], body="""
<p>Across much of Africa, a phone call is still the most natural way to get something done. That makes voice AI especially interesting here. It also makes it harder, because most models were not trained on the way people here speak.</p>
<h2>How a voice agent works</h2>
<p>A voice agent is a relay race with three runners:</p>
<ol>
<li><b>It listens.</b> Speech-to-text turns the caller's words into text.</li>
<li><b>It thinks.</b> A language model decides what to say or do next, such as checking a calendar.</li>
<li><b>It speaks.</b> Text-to-speech turns the reply into a voice.</li>
</ol>
<p>Platforms such as Retell AI and VAPI manage this relay, so you can focus on the conversation and on connecting it to your other systems. Every runner adds delay, and long pauses are what make a call feel robotic.</p>
<h2>Who is working on African languages</h2>
<ul>
<li><b>YarnGPT</b> is an open-source text-to-speech model that generates Nigerian-accented English.</li>
<li><b>Lelapa AI</b> built InkubaLM, a language model covering Swahili, Yoruba, isiXhosa, Hausa and isiZulu.</li>
<li><b>Intron</b>, a Nigerian startup, has reportedly expanded its Sahara voice model to 57 languages, including 23 African ones.</li>
</ul>
<p>This space moves quickly, and a claim on a website does not guarantee a good result on your calls. Test for yourself.</p>
<h2>What to test before you trust it</h2>
<ul>
<li><b>Mixed speech.</b> People switch between English, Pidgin, Yoruba or Sheng in one sentence. Test that, not textbook phrases.</li>
<li><b>Real phone lines.</b> Background noise and poor connections are normal. Studio-quality samples will flatter any model.</li>
<li><b>Names, numbers and addresses.</b> Small errors here cause the biggest problems, so have the agent read important details back.</li>
<li><b>Whether people accept it.</b> A voice can be accurate and still feel wrong. Let real customers listen.</li>
</ul>
<h2>Build it responsibly</h2>
<p>Tell callers they are speaking with an AI, follow local rules on recording and data, and always give people a way to reach a human. This matters most in sensitive conversations such as debt or health.</p>
<p>A good first project is one narrow job, such as confirming appointments in one language. Get that working well before you add more.</p>
"""),
 dict(slug='first-paying-automation-client', cat='Career', title='How to land your first paying automation client',
  dek='You do not need a big portfolio. You need one real problem solved, and a clear way to explain what it was worth.', sources=[], body="""
<p>Most people wait too long, because they think they need more courses first. What gets you hired is proof that you can solve one real problem.</p>
<h2>1. Build one thing for a real person</h2>
<p>Find a business you can already reach: a relative's shop, a friend's clinic or the logistics company a former classmate works at. Ask what they repeat every week and hate doing. Then build a fix. Doing this first one free or cheaply is fine, as long as you agree you can talk about the result.</p>
<h2>2. Measure before and after</h2>
<p>Note how long the task took before, and how long it takes now. "This used to take Amaka two hours a day and now takes ten minutes" will do more for you than a list of tools. Ask for permission to share it, and ask for a short testimonial while the win is fresh.</p>
<h2>3. Sell the result, not the tools</h2>
<p>A business owner does not wake up wanting an n8n workflow. They want fewer missed orders, faster follow-up or fewer hours of admin. Say "I'll make sure every lead gets a reply within five minutes", then explain the tools only if they ask.</p>
<h2>4. Reach out with something specific</h2>
<p>Generic messages get ignored. Look at how a business works, spot one thing you could improve, and say so: "I tried booking on your site and only got a form with no confirmation. I can fix that so customers get an instant reply." A short screen recording of a demo works even better.</p>
<h2>5. Price it sensibly</h2>
<ul>
<li><b>Set a fixed project price.</b> Charging by the hour punishes you for getting faster.</li>
<li><b>Tie it to the value.</b> Work out roughly what the problem costs them each month, and price well below that.</li>
<li><b>Take part of it up front.</b> A deposit filters out people who are not serious.</li>
<li><b>Charge for upkeep.</b> Tools change and things break. A monthly maintenance fee is fair, and it gives you steadier income.</li>
<li><b>Separate tool costs.</b> Be clear about who pays for subscriptions, API usage and messaging.</li>
</ul>
<h2>6. Agree the scope in writing</h2>
<p>Even a short message helps: what you will build, what is not included, how many rounds of changes they get, and when payment is due. It protects your friendship as well as your time. Then hand over simple documentation, and ask who else they know with the same problem.</p>
"""),
 dict(slug='building-automation-in-africa', cat='Building in Africa', title='Building automation in Africa: what the tutorials leave out',
  dek='Most tutorials assume steady internet, card payments and English-speaking customers. Here is how to build for the market you actually work in.', sources=[], body="""
<p>Most automation tutorials are made for somewhere else. They assume stable connections, international cards and customers who fill in forms correctly. A system that works in that demo can fall apart in Lagos or Kampala.</p>
<h2>Assume the connection will fail</h2>
<p>Networks drop and services time out. A cloud automation keeps running, but the people and systems around it may not respond, so plan for that:</p>
<ul>
<li><b>Set up retries</b> so a failed step tries again before it gives up.</li>
<li><b>Add failure alerts</b> so a person knows when something has stopped.</li>
<li><b>Never lose the data.</b> Save the incoming record first, then process it. If a later step fails, you can run it again.</li>
<li><b>Avoid doing things twice.</b> A retry should not charge or message someone a second time. Check whether a step already happened.</li>
</ul>
<h2>Budget for currency</h2>
<p>Many tools bill in dollars or euros, while your client earns in naira, cedis or shillings. A cost that looks fine today can look very different after an exchange-rate move. Quote with a buffer, state which currency each tool bills in, and agree who carries that risk. Virtual dollar cards can also fail on some services, so test payment before you commit a client to a tool.</p>
<h2>Meet customers where they are</h2>
<p>A beautifully built web form may lose to a simple WhatsApp conversation or a phone call. Start with the channel customers already use, even if it is less tidy to automate.</p>
<h2>Plan for local payments</h2>
<p>Many customers pay by bank transfer, mobile money or USSD, and not by card. Providers such as Paystack and Flutterwave can notify your automation by webhook when a payment succeeds. Bank transfers often need a matching step, because the amount or the reference may not be exact. Decide what happens when they do not match, and send those cases to a person.</p>
<h2>Handle messy, multilingual data</h2>
<p>People mix languages and spell the same name in many ways. Phone numbers appear with and without country codes. Clean this up early: store numbers in one format, and test any AI step on real local messages.</p>
<h2>Take data protection seriously</h2>
<p>Nigeria has its Data Protection Act of 2023, Kenya has its Data Protection Act of 2019, and other countries have their own laws. Collect only what you need, know which tools hold the data, and get proper advice for sensitive work. This also helps you win bigger clients, who will ask.</p>
<h2>The opportunity</h2>
<p>These constraints are also your advantage. Someone who understands how business really works here can build things that a tool made elsewhere will never handle properly.</p>
"""),
]

def read_mins(html):
    return max(2, round(len(re.sub(r'<[^>]+>', ' ', html).split()) / 200))

def post_card(p):
    return f'''<a class="post" href="blog-{p['slug']}.html"><span class="chip">{p['cat']}</span><h3>{p['title']}</h3><p>{p['dek']}</p><span class="post-meta">{read_mins(p['body'])} min read</span></a>'''

page('blog.html', 'Blog', '',
  hero('', '', '', crumb(HOME, (None, 'Blog')), 'Notes from <i>the build.</i>', 'Practical articles on no-code, AI and automation, and what it takes to build in Africa.')
  + '<section class="sheet"><div class="frame"><div class="post-grid">' + ''.join(post_card(p) for p in POSTS) + '</div></div></section>'
  + nxt('@@APPLY@@', 'Want to talk about it?', 'Apply to the community'))

for i, p in enumerate(POSTS):
    prev_p, next_p = POSTS[(i - 1) % len(POSTS)], POSTS[(i + 1) % len(POSTS)]
    src = ''
    if p['sources']:
        src = '<aside class="sources"><span class="tag">Sources</span><ul>' + ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in p['sources']) + '</ul></aside>'
    body = f"""<article class="post-page">
    <header class="pagehero"><div class="frame">
      {crumb(HOME, ('blog.html', 'Blog'), (None, p['cat']))}
      <h1 class="big">{p['title']}</h1>
      <p>{p['dek']}</p>
      <div class="post-meta">{BLOG_DATE} / {read_mins(p['body'])} min read / Nocodesquare</div>
    </div></header>
    <div class="prose">{p['body']}{src}
      <div class="post-cta"><b>Building something like this?</b><span>Bring your questions to other builders in the community.</span><a class="slab" href="@@APPLY@@">Apply to the community</a></div>
    </div>
  </article>
  <nav class="pager" aria-label="More articles"><a href="blog-{prev_p['slug']}.html"><span class="tag">Previous</span><b>← {prev_p['title']}</b></a><a href="blog-{next_p['slug']}.html"><span class="tag">Next</span><b>{next_p['title']} →</b></a></nav>"""
    page(f"blog-{p['slug']}.html", p['title'], '', body)

# ------------------------------------------------------------------ home
# Tool logos are single-colour shapes that take the band's text colour, so they match in light and dark mode
TOOL_LOGOS = json.load(open('assets/tool-logos.json'))
TOOL_LIST = [('Make.com', 'make'), ('n8n', 'n8n'), ('Zapier', 'zapier'), ('Airtable', 'airtable'), ('OpenAI', 'openai'), ('Claude', 'claude'), ('Gemini', 'googlegemini'), ('Retell AI', 'retell'), ('VAPI', 'vapi'), ('ElevenLabs', 'elevenlabs'), ('WhatsApp API', 'whatsapp'), ('Tally', 'tally')]
TOOLS = [t for t, _ in TOOL_LIST]
TICK = ''.join(f'<span><svg aria-hidden="true"><use href="#t-{k}"/></svg>{t}</span>' for t, k in TOOL_LIST)
def tool_symbol(key):
    logo = TOOL_LOGOS[key]
    paths = ''.join('<path d="' + x['d'] + '"' + (' fill-rule="' + x['rule'] + '"' if x['rule'] else '') + '/>' for x in logo['paths'])
    return f'<symbol id="t-{key}" viewBox="{logo["vb"]}">{paths}</symbol>'
TOOL_SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" fill="currentColor">' + ''.join(tool_symbol(k) for _, k in TOOL_LIST) + '</svg>'
TINY = '<svg aria-hidden="true"><use href="#cube"/></svg>'
# Add an instructor here and they appear on the Meet your instructors page.
# Tools are ('Name', key from assets/tool-logos.json, or None if there is no logo). An empty list shows a marked placeholder.
INSTRUCTORS = [
  {'name': 'Ogunyemi Ayobami', 'first': 'AYB', 'role': 'Founder, Nocodesquare. Co-founder, Spag AI', 'photo': 'img/ogunyemi-ayobami.jpg', 'pos': '50% 30%', 'story': None,
   'bio': 'AYB is an AI automation builder and co-founder of Spag AI, a voice automation agency deploying intelligent voice agents for businesses. His work is defined by one principle: automate the repetitive so humans can focus on what matters. As founder of Nocodesquare, he has led hundreds of live sessions training the next generation of no-code and AI automation builders across Africa.',
   'tools': [('Zapier', None)], 'style': 'Reinforcing the basics', 'advice': 'Consistency is how you build anything.'},
  {'name': 'Nafeesat Aliu', 'first': 'Nafeesat', 'role': 'Freelancer and instructor', 'photo': 'img/nafeesat-aliu.jpg', 'pos': '52% 40%', 'story': 'story-nafeesat-aliu.html',
   'bio': 'Nafeesat is an AI automation builder who transforms manual operations into intelligent, self-running systems. With Zapier as her core tool, she engineers workflows that are precise, scalable, and built for real-world performance. Her work is defined by execution, delivering automation that drives measurable efficiency and eliminates friction in business processes.',
   'tools': [('Zapier', None)], 'style': 'Practical, execution-driven', 'advice': 'True expertise is built through consistent application and refinement.'},
  {'name': 'Sekinat Ibrahim', 'first': 'Sekinat', 'role': 'Founder, AVOZ AI', 'photo': 'img/sekinat-ibrahim.jpg', 'pos': '50% 30%', 'story': 'story-sekinat-ibrahim.html',
   'bio': 'Sekinat is an AI automation expert and the founder of AVOZ AI. She has built and deployed automation systems for clients across multiple industries, helping businesses save time, eliminate manual work, and grow faster. Everything she teaches comes directly from the work she does every day.',
   'tools': [('Make', 'make'), ('n8n', 'n8n')], 'style': 'Learn by doing', 'advice': 'The skill you delay learning today is the income you delay earning tomorrow.'},
  {'name': 'Alli Oni', 'first': 'Alli', 'role': 'Co-founder, Spag AI', 'photo': 'img/alli-oni.jpg', 'pos': '50% 20%', 'story': None,
   'bio': 'Alli is an AI automation expert and co-founder of Spag AI, an agency helping businesses across multiple industries deploy intelligent systems that work around the clock. His work helps businesses stop losing leads, eliminate repetitive manual work, and grow faster without hiring more staff. Everything he teaches is pulled directly from active projects he builds and ships every single day.',
   'tools': [('Make', 'make')], 'style': 'Build as you learn', 'advice': 'The best time to learn this skill was last year. The second best time is today.'},
  {'name': 'Peculiar Chukwuma', 'first': 'Peculiar', 'role': 'Airtable automation expert', 'photo': 'img/peculiar-chukwuma.jpg', 'pos': '50% 30%', 'story': None,
   'bio': 'Peculiar is an Airtable automation expert who builds client portals, creates relational databases for structured data management, integrates third-party tools for seamless business operations and develops dashboards for real-time tracking and decision-making. She has worked with service-based teams to improve data flow and build scalable digital systems, and has experience in no-code system architecture.',
   'tools': [('Airtable', 'airtable')], 'style': 'Consistency through reps', 'advice': 'Results don’t come from perfect understanding, they come from repeated attempts that correct your understanding.'},
]
def tool_chip(tool):
    name, key = tool
    icon = ''
    if key:
        logo = TOOL_LOGOS[key]
        paths = ''.join('<path d="' + x['d'] + '"' + (' fill-rule="' + x['rule'] + '"' if x['rule'] else '') + '/>' for x in logo['paths'])
        icon = f'<svg viewBox="{logo["vb"]}" aria-hidden="true">{paths}</svg>'
    return f'<li>{icon}{name}</li>'
def instructor_card(t):
    chips = ''.join(tool_chip(x) for x in t['tools'])
    story = f"""<a class="more" href="{t['story']}">Read {t['first']}’s story</a>""" if t['story'] else ''
    return f"""<article class="instructor">
      <img src="{t['photo']}" alt="Portrait of {t['name']}" loading="lazy" style="object-position:{t['pos']}">
      <div class="instructor-text">
        <h2>{t['name']}</h2>
        <span class="instructor-role">{t['role']}</span>
        <p>{t['bio']}</p>
        <dl class="instructor-facts">
          <div><dt class="tag">Teaches</dt><dd><ul class="chips">{chips}</ul></dd></div>
          <div><dt class="tag">Teaching style</dt><dd>{t['style']}</dd></div>
          <div class="wide"><dt class="tag">Advice</dt><dd class="advice">{t['advice']}</dd></div>
        </dl>
        {story}
      </div>
    </article>"""

page('instructors.html', 'Meet your instructors', 'cohort.html',
  hero('', '', '', crumb(HOME, ('cohort.html', 'Academy'), (None, 'Instructors')), 'Meet your <i>instructors.</i>', 'The people teaching in the Nocodesquare Academy, the tools they teach, and how they teach them.', APPLY_COHORT)
  + '<section class="sheet"><div class="frame"><div class="instructors">' + ''.join(instructor_card(t) for t in INSTRUCTORS) + '</div></div></section>'
  + nxt('cohort.html', 'Want to learn with them?', 'See how the cohort works'))

home = f"""<body data-md="index.md">
{CUBE}
{TOOL_SPRITE}
{header('index.html')}
<main id="top">
  <section class="hero"><div class="frame">
    <div class="hero-copy">
      <h1 class="big">Africa's <svg class="glyph" aria-hidden="true"><use href="#cube"/></svg> builders <i>grow here.</i></h1>
      <p class="hero-lead">A community where we inspire each other, learn from each other and grow together. And an <a href="cohort.html">academy</a> where you can learn the skills from the start.</p>
      <div class="strip">No-code {TINY} AI {TINY} Automation</div>
      <div class="pair"><a class="slab" href="@@APPLY@@">Apply to the community</a><a class="slab ghost" href="#new">New here?</a></div>
    </div>
    <div class="africa"><canvas id="field" role="img" aria-label="Map of Africa built from Nocodesquare logo cubes, marking Lagos, Oyo, Accra, Yaoundé, Dakar, Cairo, Addis Ababa, Nairobi and Johannesburg"></canvas><a class="map-note" href="@@APPLY@@"><span>Your city next?</span><i aria-hidden="true"></i></a></div>
  </div></section>

  <div class="ticker-wrap" aria-label="Tools our builders use: {', '.join(TOOLS)}">
    <div class="ticker" aria-hidden="true"><div>{TICK}{TICK}{TICK}</div></div>
  </div>

  <section class="sheet" id="new"><div class="frame">
    <div class="intro">
      <div>
        <span class="tag">New here?</span>
        <h2 class="big">You can build <i>without code.</i></h2>
      </div>
      <div>
        <p class="say">Nocodesquare is a community for Africans who build with no-code and AI tools.</p>
        <p>These tools let you create apps, automations and AI agents without writing traditional code. Already building? Apply to the community. Just starting? The cohort is the place to begin.</p>
        <a class="more" href="about.html">More about us</a>
      </div>
    </div>
    <div class="stats">
      <div><b>Lagos</b><span class="caps">Our home base</span></div>
      <div class="on"><b>Coming soon</b><span class="caps">Events</span></div>
      <div><b>Sessions</b><span class="caps">Inside the community</span></div>
    </div>
  </div></section>

  <section class="sheet"><div class="frame">
    <div class="head">{MARK}<h2 class="big">What we do</h2><span class="tag">Ways to get involved</span></div>
    <article class="feature">
      <a class="pic" href="community.html"><img src="img/build-lab.jpg" alt="A team working together at laptops in a shared office" loading="lazy"></a>
      <div>
        <span class="chip">Community</span>
        <h3>Nobody builds alone here.</h3>
        <p>The heart of Nocodesquare. Ask questions, share what you're working on, get feedback and meet people solving the same problems.</p>
        <a class="more" href="community.html">Inside the community</a>
      </div>
    </article>
    <article class="feature">
      <a class="pic" href="community.html#sessions"><img src="img/inside-build.jpg" alt="Developer in headphones reading code on two monitors" loading="lazy"></a>
      <div>
        <span class="chip">Sessions</span>
        <h3>Learn together, in the community.</h3>
        <p>Inside the Build for going deep on a topic, Freelance Corner for the business of freelancing, and Show and Tell for walking through what members have built.</p>
        <a class="more" href="community.html#sessions">See the sessions</a>
      </div>
    </article>
    <article class="feature">
      <a class="pic" href="cohort.html"><img src="img/demo-day.jpg" alt="Women in a meeting room reviewing work on their laptops" loading="lazy"></a>
      <div>
        <span class="chip">Cohort</span>
        <h3>Ready to go further?</h3>
        <p>A guided, live program for building working automation systems. No coding needed, and no experience with the tools required.</p>
        {COUNTDOWN}
        <a class="more" href="cohort.html">How the cohort works</a>
        <a class="slab" href="apply-cohort.html">Apply to the cohort</a>
      </div>
    </article>
    <article class="feature">
      <a class="pic" href="events.html"><span class="plate"><b>Coming soon</b></span></a>
      <div>
        <span class="chip">Events</span>
        <h3>Events are coming soon.</h3>
        <p>We're working on our events. Community members will be the first to hear when they're announced.</p>
        <a class="more" href="events.html">See events</a>
      </div>
    </article>
  </div></section>

  <section class="sheet community" id="people">
    <div class="frame">
      {COMB}
      <div class="copy">
        <span class="tag">Who you'll meet</span>
        <h2 class="big">Builders <i>at every stage.</i></h2>
        <p>The community is for people already building with no-code and AI.</p>
        <ul class="who">
          <li><b>Freelancers</b>Selling no-code and AI services</li>
          <li><b>Agency founders</b>Delivering for clients, solo or with a team</li>
          <li><b>SaaS founders</b>Building products with no-code and AI</li>
          <li><b>Operators</b>Automating the business they work in</li>
          <li><b>Educators</b>Teaching clients, businesses and teams</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="sheet" id="testimonials"><div class="frame">
    <div class="head"><span class="tag">From our members</span><h2 class="big">In their <i>own words.</i></h2></div>
    {''.join(story_card(m) for m in MEMBER_STORIES)}
    {quote_cards(MEMBER_QUOTES, 'a community member') if MEMBER_QUOTES else ''}
  </div></section>

  <section class="sheet" id="youtube"><div class="frame">
    <div class="yt">
      <div>
        <span class="tag">We're on YouTube</span>
        <h2 class="big">Watch <i>and subscribe.</i></h2>
        <p>Our Show and Tell sessions are recorded and uploaded to our channel. Subscribe to catch them.</p>
      </div>
      <a class="slab" href="{YOUTUBE_URL}"{YT_ATTRS}>Subscribe on YouTube</a>
    </div>
  </div></section>

  <section class="sheet final" id="join"><div class="frame">
    <h2 class="big">Come <i>say hello.</i></h2>
    <p>The community is by application. You'll share your goal, your tools and two short Loom videos.</p>
    <a class="slab" href="@@APPLY@@">Apply to the community</a>
  </div></section>
</main>
{FOOTER}
"""
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(
    '<title>Nocodesquare</title>\n<meta charset="utf-8">\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + '<link rel="alternate" type="text/markdown" href="index.md" title="Agent-readable version">\n'
    + FONTS + '\n' + home.replace('@@APPLY@@', APPLY_LINK).replace('@@MD@@', 'index.md') + '<script src="site.js"></script>\n')

print(sorted(f for f in os.listdir(OUT) if f.endswith('.html')))

# Agent mode: a Markdown copy of every page, plus llms.txt and llms-full.txt for AI agents
import agent_md
agent_md.build(OUT)

# Cloudflare headers: declare UTF-8 on the agent files so ₦ and other symbols display correctly
with open(os.path.join(OUT, '_headers'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('/*.md\n  Content-Type: text/markdown; charset=utf-8\n/*.txt\n  Content-Type: text/plain; charset=utf-8\n')
