#!/usr/bin/env python3
"""ServiceNow Impact executive briefing — one 28-slide content model, three outputs.

  * ServiceNow-Impact-Australia-Executive-Briefing.pptx  (editable, speaker notes)
  * ServiceNow-Impact-Australia-Executive-Briefing.pdf   (landscape slides + notes pages)
  * site/deck.html                                       (browser deck with notes panel)

Run:  /home/user/pdfenv/bin/python tools/build_deck.py
"""
import os

from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ART = os.path.join(ROOT, "artifacts")
SITE = os.path.join(ROOT, "site")
os.makedirs(ART, exist_ok=True)
os.makedirs(SITE, exist_ok=True)
PPTX_PATH = os.path.join(ART, "ServiceNow-Impact-Australia-Executive-Briefing.pptx")
PDF_PATH = os.path.join(ART, "ServiceNow-Impact-Australia-Executive-Briefing.pdf")
HTML_PATH = os.path.join(SITE, "deck.html")

NAVY, BLUE, GREEN, LIGHT_GREEN, GREY, MID, WHITE = (
    "03213F", "1F4E79", "03754D", "E6F4EE", "F2F4F7", "5C6B7A", "FFFFFF")
FOOTER = "ServiceNow Impact  |  ServiceNow Australia release  |  Client briefing"
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# ============================================================ content model
S = []
S.append(dict(kind="title", title="ServiceNow Impact",
              subtitle="Application overview, business case and activation — Australia release",
              strap="Prepared from official ServiceNow Australia-release Impact documentation\n"
                    "Audience: executive sponsors, IT leadership, platform owners and architects",
              notes="Opening frame.\n\n"
                    "Purpose of today: agree what Impact is, what it is not, what it changes for us "
                    "operationally, and what we would need to do to activate it.\n\n"
                    "Three things to land by the end: (1) Impact is a subscription product that adds a "
                    "measurement and expert layer on top of the platform we already run — it does not "
                    "replace administration or Now Support; (2) roughly half of its value depends on "
                    "foundational work we control — instance connection, roles, scans and data "
                    "collection; (3) several capabilities are entitlement-dependent, so nothing in this "
                    "deck should be treated as committed until we confirm our package.\n\n"
                    "Ask for the session: agreement on the activation sequence and an owner for each "
                    "prerequisite."))

S.append(dict(kind="bullets", title="Agenda", subtitle="Eight questions this briefing answers",
              items=[(0, "1. What ServiceNow Impact actually is — and what it is not"),
                     (0, "2. Why ServiceNow built it, and which problems it solves"),
                     (0, "3. The architecture: what sits where, and what data moves"),
                     (0, "4. The feature catalogue by pillar"),
                     (0, "5. What it looks like in practice — worked client scenarios"),
                     (0, "6. Business benefits, by stakeholder and by category"),
                     (0, "7. How it differs from traditional support"),
                     (0, "8. Prerequisites, activation steps and the first 90 days")],
              notes="Set expectations on depth. Sections 1–3 are the conceptual frame, 4–6 are the "
                    "value case, 7 is the honest comparison, 8 is the operational ask.\n\n"
                    "Everything in the deck is drawn from the Australia-release product documentation "
                    "listed in the written brief (Appendix E). Where the documentation is silent or a "
                    "figure is entitlement-dependent, the slide says \u201cverify\u201d rather than guessing.\n\n"
                    "If the audience is purely executive, the recommended path is slides 1\u20137, then 17\u201319, "
                    "then 23\u201326. The technical sections (9\u201316, 20\u201322) are for the architecture and "
                    "platform audience."))

S.append(dict(kind="cards", title="Executive summary", subtitle="Three things to remember about ServiceNow Impact",
              cards=[[("1 · Prove value",
                       "Objectives → outcomes → success metrics → benchmarks → monetised Value Reports "
                       "with visible assumptions.", BLUE),
                      ("2 · Know your health",
                       "HealthScan across manageability, performance, security, upgradeability and user "
                       "experience; Scan Engine findings with real-time prevention and AI fixes; "
                       "off-instance monitoring in Instance Observer.", GREEN),
                      ("3 · Plan and execute",
                       "Capability maps show what you own and use; Product Adoption Roadmaps sequence "
                       "what comes next; Accelerators supply fixed-scope expert capacity.", BLUE)]],
              notes="The three-line version.\n\n"
                    "1. Prove value. Impact's value layer connects business objectives to measurable "
                    "outcomes with a metric, a baseline quarter and a target — and rolls that into "
                    "monetised Value Reports where the assumptions are visible. Caveat to state "
                    "upfront: a meaningful Value Report needs at least two years of product data, so "
                    "the earlier we start collecting, the earlier we can report.\n\n"
                    "2. Know your health. Thousands of leading-practice checks run against the instance "
                    "continuously rather than being discovered during an upgrade. Findings stay in our "
                    "instance. Instance Observer watches performance and availability from outside the "
                    "instance.\n\n"
                    "3. Plan and execute. Capability maps show what we own versus what we actually use; "
                    "roadmaps sequence the next phases; Accelerators are fixed-scope expert engagements "
                    "consumed against package concurrency.\n\n"
                    "The honest framing: Impact gives us measurement, guidance and expert capacity. It "
                    "does not do our remediation for us."))

S.append(dict(kind="bullets", title="1. What ServiceNow Impact is",
              subtitle="A premium customer success product — not a normal application",
              items=[(0, "Impact is a subscription-based customer success product that combines AI-powered tools with hands-on ServiceNow expertise."),
                     (0, "It is delivered in three parts:"),
                     (1, "A digital workspace inside our own instance — the Impact Store Application"),
                     (1, "A ServiceNow-hosted expert space — the Impact Delivery Instance (IDI)"),
                     (1, "Human expertise and service entitlements — the Impact Squad, Developer Support, learning credits and Accelerators"),
                     (0, "Stated core functions: plan implementation, track product adoption, maintain platform health, resolve platform issues, access expert support."),
                     (0, "From Yokohama onward the Impact Store Application is the exclusive hub for new Impact features — the IDI does not receive new features."),
                     (0, "It does not replace platform administration, change control or Now Support case handling.")],
              notes="Define it precisely, because \u201cImpact\u201d is often heard as \u201csupport\u201d or \u201canother module\u201d.\n\n"
                    "It is a subscription product with three delivery surfaces. The one that matters most "
                    "for day-to-day work is the Impact Store Application inside our instance \u2014 reached at "
                    "All \u2192 Impact. The IDI is where our named squad works; we reach it through the Activity "
                    "Center. Human expertise is the third piece: CSM, and in higher packages a Customer "
                    "Success Executive, Platform Architect and Support Account Manager.\n\n"
                    "The directional statement worth emphasising: from Yokohama onward, new innovative "
                    "Impact features land in the Store Application, not the IDI. So the app is where our "
                    "future capability will accumulate.\n\n"
                    "Close with the boundary: this is not a replacement for our admins or our support "
                    "contract, and we should not describe it that way to the business."))

S.append(dict(kind="table", title="Why it exists and what it solves",
              subtitle="From ticket resolution to value realisation",
              table=[["Client problem", "What Impact provides", "Where it lives"],
                     ["Cannot prove the value of the investment", "Objectives → measurable outcomes → benchmark/goal trend → monetised Value Reports", "Value Management"],
                     ["Bought modules nobody uses", "Capability Maps, Product Adoption Roadmaps, entitlement visibility", "Product Adoption"],
                     ["Hidden technical debt", "HealthScan definitions, Scan Engine findings, Real-Time Prevention, AI fixes", "Platform Health"],
                     ["Problems only found at upgrade time", "Upgrade readiness, update-set scanning, Proactive Code Check", "Platform Health"],
                     ["Performance found by users, not us", "Off-instance monitoring, alerts, triage, root-cause correlation", "Instance Observer"],
                     ["'What should we do next?'", "Recommendation engine, squad guidance, roadmaps, Accelerators", "Impact home / IDI"],
                     ["Expert capacity is the bottleneck", "Developer Support, Accelerators, Initiatives, learning credits", "Experts & learning"]],
              banner=("The shift", "Ticket-based support answers \u201csomething is broken\u201d. Impact answers \u201care we getting value, is it healthy, and what next?\u201d", GREEN),
              notes="This slide reframes the conversation from support to outcomes.\n\n"
                    "Walk the rows rather than reading them. The pattern is that each row is a question "
                    "our own stakeholders already ask \u2014 usually at renewal, or after an incident, or when "
                    "a business unit questions the spend.\n\n"
                    "Two rows are worth dwelling on with an executive audience. First, \u201ccannot prove "
                    "value\u201d \u2014 that is the value management row and it is the reason many organisations "
                    "adopt Impact at all. Second, \u201cwhat should we do next\u201d \u2014 most stalled programs are "
                    "not short of findings; they are short of a defensible priority order.\n\n"
                    "For a technical audience, the two rows that matter are the health and performance "
                    "rows \u2014 those are the ones that change day-to-day engineering work."))

S.append(dict(kind="cards", title="Where Impact fits on the platform",
              subtitle="Around and above the AI Platform — it does not replace our processes",
              cards=[[("Your instance",
                       "Impact Store Application · Platform Health · Value Management packs · Instance Observer telemetry", NAVY),
                      ("Service Bridge",
                       "Secure, bi-directional sync — status must read Active replication", GREEN),
                      ("Impact Delivery Instance",
                       "Impact Squad · Activity Center · catalogues · value reporting · training insights", BLUE)],
                     [("Now Support",
                       "Standard case handling stays here — Impact adds enhanced P1/P2 targets, Developer Support and proactive engagements", NAVY),
                      ("AI stack",
                       "Now Assist / ServiceNow Otto: outcome and consumption summaries, AI code fixes, GenAI root-cause analysis", BLUE),
                      ("Business outcomes",
                       "Adoption · Platform health · Performance & availability · Value realised · Upgrade readiness", GREEN)]],
              notes="Two rows, three boxes each \u2014 it reads as \u201cwhat we run\u201d, \u201cwhat connects us\u201d, \u201cwhat ServiceNow "
                    "runs for us\u201d, then where support and AI sit.\n\n"
                    "Key point for the platform team: the Service Bridge connection must reach Active "
                    "replication in both directions. That single status is the gate for almost everything "
                    "else in the product, and it is the most common place where activation stalls.\n\n"
                    "Key point for the support/operations audience: Now Support does not go away. Case "
                    "handling stays there; Impact adds response targets and Developer Support on top.\n\n"
                    "Key point for everyone: impact sits around and above the platform. It does not "
                    "replace our change, release or data governance processes."))

S.append(dict(kind="bullets", title="2. Why ServiceNow introduced it",
              subtitle="Five market drivers behind the product",
              items=[(0, "The platform outgrew ticket-based support. Customers stopped asking only \u201csomething is broken, fix it\u201d and started asking \u201care we using what we bought?\u201d"),
                     (0, "Value realisation became a board-level question — finance wants ROI evidence, not anecdotes."),
                     (0, "Technical debt accumulated silently — leading practices were never measured continuously."),
                     (0, "Expert capacity is scarce — advice had to be packaged as fixed-scope delivery, not documents."),
                     (0, "Upgrade fatigue is real — the causes of broken upgrades needed to be attacked before the upgrade window."),
                     (0, "The product response is a closed loop: instrument → interpret → recommend → measure → repeat.")],
              notes="This is the \u201cwhy does this product exist\u201d slide. It is useful when a client is "
                    "sceptical that Impact is more than rebranded support.\n\n"
                    "The strongest of the five with an Australian enterprise or government audience is "
                    "usually value realisation \u2014 audit and budget scrutiny make the ROI question "
                    "unavoidable.\n\n"
                    "For a technical audience, lead with upgrade fatigue and silent technical debt: "
                    "those are the pain points the platform team already feels weekly.\n\n"
                    "Land the closed loop at the end because it is the mental model for the architecture "
                    "slide that follows."))

S.append(dict(kind="table", title="3. Architecture — components at a glance",
              subtitle="What sits where, and what moves data",
              table=[["Layer", "Component", "Where it lives", "Moves data off-instance?"],
                     ["Customer instance", "Impact Store Application", "Your instance — All → Impact", "No"],
                     ["Customer instance", "Impact Common / Content / Health", "Dependent apps", "No — findings stay local"],
                     ["Customer instance", "Value Management data packs", "Conditional per product; jobs must be enabled", "Populates value metrics"],
                     ["Off-instance", "Instance Observer", "Off-instance cloud app (entitlement-tiered)", "Telemetry collected off-instance"],
                     ["ServiceNow side", "Impact Delivery Instance (IDI)", "ServiceNow-hosted (impact.service-now.com)", "Provider side"],
                     ["Integration", "Service Bridge", "Platform capability + dependent apps", "Yes — bi-directional sync"],
                     ["Integration", "Cloud Storage · Licensing Engine · MIF", "Dependent apps", "Yes — for the security review"],
                     ["AI", "Now Assist / ServiceNow Otto skills", "Your instance + Now Assist Admin", "Governed by Now Assist terms"]],
              after=["Security review shortlist: Service Bridge, Cloud Storage, Licensing Engine and MIF move data. Impact Common, Content and Health do not."],
              notes="This is the slide the security and architecture reviewers will photograph.\n\n"
                    "The critical answer to the inevitable question \u201cwhat leaves our instance?\u201d is in the "
                    "last column. Four components move data: the Service Bridge stack, Cloud Storage, "
                    "the Licensing Engine and the MIF Customer Instance. Impact Common, Impact Content "
                    "and Impact Health do not move data, and Scan Engine findings stay in our instance.\n\n"
                    "Note the Instance Observer row: it is off-instance monitoring by design \u2014 that is "
                    "precisely why it still works when the instance itself is degraded, and it is also "
                    "why it needs its own consent conversation for user-experience data.\n\n"
                    "Values, licensing and subscription data feed Capability Maps and the Subscriptions "
                    "view \u2014 worth naming so nobody is surprised later."))

S.append(dict(kind="diagram", title="3. Architecture — how Impact works",
              subtitle="Instrument → interpret → recommend → measure → repeat",
              notes="The one diagram to walk slowly.\n\n"
                    "Left to right: our estate, the secure sync layer, the ServiceNow side, then the "
                    "business outcomes. Underneath, the operating cadence that closes the loop.\n\n"
                    "Column 1 is everything under our control and our responsibility: the app, the Scan "
                    "Engine and HealthScan definitions, the Performance Analytics collection jobs that "
                    "feed value metrics, our users and roles, and off-instance observability.\n\n"
                    "Column 2 is the single integration point. Automated registration is preferred; "
                    "regulated and GCC customers must use manual registration.\n\n"
                    "Column 3 is what ServiceNow brings: named squad, the Activity Center, value "
                    "management, and the catalogues.\n\n"
                    "Column 4 is why we are doing this.\n\n"
                    "Two callouts to say out loud: Scan Engine findings are NOT transmitted to the IDI; "
                    "and feature availability depends on our package, add-ons, roles and installed "
                    "plugins \u2014 which is why we verify before we commit."))

S.append(dict(kind="table", title="4. Feature catalogue — the five pillars",
              subtitle="Each pillar maps to a client problem and a measurable output",
              table=[["Pillar", "What it includes", "The output the client sees"],
                     ["Platform Health", "HealthScan definitions, Scan Engine, Real-Time Prevention, Proactive Code Check, AI fixes", "Health scores by category, findings, remediation plans, upgrade readiness"],
                     ["Instance Observer", "Performance and availability monitoring, alerts, triage, root-cause correlation, user experience", "Alerts before users notice, faster MTTR, capacity evidence"],
                     ["Value Management", "Objectives, outcomes, success metrics, Outcome Insights, Value Reports, Technical KPIs", "Monetised value reporting with visible assumptions"],
                     ["Product Adoption", "Capability Maps, Product Adoption Roadmaps, recommendations, Subscriptions", "A sequenced adoption plan grounded in what we own"],
                     ["Experts & learning", "Impact Squad, Developer Support, Accelerators, Initiatives, training insights, learning credits", "Delivered artefacts and funded skills uplift"]],
              notes="This is the map for the rest of the feature discussion.\n\n"
                    "The framing to use: every pillar exists to answer a question a stakeholder already "
                    "has. Platform Health answers \u201cis the instance in good shape?\u201d. Instance Observer "
                    "answers \u201cis it performing?/will users notice?\u201d. Value Management answers \u201cwas it "
                    "worth it?\u201d. Product Adoption answers \u201cwhat should we do next?\u201d. Experts and learning "
                    "answer \u201cwho helps us, and how do we get better?\u201d\n\n"
                    "If time is short, the two pillars to cover properly are Platform Health (because it "
                    "is the most immediately useful to the platform team) and Value Management (because "
                    "it is the one the CFO will ask about).\n\n"
                    "The next four slides go one level deeper; the detailed per-feature structure is in "
                    "the written brief, section 3."))

S.append(dict(kind="bullets", title="Platform Health — insight, prevention, remediation",
              subtitle="Thousands of leading-practice checks, run continuously",
              items=[(0, "HealthScan definitions: the checks. Scan Engine: the runner. Findings: the output — and they stay in our instance."),
                     (0, "Persona dashboards mean each role sees what it owns: executive, platform owner, team lead, development team."),
                     (0, "Custom definitions let us encode our own standards; definition suites group them; exception reasons give an approved escape hatch."),
                     (0, "Real-Time Prevention validates changes as they are made rather than after the fact."),
                     (0, "Integration: findings can be routed into Jira, Azure DevOps, SPM or CWM so remediation lands in the team's existing backlog."),
                     (0, "AI: batch remediation with AI proposes fixes for review (needs Now Assist for Impact 3.03+, Now Assist for Platform 11.01+, the skill activated and sn_impact_gen_ai.ai_fix.enabled = true)."),
                     (0, "First full scan can take hours — ServiceNow recommends running it overnight, especially in production.")],
              notes="This is the pillar the platform and development teams will care about most.\n\n"
                    "Start with the locality point because it is a common objection: findings are "
                    "produced in our instance and are not transmitted to the Impact Delivery Instance.\n\n"
                    "The persona dashboards matter more than they sound \u2014 they are what stop findings "
                    "becoming an undifferentiated list. A team lead sees their team's new findings after "
                    "a sprint; an executive sees the trend.\n\n"
                    "On custom definitions: this is where we encode house rules (no business logic in "
                    "UI policies, no direct CMDB writes from integrations). Guided has a documented cap "
                    "of up to 10 active custom definitions and Total is documented as unlimited \u2014 "
                    "verify against our package.\n\n"
                    "On the first scan: set expectations now. It can take hours; run it overnight in "
                    "production and monitor Scan Status rather than re-triggering."))

S.append(dict(kind="bullets", title="Instance Observer — performance, availability, user experience",
              subtitle="Monitoring from outside the instance — including when the instance is unwell",
              items=[(0, "Off-instance observability: if the instance degrades, its own monitoring is often the first casualty — Observer keeps working."),
                     (0, "Coverage includes core performance, database, ECC queue, email, events, host health, jobs, load balancer, node health, replicas, schedulers and semaphores."),
                     (0, "Alerting: popular and custom alerts, anomaly-based thresholds, RCC alerts and long-pending-job alert cards, with webhook notifications into our existing channels."),
                     (0, "Triage and root-cause correlation turn an alert into an investigation with evidence attached."),
                     (0, "User-experience insights require an admin to accept Terms & Conditions via Manage Permissions; user IDs are anonymised by default with an opt-in for non-anonymised collection."),
                     (0, "Entitlement-tiered: seats, look-back window, alert counts and analytics differ between Guided and Total — verify. Not available in the mobile app.")],
              notes="Position this as the answer to the most demoralising class of incident: performance "
                    "problems reported by users after the fact, with no evidence left to investigate.\n\n"
                    "The off-instance argument is the headline: when an instance is degraded, in-instance "
                    "monitoring is unreliable. Observer watches from outside.\n\n"
                    "For the operations audience, the practical wins are anomaly-based alerting (fewer "
                    "noisy static thresholds) and webhook routing into the existing on-call tooling "
                    "rather than a new console nobody watches.\n\n"
                    "Raise the consent point deliberately: user-experience monitoring requires Terms & "
                    "Conditions acceptance by an admin in Manage Permissions, IDs are anonymised by "
                    "default, and there is an opt-in for non-anonymised collection. That is a "
                    "conversation for our privacy and employee-representation stakeholders, not a "
                    "technical toggle.\n\n"
                    "Finally, flag the entitlement differences and the mobile-app gap so expectations "
                    "are set correctly."))

S.append(dict(kind="table", title="Value management — proving ROI, not asserting it",
              subtitle="Every outcome carries a metric, a baseline and a target",
              table=[["Element", "What it is", "Why it matters to the client"],
                     ["Business objective", "High-level business statement, e.g. reduce cost to serve", "Speaks the language of the executive sponsor, not IT"],
                     ["Business outcome", "Measurable result connected to an objective", "Makes the objective falsifiable"],
                     ["Success metric", "The specific measure that moves", "Removes ambiguity about what 'success' means"],
                     ["Reference quarter + goal", "Baseline period and target", "Enables trend reporting and comparison"],
                     ["Outcome Insights", "On-track analysis against benchmark and goal", "Tells us where to intervene, and recommends the capability or course"],
                     ["Value Reports", "Monetised aggregation with visible assumptions", "The artefact finance will challenge — so the assumptions are shown"],
                     ["Technical KPIs", "Standardised technical measures with peer comparison", "Answers 'how good are we?' with context"]],
              banner=("Caveat to state upfront", "A meaningful Value Report needs at least two years of product data — start collecting early.", BLUE),
              notes="This is the pillar that justifies the purchase to the CFO, and the one most often "
                    "run badly.\n\n"
                    "The discipline is in the chain: objective \u2192 outcome \u2192 success metric \u2192 reference "
                    "quarter and goal. If any link is vague, the report is not defensible. Push the "
                    "sponsor to make objectives business statements (\u201creduce cost to serve\u201d) rather than "
                    "IT statements (\u201ccomplete the next upgrade\u201d).\n\n"
                    "Outcome Insights is the operational half \u2014 it tells us which outcomes are off track "
                    "and recommends the capability or the training that addresses them. Value Reports "
                    "are the reporting half, and their credibility comes from showing assumptions "
                    "rather than hiding them.\n\n"
                    "State the caveat out loud rather than letting someone discover it later: a "
                    "meaningful Value Report needs at least two years of product data. That is an "
                    "argument for starting data collection now, even if the first report is modest."))

S.append(dict(kind="bullets", title="Product adoption and recommendations",
              subtitle="Closing the gap between what we own and what we use",
              items=[(0, "Capability Maps show entitlements and adoption status, generated per instance — so we can see the gap between purchased and used."),
                     (0, "Product Adoption Roadmaps sequence capabilities into phases aligned to objectives, published and date-targeted."),
                     (0, "The recommendation engine surfaces the next best action on the Impact home page and in the IDI, each with rationale."),
                     (0, "Recommendations can be converted into work items in SPM or CWM (or Jira/Azure DevOps via integration) so they enter governed delivery."),
                     (0, "Accelerators and Initiatives are the delivery mechanism: fixed-scope expert engagements against the catalog."),
                     (0, "Concurrency governs how many can run at once — documented as 1 at a time for Guided and 7 concurrent for Total, plus Add-on concurrency."),
                     (0, "Subscriptions and the Consumption Report give transparent visibility of what was purchased and what was actually consumed.")],
              notes="Three connected ideas: see the gap, plan the closure, execute with help.\n\n"
                    "The gap point is usually the most confronting for clients \u2014 most organisations "
                    "materially under-use what they already own, and that is a renewal risk as much as "
                    "an efficiency one.\n\n"
                    "The planning point is that roadmaps are sequenced against business objectives, not "
                    "product release order. That is what makes them adoptable by the business.\n\n"
                    "The execution point is the conversion step: a recommendation that never becomes a "
                    "work item is just a notification. Route them into SPM, CWM, Jira or Azure DevOps "
                    "during normal planning.\n\n"
                    "Raise concurrency honestly: it is a real constraint on how many expert engagements "
                    "can run at once, and scheduling is subject to availability. Plan engagements in "
                    "advance rather than assuming immediate start."))

S.append(dict(kind="table", title="Experts, learning and governance",
              subtitle="The human layer that makes the tooling stick",
              table=[["Element", "What it provides", "How we consume it"],
                     ["Impact Squad", "Customer Success Manager, plus CSE / Platform Architect / SAM in higher packages", "Activity Center conversations, tasks, calendar, files"],
                     ["Developer Support", "Named engineers who help troubleshoot our existing customisations", "Named individuals raise cases; documented as 5 seats Guided / 10 Total — verify"],
                     ["Accelerators", "Fixed-scope, expert-led engagements against four sub-catalogs", "Requested from the app or IDI, consumed against concurrency"],
                     ["Initiatives", "Multi-Accelerator programs towards a larger goal", "Planned with the squad across quarters"],
                     ["Learning", "Training Insights, contextual course recommendations, learning credits", "Credits allocated against under-performing outcomes"],
                     ["Operating model", "Foundations phase, then monthly and quarterly Steady State reviews", "Calendarised governance with named attendees"]],
              notes="Tooling without a human layer produces dashboards nobody acts on \u2014 this slide is "
                    "the counterweight to the product slides.\n\n"
                    "The squad is the primary relationship: the CSM orchestrates onboarding, the "
                    "Foundations phase and the review cadence.\n\n"
                    "Be precise about Developer Support scope, because it is commonly over-estimated: "
                    "it covers troubleshooting and improving existing customisations, and explicitly "
                    "does not cover net-new implementations or customisations that break after a "
                    "family upgrade \u2014 those go to Now Support.\n\n"
                    "Learning is the most commonly wasted entitlement because credits expire unused. "
                    "The mechanism that makes it purposeful is the link from an under-performing "
                    "outcome to a specific recommended course.\n\n"
                    "Close on governance: Impact works when it is calendarised. That is the ask in "
                    "section 8."))

# --- scenarios 3 slides
SCEN = [
    [["Renewal conversation you cannot support", "Value Management: objectives → outcomes → success metrics → Value Reports",
      "Defensible ROI at renewal — but start early; Value Reports need ~2 years of data"],
     ["Shelf-ware we keep paying for", "Capability Maps, Product Adoption Roadmaps, Subscriptions",
      "Reduced shelf-ware, sequenced adoption instead of a wish list"],
     ["Technical debt found too late", "HealthScan, Scan Engine, update-set scans, Proactive Code Check, AI fixes",
      "Fewer upgrade defects and a documented pre-upgrade health baseline"],
     ["Performance reported by users, not monitoring", "Instance Observer: anomaly alerts, triage, root-cause correlation",
      "Detection before user reports; shorter MTTR with evidence attached"]],
    [["New platform owner inherits an undocumented program", "Impact Squad, home page, Digest, Activity Center, roadmaps, training",
      "Continuity of the value narrative within the first quarter"],
     ["Change management is reactive", "Real-Time Prevention, custom definitions and suites, exception reasons",
      "Fewer change-related production incidents, with evidence of enforcement"],
     ["Skills gap blocks adoption", "Training Insights, contextual learning, learning credits",
      "Measurable improvement on the linked outcome metric"],
     ["Remediation work never gets prioritised", "Recommendation → work item conversion (SPM/CWM/Jira/ADO), Accelerators",
      "Rising remediation completion; no dual-tracking of platform work"]],
    [["Multiple business units, competing priorities", "Stakeholder Groups (Group Views), per-group objectives, instance filters",
      "Higher executive engagement; cleaner value attribution per function"],
     ["Controlled environment, constrained feature set", "Documented availability restrictions; squad guidance; no domain separation",
      "No late-stage design rework from an entitlement or environment constraint"],
     ["Consumption and entitlement governance", "Consumption Report / Benefits & Usage, Accelerator and Developer Support usage",
      "Higher entitlement utilisation; evidence-based position at renewal"],
     ["Regulated onboarding: manual registration", "Manual registration path, Service Bridge, connection verification",
      "Compliant verified connection showing Active replication — the gate for everything else"]],
]
for idx, group in enumerate(SCEN):
    S.append(dict(kind="table",
                  title="5. Client scenarios — problem → capability → outcome (%d/3)" % (idx + 1),
                  subtitle="Twelve worked scenarios from Australian enterprise and government programs" if idx == 0 else None,
                  table=[["Problem", "Impact capability", "Measurable outcome"]] + group,
                  notes=("Scenario group %d of 3. Use these as discussion prompts rather than a "
                         "script.\n\nAsk which of these the client recognises as their own situation, "
                         "then go deep on that one. The strongest openers for most organisations are "
                         "the renewal-value scenario and the technical-debt scenario.\n\n"
                         "Each scenario is deliberately written as problem → capability → measurable "
                         "outcome so the conversation cannot drift into feature description without "
                         "landing on a result." % (idx + 1))))

S.append(dict(kind="table", title="6. Business benefits by stakeholder",
              subtitle="What each role gets — and the evidence they can point to",
              table=[["Stakeholder", "What they get", "Evidence"],
                     ["CIO / CDIO", "Confidence the platform delivers intended outcomes; defensible ROI position", "Value Reports, Outcome Insights, quarterly executive reviews"],
                     ["CFO / Finance", "Visible return on existing spend; reduced shelf-ware; assumption-transparent monetisation", "Value Reports, Capability Maps, Consumption Report"],
                     ["CIO office / Strategy", "Prioritised roadmap aligned to objectives; recommendations converted to governed work", "Roadmaps, SPM/CWM work items, Accelerator outcomes"],
                     ["Platform Owner", "Continuous health and performance visibility; defined cadence; expert escalation path", "Health scores, Observer alerts, Monthly Health Assessment, Tech KPIs"],
                     ["Platform Architect", "Engineering-quality evidence for design decisions; upgrade readiness", "Scan findings, custom definitions, Proactive Code Check, peer KPI comparison"],
                     ["Service Ops Manager", "Fewer user-reported incidents; faster resolution of hard cases", "Alert-to-resolution history, Developer Support outcomes"],
                     ["Developers", "Specific actionable findings; fast paths to fixes", "Team Lead dashboards, AI fix proposals, Jira/ADO integration"],
                     ["Security & Risk", "Documented data flows, consent controls, environment limitations", "Consent records, data-egress component list, availability restrictions"]],
              notes="Use this slide to make the benefits land with the person who owns the budget or the "
                    "risk.\n\n"
                    "The column that does the work is the last one \u2014 evidence. Benefits without evidence "
                    "get discounted in the room; naming the artefact that proves it is what makes the "
                    "benefit credible.\n\n"
                    "If the audience is mixed, pick two rows: CIO for the value story and Security for "
                    "the constraints story. Those are usually the two competing narratives that decide "
                    "whether the program proceeds.\n\n"
                    "The Security row is deliberate: naming the constraints and the controls openly is "
                    "what gets an approval rather than a deferral."))

S.append(dict(kind="cards", title="Business benefits by category",
              subtitle="Eight lenses for the business case",
              cards=[[("Financial", "Return on existing licence spend; avoided re-purchase; monetised value reporting", BLUE),
                      ("Risk reduction", "Technical debt measured continuously; upgrade and change risk found pre-production", GREEN),
                      ("Operational efficiency", "Remediation routed into existing backlogs; faster triage and root cause", BLUE),
                      ("Adoption & enablement", "Capability maps and roadmaps turn entitlements into used capability", GREEN)],
                     [("Governance & assurance", "Foundations → Steady State cadence with auditable artefacts", BLUE),
                      ("Decision quality", "Recommendations with rationale, peer context and expert validation", GREEN),
                      ("Predictability", "Managed upgrade readiness instead of emergency response", BLUE),
                      ("Scalability & continuity", "Expert capacity without permanent headcount; knowledge retained in the platform", GREEN)]],
              notes="Eight short lenses; do not read all eight aloud. Pick the three that match the "
                    "client's stated priorities.\n\n"
                    "For cost-pressured organisations: financial, operational efficiency and "
                    "predictability.\n\n"
                    "For regulated or high-assurance organisations: risk reduction, governance and "
                    "assurance, and decision quality.\n\n"
                    "For organisations in the middle of a transformation: adoption and enablement, and "
                    "scalability and continuity \u2014 because the constraint there is almost always skilled "
                    "people, not licences.\n\n"
                    "The honest note worth adding verbally: benefits 1\u20133 depend on us acting on findings; "
                    "benefits 4\u20138 depend on us keeping the cadence. Neither is automatic."))

S.append(dict(kind="table", title="7. Impact versus traditional support",
              subtitle="Reactive assurance versus proactive value creation — and how they coexist",
              table=[["Dimension", "Traditional reactive support", "ServiceNow Impact"],
                     ["Trigger", "A case is raised after something breaks", "Continuous instrumentation — scans, telemetry, value data"],
                     ["Scope", "Break-fix of ServiceNow base functionality", "Plus health, performance, adoption, value, upgrade readiness"],
                     ["Deliverable", "Fix, workaround, known error", "Assessments, roadmaps, monetised value reports, expert-led Accelerators"],
                     ["Expert access", "Support agents via Now Support portal", "Named Impact Squad, plus Developer Support engineers"],
                     ["Cadence", "Ad hoc, incident-driven", "Monthly operational and health reviews; quarterly outcome and executive reviews"],
                     ["Success measure", "SLA adherence and time to close", "Outcomes achieved, value realised, health trend, adoption"],
                     ["Commercial model", "Included with product support entitlements", "Subscription packages + Add-on SKUs + Accelerator concurrency"]],
              after=["What Impact does not do: it does not remove the need for administrators, change control, data governance, or a partner for net-new implementations."],
              notes="Handle this slide honestly \u2014 it is where scepticism is highest and where "
                    "over-claiming does the most damage.\n\n"
                    "The correct framing is coexistence, not replacement. Now Support remains the home "
                    "of incident management; Impact adds enhanced P1/P2 response targets (documented "
                    "as 30/120 minutes for Guided and 15/60 for Total \u2014 verify), Developer Support, "
                    "and the proactive layer.\n\n"
                    "Read the \u201cwhat Impact does not do\u201d line aloud. It buys credibility for everything "
                    "else on the slide, and it prevents the two most common client misapprehensions: "
                    "that Impact replaces support, and that Impact will fix technical debt by itself.\n\n"
                    "The most useful single sentence: support can tell us the platform is healthy "
                    "today; Impact tells us whether the platform is delivering what the business paid "
                    "for."))

S.append(dict(kind="bullets", title="8. Prerequisites — readiness before we start",
              subtitle="Most stalled deployments stall here, not on technology",
              items=[(0, "Platform: Yokohama or Xanadu Patch 2 and above; Impact Store Application entitlement (sn_entitlement) version 4.1.2 or higher — verify the live Store listing."),
                     (0, "Commercial: confirm the package (Guided / Total / Integrated Success) and any Add-ons; entitlements differ materially."),
                     (0, "People: a named contact administrator to receive the registration email, a Platform Owner, an Impact App Admin and a Scan Engine Admin."),
                     (0, "Access: Impact Squad access approval (read-only, 30 days, revocable, quarterly re-approval)."),
                     (0, "Consent: Terms & Conditions acceptance for user-experience monitoring; consent when scheduling the Monthly Health Assessment."),
                     (0, "Security: dedicated integration user, authentication method chosen (OAuth 2.0 preferred over Basic), data-egress review of Service Bridge, Cloud Storage, Licensing Engine and MIF."),
                     (0, "Data: exact instance names matching the instance_name property, full URLs, one Production designation."),
                     (0, "Capacity: storage growth (attachments dominate) and a cutover window for the first full scan."),
                     (0, "Known limitation: Impact does not support domain separation; portions are unavailable in restricted environments including Australia IRAP-Protected.")],
              notes="This slide is the operational ask. Do not rush it.\n\n"
                    "The single most important line for scheduling is the named contact administrator \u2014 "
                    "the registration email goes to that person, and if they are not identified (and "
                    "available), the whole sequence waits.\n\n"
                    "The second is the Security item: OAuth 2.0 is preferred over Basic authentication, "
                    "and the data-egress review should be scoped to the four moving components rather "
                    "than the whole product. Doing that early prevents a late security stall.\n\n"
                    "State the two limitations plainly: no domain separation, and restricted-environment "
                    "unavailability including Australia IRAP-Protected. If either applies to us, we "
                    "confirm the exact feature subset with the squad before design sign-off.\n\n"
                    "The pre-implementation checklist with owners is in section 7.10 of the written "
                    "brief \u2014 that is the artefact to take away from this slide."))

S.append(dict(kind="table", title="8. Installation and activation — the sequence (1 of 2)",
              subtitle="Each Guided Setup section must be completed to unlock the next",
              table=[["#", "Step", "Navigation", "Role"],
                     ["1", "Procure the app", "ServiceNow Store → Apps and Solutions → search Impact → Buy", "Any Impact role"],
                     ["2", "Install the app", "All → Application Manager → search Impact → Install (Sync now if missing)", "admin"],
                     ["3", "Open Guided Setup", "Application Manager → Configure, or All → Impact → Guided Setup → Get Started", "Impact App Admin / admin"],
                     ["4", "Onboard users", "All → Impact → Configuration → Guided Setup → User management", "Impact App Admin"],
                     ["5", "Platform Health users & teams", "All → Impact → Guided Setup → Assign Platform Health users; then Scan Engine Properties → Team Leads → New", "Impact App Admin / admin"],
                     ["6", "Activate Scan Engine", "Guided Setup → Impact Platform Health → Activate Scan Engine; grant Can read on sys_update_version", "Impact App Admin / admin"],
                     ["7", "(Optional) AI code fixes", "Scan Engine Properties → Real Time Scanning → Enforce real-time validation = true; Now Assist → Skills → Impact → Code Fix → Activate skill; sn_impact_gen_ai.ai_fix.enabled = true", "Scan Engine Admin"],
                     ["8", "Run the first full scan", "All → Impact → Platform Health → Scheduled Scan → Execute Now; monitor Scan Engine → Scan Status", "Impact App Admin / admin"]],
              after=["Expect the first full scan to take hours — run it overnight, especially in production. Scan Engine findings are not transmitted to the Impact Delivery Instance."],
              notes="Steps 1\u20138 are everything up to the point where the instance is scanning.\n\n"
                    "Two sequencing traps worth calling out. First, Guided Setup steps lock \u2014 you cannot "
                    "jump ahead, and marking a step complete prematurely hides a failure until much "
                    "later in the sequence. Mark complete only on genuine success.\n\n"
                    "Second, step 6 has a non-obvious sub-step that blocks most first installations: "
                    "when the Scan Engine error banner appears, you must follow the sys_update_version "
                    "link to the Tables page, open the Application Access tab, select Can read and "
                    "update. Without that, scanning does not start.\n\n"
                    "Step 8 timing: a first full scan can legitimately take hours on a large instance. "
                    "Run it overnight in production and watch Scan Status rather than re-triggering it."))

S.append(dict(kind="table", title="8. Installation and activation — the sequence (2 of 2)",
              subtitle="Connection, registration, migration, then the value layer",
              table=[["#", "Step", "Navigation", "Role"],
                     ["9", "Register instances", "ALL → Impact → Configuration → Scan Engine Properties → My SN Instances → New", "sn_se.scan_engine_admin"],
                     ["10", "Configure authentication", "OAuth 2.0 preferred (production or development variant) or Basic authentication", "admin / Scan Engine Admin"],
                     ["11", "Validate connection", "My SN Instances → open record → Validate Connection → status 'Connection valid'", "sn_se.scan_engine_admin"],
                     ["12", "Automated registration", "All → Impact → Configuration → Guided Setup → Register your instance", "Impact App Admin + IDI admin"],
                     ["12b", "Manual registration (regulated / GCC)", "IDI → Activity Center → Instance registration → Add instance", "admin / any Impact role"],
                     ["13", "Verify data connection", "Guided Setup → Verify the Connection — success is Inbound + Outbound 'Active replication'", "Impact App Admin"],
                     ["14", "Initiate sync & migration", "All → Impact → Configuration → Guided Setup → Initiate sync & migration → Start Data Migration", "Impact App Admin / admin"],
                     ["15", "Enable value layer", "Objectives and outcomes; per-product data collection jobs (dc-*-install / activate / config); Instance Observer configuration", "Impact Admin / Platform Owner"]],
              after=["Validation warning: resolve the root cause before retrying a failed connection — repeated failures trigger the account lockout policy. Two flags must be cleared to recover: locked_out and password_needs_reset."],
              notes="Steps 9\u201315 are the connection and value-enablement half.\n\n"
                    "Step 9 has three data-quality requirements that cause most validation failures: the "
                    "instance name must match the instance_name system property exactly, the URL must be "
                    "exactly https://instancename.service-now.com with no www., no trailing slash and no "
                    "path, and only one instance in the stack may be designated Production.\n\n"
                    "Step 11 is where impatience is expensive. Every failed validation attempt "
                    "contributes to the account lockout policy. If validation fails, fix the root cause "
                    "first \u2014 do not retry blind. If the account does lock, remember that two flags must "
                    "be cleared, locked_out and password_needs_reset; clearing only one is insufficient.\n\n"
                    "Step 15 is the step people forget. Installing a data collection pack does not "
                    "collect data \u2014 the jobs must be enabled. And objectives and outcomes should be "
                    "agreed early, because Value Reports need at least two years of product data."))

S.append(dict(kind="bullets", title="9. The first 90 days — Foundations",
              subtitle="From activation to the first credible read-out",
              items=[(0, "Week 0 — kickoff and alignment: Impact Kickoff Meeting, success criteria agreed, named contacts confirmed, squad access approved."),
                     (0, "Weeks 1–2 — technical enablement: app installed, Guided Setup started, users and roles assigned, Platform Health users placed in groups, development teams created."),
                     (0, "Weeks 2–3 — baseline the platform: Scan Engine activated, first full scan run overnight, findings triaged, remediation backlog created."),
                     (0, "Weeks 2–4 — connect and migrate: instances registered, authentication configured, connection validated, registration completed, Active replication confirmed, data migration run."),
                     (0, "Weeks 3–6 — agree the value story: objectives and outcomes agreed with baselines and targets; data collection jobs enabled per product."),
                     (0, "Weeks 4–8 — plan the work: Capability Map reviewed, Product Adoption Roadmap published, recommendations converted into governed work items."),
                     (0, "Weeks 6–10 — extend observability: Instance Observer enabled, thresholds tuned, webhook notifications routed, consent captured if in scope."),
                     (0, "Weeks 8–12 — first value read-out: Monthly Health Assessment reviewed, outcome trends analysed, learning credits allocated."),
                     (0, "Exit criteria: connection verified, full scan complete with owned findings, outcomes with baselines, published roadmap, calendarised reviews.")],
              notes="Foundations is roughly the first 90\u2013120 days and its job is to get the loop running "
                    "end to end and produce a first credible read-out.\n\n"
                    "Two things to emphasise. First, the ordering is deliberate: connection and scans "
                    "before value reporting, because the value layer needs data to accumulate. Second, "
                    "the milestone that matters most is at week 12 \u2014 not \u201ceverything installed\u201d but "
                    "\u201cfindings owned, outcomes baselined, roadmap published, reviews in diaries\u201d.\n\n"
                    "The most commonly skipped item is the last exit criterion: calendarising the "
                    "reviews. Programs that do not calendarise the cadence quietly stop using the "
                    "product within two quarters.\n\n"
                    "Useful framing for the sponsor: by day 90 we should be able to show the health "
                    "baseline and the first outcome trends, even though a full value report needs "
                    "considerably more data history."))

S.append(dict(kind="table", title="Steady state — the repeating cadence",
              subtitle="What happens monthly, quarterly and annually once Foundations is complete",
              table=[["Cadence", "Forum", "Inputs", "Outputs"],
                     ["Monthly", "Operational and health review (Platform Owner + CSM + team leads)", "New scan findings, health score movement, Observer alerts, remediation backlog", "Prioritised actions with owners and dates"],
                     ["Monthly", "Health assessment review", "Monthly Health Assessment output (reports typically ~2 weeks after the assessment)", "Accepted recommendations, next month's focus"],
                     ["Quarterly", "Outcome review (business stakeholders + CSM)", "Outcome Insights vs benchmark and goal, adoption status, roadmap progress", "Roadmap adjustments, new or retired outcomes, Accelerator re-planning"],
                     ["Quarterly", "Support and executive review", "Case trends P1–P4, Developer Support usage, Accelerator consumption, learning balance", "Value narrative update, investment decisions"],
                     ["Quarterly", "Governance hygiene", "Squad access (read-only, 30 days, revocable)", "Renewed or revoked access"],
                     ["Annually", "Value realisation", "Value Reports with assumptions, Consumption Report", "Renewal position, package right-sizing, next-year objectives"]],
              notes="Steady State is a repeating cadence, not a project phase \u2014 this slide is the "
                    "operating contract.\n\n"
                    "The two meetings that carry the most weight are the monthly operational and health "
                    "review (which keeps technical work moving) and the quarterly executive review "
                    "(which keeps sponsorship alive). If only one can be protected, protect the "
                    "quarterly executive review.\n\n"
                    "Note the practical detail on health assessment reporting: reports typically arrive "
                    "around two weeks after the assessment, so plan the review meeting accordingly "
                    "rather than expecting same-week output.\n\n"
                    "Also note what is explicitly not ServiceNow's responsibility: implementation and "
                    "management of the Monthly Health Assessment sits with us. Budget internal ownership "
                    "for it rather than assuming the squad runs it end to end."))

S.append(dict(kind="table", title="Verify before you commit",
              subtitle="Entitlement-dependent or documentation-inconsistent points to confirm first",
              table=[["Point to verify", "Why"],
                     ["Package deltas (Guided / Total / Integrated Success)", "Custom definition limits, Observer seats and look-back, alert counts, Accelerator concurrency and Developer Support seats all differ"],
                     ["P1 / P2 response targets by package", "Documented as 30/120 minutes (Guided) and 15/60 minutes (Total)"],
                     ["Proactive Code Check status", "Documented as deprecating from Impact Zurich 6.0.8 — confirm before multi-year planning"],
                     ["Group Views availability", "Documented as initially available to limited customers; requires squad enablement"],
                     ["On-demand Accelerators", "Documented as not available to Guided — confirm for our package"],
                     ["Restricted-environment availability", "Portions of Impact are unavailable in FedRAMP, NSC DOD IL5 and Australia IRAP-Protected environments, and for self-hosted users and MSPs (except internal use)"],
                     ["AI capabilities", "Now Assist / ServiceNow Otto skills require version, entitlement and activation (e.g. Now Assist for Impact 3.03+, Now Assist for Platform 11.01+)"],
                     ["Domain separation", "Not supported for Impact — a design constraint, not a configuration option"],
                     ["Value Reports", "Need at least two years of product data to be meaningful"]],
              notes="This is the integrity slide, and it is worth its place in the deck.\n\n"
                    "The single most common source of client disappointment in Impact programs is "
                    "assuming a capability is included when it is entitlement-dependent. Going through "
                    "this list openly \u2014 and committing to confirm each item against the contract \u2014 is "
                    "what prevents that.\n\n"
                    "Three items deserve specific mention. Domain separation is simply not supported, so "
                    "if our design assumes it, we need a different design. Restricted-environment "
                    "availability matters directly for Australian government and defence-adjacent "
                    "estates. And Value Reports need at least two years of data \u2014 that is an argument "
                    "for starting now, not a reason to defer.\n\n"
                    "The message to land: everything on this slide is a question we will answer in "
                    "writing before we commit to a plan."))

S.append(dict(kind="cards", title="Next steps", subtitle="What we are asking for",
              cards=[[("1 · Confirm entitlement",
                       "Verify the exact package, Add-ons and entitlement figures in writing with ServiceNow before committing to a plan.", GREEN),
                      ("2 · Name the people",
                       "Named contact administrator, Platform Owner, Impact App Admin and Scan Engine Admin.", BLUE),
                      ("3 · Approve access & consent",
                       "Squad access (read-only, 30 days, quarterly re-approval) and the consent decisions for monitoring.", GREEN)],
                     [("4 · Schedule the sequence",
                       "Procure → install → Guided Setup → scan (overnight) → register → validate → Active replication → migrate.", BLUE),
                      ("5 · Agree the value story",
                       "Objectives and outcomes with metrics, baselines and targets — before the first report is expected.", GREEN),
                      ("6 · Calendarise governance",
                       "Lock the monthly operational/health review and the quarterly outcome and executive reviews.", BLUE)]],
              notes="Close with a specific, ownable ask rather than a summary.\n\n"
                    "These six items map directly onto the prerequisites and activation sequence, and "
                    "each one has a named owner in the pre-implementation checklist (section 7.10 of the "
                    "written brief).\n\n"
                    "If the client can only commit to some of them, the two that matter most for "
                    "schedule are items 2 and 4: naming the contact administrator, and booking the "
                    "first scan's cutover window. Everything else can follow, but those two gate the "
                    "start.\n\n"
                    "Offer the written brief and the pre-implementation checklist as the take-away, and "
                    "propose the follow-up session as the entitlement confirmation rather than a general "
                    "review."))

S.append(dict(kind="bullets", title="Summary — the client message",
              subtitle="Five sentences to remember",
              items=[(0, "Impact is a subscription customer success product: a workspace in our instance, an expert workspace at ServiceNow, and named people — not another module."),
                     (0, "It answers four questions: is the instance healthy, is it performing, are we realising value, and what should we do next."),
                     (0, "Its evidence is artefacts we can show: health scores, findings, adoption roadmaps, and monetised value reports with visible assumptions."),
                     (0, "It coexists with Now Support rather than replacing it, and it does not remove the need for our own administration and governance."),
                     (0, "About half the value depends on foundational work we control — connection, roles, scans and data collection — so the sequence matters more than the licence.")],
              notes="This is the closing slide; keep it to the five sentences.\n\n"
                    "If the audience remembers nothing else: Impact is a measurement and expert-capacity "
                    "layer, its value is demonstrated through artefacts rather than assertions, and it "
                    "requires foundational work from us before it can deliver anything.\n\n"
                    "Invite the two questions that usually decide the next step: \u201cwhat exactly is in "
                    "our package?\u201d and \u201cwho owns the activation sequence internally?\u201d Both are "
                    "answered in the written brief."))

S.append(dict(kind="table", title="Appendix · Glossary",
              subtitle="Key Impact terms used in this briefing",
              table=[["Term", "Meaning"],
                     ["Impact Store Application", "The Impact application installed in your ServiceNow instance — the consumer-side UI (All → Impact)"],
                     ["Impact Delivery Instance (IDI)", "The ServiceNow-hosted provider instance where the Impact Squad works (impact.service-now.com)"],
                     ["Service Bridge", "The integration technology enabling secure bi-directional sync between your instance and the IDI"],
                     ["HealthScan", "The library of leading-practice checks the Scan Engine runs against your instance"],
                     ["Scan Engine", "The component that executes HealthScan definitions and produces findings in your instance"],
                     ["Finding", "A specific scan result — the unit of remediation work; findings are not sent to the IDI"],
                     ["Capability Map", "A per-instance view of entitled capabilities and their adoption status"],
                     ["Product Adoption Roadmap (PAR)", "A phased, published plan sequencing capabilities towards objectives"],
                     ["Outcome", "A measurable business result linked to an objective, with a success metric, baseline and goal"],
                     ["Value Report", "A monetised aggregation of outcome performance with visible assumptions"],
                     ["Accelerator / Initiative", "A fixed-scope expert-led engagement / a programme sequencing several Accelerators"],
                     ["Concurrency", "The number of Accelerators that may run at the same time under your package"],
                     ["Instance Observer", "Off-instance performance and availability monitoring (also written 'Instance Observatory')"],
                     ["ServiceNow Otto", "The Australia-release rebrand of Now Assist capabilities in this context"],
                     ["CIP", "Customer Impact Plan — Impact's planning construct with the squad"]],
              notes="Reference slide \u2014 do not present it line by line. It exists so the deck is "
                    "self-contained when it is circulated without a presenter.\n\n"
                    "If a question arises mid-session on terminology, this is the place to jump to. The "
                    "three terms most often confused are Impact Store Application (in our instance) "
                    "versus Impact Delivery Instance (ServiceNow-hosted), Accelerator versus Initiative, "
                    "and concurrency.\n\n"
                    "One terminology warning worth stating if \u201cSuccess Plans\u201d comes up: that name belongs "
                    "to ServiceNow's separate Customer Success Management product, not Impact. Inside "
                    "Impact the planning constructs are the Customer Impact Plan, Product Adoption "
                    "Roadmaps and objectives/outcomes."))

S.append(dict(kind="table", title="Appendix · Decision points and FAQs",
              subtitle="The questions that usually come up next",
              table=[["Question", "Short answer"],
                     ["Does Impact replace our support contract?", "No. Now Support continues to handle cases; Impact adds enhanced P1/P2 targets, Developer Support and proactive engagements."],
                     ["Will it fix our technical debt?", "It finds, prioritises and routes it, and can propose AI-assisted fixes. Remediation still consumes our delivery capacity."],
                     ["When will we see hard ROI?", "Value Reports need at least two years of product data, so outcomes must be baselined early to report later."],
                     ["Do we need to be on a particular release?", "Yokohama or Xanadu Patch 2 and above, with sn_entitlement 4.1.2+ — verify the live Store listing."],
                     ["Does our data leave the instance?", "Service Bridge, Cloud Storage, Licensing Engine and MIF move data. Impact Common, Content and Health do not; Scan Engine findings stay local."],
                     ["Can we use it with domain separation?", "No — domain separation is not supported for Impact."],
                     ["What about IRAP-Protected environments?", "Portions of Impact are documented as unavailable in restricted environments including Australia IRAP-Protected data centres — confirm the feature subset."],
                     ["How many Accelerators can run at once?", "Documented as 1 at a time for Guided and 7 concurrent for Total, plus Add-on concurrency — verify."],
                     ["Who runs the Monthly Health Assessment?", "ServiceNow delivers the assessment; ServiceNow is not responsible for implementing or managing it — that ownership is ours."],
                     ["What is the first thing to do?", "Name the contact administrator, confirm entitlement, then procure and install the Store Application."]],
              notes="Anticipated-question slide for the Q&A and for circulation.\n\n"
                    "The three questions that decide whether a program proceeds are usually the first "
                    "three: does it replace support, will it fix our debt, and when do we see ROI. Each "
                    "answer here is deliberately calibrated to under-promise rather than over-claim.\n\n"
                    "The data-egress question will come from security, and the domain-separation and "
                    "IRAP questions from architecture or risk. Having them answered in the deck saves a "
                    "follow-up session.\n\n"
                    "Anything not answered here is addressed in the written brief, which carries the "
                    "full source-topic list in Appendix E."))

def BL(item):
    """Normalise a bullet to (text, level); accepts (level, text) or a plain string."""
    if isinstance(item, tuple):
        a, b = item
        return (a, b) if isinstance(a, str) else (b, a)
    return (item, 0)


# ============================================================ measurement utils
_pil = {}


def _pil_font(bold, pt):
    key = (bold, round(pt, 1))
    if key not in _pil:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        _pil[key] = ImageFont.truetype(FONT_DIR + name, int(round(pt * 4)))
    return _pil[key]


def text_w_pt(text, bold, pt):
    return _pil_font(bold, pt).getlength(str(text)) / 4.0


def wrap_lines(text, bold, pt, width_in):
    limit = width_in * 72.0
    total = 0
    for para in str(text).split("\n"):
        words = para.split()
        if not words:
            total += 1
            continue
        cur, n = "", 1
        for w in words:
            t = (cur + " " + w).strip()
            if text_w_pt(t, bold, pt) <= limit:
                cur = t
            else:
                n += 1
                cur = w
        total += n
    return total


def para_h_in(text, bold, pt, width_in, space_after_pt=0.0):
    return wrap_lines(text, bold, pt, width_in) * pt * 1.26 / 72.0 + space_after_pt / 72.0


# ============================================================ PPTX renderer
def hexc(h):
    return RGBColor.from_string(h)


def build_pptx(path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    BLANK = prs.slide_layouts[6]

    def notes(slide, text):
        slide.notes_slide.notes_text_frame.text = text

    def header(s, title, subtitle):
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.95))
        bar.fill.solid(); bar.fill.fore_color.rgb = hexc(NAVY); bar.line.fill.background()
        tf = bar.text_frame
        tf.margin_left = Inches(0.5); tf.margin_top = Inches(0.1)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.text = title
        p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = hexc(WHITE)
        if subtitle:
            p2 = tf.add_paragraph(); p2.text = subtitle
            p2.font.size = Pt(12); p2.font.color.rgb = RGBColor(0xC9, 0xD6, 0xE2)
        ftr = s.shapes.add_textbox(Inches(0.5), Inches(7.02), Inches(12.3), Inches(0.35))
        fp = ftr.text_frame.paragraphs[0]; fp.text = FOOTER
        fp.font.size = Pt(9); fp.font.color.rgb = hexc(MID)

    def card(s, x, y, w, h, title, body, color=BLUE, tsize=13, bsize=11, dark_text=False):
        tw = w - 0.24
        while tsize > 6.0:
            need = (para_h_in(title, True, tsize, tw, 2)
                    + (para_h_in(body, False, bsize, tw) if body else 0) + 0.16)
            if need <= h:
                break
            tsize *= 0.94
            bsize *= 0.94
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                                 Inches(w), Inches(h))
        box.fill.solid(); box.fill.fore_color.rgb = hexc(color)
        box.line.fill.background()
        box.shadow.inherit = False
        tf = box.text_frame; tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.margin_left = Inches(0.1); tf.margin_right = Inches(0.1); tf.margin_top = Inches(0.06)
        fg = hexc(NAVY) if dark_text else hexc(WHITE)
        p = tf.paragraphs[0]; p.text = title; p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(tsize); p.font.bold = True; p.font.color.rgb = fg
        if body:
            p2 = tf.add_paragraph(); p2.text = body; p2.alignment = PP_ALIGN.CENTER
            p2.font.size = Pt(bsize); p2.font.color.rgb = fg

    def bullets_height(items, size, spacing):
        total = 0.0
        for item in items:
            txt, lvl = BL(item)
            total += para_h_in(txt, False, size - 2 * lvl, 12.1 - 0.24 - 0.3 * lvl, spacing)
        return total

    def draw_bullets(s, items, top, size=13, spacing=7):
        avail = 6.5 - top
        while size > 8.0 and bullets_height(items, size, spacing * size / 13.0) > avail:
            size -= 0.5
        spacing = spacing * size / 13.0
        tb = s.shapes.add_textbox(Inches(0.6), Inches(top), Inches(12.1), Inches(max(0.4, avail)))
        tf = tb.text_frame; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
        first = True
        for item in items:
            txt, lvl = BL(item)
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = txt; p.level = lvl
            p.font.size = Pt(size - 2 * lvl)
            p.font.color.rgb = hexc(NAVY) if lvl == 0 else hexc(MID)
            p.font.bold = (lvl == 0 and txt.endswith(":"))
            p.space_after = Pt(spacing)

    def table_widths(cols, weights):
        weights = weights or [1.0] * cols
        total = sum(weights)
        return [12.1 * w / total for w in weights]

    def table_fit(data, font, weights, avail_h):
        widths = table_widths(len(data[0]), weights)
        heights = []
        for r, row in enumerate(data):
            h = 0.0
            for c, val in enumerate(row):
                h = max(h, para_h_in(val, r == 0, font, widths[c] - 0.16) + 0.10)
            heights.append(h)
        return heights if sum(heights) <= avail_h else None

    def draw_table(s, data, top, font=10, weights=None):
        rows, cols = len(data), len(data[0])
        avail_h = max(1.0, 6.58 - top)
        heights = None
        while font > 6.0:
            heights = table_fit(data, font, weights, avail_h)
            if heights:
                break
            font -= 0.5
        if not heights:
            font, heights = 6.0, table_fit(data, 6.0, weights, 99.0)
        shp = s.shapes.add_table(rows, cols, Inches(0.6), Inches(top), Inches(12.1),
                                 Inches(sum(heights)))
        tbl = shp.table
        widths = table_widths(cols, weights)
        for c in range(cols):
            tbl.columns[c].width = Inches(widths[c])
        for r in range(rows):
            tbl.rows[r].height = Inches(heights[r])
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                cell = tbl.cell(r, c); cell.text = str(val)
                cell.margin_left = Inches(0.06); cell.margin_right = Inches(0.06)
                cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                for p in cell.text_frame.paragraphs:
                    p.font.size = Pt(font)
                    p.font.color.rgb = hexc(WHITE if r == 0 else NAVY)
                    if r == 0:
                        p.font.bold = True
                cell.fill.solid()
                cell.fill.fore_color.rgb = hexc(BLUE if r == 0 else (WHITE if r % 2 else "F2F4F7"))

    def build_diagram(s):
        for x, w, label, colour in [(0.35, 3.5, "1. Your estate", NAVY),
                                    (4.35, 2.2, "2. Sync layer", GREEN),
                                    (7.05, 4.2, "3. ServiceNow side", BLUE),
                                    (11.6, 1.4, "4. Outcomes", NAVY)]:
            card(s, x, 1.15, w, 0.5, label, "", colour, tsize=12)

        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(1.8),
                                 Inches(3.5), Inches(3.55))
        box.fill.solid(); box.fill.fore_color.rgb = hexc("F2F4F7")
        box.line.color.rgb = hexc(MID)
        tf = box.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.12)
        for i, t in enumerate(["ServiceNow instances (Prod / Test / Dev)",
                               "• Impact Store Application\n  (Common, Content, Health)",
                               "• Scan Engine + HealthScan\n  + real-time prevention",
                               "• Value data collection\n  (PA packs per product)",
                               "• Users & roles by persona",
                               "• Instance Observer\n  (off-instance telemetry)"]):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = t; p.font.size = Pt(9.5); p.font.bold = (i == 0)
            p.font.color.rgb = hexc(NAVY); p.space_after = Pt(4)

        ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.92), Inches(3.15), Inches(0.38), Inches(0.5))
        ar.fill.solid(); ar.fill.fore_color.rgb = hexc(GREEN); ar.line.fill.background()
        card(s, 4.35, 2.55, 2.2, 1.6, "Service Bridge",
             "Automated registration (preferred) or manual (regulated / GCC). Inbound + outbound payloads.",
             GREEN, tsize=12, bsize=9)
        ar2 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.62), Inches(3.15), Inches(0.38), Inches(0.5))
        ar2.fill.solid(); ar2.fill.fore_color.rgb = hexc(GREEN); ar2.line.fill.background()

        box2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.05), Inches(1.8),
                                  Inches(4.2), Inches(3.55))
        box2.fill.solid(); box2.fill.fore_color.rgb = hexc(LIGHT_GREEN)
        box2.line.color.rgb = hexc(GREEN)
        tf2 = box2.text_frame; tf2.word_wrap = True; tf2.margin_left = Inches(0.12)
        for i, t in enumerate(["Impact Delivery Instance (provider)",
                               "• Impact Squad (CSM, CSE, Platform Architect, SAM)",
                               "• Activity Center (conversations, tasks, files)",
                               "• Value management (objectives, outcomes, reports)",
                               "• Catalogues (Accelerators, PARs, capability maps)",
                               "• Training Insights & learning credits"]):
            p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
            p.text = t; p.font.size = Pt(9.5); p.font.bold = (i == 0)
            p.font.color.rgb = hexc(NAVY); p.space_after = Pt(5)

        for i, (label, col) in enumerate([("Adoption", BLUE), ("Platform health", GREEN),
                                          ("Performance", BLUE), ("Value realised", BLUE),
                                          ("Upgrade readiness", GREEN)]):
            card(s, 11.6, 1.8 + i * 0.71, 1.4, 0.6, label, "", col, tsize=9)

        loop = s.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(0.35), Inches(5.62),
                                  Inches(10.9), Inches(0.5))
        loop.fill.solid(); loop.fill.fore_color.rgb = hexc("D9E2EC"); loop.line.fill.background()
        p = loop.text_frame.paragraphs[0]
        p.text = ("Foundations → Steady State cadence: monthly operational & health reviews · "
                  "quarterly outcome, support and executive reviews")
        p.font.size = Pt(10); p.font.color.rgb = hexc(NAVY); p.alignment = PP_ALIGN.CENTER

        tb = s.shapes.add_textbox(Inches(0.35), Inches(6.28), Inches(12.6), Inches(0.6))
        p = tb.text_frame.paragraphs[0]
        p.text = ("Callouts: Scan Engine findings are NOT transmitted to IDI  ·  Feature availability "
                  "depends on package, add-ons, roles and plugins")
        p.font.size = Pt(10); p.font.color.rgb = hexc(MID)

    for i, spec in enumerate(S, start=1):
        s = prs.slides.add_slide(BLANK)
        kind = spec["kind"]
        if kind == "title":
            bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
            bg.fill.solid(); bg.fill.fore_color.rgb = hexc(NAVY); bg.line.fill.background()
            tb = s.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(11.5), Inches(3.2))
            tf = tb.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; p.text = spec["title"]
            p.font.size = Pt(54); p.font.bold = True; p.font.color.rgb = hexc(WHITE)
            p2 = tf.add_paragraph(); p2.text = spec["subtitle"]
            p2.font.size = Pt(20); p2.font.color.rgb = hexc(GREEN)
            for line in spec["strap"].split("\n"):
                p3 = tf.add_paragraph(); p3.text = line; p3.space_before = Pt(6)
                p3.font.size = Pt(13); p3.font.color.rgb = RGBColor(0xC9, 0xD6, 0xE2)
        else:
            header(s, spec["title"], spec.get("subtitle"))
            y = 1.15
            if spec.get("banner"):
                card(s, 0.6, y, 12.1, 1.0, spec["banner"][0], spec["banner"][1],
                     spec["banner"][2], tsize=16, bsize=12)
                y += 1.2
            if kind == "bullets":
                draw_bullets(s, spec["items"], y + 0.1,
                             size=max(11, min(14, 14 - max(0, len(spec["items"]) - 8))))
            elif kind == "table":
                data = spec["table"]
                cols = len(data[0])
                weights = [1.0, 1.3, 1.5, 1.5, 1.3] if cols == 5 else (
                    [0.28, 1.5, 3.2, 1.3] if data[0][0] == "#" else None)
                draw_table(s, data, y, font=10 if cols <= 3 else (9.5 if cols == 4 else 9),
                           weights=weights)
            elif kind == "cards":
                rows = spec["cards"]
                nrows = len(rows)
                top = y + 0.05
                h = min(2.7, (6.55 - top - 0.25 * (nrows - 1)) / nrows)
                for r, row in enumerate(rows):
                    n = len(row)
                    w = (12.1 - 0.25 * (n - 1)) / n
                    for c, (t, b, col) in enumerate(row):
                        card(s, 0.6 + c * (w + 0.25), top + r * (h + 0.25), w, h, t, b, col,
                             tsize=16 if n <= 3 else 13.5, bsize=12 if n <= 3 else 10.5)
            elif kind == "diagram":
                build_diagram(s)
            if spec.get("after"):
                off = 6.25 if kind in ("cards", "diagram") else 5.5
                tb = s.shapes.add_textbox(Inches(0.6), Inches(off), Inches(12.1), Inches(0.9))
                tf = tb.text_frame; tf.word_wrap = True
                for j, line in enumerate(spec["after"]):
                    p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
                    p.text = line; p.font.size = Pt(10.5); p.font.color.rgb = hexc(MID)
        if i > 1:
            tb = s.shapes.add_textbox(Inches(12.5), Inches(7.02), Inches(0.65), Inches(0.3))
            p = tb.text_frame.paragraphs[0]; p.text = str(i); p.alignment = PP_ALIGN.RIGHT
            p.font.size = Pt(9); p.font.color.rgb = hexc(MID)
        if spec.get("notes"):
            notes(s, spec["notes"])
    prs.save(path)
    return prs


# ============================================================ PDF renderer
def build_pdf(path):
    page_w, page_h = 960.0, 540.0
    margin = 40.0
    frame_bottom = 44.0
    pdfmetrics.registerFont(TTFont("DejaVu", FONT_DIR + "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
    regular, bold = "DejaVu", "DejaVu-Bold"
    c = rl_canvas.Canvas(path, pagesize=(page_w, page_h))
    c.setTitle("ServiceNow Impact — Executive Briefing (Australia release)")
    c.setAuthor("ServiceNow architecture & advisory team")
    state = {"page": 0, "slide": 0}

    def C(h):
        return HexColor("#" + h)

    def wrap(text, font, size, maxw):
        out = []
        for raw in str(text).split("\n"):
            words, cur = raw.split(), ""
            if not words:
                out.append("")
                continue
            for w in words:
                t = (cur + " " + w).strip()
                if pdfmetrics.stringWidth(t, font, size) <= maxw:
                    cur = t
                else:
                    if cur:
                        out.append(cur)
                    cur = w
            out.append(cur)
        return out or [""]

    def start_page(title, subtitle=None, cont=False, right_label=None, bookmark=None):
        if state["page"] > 0:
            c.showPage()
        state["page"] += 1
        c.setFillColor(C(NAVY)); c.rect(0, page_h - 68, page_w, 68, stroke=0, fill=1)
        c.setFillColor(C(WHITE)); c.setFont(bold, 21)
        c.drawString(margin, page_h - 40, title + ("  (continued)" if cont else ""))
        if subtitle and not cont:
            c.setFillColor(C("C9D6E2")); c.setFont(regular, 10.5)
            c.drawString(margin, page_h - 58, subtitle[:160])
        c.setFillColor(C(MID)); c.setFont(regular, 7.5)
        c.drawString(margin, 20, FOOTER)
        c.drawRightString(page_w - margin, 20, right_label or ("Page %d" % state["page"]))
        c.setStrokeColor(C("D9E2EC")); c.setLineWidth(0.5)
        c.line(margin, 30, page_w - margin, 30)
        if bookmark and not cont:
            key = "sec_%d" % state["page"]
            c.bookmarkPage(key)
            c.addOutlineEntry(bookmark, key, level=0, closed=False)
        return page_h - 88

    def draw_bullets(items, y, size=11.5, scale=1.0, dry=False):
        for item in items:
            txt, lvl = BL(item)
            fsize = (size - 1.2 * lvl) * scale
            lead = fsize * 1.35
            gap = 5.0 * scale
            indent = margin + 14 + lvl * 16
            lines = wrap(txt, regular, fsize, page_w - indent - margin - 8)
            need = len(lines) * lead + gap
            if dry:
                y -= need
                continue
            if y - need < 46:
                y = start_page(state["title"], cont=True,
                               right_label="Slide %d of %d (cont.)" % (state["slide"], len(S)))
            c.setFillColor(C(GREEN) if lvl == 0 else C(MID)); c.setFont(bold, fsize)
            c.drawString(indent - 12, y - fsize, "•" if lvl == 0 else "–")
            c.setFillColor(C(NAVY) if lvl == 0 else C(MID)); c.setFont(regular, fsize)
            for ln in lines:
                c.drawString(indent, y - fsize, ln); y -= lead
            y -= gap
        return y

    def draw_table(data, y, weights=None, scale=1.0, dry=False):
        rows, cols = len(data), len(data[0])
        fsize = (8.6 if cols <= 3 else (8.0 if cols == 4 else 7.3)) * scale
        avail = page_w - 2 * margin
        weights = weights or [1] * cols
        total_w = sum(weights)
        widths = [avail * w / total_w for w in weights]
        pad = 4.0 * scale
        line_h = fsize * 1.28
        for r, row in enumerate(data):
            font = bold if r == 0 else regular
            cell_lines = [wrap(str(row[c]), font, fsize, widths[c] - 2 * pad) for c in range(cols)]
            row_h = max(len(l) for l in cell_lines) * line_h + 2 * pad
            if dry:
                y -= row_h
                continue
            if y - row_h < 46:
                y = start_page(state["title"], cont=True,
                               right_label="Slide %d of %d (cont.)" % (state["slide"], len(S)))
                if r != 0:
                    hl = [wrap(str(data[0][c]), bold, fsize, widths[c] - 2 * pad) for c in range(cols)]
                    hh = max(len(l) for l in hl) * line_h + 2 * pad
                    c.setFillColor(C(BLUE)); c.rect(margin, y - hh, avail, hh, stroke=0, fill=1)
                    c.setFillColor(C(WHITE)); c.setFont(bold, fsize)
                    yy = y - pad - fsize
                    for ci, lines in enumerate(hl):
                        for ln in lines:
                            c.drawString(margin + sum(widths[:ci]) + pad, yy, ln)
                            yy -= line_h
                    y -= hh
            c.setFillColor(C(BLUE) if r == 0 else (C(GREY) if r % 2 == 0 else C(WHITE)))
            c.rect(margin, y - row_h, avail, row_h, stroke=0, fill=1)
            c.setStrokeColor(C("B6C4D2")); c.setLineWidth(0.4)
            c.rect(margin, y - row_h, avail, row_h, stroke=1, fill=0)
            c.setFillColor(C(WHITE) if r == 0 else C(NAVY)); c.setFont(font, fsize)
            x = margin
            for ci, lines in enumerate(cell_lines):
                yy = y - pad - fsize
                for ln in lines:
                    c.drawString(x + pad, yy, ln); yy -= line_h
                if ci:
                    c.setStrokeColor(C("B6C4D2")); c.line(x, y - row_h, x, y)
                x += widths[ci]
            y -= row_h
        return y - 8 * scale

    def draw_cards(rows, y, scale=1.0, dry=False):
        avail = page_w - 2 * margin
        gap = 14.0 * scale
        v_pad = 16.0 * scale
        for row in rows:
            n = len(row)
            w = (avail - gap * (n - 1)) / n
            tf = (13.0 if n <= 3 else 11.0) * scale
            bf = (10.0 if n <= 3 else 8.8) * scale
            heights = []
            for t, b, _c in row:
                lt = wrap(t, bold, tf, w - 16 * scale)
                lb = wrap(b, regular, bf, w - 16 * scale)
                heights.append(len(lt) * tf * 1.25 + 5 * scale + len(lb) * bf * 1.3 + v_pad)
            h = max(heights)
            if dry:
                y -= (h + gap)
                continue
            for ci, (t, b, col) in enumerate(row):
                x = margin + ci * (w + gap)
                c.setFillColor(C(col)); c.roundRect(x, y - h, w, h, 8, stroke=0, fill=1)
                lines_t = wrap(t, bold, tf, w - 16 * scale)
                lines_b = wrap(b, regular, bf, w - 16 * scale)
                total = len(lines_t) * tf * 1.25 + 5 * scale + len(lines_b) * bf * 1.3
                yy = y - max(v_pad / 2.0, (h - total) / 2.0) - tf
                c.setFillColor(C(WHITE)); c.setFont(bold, tf)
                for ln in lines_t:
                    c.drawCentredString(x + w / 2, yy, ln); yy -= tf * 1.25
                yy -= 5 * scale
                c.setFont(regular, bf)
                for ln in lines_b:
                    c.drawCentredString(x + w / 2, yy, ln); yy -= bf * 1.3
            y -= (h + gap)
        return y

    def draw_diagram(y, avail=None, dry=False):
        cols = [(margin, 239.0, "1. Your estate", NAVY),
                (margin + 252, 180.0, "2. Sync layer", GREEN),
                (margin + 445, 281.0, "3. ServiceNow side", BLUE),
                (margin + 739, 137.0, "4. Outcomes", NAVY)]
        c1 = ["• Impact Store Application", "   (Common, Content, Health)", "• Scan Engine + HealthScan",
              "   + real-time prevention", "• Value data collection (PA packs)", "• Users & roles by persona",
              "• Instance Observer telemetry"]
        c2 = ["Automated registration", "(preferred) or manual", "(regulated / GCC).",
              "Inbound + outbound payloads.", "Status: Active replication."]
        c3 = ["• Impact Squad (CSM, CSE,", "   Platform Architect, SAM)", "• Activity Center: conversations,",
              "   tasks, files, calendar", "• Value management (objectives,", "   outcomes, value reports)",
              "• Catalogues: Accelerators, PARs,", "   Capability Maps, Training"]
        outcomes = ["Adoption", "Platform health", "Performance", "Value realised", "Upgrade readiness"]

        scale = 0.9
        for cand in [1.0 + 0.05 * k for k in range(9, -1, -1)]:
            bs = 8.2 * cand
            ok = True
            for lines, w in ((c1, cols[0][1]), (c2, cols[1][1]), (c3, cols[2][1])):
                for ln in lines:
                    if pdfmetrics.stringWidth(ln, regular, bs) + 16 * cand > w - 4:
                        ok = False
            for t, w in (("ServiceNow instances (Prod / Test / Dev)", cols[0][1]),
                         ("Service Bridge", cols[1][1]),
                         ("Impact Delivery Instance (provider)", cols[2][1])):
                if pdfmetrics.stringWidth(t, bold, 10.0 * cand) > w - 18:
                    ok = False
            for o in outcomes:
                if pdfmetrics.stringWidth(o, bold, 8.5 * cand) + 16 * cand > cols[3][1]:
                    ok = False
            if ok:
                scale = cand
                break
        ts, bs = 10.0 * scale, 8.2 * scale
        head_h, gap1, bar_h, gap2, callout_h = 24.0, 12.0, 26.0, 16.0, 12.0
        fixed = head_h + gap1 + gap2 + bar_h + gap2 + callout_h
        max_lines = max(len(c1), len(c2), len(c3))
        natural_lead = 11.0 * scale
        box_h = max(30.0 * scale + (max_lines - 1) * natural_lead + 18.0,
                    (avail - fixed) if avail else 0.0)
        lead = natural_lead
        if avail:
            lead = min(2.1 * bs, max(natural_lead,
                                     (box_h - 30.0 * scale - 14.0) / max(1, max_lines - 1)))
        if dry:
            return y - (fixed + box_h)

        for x, w, label, col in cols:
            c.setFillColor(C(col)); c.roundRect(x, y - head_h, w, head_h, 4, stroke=0, fill=1)
            c.setFillColor(C(WHITE)); c.setFont(bold, ts)
            c.drawString(x + 7, y - 16.5, label)
        top = y - head_h - gap1

        def box(x, w, colour, title, body_lines, border=None):
            c.setFillColor(C(colour))
            c.roundRect(x, top - box_h, w, box_h, 6, stroke=1 if border else 0, fill=1)
            if border:
                c.setStrokeColor(C(border)); c.roundRect(x, top - box_h, w, box_h, 6, stroke=1, fill=0)
            title_lines = wrap(title, bold, ts, w - 20)
            block = len(title_lines) * ts * 1.3 + 6 + len(body_lines) * lead
            yy = top - max(12.0, (box_h - block) / 2.0) - 12.0 * scale
            c.setFillColor(C(NAVY)); c.setFont(bold, ts)
            for tl in title_lines:
                c.drawString(x + 9, yy, tl); yy -= ts * 1.3
            yy -= 6
            c.setFont(regular, bs)
            for ln in body_lines:
                c.drawString(x + 9, yy, ln); yy -= lead

        box(cols[0][0], cols[0][1], "F2F4F7", "ServiceNow instances (Prod / Test / Dev)", c1, border=MID)
        mid = top - box_h / 2.0
        c.setStrokeColor(C(GREEN)); c.setLineWidth(3)
        c.line(cols[0][0] + cols[0][1] + 3, mid, cols[1][0] - 3, mid)
        c.setFillColor(C(GREEN)); c.setFont(bold, 12 * scale)
        c.drawString(cols[1][0] - 16, mid + 4, "→")
        c.line(cols[1][0] + cols[1][1] + 3, mid, cols[2][0] - 3, mid)
        c.drawString(cols[2][0] - 16, mid + 4, "→")
        bh = min(box_h - 30.0, 30.0 * scale + (len(c2) - 1) * lead + 18.0)
        by0 = top - box_h / 2.0 - bh / 2.0
        c.setFillColor(C(LIGHT_GREEN)); c.roundRect(cols[1][0], by0, cols[1][1], bh, 6, stroke=1, fill=1)
        c.setStrokeColor(C(GREEN)); c.roundRect(cols[1][0], by0, cols[1][1], bh, 6, stroke=1, fill=0)
        c.setFillColor(C(NAVY)); c.setFont(bold, ts)
        c.drawString(cols[1][0] + 9, by0 + bh - 20, "Service Bridge")
        c.setFont(regular, bs)
        yy = by0 + bh - 20 - max(14.0, lead)
        for ln in c2:
            c.drawString(cols[1][0] + 9, yy, ln); yy -= lead
        box(cols[2][0], cols[2][1], LIGHT_GREEN, "Impact Delivery Instance (provider)", c3, border=GREEN)

        pill_h = min(30.0, (box_h - 4 * 6.0) / 5.0)
        pitch = (box_h - pill_h) / 4.0
        for i, o in enumerate(outcomes):
            py = top - pill_h - i * pitch
            c.setFillColor(C(BLUE if i % 2 == 0 else GREEN))
            c.roundRect(cols[3][0], py, cols[3][1], pill_h, 5, stroke=0, fill=1)
            c.setFillColor(C(WHITE)); c.setFont(bold, 9.0 * scale)
            c.drawCentredString(cols[3][0] + cols[3][1] / 2, py + pill_h / 2 - 3.2 * scale, o)

        y = top - box_h - gap2
        c.setFillColor(C("D9E2EC")); c.roundRect(margin, y - bar_h, page_w - 2 * margin, bar_h, 4, stroke=0, fill=1)
        c.setFillColor(C(NAVY)); c.setFont(regular, 9.0 * scale)
        c.drawCentredString(page_w / 2, y - bar_h + 8.5 * scale,
                            "Foundations → Steady State cadence: monthly operational & health reviews · "
                            "quarterly outcome, support and executive reviews")
        y -= bar_h + gap2
        c.setFillColor(C(MID)); c.setFont(regular, 8.4 * scale)
        c.drawCentredString(page_w / 2, y - 2,
                            "Callouts: Scan Engine findings are NOT transmitted to IDI  ·  "
                            "Feature availability depends on package, add-ons, roles and plugins")
        return y - callout_h

    for i, spec in enumerate(S, start=1):
        state["slide"] = i
        state["title"] = spec["title"]
        if spec["kind"] == "title":
            if state["page"] > 0:
                c.showPage()
            state["page"] += 1
            c.setFillColor(C(NAVY)); c.rect(0, 0, page_w, page_h, stroke=0, fill=1)
            c.setFillColor(C(WHITE)); c.setFont(bold, 42)
            c.drawString(64, page_h - 240, spec["title"])
            c.setFillColor(C(GREEN)); c.setFont(regular, 16)
            c.drawString(64, page_h - 275, spec["subtitle"])
            c.setFillColor(C("C9D6E2")); c.setFont(regular, 11.5)
            yy = page_h - 310
            for line in spec["strap"].split("\n"):
                c.drawString(64, yy, line); yy -= 17
            c.setFillColor(C(MID)); c.setFont(regular, 7.5)
            c.drawRightString(page_w - 40, 20, "Slide 1 of %d" % len(S))
            continue
        y = start_page(spec["title"], spec.get("subtitle"),
                       right_label="Slide %d of %d" % (i, len(S)),
                       bookmark="%d. %s" % (i, spec["title"]))
        body_top = y
        if spec.get("banner") and spec["kind"] != "cards":
            c.setFillColor(C(spec["banner"][2]))
            c.roundRect(margin, y - 56, page_w - 2 * margin, 56, 8, stroke=0, fill=1)
            c.setFillColor(C(WHITE)); c.setFont(bold, 14.5)
            c.drawCentredString(page_w / 2, y - 24, spec["banner"][0])
            c.setFont(regular, 10.5)
            c.drawCentredString(page_w / 2, y - 42, spec["banner"][1])
            body_top -= 70
        weights = None
        if spec["kind"] == "table":
            if len(spec["table"][0]) == 5:
                weights = [1.0, 1.3, 1.5, 1.5, 1.3]
            elif spec["table"][0][0] == "#":
                weights = [0.28, 1.5, 3.2, 1.3]

        def render_body(sc, dry):
            yy = body_top
            if spec["kind"] == "bullets":
                size = max(9.5, min(11.5, 11.5 - max(0, len(spec["items"]) - 8) * 0.25))
                yy = draw_bullets(spec["items"], yy - 8 * sc, size=size, scale=sc, dry=dry)
            elif spec["kind"] == "table":
                yy = draw_table(spec["table"], yy - 8 * sc, weights=weights, scale=sc, dry=dry)
            elif spec["kind"] == "cards":
                yy = draw_cards(spec["cards"], yy - 8 * sc, scale=sc, dry=dry)
            elif spec["kind"] == "diagram":
                yy = draw_diagram(yy - 6 * sc, avail=(body_top - 6 * sc - frame_bottom), dry=dry)
            if spec.get("after"):
                yy = draw_bullets([(a, 0) for a in spec["after"]], yy - 4 * sc, size=9.5,
                                  scale=sc, dry=dry)
            return yy

        if spec["kind"] == "diagram":
            render_body(1.0, dry=False)
        else:
            scale = 1.0
            for cand in [1.0 + 0.05 * k for k in range(15, -1, -1)]:
                if body_top - render_body(cand, dry=True) <= body_top - frame_bottom:
                    scale = cand
                    break
            render_body(scale, dry=False)

    for i, spec in enumerate(S, start=1):
        if not spec.get("notes"):
            continue
        y = start_page("Speaker notes — Slide %d: %s" % (i, spec["title"]),
                       right_label="Speaker notes", bookmark="Notes — Slide %d" % i)
        for para in spec["notes"].split("\n\n"):
            lines = wrap(" ".join(para.split()), regular, 10.5, page_w - 2 * margin)
            need = len(lines) * 14 + 8
            if y - need < 46:
                y = start_page("Speaker notes — Slide %d: %s" % (i, spec["title"]), cont=True,
                               right_label="Speaker notes")
            c.setFillColor(C(NAVY)); c.setFont(regular, 10.5)
            for ln in lines:
                c.drawString(margin, y - 12, ln); y -= 14
            y -= 8
    c.showPage()
    c.save()


# ============================================================ HTML renderer
def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_html(path):
    slides_html = []
    notes_html = []
    for i, spec in enumerate(S, start=1):
        kind = spec["kind"]
        inner = ""
        if kind == "title":
            inner = ('<div class="t-title">%s</div><div class="t-sub">%s</div>'
                     '<div class="t-strap">%s</div>' % (
                         esc(spec["title"]), esc(spec["subtitle"]),
                         "<br>".join(esc(x) for x in spec["strap"].split("\n"))))
            slides_html.append('<section class="slide slide-title" id="s%d">%s</section>' % (i, inner))
        else:
            head = '<div class="slide-head"><h2>%s</h2>%s</div>' % (
                esc(spec["title"]),
                '<p class="slide-sub">%s</p>' % esc(spec["subtitle"]) if spec.get("subtitle") else "")
            body = ""
            if spec.get("banner") and kind != "cards":
                body += ('<div class="banner %s"><b>%s</b><span>%s</span></div>'
                         % (spec["banner"][2].lower(), esc(spec["banner"][0]),
                            esc(spec["banner"][1])))
            if kind == "bullets":
                items = ""
                for item in spec["items"]:
                    txt, lvl = BL(item)
                    items += '<li class="lvl%d">%s</li>' % (lvl, esc(txt))
                body += '<ul class="blist">%s</ul>' % items
            elif kind == "table":
                rows = spec["table"]
                thead = "".join("<th>%s</th>" % esc(x) for x in rows[0])
                tbody = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % esc(x) for x in r)
                                 for r in rows[1:])
                body += '<table class="dtable"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (thead, tbody)
            elif kind == "cards":
                rows_html = ""
                for row in spec["cards"]:
                    cells = "".join(
                        '<div class="card %s"><div class="card-t">%s</div>'
                        '<div class="card-b">%s</div></div>' % (col.lower(), esc(t), esc(b))
                        for (t, b, col) in row)
                    rows_html += '<div class="card-row" style="--n:%d">%s</div>' % (len(row), cells)
                body += rows_html
            elif kind == "diagram":
                cols = [("1. Your estate", "navy", ["Impact Store Application (Common, Content, Health)",
                                                    "Scan Engine + HealthScan + real-time prevention",
                                                    "Value data collection (PA packs)",
                                                    "Users &amp; roles by persona",
                                                    "Instance Observer telemetry"]),
                        ("2. Sync layer", "green", ["Service Bridge",
                                                    "Automated registration (preferred) or manual (regulated / GCC)",
                                                    "Inbound + outbound payloads; status: Active replication"]),
                        ("3. ServiceNow side", "blue", ["Impact Delivery Instance (provider)",
                                                        "Impact Squad — CSM, CSE, Platform Architect, SAM",
                                                        "Activity Center: conversations, tasks, files",
                                                        "Value management: objectives, outcomes, reports",
                                                        "Catalogues: Accelerators, PARs, Capability Maps"]),
                        ("4. Outcomes", "navy", ["Adoption", "Platform health", "Performance",
                                                 "Value realised", "Upgrade readiness"])]
                cells = ""
                for title, tone, bullets in cols:
                    lis = "".join("<li>%s</li>" % b for b in bullets)
                    cells += ('<div class="diag-col"><div class="diag-head %s">%s</div>'
                              '<ul class="diag-body">%s</ul></div>' % (tone, title, lis))
                body += ('<div class="diagram"><div class="diag-row">%s</div>'
                         '<div class="diag-loop">Foundations → Steady State cadence: monthly operational '
                         '&amp; health reviews · quarterly outcome, support and executive reviews</div>'
                         '<div class="diag-note">Callouts: Scan Engine findings are NOT transmitted to IDI · '
                         'Feature availability depends on package, add-ons, roles and plugins</div></div>' % cells)
            if spec.get("after"):
                body += "".join('<p class="after">%s</p>' % esc(a) for a in spec["after"])
            slides_html.append('<section class="slide" id="s%d">%s<div class="slide-body">%s</div>'
                               '<div class="slide-num">Slide %d of %d</div></section>'
                               % (i, head, body, i, len(S)))
        if spec.get("notes"):
            notes_html.append(
                '<section class="note" id="n%d"><h3>Slide %d — %s</h3>%s</section>'
                % (i, i, esc(spec["title"]),
                   "".join("<p>%s</p>" % esc(p.strip()) for p in spec["notes"].split("\n\n") if p.strip())))

    toc = "".join('<a href="#s%d"><span>%02d</span>%s</a>' % (i, i, esc(s["title"]))
                  for i, s in enumerate(S, start=1))
    tpl = DECK_HTML.replace("{{", "{").replace("}}", "}")
    page = (tpl.replace("__SLIDES__", "\n".join(slides_html))
               .replace("__NOTES__", "\n".join(notes_html))
               .replace("__TOC__", toc).replace("__N__", str(len(S))))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)


DECK_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ServiceNow Impact — Executive Briefing (Australia release)</title>
<style>
:root { --navy:#03213f; --blue:#1f4e79; --green:#03754d; --light:#e6f4ee; --grey:#f2f4f7;
  --mid:#5c6b7a; --rule:#d9e2ec; }
* { box-sizing:border-box; }
body { margin:0; background:#0d1b2a; font-family:"Segoe UI",Roboto,-apple-system,Arial,sans-serif;
  color:var(--navy); }
.top { position:sticky; top:0; z-index:20; background:#08192b; color:#fff; display:flex;
  align-items:center; gap:12px; padding:9px 16px; border-bottom:1px solid #1d3550; }
.top .brand { font-weight:700; font-size:.9rem; }
.top .brand small { display:block; font-weight:400; color:#8fa6bd; font-size:.72rem; }
.top .spacer { flex:1; }
.top button, .top a.btn { background:#12314f; color:#cfe0f0; border:1px solid #1d3550; border-radius:5px;
  padding:6px 11px; font-size:.78rem; cursor:pointer; text-decoration:none; }
.top button:hover, .top a.btn:hover { background:#1b4a74; color:#fff; }
.counter { font-size:.78rem; color:#8fa6bd; min-width:88px; text-align:right; }
.stage { display:grid; grid-template-columns:260px 1fr; gap:0; min-height:calc(100vh - 46px); }
aside { background:#0b2136; color:#cfe0f0; overflow-y:auto; padding:14px 10px 60px; }
aside h4 { color:#7fd8b0; font-size:.7rem; letter-spacing:.13em; text-transform:uppercase;
  margin:0 0 10px 6px; }
aside a { display:flex; gap:8px; color:#cfe0f0; text-decoration:none; font-size:.8rem;
  padding:6px 8px; border-radius:5px; }
aside a span { color:#5d7d9c; font-variant-numeric:tabular-nums; }
aside a:hover { background:#12314f; color:#fff; }
aside a.active { background:var(--green); color:#fff; }
aside a.active span { color:#cbeee0; }
main { padding:26px 30px 90px; overflow-x:hidden; }
.slide { display:none; background:#fff; border-radius:10px; max-width:1180px; margin:0 auto;
  padding:28px 34px 44px; position:relative; box-shadow:0 10px 40px rgba(0,0,0,.35); min-height:60vh; }
.slide.active { display:block; }
.slide-head h2 { font-size:1.6rem; margin:0 0 4px; color:var(--navy); }
.slide-sub { color:var(--mid); margin:0 0 16px; font-size:.92rem; }
.slide-title { background:var(--navy); color:#fff; display:none; }
.slide-title.active { display:block; }
.t-title { font-size:3rem; font-weight:800; margin:70px 0 10px; }
.t-sub { color:#7fd8b0; font-size:1.2rem; font-weight:600; }
.t-strap { color:#c9d6e2; margin-top:26px; line-height:1.7; }
.banner { background:var(--green); color:#fff; border-radius:8px; padding:12px 16px;
  margin:0 0 18px; display:flex; flex-direction:column; gap:2px; }
.banner.b { background:var(--blue); }
.banner.naval { background:var(--navy); }
.banner.navy { background:var(--navy); }
.blist { list-style:none; padding:0; margin:0; }
.blist li { position:relative; padding:6px 0 6px 26px; font-size:.94rem; line-height:1.5; }
.blist li:before { content:"•"; position:absolute; left:6px; color:var(--green); font-weight:700; }
.blist li.lvl1 { margin-left:26px; font-size:.9rem; color:#41546a; }
.blist li.lvl1:before { content:"–"; color:var(--mid); }
table.dtable { width:100%; border-collapse:collapse; font-size:.82rem; }
table.dtable th { background:var(--blue); color:#fff; text-align:left; padding:8px 10px;
  border:1px solid #b6c4d2; }
table.dtable td { padding:8px 10px; border:1px solid #b6c4d2; vertical-align:top; color:#22364a; }
table.dtable tbody tr:nth-child(even) td { background:var(--grey); }
.card-row { display:grid; grid-template-columns:repeat(var(--n),1fr); gap:16px; margin-bottom:16px; }
.card { border-radius:8px; padding:16px 18px; color:#fff; }
.card.blue { background:var(--blue); } .card.green { background:var(--green); }
.card.navy { background:var(--navy); }
.card-t { font-weight:700; margin-bottom:6px; font-size:1rem; }
.card-b { font-size:.86rem; line-height:1.5; opacity:.95; }
.after { color:var(--mid); font-size:.85rem; margin:12px 0 0; }
.slide-num { position:absolute; right:18px; bottom:12px; color:var(--mid); font-size:.75rem; }
.diagram { margin-top:6px; }
.diag-row { display:grid; grid-template-columns:1.5fr 1fr 1.45fr 1fr; gap:12px; }
.diag-col { display:flex; flex-direction:column; }
.diag-head { color:#fff; font-weight:700; font-size:.82rem; padding:8px 10px; border-radius:6px 6px 0 0; }
.diag-head.navy { background:var(--navy); } .diag-head.green { background:var(--green); }
.diag-head.blue { background:var(--blue); }
.diag-body { margin:0; padding:10px 12px 12px 26px; background:var(--light); border:1px solid var(--rule);
  border-top:0; border-radius:0 0 6px 6px; font-size:.78rem; flex:1; }
.diag-loop { background:#d9e2ec; text-align:center; padding:9px; border-radius:5px; margin-top:12px;
  font-size:.82rem; }
.diag-note { text-align:center; color:var(--mid); font-size:.78rem; margin-top:9px; }
.notes-panel { display:none; background:#fff; border-radius:10px; max-width:1180px; margin:14px auto 0;
  padding:22px 28px; }
.notes-panel.on { display:block; }
.note h3 { font-size:1rem; color:var(--blue); margin:18px 0 6px; }
.note p { font-size:.9rem; line-height:1.6; margin:6px 0; }
.footer-nav { display:flex; justify-content:center; gap:12px; margin:18px auto 0; }
.footer-nav button { background:var(--green); color:#fff; border:0; border-radius:6px; padding:10px 20px;
  font-size:.9rem; font-weight:600; cursor:pointer; }
.footer-nav button:disabled { background:#3d5a72; cursor:default; }
.overview .slide { display:block !important; margin-bottom:18px; min-height:0; cursor:pointer; }
.overview .slide-body, .overview .diagram { display:none; }
.overview .slide-head h2 { font-size:1rem; }
@media (max-width:1000px) { .stage { grid-template-columns:1fr; } aside { display:none; }
  .diag-row, .card-row { grid-template-columns:1fr !important; } }
@media print {
  body { background:#fff; } .top, aside, .footer-nav { display:none !important; }
  .stage { display:block; } main { padding:0; }
  .slide { display:block !important; box-shadow:none; border-radius:0; page-break-after:always;
    min-height:0; max-width:none; padding:24px 26px; }
  .slide-title { background:var(--navy) !important; -webkit-print-color-adjust:exact;
    print-color-adjust:exact; }
  .note { page-break-after:always; }
  .notes-panel { display:block !important; padding:0; }
  @page { size:landscape; margin:12mm; }
}
</style>
</head>
<body>
<div class="top">
  <div class="brand">ServiceNow Impact — Executive Briefing<small>Australia release · __N__ slides with speaker notes</small></div>
  <div class="spacer"></div>
  <div class="counter" id="counter">Slide 1 / 28</div>
  <button onclick="toggleNotes()" id="notesBtn">Notes (N)</button>
  <button onclick="toggleOverview()" id="ovBtn">Overview (G)</button>
  <button onclick="window.print()">Print / PDF</button>
  <a class="btn" href="ServiceNow-Impact-Australia-Executive-Briefing.pptx" download>PPTX</a>
  <a class="btn" href="ServiceNow-Impact-Australia-Executive-Briefing.pdf" download>PDF</a>
  <a class="btn" href="index.html">All files</a>
</div>
<div class="stage">
  <aside><h4>Slides</h4>__TOC__</aside>
  <main id="main">
    __SLIDES__
    <div class="footer-nav">
      <button onclick="go(-1)" id="prev">← Previous</button>
      <button onclick="go(1)" id="next">Next →</button>
    </div>
    <div class="notes-panel" id="notesPanel">__NOTES__</div>
  </main>
</div>
<script>
var idx = 0, slides = [].slice.call(document.querySelectorAll('.slide')),
    links = [].slice.call(document.querySelectorAll('aside a')), ov = false;
function show(i) {{
  idx = Math.max(0, Math.min(slides.length - 1, i));
  slides.forEach(function (s, k) {{ s.classList.toggle('active', k === idx); }});
  links.forEach(function (a, k) {{ a.classList.toggle('active', k === idx); }});
  document.getElementById('counter').textContent = 'Slide ' + (idx + 1) + ' / ' + slides.length;
  document.getElementById('prev').disabled = idx === 0;
  document.getElementById('next').disabled = idx === slides.length - 1;
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
  if (location.hash !== '#s' + (idx + 1)) history.replaceState(null, '', '#s' + (idx + 1));
}}
function go(d) {{ show(idx + d); }}
function toggleNotes() {{
  var p = document.getElementById('notesPanel');
  p.classList.toggle('on');
  document.getElementById('notesBtn').textContent = p.classList.contains('on') ? 'Hide notes (N)' : 'Notes (N)';
  if (p.classList.contains('on')) p.scrollIntoView({{ behavior: 'smooth' }});
}}
function toggleOverview() {{
  ov = !ov;
  document.getElementById('main').classList.toggle('overview', ov);
  document.getElementById('ovBtn').textContent = ov ? 'Slide view (G)' : 'Overview (G)';
  if (ov) {{ slides.forEach(function (s) {{ s.classList.add('active'); }}); }}
  else show(idx);
}}
document.addEventListener('keydown', function (e) {{
  if (e.key === 'ArrowRight' || e.key === 'PageDown') go(1);
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') go(-1);
  else if (e.key.toLowerCase() === 'n') toggleNotes();
  else if (e.key.toLowerCase() === 'g') toggleOverview();
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(slides.length - 1);
}});
links.forEach(function (a, k) {{ a.addEventListener('click', function (e) {{ e.preventDefault(); show(k); }}); }});
slides.forEach(function (s, k) {{ s.addEventListener('click', function () {{ if (ov) {{ ov = false;
  document.getElementById('main').classList.remove('overview');
  document.getElementById('ovBtn').textContent = 'Overview (G)'; show(k); }} }}); }});
var start = parseInt((location.hash || '#s1').slice(2), 10) || 1;
show(start - 1);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build_pptx(PPTX_PATH)
    build_pdf(PDF_PATH)
    build_html(HTML_PATH)
    print("slides:", len(S))
    print("wrote:", PPTX_PATH)
    print("wrote:", PDF_PATH)
    print("wrote:", HTML_PATH)
