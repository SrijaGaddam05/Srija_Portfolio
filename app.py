import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from flask import Flask, request, jsonify
from html import escape as e

from urllib.parse import quote

app = Flask(__name__)

ME = dict(name="Gaddam Srija", role="Data Analyst", loc="Hyderabad, India",
          email="gaddamsrija005@gmail.com", phone="+91-9032837576",
          li="https://www.linkedin.com/in/gaddam-srija-749230325/",
          gh="https://github.com/SrijaGaddam05")

PROJECTS = [
 dict(n="JobMarket Intelligence", y="2026", t="Data Analytics Platform", org="Personal Project", cat="analytics",
  sum="A job-market engine that shows which skills Data Analyst roles actually ask for.",
  met=[("24,831", "Job records analyzed"), ("90.6%", "Skill-match baseline")],
  what="Analyzed 24,831 job records for hiring trends, in-demand skills, salary benchmarks and location insights. Built a Career Advisor that recommends skills by incremental job-market lift.",
  tools="Python, Pandas, NumPy, FastAPI, HTML/CSS/JS, Pytest",
  impact="90.6% baseline skill match for Data Analyst roles; pipeline automated with 6/6 Pytest tests passing.",
  tags=["Python", "Pandas", "NumPy", "FastAPI", "Pytest"], links=[("Live Demo", "https://jobmarket-intelligence-4.onrender.com/")]),
 dict(n="New Sandarshini Restaurant Website", y="Jan 2026", t="Paid Freelance Client Project", org="College Team", cat="client",
  sum="A live website for a Kadthal restaurant, built with college teammates.",
  met=[("Live", "Client website"), ("Firebase", "Database & backend")],
  what="With college teammates, built a live website for a restaurant in Kadthal. My role: data handling, database and backend, storing customer reviews in Firebase.",
  tools="Firebase (database and backend), team collaboration",
  impact="Delivered a live site the client was satisfied with: customers browse the menu, leave reviews and reach the restaurant on WhatsApp.",
  tags=["Firebase", "Backend", "Data Handling", "Teamwork"], links=[("Live Site", "https://newsandarshini.in/")]),
 dict(n="ClinicAI - Clinical Copilot", y="2026", t="Data Science Internship Project", org="Internship Project", cat="analytics",
  sum="Healthcare data turned into appointment, no-show and waiting-time insights.",
  met=[("3", "Insight areas"), ("EDA", "Statistical analysis")],
  what="Cleaned, preprocessed and explored healthcare data; ran statistical analysis and built visualizations.",
  tools="Python, Pandas, NumPy, SQL, Jupyter, Matplotlib, Seaborn",
  impact="Surfaced appointment trends, patient no-show patterns and waiting-time insights.",
  tags=["Python", "Pandas", "SQL", "Seaborn"], links=[]),
 dict(n="MarketMind AI", y="2024", t="Marketing Data Analytics", org="Personal Project", cat="analytics ai",
  sum="Sentiment, trends and sales forecasting from marketing data.",
  met=[("3", "Analyses: sentiment, trends, forecast"), ("NLP", "Feedback classification")],
  what="Ran sentiment analysis, trend visualization and sales forecasting on marketing datasets; classified customer feedback with NLP.",
  tools="Python, NLP (tokenization, feature extraction), FastAPI",
  impact="Turned raw feedback into stakeholder-ready insight reports.",
  tags=["NLP", "Sentiment", "Forecasting", "FastAPI"], links=[("GitHub", "https://github.com/SrijaGaddam05/Market_Minds")]),
 dict(n="AI Hand Workspace", y="2025", t="Computer Vision + Generative AI", org="Personal Project", cat="ai",
  sum="Control your workspace with hand gestures, powered by computer vision and GenAI.",
  met=[("Real-time", "Gesture control"), ("GenAI", "Function-calling")],
  what="Built a real-time gesture-based productivity system with a low-latency inference pipeline; integrated Google GenAI with function-calling.",
  tools="Python, OpenCV, MediaPipe, Google GenAI API",
  impact="Gestures trigger intelligent, automated features hands-free.",
  tags=["OpenCV", "MediaPipe", "GenAI", "Python"], links=[]),
]
LAB = {"analytics": "Data Analytics", "ai": "AI & ML", "client": "Client Work"}

JOBS = [
 dict(id="role-neoskillz", type="Internship", role="Data Analytics Intern", co="Neoskillz", big="4 Months", small="2026", per="2026 · 4 Months",
      sum="Python, SQL and Pandas on real datasets: cleaning, exploring and visualizing data to surface trends.",
      pts=["Applied hands-on training in Python, SQL and Pandas to explore, clean and preprocess structured datasets for analysis.",
           "Performed exploratory data analysis (EDA) and visualized trends with Matplotlib and Seaborn to surface patterns.",
           "Practiced feature engineering, including encoding, feature scaling and PCA, to prepare data for machine learning models.",
           "Wrote MySQL queries with joins, and completed foundational training in NLP text preprocessing and Generative AI concepts."],
      tags=["Python", "Pandas", "SQL", "EDA", "Matplotlib", "Seaborn", "PCA", "MySQL"]),
 dict(id="role-winzee", type="Professional Experience", role="Customer Support Executive", co="Winzee (Online Gaming Platform)", big="May - Jun", small="2026", per="May - Jun 2026",
      sum="Tracked high-volume support data to spot recurring issue patterns and reported trends to teams.",
      pts=["Tracked and analyzed high-volume customer interaction data across account, payment and gameplay issues to identify recurring patterns and trends.",
           "Applied data-driven problem-solving to improve resolution speed and accuracy in a fast-paced, metrics-focused environment.",
           "Reported issue trends to cross-functional teams, strengthening analytical reporting and communication skills."],
      tags=["Trend Analysis", "Reporting", "Problem Solving", "Communication"]),
]


def tags(t):
    return "".join(f"<span class='tag'>{e(x)}</span>" for x in t)


# level: Proficient / Working / Familiar
SKILLS = {
 "Data Analysis": [("Python", "Proficient", "Pipelines on 24,831 records"), ("Pandas & NumPy", "Proficient", "Internship + JobMarket"),
   ("Data Cleaning & EDA", "Proficient", "Neoskillz, ClinicAI"), ("Statistical Analysis", "Familiar", "Applied in ClinicAI")],
 "Databases": [("MySQL", "Working", "Joins, aggregations, grouping"), ("SQL Queries", "Working", "MySQL Using AI certified")],
 "Visualization": [("Matplotlib & Seaborn", "Working", "Trend and EDA charts"), ("Excel", "Working", "Microsoft Office Specialist"),
   ("Power BI", "Familiar", "Dashboard-ready metrics")],
 "Machine Learning & AI": [("Feature Engineering & PCA", "Working", "Encoding, scaling, PCA"), ("NLP", "Working", "MarketMind AI"),
   ("Generative AI & Prompting", "Working", "AI Hand Workspace"), ("Scikit-learn", "Familiar", "ML fundamentals")],
 "Backend & Tools": [("FastAPI", "Working", "JobMarket dashboard"), ("Pytest", "Working", "6/6 tests passed"),
   ("Git & GitHub", "Working", "Version control"), ("Jupyter & Colab", "Working", "Daily analysis")],
}

CERTS = [
 ("Python Essentials 2", "Cisco Networking Academy x OpenEDG Python Institute · Sep 19, 2026",
  "Statement of Achievement: multi-module Python 3 programs, OOP and modeling real-life problems.", ["Python", "OOP"], [("View Certificate", "/static/certs/python-essentials-2.jpeg")]),
 ("ServiceNow Virtual Internship Program", "ServiceNow University x SmartBridge (AICTE) · Jul 31, 2026 · ID SNU2034647",
  "Completed Agentic AI, ServiceNow Administration Fundamentals, Flows, Automated Test Framework, Reports and CSA exam preparation.", ["ServiceNow", "Agentic AI", "Reports"], [("View Certificate", "/static/certs/servicenow-virtual-internship.pdf")]),
 ("Data Analytics Job Simulation", "Deloitte via Forage · Jan 31, 2026",
  "Completed practical tasks in data analysis and forensic technology.", ["Data Analysis", "Deloitte"], [("View Certificate", "/static/certs/deloitte-data-analytics.pdf")]),
 ("Alpha: DSA with Java", "Apna College · Credential ID 6a2ed8da27332ae2ff086aca",
  "Course completion in Data Structures & Algorithms with Java; 50+ LeetCode problems solved.", ["Java", "DSA"], [("View Certificate", "/static/certs/apna-alpha-dsa-java.pdf")]),
 ("AI Automation Workshop", "10000 Coders · Workshop participation",
  "Certificate of participation in an AI automation workshop.", ["AI", "Automation"], [("View Certificate", "/static/certs/ai-automation-workshop.jpeg")]),
 ("Microsoft Office Specialist", "Excel, Word, PowerPoint",
  "Advanced spreadsheet and data presentation skills.", ["Excel", "MOS"], []),
 ("MySQL Using AI", "AI-assisted database tasks",
  "Structured query writing, joins and aggregations.", ["MySQL", "SQL"], []),
]

CASES = [
 ("Which skills do Data Analyst jobs actually ask for?", "JobMarket Intelligence",
  "Job listings are noisy and unstructured, so it is hard to know which skills to learn first.",
  "Cleaned and analyzed 24,831 job records with Pandas/NumPy: skill demand, salary benchmarks, month-over-month growth. Added a skill-match engine ranking skills by incremental lift.",
  "90.6% baseline skill match for Data Analyst roles, served through a FastAPI dashboard with 6/6 automated tests."),
 ("Turning customer feedback into decisions", "MarketMind AI",
  "Marketing teams hold feedback and sales data but lack quick, readable insight.",
  "Applied NLP (tokenization, feature extraction) to classify feedback, then paired sentiment trends with sales forecasting.",
  "Structured, stakeholder-ready insight reports."),
]

CSS = """
:root{--bg:#f3f3ee;--card:#fff;--ink:#111;--mut:#5f5f5a;--line:#d9d9d2;--g:#059669}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'JetBrains Mono',Consolas,'Courier New',monospace;background:var(--bg);color:var(--ink);line-height:1.65;font-size:14px}
a{color:var(--ink);text-decoration:none}
header{position:sticky;top:0;background:rgba(243,243,238,.93);backdrop-filter:blur(8px);border-bottom:1px solid var(--ink);z-index:9}
.nav{max-width:1100px;margin:auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.1em;font-size:15px;line-height:1.2}
.logo svg{width:50px;height:25px}.logo small{display:block;font-size:9px;color:var(--mut);font-weight:500;letter-spacing:.2em}
.nav nav{display:flex;gap:16px;flex-wrap:wrap;font-size:11px;align-items:center;text-transform:uppercase;letter-spacing:.1em}
.nav nav a{color:var(--mut)}.nav nav a.on,.nav nav a:hover{color:var(--ink);text-decoration:underline;text-underline-offset:6px}
.btn{display:inline-block;padding:10px 20px;border:1px solid var(--ink);background:var(--ink);color:#fff!important;font-weight:700;font-size:11px;letter-spacing:.1em;text-transform:uppercase;transition:.2s}
.btn.o{background:transparent;color:var(--ink)!important}.btn:hover{box-shadow:4px 4px 0 var(--g);transform:translate(-2px,-2px)}
main{max-width:1100px;margin:auto;padding:48px 20px}
.eyebrow{font-size:11px;letter-spacing:.2em;color:var(--mut);font-weight:700;text-transform:uppercase}
h1{font-family:'Oswald','Arial Narrow',Impact,sans-serif;font-weight:700;text-transform:uppercase;font-size:clamp(34px,6vw,60px);line-height:1.05;margin:10px 0 14px}
h2{font-family:'Oswald','Arial Narrow',sans-serif;text-transform:uppercase;font-size:24px;margin:38px 0 6px}h3{font-size:15px}
.lead{color:var(--mut);max-width:640px;margin-bottom:20px}
.row{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin-top:16px}
.card{background:var(--card);border:1px solid var(--ink);padding:22px;box-shadow:5px 5px 0 var(--line);transition:.2s}
.card:hover{box-shadow:5px 5px 0 var(--g)}
.stat b{display:block;font-family:'Oswald',sans-serif;font-size:32px}.stat span{color:var(--mut);font-size:12px}
.tag{display:inline-block;font-size:11px;padding:2px 10px;background:#e8e8e1;border:1px solid var(--line);margin:0 6px 6px 0}
.lv{float:right;font-size:10px;font-weight:700;padding:2px 9px;border:1px solid var(--ink);text-transform:uppercase;letter-spacing:.08em}
.lv.Proficient{background:var(--ink);color:#fff}.lv.Working{background:var(--line)}
.m{color:var(--mut);font-size:13px}.l{margin-top:8px;font-size:13px}.l b{color:var(--ink)}
ul{padding-left:20px;margin-top:8px;font-size:14px}
footer{border-top:1px solid var(--ink);padding:28px 20px;text-align:center;color:var(--mut);font-size:12px}
.hero{display:grid;grid-template-columns:1.25fr 1fr;gap:64px;align-items:center;padding-top:10px}
.slides{position:relative;height:300px}
.slide{position:absolute;inset:0;opacity:0;animation:sl 20s infinite}
.slide:nth-child(2){animation-delay:5s}.slide:nth-child(3){animation-delay:10s}.slide:nth-child(4){animation-delay:15s}
@keyframes sl{0%{opacity:0;transform:translateY(16px)}3%,22%{opacity:1;transform:none}25%,100%{opacity:0}}
.slides:hover .slide,.slides:hover~.dots i:after{animation-play-state:paused}
.dots{display:flex;gap:8px;margin:4px 0 6px}.dots i{width:32px;height:3px;background:#cfcfc8;position:relative;overflow:hidden}
.dots i:after{content:'';position:absolute;inset:0;background:var(--ink);transform:scaleX(0);transform-origin:left;animation:fill 20s infinite}
.dots i:nth-child(2):after{animation-delay:5s}.dots i:nth-child(3):after{animation-delay:10s}.dots i:nth-child(4):after{animation-delay:15s}
@keyframes fill{0%{transform:scaleX(0)}25%{transform:scaleX(1)}25.1%,100%{transform:scaleX(0)}}
.ct p{margin:6px 0}.ct b{display:inline-block;width:84px;color:var(--mut);font-weight:500}
.frame{position:relative;width:100%;max-width:370px;justify-self:center;margin-top:44px}
.frame .ghost{position:absolute;inset:0;transform:translate(14px,14px);border:2px solid #777}
.frame .in{position:relative;background:#fff;border:1px solid var(--ink);padding:10px 10px 0}
.frame img{width:100%;display:block;aspect-ratio:4/5;object-fit:cover}
.badge{position:absolute;top:22px;right:22px;background:#111;color:#fff;font-size:10px;letter-spacing:.14em;padding:4px 10px}
.foot{display:flex;justify-content:space-between;font-size:10px;letter-spacing:.08em;padding:12px 2px;color:var(--mut);text-transform:uppercase}
.foot b{color:var(--ink)}.foot i{display:inline-block;width:8px;height:8px;background:var(--g);margin-right:6px}
.ghosttxt{position:absolute;top:-46px;left:-58px;z-index:2;font:700 78px/1 'Oswald','Arial Narrow',sans-serif;color:transparent;-webkit-text-stroke:1.5px #444;pointer-events:none}
.ticker{overflow:hidden;background:var(--ink);color:#fff;padding:12px 0;margin-top:64px}
.ticker div{display:inline-block;white-space:nowrap;animation:mq 30s linear infinite;font-size:11px;letter-spacing:.24em;text-transform:uppercase}
.ticker:hover div{animation-play-state:paused}
@keyframes mq{to{transform:translateX(-50%)}}
@media(max-width:800px){.hero{grid-template-columns:1fr;gap:36px}.frame{order:-1;max-width:300px}.ghosttxt{font-size:52px;left:-10px;top:-34px}.slides{height:340px}}

:root{--r:#e5000f}
body{font-family:'Inter',system-ui,sans-serif}
.eyebrow,.nav nav,.btn,.foot,.m,.ct b,.tag,.lv,.ticker div{font-family:'JetBrains Mono',Consolas,monospace}
.eyebrow{color:var(--r)}
.wide{font-family:'Syne','Arial Black',sans-serif;font-weight:800;text-transform:none;letter-spacing:-.02em;line-height:1.08;font-size:clamp(28px,4.6vw,52px)}
.card:hover{box-shadow:5px 5px 0 var(--r)}.btn:hover{box-shadow:4px 4px 0 var(--r)}
.logo{gap:12px}.lbox{width:46px;height:46px;background:#111;display:grid;place-items:center}.lbox svg{width:30px;height:15px}.lbox svg path{stroke:#fff}
.logo small{font-family:'JetBrains Mono',monospace}
.nav nav{font-size:12px;font-weight:700;gap:26px}.nav nav a{color:var(--ink);padding-bottom:4px;text-decoration:none!important;border-bottom:2px solid transparent}
.nav nav a.on,.nav nav a:hover{border-color:var(--ink)}.nav nav a.btn{border:1px solid #111;padding:14px 22px;color:#fff}
.dom{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;margin-top:96px}
.vl{font:700 12px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase}
.acc{margin-top:48px;border-top:1px solid #111}.acc details{border-bottom:1px solid #111}
.acc summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:28px;padding:26px 0}
.acc summary::-webkit-details-marker{display:none}
.acc .st{font:700 12px 'JetBrains Mono',monospace;color:#8a97ad;letter-spacing:.06em;min-width:72px}
.acc h3{font:500 clamp(22px,3.4vw,38px)/1.1 'Oswald','Arial Narrow',sans-serif;text-transform:uppercase;flex:1;transition:.2s}
.acc .pl{width:40px;height:40px;border:1px solid #bbb;display:grid;place-items:center;font-size:20px;transition:.2s}
.acc .pl:before{content:'+'}.acc details[open] .pl:before{content:'−'}
.acc summary:hover h3,.acc details[open] h3{color:var(--r)}
.acc summary:hover .pl,.acc details[open] .pl{background:#111;color:#fff;border-color:#111}
.acc summary:hover .st,.acc details[open] .st{color:#111}
.acc .bd{padding:0 0 28px 100px;max-width:780px;color:var(--mut)}
.cta{text-align:center;padding:100px 0 20px}.cta .wide{font-size:clamp(28px,5.2vw,62px);margin:16px auto 0;max-width:1000px}
.cta p{color:var(--mut);max-width:620px;margin:22px auto 32px;font-size:17px}.cta .row{justify-content:center}
footer{background:#0b0d10;color:#c9ced6;border:0;text-align:left;padding:56px 20px 24px;font-size:14px;margin-top:80px}
.fi{max-width:1100px;margin:auto;display:grid;grid-template-columns:1.4fr 1fr 1fr 1.3fr;gap:36px}
footer h4{font:500 15px 'Oswald',sans-serif;text-transform:uppercase;color:#fff;margin-bottom:18px}
footer a{color:#c9ced6;font:700 12px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;display:block;margin:12px 0}
footer .lbox{background:#fff}footer .lbox svg path{stroke:#111}
.brand{display:flex;gap:12px;align-items:center;color:#fff;font:500 18px 'Oswald',sans-serif;letter-spacing:.08em}
.brand small{display:block;color:var(--r);font:700 10px 'JetBrains Mono',monospace;letter-spacing:.14em}
.soc{display:flex;gap:10px;margin-top:20px}.soc a{width:40px;height:40px;border:1px solid #444;display:grid;place-items:center;margin:0;color:#fff}
.soc svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:1.6}
.ci{display:flex;gap:12px;margin-bottom:16px}.ci svg{width:20px;height:20px;stroke:var(--r);fill:none;stroke-width:1.6;flex:none;margin-top:4px}
.ci small{display:block;font:700 9px 'JetBrains Mono',monospace;letter-spacing:.12em;color:#8a93a0}
.ci span{color:#fff;font-family:'JetBrains Mono',monospace;font-size:13px;word-break:break-all}
.fb{max-width:1100px;margin:44px auto 0;border-top:1px solid #23272e;padding-top:24px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:12px 'JetBrains Mono',monospace;color:#8a93a0}
.fb b{font-weight:400;border:1px solid #0a8f5f;color:#10d28a;padding:3px 9px;margin-left:8px}
@media(max-width:800px){.fi{grid-template-columns:1fr 1fr}.acc .bd{padding-left:0}.acc summary{gap:14px}.lbox{width:40px;height:40px}}

.nav,main,.fi{max-width:1400px}
main{padding-bottom:80px}
footer{margin-top:0;padding:80px 20px 44px}
.cta{padding:100px 0 110px}
.fi{grid-template-columns:repeat(4,1fr);gap:40px}
footer p{font-size:15px;line-height:1.65;color:#c9ced6;max-width:330px}
footer h4{font:700 17px 'Oswald',sans-serif;letter-spacing:.01em;margin-bottom:22px}
footer a{font-size:14px;line-height:30px;margin:0;color:#c5cad3;letter-spacing:.06em}
footer a:hover{color:#fff}
.brand{font-size:22px}.brand small{font-size:11px;margin-top:2px}
.soc{margin-top:26px}.soc a{border-color:#4a4f57}
.ci{margin-bottom:14px;gap:14px}.ci span{font-size:14.5px}
.fb{max-width:1520px;padding:36px 60px 0;margin-top:60px;font-size:13px}
.fb b{font-size:12px;padding:4px 10px;background:rgba(16,185,129,.08);border-color:#12a36a;color:#22e29a}
@media(max-width:800px){.fb{padding:28px 0 0}.fi{grid-template-columns:1fr 1fr}}

footer a i{font-style:normal;font-size:11px;color:#8a93a0;margin-left:8px;vertical-align:2px}

header{background:#f6f6f2;border-bottom:1px solid #111}
.nav{padding:16px 20px;min-height:80px;gap:24px;flex-wrap:nowrap}
.nav nav{gap:40px;font-size:13px;letter-spacing:.14em;flex:1;justify-content:center}
.nav nav a{padding-bottom:6px}
.nav>a.btn{padding:18px 28px;font-size:12px;letter-spacing:.12em;white-space:nowrap}
.logo{min-width:200px}.lbox{width:50px;height:50px}.lbox svg{width:32px;height:16px}
@media(max-width:1000px){.nav{flex-wrap:wrap}.nav nav{order:3;width:100%;flex:none;gap:20px;justify-content:center}}

.nar{display:grid;grid-template-columns:1.5fr 1fr;gap:56px;align-items:start}
.nar p{color:#3b3f46;font-size:16px;margin-bottom:18px;max-width:660px}
.skb{background:#111;color:#fff;padding:32px;box-shadow:8px 8px 0 var(--r);margin-top:8px}
.skb .eyebrow{color:#ff5a64}.skb h3{font:500 24px 'Oswald',sans-serif;text-transform:uppercase;margin:8px 0 0}
.skb p{color:#d5d9e0;margin:12px 0 0;font-size:15px}
.tri{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin-top:48px}
.tri .card h3,.pub .card h3{font:500 21px/1.25 'Oswald',sans-serif;text-transform:uppercase;margin-bottom:8px}
.sec{margin-top:110px}.sh{font:700 clamp(30px,4.6vw,56px)/1.05 'Oswald',sans-serif;text-transform:uppercase;margin:10px 0 12px}
.edu{margin-top:36px;border-top:1px solid #111}
.edu .r{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding:30px 0;border-bottom:1px solid #111}
.edu h3{font:500 clamp(20px,2.6vw,30px)/1.15 'Oswald',sans-serif;text-transform:uppercase}
.edu .meta{text-align:right}.edu .meta b{display:block;font:700 22px 'Oswald',sans-serif}
.pub{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-top:30px}
@media(max-width:800px){.nar{grid-template-columns:1fr;gap:28px}.edu .meta{text-align:left}}

.stat-line{font:700 12px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin:34px 0 14px;display:flex;align-items:center;gap:10px}
.stat-line i{width:9px;height:9px;background:var(--g);display:inline-block}
.tl{display:grid;gap:28px}
.job{display:grid;grid-template-columns:210px 1fr 56px;gap:34px;align-items:start;background:#fff;border:1px solid #111;padding:36px;box-shadow:8px 8px 0 var(--line);transition:.2s;cursor:pointer;color:inherit}
.job:hover{box-shadow:8px 8px 0 var(--r);transform:translate(-3px,-3px)}
.job .when b{display:block;font:700 36px/1 'Oswald',sans-serif;text-transform:uppercase}
.job .when span{font:700 11px 'JetBrains Mono',monospace;letter-spacing:.12em;color:var(--mut);text-transform:uppercase}
.job h2{font:700 clamp(24px,3vw,38px)/1.1 'Oswald',sans-serif;text-transform:uppercase;margin:10px 0 4px}
.co{font:700 13px 'JetBrains Mono',monospace;color:var(--mut)}.job p{color:#3b3f46;margin:14px 0}
.go{width:48px;height:48px;border:1px solid #111;display:grid;place-items:center;font-size:22px;transition:.2s}.job:hover .go{background:#111;color:#fff}
.type{display:inline-block;background:#111;color:#fff;font:700 10px 'JetBrains Mono',monospace;letter-spacing:.14em;padding:3px 10px;text-transform:uppercase}
.modal{display:none;position:fixed;inset:0;z-index:50;background:rgba(10,10,10,.74);align-items:center;justify-content:center;padding:20px}
.modal:target{display:flex}.close-bg{position:absolute;inset:0}
.mbox{position:relative;background:#fff;border:1px solid #111;box-shadow:12px 12px 0 var(--r);width:min(960px,100%);max-height:90vh;overflow:auto;padding:52px}
.mbox h2{font:700 clamp(30px,4.5vw,54px)/1.05 'Oswald',sans-serif;text-transform:uppercase;margin:12px 0 6px}
.mx{position:absolute;top:16px;right:16px;border:1px solid #111;padding:8px 14px;font:700 11px 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;background:#fff}
.mx:hover{background:#111;color:#fff}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));margin:26px 0;border:1px solid #111}
.facts div{padding:16px 18px;border-right:1px solid #111}.facts div:last-child{border:0}
.facts small{display:block;font:700 10px 'JetBrains Mono',monospace;letter-spacing:.14em;color:var(--mut);text-transform:uppercase}
.facts b{font:500 18px 'Oswald',sans-serif;text-transform:uppercase}
.mbox h4{font:700 12px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--r);margin:28px 0 8px}
.mbox li{margin:10px 0;font-size:15.5px}
@media(max-width:800px){.job{grid-template-columns:1fr;padding:24px;gap:16px}.go{display:none}.mbox{padding:56px 22px 28px}}

.open{display:inline-flex;align-items:center;gap:10px;margin-top:18px;padding:11px 18px;border:1px solid #111;background:#111;color:#fff;font:700 11px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;transition:.2s}
.open i{font-style:normal;font-size:18px;line-height:1;animation:nudge 1.4s ease-in-out infinite}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(7px)}}
.job:hover .open{background:var(--r);border-color:var(--r)}
.go{font-size:24px}

.flt input{position:absolute;opacity:0;pointer-events:none}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin:30px 0 8px}
.chips label{border:1px solid #111;padding:9px 16px;font:700 11px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;cursor:pointer;background:#fff;transition:.2s}
.chips label:hover{box-shadow:3px 3px 0 var(--r)}
#f-all:checked~.chips label[for=f-all],#f-analytics:checked~.chips label[for=f-analytics],#f-ai:checked~.chips label[for=f-ai],#f-client:checked~.chips label[for=f-client]{background:#111;color:#fff}
#f-analytics:checked~.pgrid .pc:not(.analytics),#f-ai:checked~.pgrid .pc:not(.ai),#f-client:checked~.pgrid .pc:not(.client){display:none}
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:34px;margin-top:26px}
.pc{position:relative;display:block;background:#fff;border:1px solid #111;padding:34px 30px 30px;box-shadow:8px 8px 0 var(--line);transition:.25s;color:inherit;overflow:hidden}
.pc:hover{transform:translate(-4px,-4px) rotate(-.4deg);box-shadow:10px 10px 0 var(--r)}
.pc .ix{position:absolute;top:8px;right:18px;font:700 84px/1 'Oswald',sans-serif;color:transparent;-webkit-text-stroke:1.2px #cfcfc8}
.pc h2{font:700 clamp(24px,2.4vw,32px)/1.1 'Oswald',sans-serif;text-transform:uppercase;margin:8px 0 4px;position:relative}
.pc p{color:#3b3f46;margin:12px 0 18px;position:relative}
.mets{display:grid;grid-template-columns:1fr 1fr;border:1px solid #111;margin-bottom:18px}
.met{padding:14px 16px}.met:first-child{background:#111;color:#fff}
.met b{display:block;font:700 26px/1.1 'Oswald',sans-serif}.met span{font:700 10px 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;opacity:.75}
.mlinks{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.mbox p{max-width:760px}
"""


INF = ('<path d="M24 12C20 5 14 3 9 6C4 9 4 15 9 18C14 21 20 19 24 12C28 5 34 3 39 6C44 9 44 15 39 18C34 21 28 19 24 12Z" '
       'fill="none" stroke="#111" stroke-width="2.6" stroke-linejoin="round"/><circle cx="24" cy="12" r="2.2" fill="#059669"/>')
LOGO = f'<svg viewBox="0 0 48 24" aria-label="Srija infinity logo">{INF}</svg>'
FAV = "data:image/svg+xml," + quote(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 24">{INF}</svg>')

PAGES = [("/", "Home"), ("/about", "About"), ("/experience", "Experience"), ("/projects", "Projects"),
         ("/skills", "Skills"), ("/certifications", "Certifications"), ("/case-studies", "Case Studies")]


def footer():
    ic = lambda p: f'<svg viewBox="0 0 24 24">{p}</svg>'
    mail = ic('<rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 7l9 6 9-6"/>')
    tel = ic('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>')
    pin = ic('<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>')
    li = '<svg viewBox="0 0 24 24" style="fill:#fff;stroke:none"><rect x="3" y="9" width="4" height="12"/><circle cx="5" cy="5" r="2.2"/><path d="M10 9h4v2c.8-1.4 2.2-2.3 4-2.3 3 0 4 2 4 5V21h-4v-6c0-1.4-.4-2.4-1.8-2.4S14 13.6 14 15v6h-4z"/></svg>'
    return f"""<footer><div class="fi"><div><div class="brand"><span class="lbox">{LOGO}</span><span>SRIJA GADDAM<small>DATA ANALYST</small></span></div>
<p style="margin-top:22px">B.Tech student in Computer Science &amp; Engineering (AI &amp; ML) at Sri Indu Institute of Engineering &amp; Technology, Hyderabad, graduating 2027. Aspiring to an entry-level Data Analyst role, turning raw data into clear decisions.</p>
<div class="soc"><a href="{ME['li']}" aria-label="LinkedIn" target="_blank" rel="noopener">{li}</a><a href="mailto:{ME['email']}" aria-label="Gmail">{mail}</a></div></div>
<div><h4>Directory</h4><a href="/about">About Bio<i>&nearr;</i></a><a href="/experience">Career History<i>&nearr;</i></a><a href="/projects">Projects<i>&nearr;</i></a><a href="/skills">Competencies<i>&nearr;</i></a></div>
<div><h4>Excellence &amp; Studies</h4><a href="/certifications">Achievements<i>&nearr;</i></a><a href="/case-studies">Case Write-ups<i>&nearr;</i></a><a href="/contact">Connect With Me<i>&nearr;</i></a></div>
<div><h4>Direct Office</h4><div class="ci">{mail}<div><small>EMAIL</small><span>{ME['email']}</span></div></div>
<div class="ci">{tel}<div><small>PHONE</small><span>{ME['phone']}</span></div></div>
<div class="ci">{pin}<div><small>LOCATION</small><span>Hyderabad, Telangana, IN</span></div></div></div></div>
<div class="fb"><span>&copy; 2026 Gaddam Srija. All Rights Reserved.</span><span>Core Stack:<b>PYTHON</b><b>SQL</b><b>PANDAS</b></span></div></footer>"""


def page(path, title, body):
    nav = "".join(f'<a class="{"on" if p == path else ""}" href="{p}">{n}</a>' for p, n in PAGES)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Gaddam Srija - Data Analyst</title>
<meta name="description" content="Data Analyst portfolio of Gaddam Srija: Python, SQL, Pandas, EDA and dashboards.">
<link rel="icon" href="{FAV}"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;700&family=Oswald:wght@500;700&family=Syne:wght@800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>
<header><div class="nav"><a class="logo" href="/"><span class="lbox">{LOGO}</span><span>SRIJA<small>DATA ANALYST</small></span></a>
<nav>{nav}</nav><a class="btn" href="/contact">Say Hello &rarr;</a></div></header>
<main>{body}</main>
{footer()}
</body></html>"""


def head(eyebrow, title, lead=""):
    return f'<div class="eyebrow">{e(eyebrow)}</div><h1>{e(title)}</h1><p class="lead">{e(lead)}</p>'


def project_card(p):
    links = "".join(f'<a class="btn o" href="{u}" target="_blank" rel="noopener">{e(t)}</a>' for t, u in p["links"])
    return f"""<div class="card"><span class="m">{e(p['y'])} &middot; {e(p['t'])}</span><h3>{e(p['n'])}</h3>
<p class="l"><b>What I Did:</b> {e(p['what'])}</p><p class="l"><b>Tools:</b> {e(p['tools'])}</p>
<p class="l"><b>Impact:</b> {e(p['impact'])}</p><div class="row">{links}</div></div>"""


@app.route("/")
def home():
    kw = ["Python", "SQL", "Pandas", "NumPy", "EDA", "Data Cleaning", "Matplotlib", "Seaborn", "FastAPI", "Excel", "NLP", "Power BI"]
    tick = "".join(f"{k} &nbsp;&#8734;&nbsp; " for k in kw) * 2
    stats = [("24,831", "job records analyzed"), ("90.6%", "skill-match baseline"), ("6/6", "tests passed"), ("7.91", "CGPA")]
    st = "".join(f'<div class="stat"><b>{a}</b><span>{b}</span></div>' for a, b in stats)
    dom = [("Data Cleaning & Exploratory Analysis", "Cleaning, preprocessing and EDA on structured datasets with Python, Pandas and SQL, then charts in Matplotlib and Seaborn. Applied during my Neoskillz internship and the ClinicAI project."),
           ("Analytics Pipelines & Dashboards", "Built JobMarket Intelligence: 24,831 job records analyzed for skill demand, salary benchmarks and growth trends, served through a FastAPI dashboard and covered by 6/6 Pytest tests."),
           ("NLP, ML & Generative AI", "Sentiment analysis and forecasting in MarketMind AI, feature engineering with encoding, scaling and PCA, and a gesture-control system using OpenCV and Google GenAI.")]
    acc = "".join(f'<details><summary><span class="st">STAGE 0{i}</span><h3>{e(t)}</h3><span class="pl"></span></summary><div class="bd">{e(b)}</div></details>' for i, (t, b) in enumerate(dom, 1))
    body = f"""<div class="hero"><div>
<div class="slides">
<div class="slide"><div class="eyebrow">01 / Hello</div><h1>I'm Srija<br>Gaddam.</h1>
<p class="lead">Data Analyst in the making. I turn messy data into clear decisions.</p></div>
<div class="slide"><div class="eyebrow">02 / About me</div><h1>Analytical by training.</h1>
<p class="lead">CS undergraduate (AI &amp; ML) with a Data Analytics internship and a 24,000+ record job-market platform. Seeking an entry-level Data Analyst role.</p>
<span class="tag">Python</span><span class="tag">SQL</span><span class="tag">Pandas</span><span class="tag">EDA</span></div>
<div class="slide ct"><div class="eyebrow">03 / Contact</div><h1>Let's talk.</h1>
<p><b>Email</b><a href="mailto:{ME['email']}">{ME['email']}</a></p><p><b>Phone</b>{ME['phone']}</p>
<p><b>LinkedIn</b><a href="{ME['li']}">gaddam-srija-749230325</a></p><p><b>GitHub</b><a href="{ME['gh']}">SrijaGaddam05</a></p></div>
<div class="slide"><div class="eyebrow">04 / Highlights</div><h1>By the numbers.</h1>
<div class="grid" style="grid-template-columns:1fr 1fr">{st}</div></div>
</div>
<div class="dots"><i></i><i></i><i></i><i></i></div>
<div class="row"><a class="btn" href="/projects">View Projects</a>
<a class="btn o" href="/static/Srija_Data_Analyst_Resume.pdf" download>Resume</a></div></div>
<div class="frame"><div class="ghosttxt">SRIJA</div><div class="ghost"></div>
<div class="in"><span class="badge">DATA ANALYST</span><img src="/static/photo.jpg" alt="Gaddam Srija">
<div class="foot"><span>Location: Hyderabad, IN</span><b><i></i>Available</b></div></div></div></div>
<div class="ticker"><div>{tick}</div></div>
<div class="dom"><div><div class="eyebrow">Core Domains // 01 - 03</div>
<h2 class="wide" style="margin:10px 0 0;max-width:780px">Data Analysis, Pipelines &amp; Insight Delivery</h2></div>
<a class="vl" href="/skills">View Competencies &rarr;</a></div>
<div class="acc">{acc}</div>
<div class="cta"><div class="eyebrow">Portfolio Action</div><h2 class="wide">Ready to review data-driven analysis?</h2>
<p>Download my resume, or browse the projects behind the numbers: a 24,831-record job-market platform, NLP analytics and more.</p>
<div class="row"><a class="btn" href="/projects">View Projects &rarr;</a><a class="btn o" href="/contact">Get in Touch &rarr;</a></div></div>"""
    return page("/", "Home", body)


ABOUT_STATS = [("Academic Record", "B.Tech AI & ML, CGPA 7.91"), ("Flagship Project", "24,831 job records analyzed"),
               ("Hackathon Leader", "Smart India Hackathon Team Leader")]
RECOG = [("Smart India Hackathon", "Served as Team Leader for the Smart India Hackathon.", ["Team Leader", "Hackathon"]),
         ("Academic Poster Presenter", "Presented an AI/ML poster in an academic setting.", ["AI/ML", "Poster Presentation"]),
         ("NxtWave Buildathon", "Participated in the NxtWave Buildathon.", ["Participant", "Buildathon"])]
FIELD = [("Data Analytics Intern", "Neoskillz · 4 Months · 2026",
          "Hands-on training in Python, SQL and Pandas: cleaned and explored datasets, ran EDA with Matplotlib and Seaborn, and practiced feature engineering (encoding, scaling, PCA)."),
         ("Customer Support Executive", "Winzee (Online Gaming) · May - Jun 2026",
          "Tracked high-volume customer interaction data across account, payment and gameplay issues to spot recurring patterns, and reported trends to cross-functional teams."),
         ("Freelance Backend Developer (Team)", "New Sandarshini Restaurant · Jan 2026",
          "Worked with college teammates on a paid client website. Handled data and the Firebase database and backend that stores customer reviews. The client was satisfied with the result.")]


@app.route("/about")
def about():
    stats = "".join(f"<div class='card'><h3>{e(a)}</h3><p class='m'>{e(b)}</p></div>" for a, b in ABOUT_STATS)
    rec = "".join(f"<div class='card'><h3>{e(t)}</h3><p class='l'>{e(d)}</p><div class='row' style='margin-top:14px'>" +
                  "".join(f"<span class='tag'>{e(x)}</span>" for x in tg) + "</div></div>" for t, d, tg in RECOG)
    fld = "".join(f"<div class='card'><span class='m'>{e(m)}</span><h3 style='margin-top:6px'>{e(r)}</h3><p class='l'>{e(d)}</p></div>" for r, m, d in FIELD)
    hob = "".join(f"<div class='card'><h3>{e(t)}</h3><p class='l'>{e(d)}</p></div>" for t, d in
                  [("Crafts & DIY", "Making things by hand."), ("Crochet", "Patience and detail, one stitch at a time."), ("Learning Songs", "Picking up new songs for fun.")])
    body = f"""<div class="nar"><div><div class="eyebrow">My Narrative</div>
<h1>Where AI &amp; ML foundations meet data analytics</h1>
<p>My journey began in Computer Science with a specialization in AI and Machine Learning, where I learned how data and models work. Hands-on analytics training in Python, SQL and Pandas showed me that the most valuable skill is turning raw, messy data into insight people can trust.</p>
<p>Today I clean, transform and analyze structured datasets, build analytics pipelines, and explain what the numbers mean. My flagship project analyzes 24,831 job records for hiring trends, in-demand skills and salary benchmarks, and I focus on analysis that ends in a decision, not just a chart.</p></div>
<div class="skb"><div class="eyebrow">Transferable Skillset</div><h3>From raw data to decisions</h3>
<p>My AI &amp; ML training lets me take data from cleaning and EDA through feature engineering (encoding, scaling, PCA) and NLP, then present the result in plain language.</p></div></div>
<div class="tri">{stats}</div>
<div class="sec"><div class="eyebrow">Education</div><h2 class="sh">Academic Credentials</h2>
<p class="lead">A computer science degree with a specialization in AI and Machine Learning.</p>
<div class="edu"><div class="r"><div><h3>B.Tech. Computer Science &amp; Engineering (AI &amp; ML)</h3>
<p class="m">Sri Indu Institute of Engineering &amp; Technology | Hyderabad</p><p class="l">Specialization in AI &amp; Machine Learning</p></div>
<div class="meta"><b>CGPA 7.91</b><span class="m">2023 – 2027</span></div></div></div></div>
<div class="sec"><div class="eyebrow">Recognition</div><h2 class="sh">Hackathons &amp; Presentations</h2>
<p class="lead">Building and presenting AI/ML work in competitive and academic settings.</p><div class="pub">{rec}</div></div>
<div class="sec"><div class="eyebrow">Field Experience</div><h2 class="sh">Internships &amp; Industry Exposure</h2>
<p class="lead">Applying data cleaning, analysis and reporting in real working environments.</p><div class="pub">{fld}</div></div>
<div class="sec"><div class="eyebrow">Beyond The Code</div><h2 class="sh">Hands-on Creativity</h2>
<p class="lead">Away from the screen, I like making things.</p><div class="pub">{hob}</div></div>"""
    return page("/about", "About", body)


@app.route("/experience")
def experience():
    cards, mods = "", ""
    for j in JOBS:
        cards += (f'<a class="job" href="#{j["id"]}"><div class="when"><b>{e(j["big"])}</b><span>{e(j["small"])}</span></div>'
                  f'<div><span class="type">{e(j["type"])}</span><h2>{e(j["role"])}</h2><div class="co">{e(j["co"])}</div>'
                  f'<p>{e(j["sum"])}</p>{tags(j["tags"][:5])}<div><span class="open">View full record <i>&rarr;</i></span></div></div><div class="go">&rarr;</div></a>')
        lis = "".join(f"<li>{e(x)}</li>" for x in j["pts"])
        mods += (f'<div class="modal" id="{j["id"]}"><a class="close-bg" href="#timeline" aria-label="Close"></a><div class="mbox">'
                 f'<a class="mx" href="#timeline">Close &times;</a><span class="type">{e(j["type"])}</span><h2>{e(j["role"])}</h2>'
                 f'<div class="co">{e(j["co"])}</div><div class="facts"><div><small>Company</small><b>{e(j["co"])}</b></div>'
                 f'<div><small>Type</small><b>{e(j["type"])}</b></div><div><small>Period</small><b>{e(j["per"])}</b></div></div>'
                 f'<h4>What I Did</h4><ul>{lis}</ul><h4>Skills Applied</h4>{tags(j["tags"])}</div></div>')
    body = head("Timeline Register", "Work Experience & Analytics Records",
                "A chronological record of my hands-on data work. Use the arrow on any role to open its full record.") + f"""
<div class="stat-line"><i></i>Active system logs: {len(JOBS)} roles logged</div>
<div class="tl" id="timeline">{cards}</div>{mods}
<div class="skb" style="margin-top:70px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:center">
<div><div class="eyebrow">Analysis Samples</div><h3>See the work behind the numbers</h3>
<p>Browse the projects built during and after these roles, or send me a message.</p></div>
<div class="row"><a class="btn" style="background:#fff;color:#111!important" href="/projects">View Projects &rarr;</a>
<a class="btn o" style="color:#fff!important;border-color:#fff" href="/contact">Send a Message &rarr;</a></div></div>"""
    return page("/experience", "Experience", body)


@app.route("/projects")
def projects():
    chips = [("all", "All Projects"), ("analytics", "Data Analytics"), ("ai", "AI & ML"), ("client", "Client Work")]
    radios = "".join(f'<input type="radio" name="f" id="f-{k}"{" checked" if k == "all" else ""}>' for k, _ in chips)
    labs = "".join(f'<label for="f-{k}">{e(v)}</label>' for k, v in chips)
    cards, mods = "", ""
    for i, p in enumerate(PROJECTS, 1):
        pid = f"project-{i}"
        lab = LAB[p["cat"].split()[0]]
        mets = "".join(f'<div class="met"><b>{e(v)}</b><span>{e(l)}</span></div>' for v, l in p["met"])
        cards += (f'<a class="pc {p["cat"]}" href="#{pid}"><span class="ix">0{i}</span><span class="type">{e(lab)}</span>'
                  f'<div class="co" style="margin-top:12px">{e(p["org"])}</div><h2>{e(p["n"])}</h2><p>{e(p["sum"])}</p>'
                  f'<div class="mets">{mets}</div>{tags(p["tags"][:4])}<div><span class="open">Open case file <i>&rarr;</i></span></div></a>')
        btn = "".join(f'<a class="btn" href="{u}" target="_blank" rel="noopener">{e(t)} &nearr;</a>' for t, u in p["links"])
        mods += (f'<div class="modal" id="{pid}"><a class="close-bg" href="#registry" aria-label="Close"></a><div class="mbox">'
                 f'<a class="mx" href="#registry">Close &times;</a><span class="type">{e(lab)}</span><h2>{e(p["n"])}</h2><div class="co">{e(p["org"])}</div>'
                 f'<div class="facts"><div><small>Year</small><b>{e(p["y"])}</b></div><div><small>Type</small><b>{e(p["t"])}</b></div></div>'
                 f'<h4>What I Did</h4><p>{e(p["what"])}</p><h4>Tools</h4><p>{e(p["tools"])}</p><h4>Impact</h4><p>{e(p["impact"])}</p>'
                 f'<div class="mlinks">{btn}</div></div></div>')
    body = head("Project Archive", "Data Casework & Builds",
                "Analytics platforms, AI systems and client work. Filter the registry, then open any case file for the full story.") + f"""
<div class="flt" id="registry">{radios}<div class="chips">{labs}</div>
<div class="stat-line"><i></i>Active registry: {len(PROJECTS)} records found</div><div class="pgrid">{cards}</div></div>{mods}
<div class="skb" style="margin-top:80px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:center">
<div><div class="eyebrow">More On GitHub</div><h3>Browse the code behind the numbers</h3><p>More projects and links are being added. Follow along on GitHub.</p></div>
<div class="row"><a class="btn" style="background:#fff;color:#111!important" href="{ME['gh']}" target="_blank" rel="noopener">Open GitHub &nearr;</a>
<a class="btn o" style="color:#fff!important;border-color:#fff" href="/contact">Get in Touch &rarr;</a></div></div>"""
    return page("/projects", "Projects", body)


@app.route("/skills")
def skills():
    out = head("Competency Directory", "Core skills", "Hands-on skills backed by projects, internships and certifications.")
    for g, items in SKILLS.items():
        out += f"<h2>{e(g)}</h2><div class='grid'>" + "".join(
            f"<div class='card'><h3>{e(n)}</h3><p class='m'>{e(w)}</p></div>" for n, l, w in items) + "</div>"
    return page("/skills", "Skills", out)


@app.route("/certifications")
def certifications():
    def card(t, m, d, tg, ln=()):
        sub = f"<span class='m'>{e(m)}</span>" if m else ""
        btn = "".join(f"<a class='btn o' style='padding:8px 14px' href='{u}' target='_blank' rel='noopener'>{e(x)} &nearr;</a>" for x, u in ln)
        return (f"<div class='card'>{sub}<h3 style='margin-top:6px'>{e(t)}</h3><p class='l'>{e(d)}</p><div class='row' style='margin-top:14px'>"
                + "".join(f"<span class='tag'>{e(x)}</span>" for x in tg) + f"</div><div class='row'>{btn}</div></div>")
    c = "".join(card(*x) for x in CERTS)
    a = "".join(card(t, "", d, tg) for t, d, tg in RECOG)
    body = (head("Credentials", "Certifications & achievements", "Courses, simulations and workshops, newest first.")
            + f"<div class='pub' style='margin-top:30px'>{c}</div>"
            + f"<div class='sec'><div class='eyebrow'>Recognition</div><h2 class='sh'>Hackathons &amp; Presentations</h2><div class='pub'>{a}</div></div>")
    return page("/certifications", "Certifications", body)


@app.route("/case-studies")
def cases():
    g = "".join(f"""<div class='card'><span class='m'>{e(p)}</span><h3>{e(t)}</h3>
<p class='l'><b>Problem:</b> {e(a)}</p><p class='l'><b>Approach:</b> {e(b)}</p><p class='l'><b>Outcome:</b> {e(c)}</p></div>"""
                 for t, p, a, b, c in CASES)
    return page("/case-studies", "Case Studies", head("Case Studies", "Problem, approach, outcome") + f"<div class='grid'>{g}</div>")


@app.route("/contact")
def contact():
    ic = lambda p: f'<svg viewBox="0 0 24 24">{p}</svg>'
    mail = ic('<rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 7l9 6 9-6"/>')
    tel = ic('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>')
    pin = ic('<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>')
    clk = ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
    info = [("01", "Email Registry", ME["email"], "mailto:" + ME["email"], mail),
            ("02", "Direct Hotline", ME["phone"], "tel:" + ME["phone"].replace("-", ""), tel),
            ("03", "Headquarters", "Hyderabad, Telangana, India", "", pin),
            ("04", "Operational Window", "Entry-Level Data Analyst Roles", "", clk)]
    cells = "".join(
        f"<div class='cx'><span class='cn'>{n}</span><span class='ci2'>{i}</span><div><small>{e(a)}</small>" +
        (f"<a href='{u}'>{e(v)}</a>" if u else f"<b>{e(v)}</b>") + "</div>" +
        (f"<a class='ar' href='{u}'>&nearr;</a>" if u else "") + "</div>"
        for n, a, v, u, i in info)
    style = """<style>
.cs h1{font-size:clamp(26px,4vw,40px);margin:8px 0 10px}
.cs .lead{font-size:13px;margin-bottom:0}
.cs .eyebrow{font-size:10px}
.stbar{display:flex;gap:10px 22px;flex-wrap:wrap;margin:22px 0 0;padding:12px 16px;border:1px solid #111;background:#fff;font:700 10px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase}
.stbar i{display:inline-block;width:8px;height:8px;background:var(--g);margin-right:8px;animation:pl 1.6s infinite}
@keyframes pl{50%{opacity:.25}}
.stbar span{color:var(--mut)}
.cwrap{display:grid;grid-template-columns:1fr 1.15fr;gap:36px;align-items:start;margin-top:28px}
.cinfo{display:grid;gap:14px}
.cx{position:relative;display:flex;align-items:center;gap:14px;background:#fff;border:1px solid #111;padding:16px 18px;box-shadow:5px 5px 0 var(--line);transition:.2s}
.cx:hover{transform:translate(-2px,-2px);box-shadow:7px 7px 0 var(--r)}
.cn{position:absolute;top:6px;right:12px;font:700 26px/1 'Oswald',sans-serif;color:transparent;-webkit-text-stroke:1px #cfcfc8}
.ci2{width:38px;height:38px;flex:none;background:#111;display:grid;place-items:center}
.ci2 svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:1.6}
.cx small{display:block;font:700 9px 'JetBrains Mono',monospace;letter-spacing:.14em;color:var(--mut);text-transform:uppercase}
.cx a,.cx b{font:500 14px 'Inter',sans-serif;word-break:break-all}
.cx a:hover{color:var(--r)}
.cx .ar{margin-left:auto;margin-right:34px;width:28px;height:28px;border:1px solid #111;display:grid;place-items:center;font-size:14px;flex:none}
.cx .ar:hover{background:#111;color:#fff}
.onl{background:#111;color:#fff;padding:22px;box-shadow:6px 6px 0 var(--r)}
.onl .eyebrow{color:#ff5a64}
.onl h3{font:500 17px 'Oswald',sans-serif;text-transform:uppercase;margin:6px 0 8px}
.onl p{font-size:12px;color:#c9ced6;margin-bottom:14px}
.onl .row{margin-top:0}
.onl .btn{padding:9px 14px;font-size:10px;background:#fff;color:#111!important;border-color:#fff}
.onl .btn.o{background:transparent;color:#fff!important}
.cform{background:#fff;border:1px solid #111;box-shadow:8px 8px 0 var(--line)}
.ch{display:flex;justify-content:space-between;align-items:center;padding:12px 24px;border-bottom:1px solid #111;background:#f6f6f2;font:700 10px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase}
.ch b{color:var(--g);font-weight:700}
.cb{padding:24px}
.cb h2{font:700 20px 'Oswald',sans-serif;text-transform:uppercase;margin:0 0 4px}
.cb>p{font-size:12px;color:var(--mut)}
.cb label.fl{display:block;font:700 9px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:16px 0 6px}
.cb label.fl em{color:var(--r);font-style:normal}
.cb input[type=text],.cb input[type=email],.cb textarea{width:100%;border:1px solid #111;background:var(--bg);padding:11px 12px;font:13px 'Inter',sans-serif;color:var(--ink);outline:none;transition:.2s}
.cb input:focus,.cb textarea:focus{background:#fff;box-shadow:3px 3px 0 var(--r)}
.cb textarea{min-height:120px;resize:vertical}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.sub input{position:absolute;opacity:0;pointer-events:none}
.sub{display:flex;gap:8px;flex-wrap:wrap}
.sub label{border:1px solid #111;padding:7px 12px;font:700 10px 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;background:#fff;transition:.2s}
.sub label:hover{box-shadow:2px 2px 0 var(--r)}
.sub input:checked+label{background:#111;color:#fff}
.cb button{margin-top:20px;width:100%;cursor:pointer;padding:14px;border:1px solid #111;background:#111;color:#fff;font:700 11px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;transition:.2s}
.cb button:hover{box-shadow:4px 4px 0 var(--r);transform:translate(-2px,-2px)}
.cb button:disabled{opacity:.6;cursor:wait}
.note{margin-top:12px;font:10px 'JetBrains Mono',monospace;color:var(--mut);letter-spacing:.06em;text-align:center}
.ticker.sm{margin-top:56px}.ticker.sm div{font-size:10px}
@media(max-width:800px){.cwrap{grid-template-columns:1fr}.two{grid-template-columns:1fr}}
</style>"""
    subs = "".join(
        f'<input type="radio" name="s" id="s{i}" value="{e(v)}"{" checked" if i == 0 else ""}><label for="s{i}">{e(v)}</label>'
        for i, v in enumerate(["Job Opportunity", "Project Work", "Collaboration", "Just Saying Hi"]))
    form = f"""<form class="cform" id="cf"><div class="ch"><span>Message Form / Secure Dispatch</span><b>&#9679; Online</b></div>
<div class="cb"><h2>Drop a Message</h2><p>Fill in the brief below and I will get back to you soon.</p>
<label class="fl">Purpose</label><div class="sub">{subs}</div>
<div class="two"><div><label class="fl" for="n">Sender Name <em>*</em></label><input type="text" id="n" placeholder="Your full name" required></div>
<div><label class="fl" for="m">Email <em>*</em></label><input type="email" id="m" placeholder="you@company.com" required></div></div>
<label class="fl" for="t">Detailed Message Brief <em>*</em></label><textarea id="t" placeholder="Tell me about the role, project or idea..." required></textarea>
<input type="text" id="w" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<button type="submit" id="btn">Dispatch Message &rarr;</button>
<div class="note" id="st">Your message is sent directly to my inbox</div></div></form>
<script>
document.getElementById('cf').addEventListener('submit',function(ev){{
ev.preventDefault();
var b=document.getElementById('btn'),st=document.getElementById('st');
b.disabled=true;b.textContent='Sending...';
fetch('/send',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{
name:document.getElementById('n').value,email:document.getElementById('m').value,
message:document.getElementById('t').value,purpose:document.querySelector('input[name=s]:checked').value,
website:document.getElementById('w').value}})}})
.then(function(r){{return r.json()}})
.then(function(d){{
if(d.ok){{st.textContent='Message sent. Thank you, I will reply soon.';st.style.color='#059669';document.getElementById('cf').reset();}}
else{{st.textContent=d.error||'Something went wrong.';st.style.color='#e5000f';}}
b.disabled=false;b.innerHTML='Dispatch Message &rarr;';
}})
.catch(function(){{st.textContent='Network error. Please try again.';st.style.color='#e5000f';b.disabled=false;b.innerHTML='Dispatch Message &rarr;';}});
}});
</script>"""
    online = f"""<div class="onl"><div class="eyebrow">Find Me Online</div><h3>Prefer a different channel?</h3>
<p>Connect on LinkedIn or browse my code on GitHub.</p>
<div class="row"><a class="btn" href="{ME['li']}" target="_blank" rel="noopener">LinkedIn &nearr;</a>
<a class="btn o" href="{ME['gh']}" target="_blank" rel="noopener">GitHub &nearr;</a></div></div>"""
    status = ('<div class="stbar"><div><i></i>Available for entry-level roles</div><span>Replies within 24 hrs</span>'
              '<span>Hyderabad, IN (IST)</span></div>')
    kw = ["Open To Work", "Python", "SQL", "Pandas", "EDA", "Dashboards", "Data Analyst"]
    tick = "".join(f"{k} &nbsp;&#8734;&nbsp; " for k in kw) * 4
    body = (style + '<div class="cs">' + head("Connect Registry", "Establish Contact",
            "Open to entry-level Data Analyst roles. Reach out through any channel below.")
            + status + f"<div class='cwrap'><div class='cinfo'>{cells}{online}</div>{form}</div>"
            + f'<div class="ticker sm"><div>{tick}</div></div></div>')
    return page("/contact", "Contact", body)


@app.route("/send", methods=["POST"])
def send():
    """Receives the contact form and emails it to you with a private
    '[PORTFOLIO]' note that the visitor never sees."""
    d = request.get_json(silent=True) or {}
    if d.get("website"):  # honeypot: bots fill this hidden field
        return jsonify(ok=True)

    name, mail, msg, purpose = (str(d.get(k, "")).strip() for k in ("name", "email", "message", "purpose"))
    if not (name and mail and msg) or "@" not in mail:
        return jsonify(ok=False, error="Please fill all fields."), 400

    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    if not (smtp_user and smtp_pass):
        return jsonify(ok=False, error="Mail is not configured. Please email me directly."), 500

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    m = EmailMessage()
    m["From"] = smtp_user
    m["To"] = ME["email"]
    m["Reply-To"] = mail  # hitting Reply goes straight to the visitor
    m["Subject"] = f"[PORTFOLIO] {purpose or 'Message'} from {name}"
    m.set_content(
        "*** SENT VIA YOUR PORTFOLIO CONTACT FORM ***\n"
        f"Purpose : {purpose}\nName    : {name}\nEmail   : {mail}\n"
        f"Time    : {datetime.now():%d %b %Y, %I:%M %p}\nIP      : {ip}\n"
        "-----------------------------------------\n\n"
        f"{msg}\n"
    )
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(smtp_user, smtp_pass)
            s.send_message(m)
    except Exception:
        return jsonify(ok=False, error="Could not send. Please email me directly."), 500
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True)