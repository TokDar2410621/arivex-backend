"""Seed the 6 blog posts that were mocked up in translations.ts.

Each article has an FR and EN version sharing the same translation_group UUID.
Run via `railway ssh` inside the container:
    /opt/venv/bin/python seed_mockup_articles.py
"""
import os
import uuid
from datetime import date

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.blog.models import BlogPost, Category, Tag


# ─── Categories ───────────────────────────────────────────────────────────

CATEGORIES = {
    "automatisation":   "Automatisation",
    "ia":               "Intelligence Artificielle",
    "developpement-web":"Développement Web",
    "entrepreneuriat":  "Entrepreneuriat",
    "pme-quebec":       "PME Québec",
}

cat_objs = {}
for slug, name in CATEGORIES.items():
    cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
    cat_objs[slug] = cat


# ─── Tags ─────────────────────────────────────────────────────────────────

def _tag(name):
    t, _ = Tag.objects.get_or_create(name=name)
    return t


# ─── Articles ─────────────────────────────────────────────────────────────

ARTICLES = [
    {
        "slug": "automatiser-pme-quebec-2026",
        "category_slug": "automatisation",
        "cover_image": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600&q=80",
        "reading_time": 7,
        "featured": True,
        "published_at": date(2026, 4, 15),
        "tags": ["Automatisation", "PME", "Québec"],
        "fr": {
            "title": "Les 5 processus que chaque PME québécoise devrait automatiser en 2026",
            "excerpt": "Prise de rendez-vous, facturation, relances clients — voici les tâches qui vous coûtent le plus de temps et comment les éliminer sans transformer votre équipe en experts en IT.",
            "content": """La plupart des PME québécoises perdent **entre 10 et 15 heures par semaine** sur des tâches répétitives qui n'ont rien à voir avec leur vrai métier. Pas parce que les dirigeants ne savent pas — parce qu'ils n'ont ni le temps, ni l'équipe pour s'y attaquer.

Voici les cinq processus qu'on voit revenir systématiquement en audit, avec pour chacun : le temps qu'il bouffe, la solution type et ce que ça coûte.

# 1. La prise de rendez-vous

Entre les courriels "vous avez une dispo jeudi ?", les rappels manuels et les oublis, une réceptionniste ou une adjointe peut passer *jusqu'à 6 heures par semaine* à orchestrer des calendriers.

La solution : un lien de réservation (Calendly, Cal.com, ou SimplyBook) branché directement sur le calendrier Google ou Outlook de l'équipe. Le client choisit son créneau, la confirmation part toute seule, les rappels SMS/email sont envoyés automatiquement 24h avant.

Coût : de 0 à 15 $/utilisateur/mois. Installation : une demi-journée.

# 2. La facturation et les relances

Facturer à la main, suivre les impayés dans un tableur, envoyer des rappels un par un : chaque heure passée là-dessus est une heure qu'on ne passe pas à vendre ou à livrer.

L'automatisation combine trois briques :

- Un outil de facturation connecté à votre banque et à Revenu Québec (QuickBooks, Acomba, ou Sage)
- Un déclencheur qui envoie la facture dès que le projet est marqué "livré" dans votre CRM
- Une séquence de relances automatiques à J+7, J+14 et J+30

Gain typique : 4 à 6 heures par semaine, et surtout **une baisse des délais de paiement de 20 à 40 %**.

# 3. Les relances clients (prospects et existants)

Un lead rentre par votre formulaire de contact. Vous répondez le lendemain. Le prospect a déjà parlé à trois concurrents. Vous perdez la vente que vous auriez dû gagner.

La solution : une séquence d'accueil automatisée. Dès qu'un lead arrive, un email de confirmation part dans la minute, puis une série de 2-3 messages étalés sur 10 jours (valeur, preuve sociale, CTA). Pour les clients existants, une cadence similaire : check-in trimestriel, upsell, demande d'avis.

Stack : un CRM simple (HubSpot gratuit, Airtable ou Pipedrive) + Make ou n8n pour les déclencheurs.

# 4. L'onboarding des nouveaux clients

Signer un contrat, envoyer les documents d'accès, planifier la réunion de kickoff, créer l'espace projet, envoyer la facture d'acompte : *7 à 10 étapes manuelles* que tout le monde oublie à mi-chemin.

Un flux d'onboarding automatisé fait tout ça en série dès qu'un contrat est signé dans DocuSign ou Dropbox Sign. Le client reçoit un email structuré avec ses accès, son calendrier, sa facture. Votre équipe reçoit une notification Slack avec le brief. Zéro étape oubliée.

# 5. Les rapports hebdomadaires

Compiler manuellement les ventes de la semaine, les tickets support ouverts et les KPI pour le meeting du lundi : 2-3 heures chaque semaine pour une info qui devrait être sous les yeux en temps réel.

Un dashboard automatisé (Looker Studio, Metabase, ou même un Google Sheet bien branché) extrait les chiffres des sources (Stripe, HubSpot, Zendesk) et les met à jour automatiquement. Vous arrivez au meeting, tout est déjà là.

# Combien ça coûte vraiment

Pour une PME de 5 à 20 employés, un projet d'automatisation complet sur ces 5 axes se chiffre entre **2 000 $ et 6 000 $ en one-shot**, plus 50 à 200 $ par mois d'abonnements outils.

Le ROI typique se mesure en semaines, pas en années. 12 heures économisées par semaine × 40 $/heure × 50 semaines = **24 000 $ par an** de temps récupéré — sans compter les clients gagnés grâce aux relances qui partent enfin à l'heure.

# FAQ

**Est-ce qu'il faut une équipe tech pour maintenir tout ça ?**
Non. Les outils comme Make ou n8n sont conçus pour être maintenus par quelqu'un qui n'est pas développeur. Une fois les flux en place, ils tournent seuls pendant des mois.

**Et si un outil change ses tarifs ou son API ?**
C'est un vrai risque — d'où l'intérêt de choisir des outils matures et de documenter chaque flux. Chez Arivex on livre une doc minimale pour chaque automatisation.

**Par où commencer si on a peu de budget ?**
Le processus qui vous énerve le plus. Celui qui vous fait soupirer chaque lundi. C'est celui qui a le meilleur ROI parce que c'est celui que vous allez réellement laisser tourner.

---

Envie de savoir lequel de ces 5 processus vous coûte le plus cher en ce moment ? L'audit gratuit de 30 minutes commence par cette question.
""",
        },
        "en": {
            "title": "The 5 processes every Québec SMB should automate in 2026",
            "excerpt": "Booking, invoicing, client follow-ups — here are the tasks costing you the most time and how to eliminate them without turning your team into IT experts.",
            "content": """Most Québec SMBs lose **between 10 and 15 hours a week** on repetitive tasks that have nothing to do with their actual business. Not because leaders don't care — because they have neither the time nor the team to tackle it.

Here are the five processes we see over and over during audits, each with: how much time it eats, the typical solution, and what it costs.

# 1. Appointment booking

Between "do you have a slot Thursday?" emails, manual reminders and no-shows, a receptionist can spend *up to 6 hours a week* orchestrating calendars.

The fix: a booking link (Calendly, Cal.com, or SimplyBook) wired into the team's Google or Outlook calendar. The client picks a slot, confirmation goes out automatically, SMS/email reminders fire 24h before.

Cost: $0 to $15/user/month. Setup: half a day.

# 2. Invoicing and follow-ups

Invoicing manually, tracking unpaid invoices in a spreadsheet, sending reminders one by one: every hour spent here is an hour not spent selling or delivering.

Automation combines three pieces:

- An invoicing tool connected to your bank and Revenu Québec (QuickBooks, Acomba, or Sage)
- A trigger that sends the invoice the moment a project is marked "delivered" in your CRM
- An automatic reminder sequence at D+7, D+14 and D+30

Typical gain: 4 to 6 hours per week, and more importantly **a 20–40% drop in payment delays**.

# 3. Client follow-ups (prospects and existing)

A lead comes in through your contact form. You reply the next day. The prospect has already spoken to three competitors. You lose the deal you should have won.

The fix: an automated welcome sequence. The moment a lead arrives, a confirmation email fires within a minute, then a 2-3 message series over 10 days (value, social proof, CTA). For existing clients, a similar cadence: quarterly check-in, upsell, review request.

Stack: a simple CRM (free HubSpot, Airtable or Pipedrive) + Make or n8n for triggers.

# 4. New client onboarding

Sign a contract, send access docs, schedule the kickoff meeting, create the project space, send the deposit invoice: *7 to 10 manual steps* that everyone forgets halfway through.

An automated onboarding flow does all of this in series the moment a contract is signed in DocuSign or Dropbox Sign. The client gets a structured email with access, calendar, invoice. Your team gets a Slack notification with the brief. Zero forgotten steps.

# 5. Weekly reports

Manually compiling weekly sales, open support tickets and KPIs for Monday's meeting: 2-3 hours every week for information that should be visible in real time.

An automated dashboard (Looker Studio, Metabase, or even a well-wired Google Sheet) pulls numbers from sources (Stripe, HubSpot, Zendesk) and refreshes them automatically. You walk into the meeting, everything is already there.

# What it really costs

For an SMB of 5 to 20 employees, a full automation project across these 5 areas runs between **$2,000 and $6,000 one-shot**, plus $50 to $200 per month of tool subscriptions.

Typical ROI is measured in weeks, not years. 12 hours saved per week × $40/hour × 50 weeks = **$24,000 per year** of reclaimed time — not counting clients won because follow-ups finally go out on time.

# FAQ

**Do you need a tech team to maintain all this?**
No. Tools like Make or n8n are designed to be maintained by someone who isn't a developer. Once the flows are in place, they run on their own for months.

**What if a tool changes pricing or API?**
It's a real risk — which is why you pick mature tools and document every flow. At Arivex we deliver minimal docs for every automation.

**Where to start with a small budget?**
The process that annoys you the most. The one that makes you sigh every Monday. That's the one with the best ROI because it's the one you'll actually let run.

---

Curious which of these 5 processes is costing you the most right now? The free 30-minute audit starts with that question.
""",
        },
    },
    {
        "slug": "ia-generative-service-client",
        "category_slug": "ia",
        "cover_image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&q=80",
        "reading_time": 5,
        "featured": True,
        "published_at": date(2026, 4, 8),
        "tags": ["IA", "Service client", "PME"],
        "fr": {
            "title": "Comment l'IA générative transforme le service client des petites entreprises",
            "excerpt": "Les grands groupes ont des équipes IA. Voici comment une PME de 5 employés peut avoir les mêmes outils pour environ 200 $ par mois.",
            "content": """Il y a deux ans, déployer un assistant IA exploitable pour son service client demandait une équipe data, un budget à 6 chiffres et six mois de R&D. En 2026, le ticket d'entrée est tombé à **environ 200 $ par mois et deux jours de mise en place**.

Ce qui change pour les PME, concrètement.

# Ce que l'IA générative résout vraiment

Ignorez les démos glamour. Pour une PME, la vraie valeur se mesure sur trois axes :

- Diminuer le temps moyen de réponse sans embaucher
- Filtrer les questions simples pour que l'humain se concentre sur les dossiers complexes
- Rester disponible le soir et les week-ends, quand les clients ont le plus besoin

L'IA ne remplace pas le service client — elle absorbe la couche répétitive qui empêche votre équipe de bien faire son travail.

# Trois cas d'usage éprouvés en 2026

## Un chatbot entraîné sur votre vraie documentation

Pas un chatbot générique qui invente des réponses. Un chatbot qui lit **votre PDF de conditions, votre FAQ, vos emails de support des 12 derniers mois** et répond avec le vocabulaire de votre entreprise. Outils : Intercom Fin, Chatbase, ou une solution maison avec Claude + retrieval augmenté.

Installation : 2 à 5 jours selon le volume de doc. Coût : 50 à 150 $/mois.

## Le tri et résumé automatique des emails entrants

Chaque email qui arrive dans support@ est catégorisé (urgent, question produit, demande de remboursement, bug), résumé en 2 lignes et routé vers la bonne personne. Plus besoin de lire trois paragraphes pour comprendre de quoi il s'agit.

Outils : Gmail + Apps Script, Zapier + Claude API, ou Make + OpenAI. Coût : 20 à 80 $/mois.

## Des réponses pré-rédigées dans le ton de l'entreprise

Quand un employé doit répondre à un client, l'IA propose 2-3 versions de réponse dans le ton déjà établi de l'entreprise. L'employé choisit, ajuste, envoie. Temps moyen de rédaction divisé par 3.

Outils : HelpScout avec AI Assist, ou une intégration custom ChatGPT dans votre CRM.

# La stack complète à 200 $/mois

| Brique | Outil | Coût |
|--------|-------|------|
| Chatbot FAQ | Chatbase (plan Standard) | 50 $/mois |
| Tri emails | Make + Claude API | 60 $/mois |
| Assistant rédaction | HelpScout AI ou ChatGPT Team | 75 $/mois |
| Logs + analytics | Google Sheet + Looker Studio | gratuit |
| **Total** | | **~185 $/mois** |

Setup initial : 1 500 à 3 000 $ pour un prestataire qui livre la stack configurée et documentée.

# Les pièges à éviter

**Ne pas brancher l'IA sur de la vieille doc**. Si votre FAQ date de 2023 et cite des produits qui n'existent plus, l'IA va les citer aussi. Audit documentaire d'abord.

**Garder une sortie humaine facile**. Tout chatbot doit avoir un bouton "parler à un humain" visible en un clic. Sinon les clients frustrés vont pester en ligne avant que vous puissiez les aider.

**Loguer les échanges**. Si l'IA se trompe, vous devez pouvoir retrouver le fil de la conversation pour corriger le tir.

# FAQ

**Est-ce que mes données sont en sécurité ?**
Avec Claude, GPT-4 et les équivalents entreprises, les données ne sont pas utilisées pour réentraîner les modèles. Vérifier la doc API de chaque fournisseur et privilégier les plans "business" ou "enterprise".

**Est-ce que l'IA peut vraiment comprendre le français québécois ?**
Claude 4.7 et GPT-5 comprennent le français québécois sans problème. Les régionalismes passent. Ce qui coince encore parfois : les expressions très spécifiques à un secteur (BTP, agroalimentaire), à documenter dans le prompt système.

**Combien de temps avant de voir un ROI ?**
Mesurable en 4 à 6 semaines si l'implémentation est bien cadrée. Métrique clé : **le pourcentage de tickets résolus sans intervention humaine**. Objectif réaliste pour une PME : 30 à 50 %.

---

On aide les PME québécoises à déployer ce genre de stack chez eux. Si vous voulez voir ce que ça donnerait chez vous, l'audit gratuit de 30 minutes est un bon point de départ.
""",
        },
        "en": {
            "title": "How generative AI is transforming customer service for small businesses",
            "excerpt": "Big corporations have AI teams. Here's how a 5-person SMB can have the same tools for about $200 a month.",
            "content": """Two years ago, deploying a usable AI assistant for customer service required a data team, a six-figure budget, and six months of R&D. In 2026, the entry ticket has dropped to **about $200 a month and two days of setup**.

What it actually changes for SMBs.

# What generative AI really solves

Ignore the glamorous demos. For an SMB, real value is measured on three axes:

- Reducing average response time without hiring
- Filtering simple questions so humans can focus on complex cases
- Staying available evenings and weekends, when clients need help most

AI doesn't replace customer service — it absorbs the repetitive layer that prevents your team from doing its job well.

# Three proven use cases in 2026

## A chatbot trained on your actual documentation

Not a generic chatbot that makes up answers. A chatbot that reads **your terms PDF, your FAQ, your last 12 months of support emails** and replies using your company's vocabulary. Tools: Intercom Fin, Chatbase, or a home-grown solution with Claude + retrieval augmentation.

Setup: 2 to 5 days depending on doc volume. Cost: $50 to $150/month.

## Automatic sorting and summarizing of incoming emails

Every email landing in support@ gets categorized (urgent, product question, refund request, bug), summarized in 2 lines, and routed to the right person. No more reading three paragraphs to understand what's going on.

Tools: Gmail + Apps Script, Zapier + Claude API, or Make + OpenAI. Cost: $20 to $80/month.

## Pre-drafted replies in your company's tone

When an employee needs to reply to a client, the AI proposes 2-3 versions of the response in the already-established company tone. The employee picks, tweaks, sends. Average drafting time cut by 3×.

Tools: HelpScout with AI Assist, or a custom ChatGPT integration in your CRM.

# The full $200/month stack

| Piece | Tool | Cost |
|-------|------|------|
| FAQ chatbot | Chatbase (Standard plan) | $50/mo |
| Email sorting | Make + Claude API | $60/mo |
| Drafting assistant | HelpScout AI or ChatGPT Team | $75/mo |
| Logs + analytics | Google Sheet + Looker Studio | free |
| **Total** | | **~$185/mo** |

Initial setup: $1,500 to $3,000 for a provider delivering the stack configured and documented.

# Pitfalls to avoid

**Don't connect AI to stale docs.** If your FAQ is from 2023 and cites products that no longer exist, the AI will cite them too. Do a documentation audit first.

**Keep an easy human exit.** Every chatbot must have a visible "talk to a human" button in one click. Otherwise frustrated clients will rant online before you get a chance to help them.

**Log conversations.** When the AI gets it wrong, you need to be able to trace the conversation to fix the prompt.

# FAQ

**Is my data safe?**
With Claude, GPT-4 and their business equivalents, data isn't used to retrain models. Check each provider's API docs and prefer "business" or "enterprise" plans.

**Can AI really understand Québec French?**
Claude 4.7 and GPT-5 understand Québec French without issue. Regionalisms work. What still occasionally trips up: sector-specific expressions (construction, agri-food), which should be documented in the system prompt.

**How long before seeing ROI?**
Measurable in 4 to 6 weeks if implementation is well scoped. Key metric: **percentage of tickets resolved without human intervention**. Realistic target for an SMB: 30 to 50%.

---

We help Québec SMBs deploy this kind of stack in-house. If you want to see what it would look like for you, the free 30-minute audit is a good starting point.
""",
        },
    },
    {
        "slug": "site-vitrine-vs-app-web",
        "category_slug": "developpement-web",
        "cover_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80",
        "reading_time": 6,
        "featured": False,
        "published_at": date(2026, 4, 1),
        "tags": ["Développement Web", "PME"],
        "fr": {
            "title": "Site vitrine vs application web : lequel choisir pour votre PME en 2026 ?",
            "excerpt": "La différence entre les deux peut représenter des milliers de dollars et plusieurs mois de travail. Voici comment faire le bon choix selon votre situation.",
            "content": """On nous pose cette question au moins une fois par semaine : *"J'ai besoin d'un site pour ma PME, mais je ne sais pas si un site vitrine suffit ou s'il faut vraiment une application web."*

La réponse courte : ça dépend de ce que votre site doit **faire**, pas de ce qu'il doit **montrer**.

# La vraie différence

Un **site vitrine** présente de l'information statique : qui vous êtes, ce que vous vendez, comment vous contacter. Le visiteur consomme, il ne transforme rien. Exemples : le site d'un restaurant, d'un cabinet d'avocats, d'une agence.

Une **application web** fait travailler vos visiteurs. Ils créent un compte, saisissent des données, interagissent avec votre logique métier. Exemples : un portail client pour suivre une commande, un tableau de bord pour gérer des abonnements, une plateforme de réservation.

Entre les deux, il existe un **site vitrine avec fonctionnalités** : blog, formulaire de contact, prise de rendez-vous en ligne, newsletter. C'est là que 70 % des PME atterrissent sans s'en rendre compte.

# Les trois questions qui tranchent

## 1. Est-ce que vos visiteurs ont besoin d'un compte ?

Si oui → application web. Dès qu'il y a authentification, persistance de données et permissions, vous êtes dans du SaaS léger, pas dans de la vitrine.

Si non → site vitrine suffit, même avec formulaires et blog.

## 2. Est-ce que les données doivent être lues ou écrites ?

Un site qui affiche des produits depuis un CMS (Sanity, Strapi, Contentful) est un site vitrine, même si son contenu change souvent. La logique est en lecture seule côté visiteur.

Dès qu'un visiteur peut modifier l'état du système (passer commande, uploader un document, voter), vous basculez en application.

## 3. Quel est le coût d'une bogue ?

Sur un site vitrine, une bogue d'affichage est agaçante mais réversible. Sur une application web, une bogue dans la logique de facturation peut coûter des centaines de dollars avant d'être détectée. C'est pour ça que les applications demandent plus de tests, plus de rigueur et donc plus de budget.

# Les ordres de grandeur en 2026

| Type de projet | Délai typique | Budget | Exemple |
|----------------|---------------|--------|---------|
| Site vitrine simple (5-8 pages) | 2-3 semaines | 2 000 à 5 000 $ | Agence de services, restaurant |
| Site vitrine + blog + formulaires | 3-5 semaines | 4 000 à 8 000 $ | PME avec stratégie de contenu |
| Site vitrine + e-commerce | 5-8 semaines | 6 000 à 15 000 $ | Boutique < 100 SKU |
| Application web custom | 2-4 mois | 15 000 à 60 000 $+ | Portail client, tableau de bord, SaaS |

Ces chiffres sont des fourchettes réalistes pour un prestataire québécois en 2026. Moins cher, vous achetez un template mal adapté. Beaucoup plus cher, vous payez de la marge d'agence.

# Les erreurs qu'on voit le plus

**Partir sur une application web quand un site vitrine suffit.** C'est le piège classique : on imagine des fonctionnalités qu'on n'utilisera jamais. Résultat : 40 000 $ dépensés pour une fonctionnalité "espace client" qui sert à 3 personnes.

**Partir sur un site vitrine quand une application est nécessaire.** L'inverse aussi : on croit qu'un Wix + un Calendly fera l'affaire, et six mois plus tard on doit tout refaire parce que le formulaire de réservation ne gère pas le calcul des forfaits.

**Oublier le coût de l'évolution.** Un site vitrine à 3 000 $ qui doit devenir une application à 30 000 $ six mois plus tard est plus cher qu'une application à 25 000 $ bien cadrée dès le départ.

# Comment trancher concrètement

Posez-vous cette question : *"Est-ce que mon visiteur doit se connecter, saisir des données qui persistent, ou voir quelque chose de personnalisé pour lui ?"*

- Trois "non" → **site vitrine** suffit.
- Un "oui" → **site vitrine enrichi** (CMS + formulaires + intégrations).
- Deux "oui" ou plus → **application web**. Prévoir le budget et le délai qui vont avec.

# FAQ

**Est-ce qu'un WordPress peut faire office d'application web ?**
Avec beaucoup de plugins, oui, pour des cas simples. Au-delà, la maintenance devient un cauchemar et les coûts d'hébergement explosent. À partir d'un certain niveau, repartir d'un framework moderne (Django, Laravel, Next.js) est moins cher sur 3 ans.

**Puis-je commencer vitrine et migrer vers une application plus tard ?**
Oui, à condition de l'anticiper dès la conception du site vitrine : nom de domaine, design system, contenu. Migrer "en douceur" est parfaitement viable si on y pense dès le départ.

**Le no-code (Webflow, Bubble) est-il une alternative ?**
Pour un site vitrine, Webflow est excellent. Pour une application avec de la logique métier, Bubble marche jusqu'à un certain volume — au-delà, les performances et les limites de la plateforme deviennent un problème. Règle du pouce : si vous envisagez > 1 000 utilisateurs actifs/mois, partez sur du code.

---

Pas sûr de ce qu'il vous faut vraiment ? Un audit gratuit de 30 minutes permet de trancher. On préfère vous dire "un site vitrine suffit" et vous vendre pour 4 000 $ plutôt que pour 40 000 $.
""",
        },
        "en": {
            "title": "Brochure site vs web app: which one for your SMB in 2026?",
            "excerpt": "The difference between the two can mean thousands of dollars and several months of work. Here's how to make the right choice for your situation.",
            "content": """We get this question at least once a week: *"I need a site for my SMB, but I don't know if a brochure site is enough or if I really need a web app."*

The short answer: it depends on what your site needs to **do**, not what it needs to **show**.

# The real difference

A **brochure site** presents static information: who you are, what you sell, how to reach you. The visitor consumes, they don't transform anything. Examples: a restaurant's site, a law firm, an agency.

A **web app** makes your visitors work. They create an account, enter data, interact with your business logic. Examples: a client portal tracking an order, a dashboard managing subscriptions, a booking platform.

Between the two, there's a **brochure site with features**: blog, contact form, online booking, newsletter. That's where 70% of SMBs land without realizing it.

# The three questions that settle it

## 1. Do your visitors need an account?

If yes → web app. The moment there's authentication, data persistence, and permissions, you're in light SaaS territory, not brochure.

If no → brochure site works, even with forms and a blog.

## 2. Is data read or written?

A site displaying products from a CMS (Sanity, Strapi, Contentful) is a brochure site, even if its content changes often. Logic is read-only from the visitor's side.

The moment a visitor can modify the system's state (place an order, upload a document, vote), you're in web app territory.

## 3. What's the cost of a bug?

On a brochure site, a display bug is annoying but reversible. On a web app, a bug in the billing logic can cost hundreds of dollars before it's detected. That's why web apps require more testing, more rigor, and therefore more budget.

# Ballpark numbers in 2026

| Project type | Typical timeline | Budget | Example |
|--------------|------------------|--------|---------|
| Simple brochure (5-8 pages) | 2-3 weeks | $2,000 to $5,000 | Service agency, restaurant |
| Brochure + blog + forms | 3-5 weeks | $4,000 to $8,000 | SMB with content strategy |
| Brochure + e-commerce | 5-8 weeks | $6,000 to $15,000 | Shop < 100 SKUs |
| Custom web app | 2-4 months | $15,000 to $60,000+ | Client portal, dashboard, SaaS |

These numbers are realistic ranges for a Québec-based provider in 2026. Cheaper and you buy a misfit template. A lot more and you're paying agency margin.

# The mistakes we see the most

**Going with a web app when a brochure site would do.** The classic trap: imagining features you'll never use. Result: $40,000 spent on a "client area" that three people use.

**Going with a brochure site when an app is needed.** The reverse: thinking Wix + Calendly will cover it, and six months later you have to redo everything because the booking form can't handle your pricing logic.

**Forgetting evolution cost.** A $3,000 brochure site that must become a $30,000 app six months later costs more than a well-scoped $25,000 app from day one.

# How to decide concretely

Ask yourself: *"Does my visitor need to log in, enter data that persists, or see something personalized for them?"*

- Three "no" → **brochure site** is enough.
- One "yes" → **enriched brochure** (CMS + forms + integrations).
- Two or more "yes" → **web app**. Budget and timeline accordingly.

# FAQ

**Can WordPress act as a web app?**
With a lot of plugins, yes, for simple cases. Beyond that, maintenance becomes a nightmare and hosting costs explode. At a certain level, starting over from a modern framework (Django, Laravel, Next.js) is cheaper over 3 years.

**Can I start brochure and migrate to a web app later?**
Yes, provided you plan for it during the brochure site's design: domain name, design system, content. A smooth migration is perfectly viable if thought through from the start.

**Is no-code (Webflow, Bubble) an alternative?**
For a brochure site, Webflow is excellent. For an app with business logic, Bubble works up to a certain volume — beyond that, performance and platform limits become an issue. Rule of thumb: if you anticipate > 1,000 monthly active users, go with code.

---

Not sure what you actually need? A free 30-minute audit lets us figure it out together. We'd rather tell you "a brochure site is enough" and sell you $4,000 of work than $40,000.
""",
        },
    },
    {
        "slug": "fonder-entreprise-20-ans-quebec",
        "category_slug": "entrepreneuriat",
        "cover_image": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1600&q=80",
        "reading_time": 8,
        "featured": False,
        "published_at": date(2026, 4, 18),
        "tags": ["Entrepreneuriat", "Québec"],
        "fr": {
            "title": "Fonder une entreprise à 20 ans au Québec : ce que personne ne vous dit",
            "excerpt": "Le REQ, le clicSÉQUR, la Charte de la langue française — le guide honnête pour immatriculer votre première entreprise sans se perdre dans les formulaires.",
            "content": """J'ai immatriculé Arivex à 20 ans, en avril 2026, depuis Saguenay. Entre la paperasse, les frais cachés et les petits détails que personne ne mentionne, j'ai perdu trois jours à cocher des cases que j'aurais pu éviter. Voici le guide que j'aurais aimé lire avant de commencer.

# Étape 1 : le Registraire des entreprises du Québec (REQ)

C'est le passage obligé. Pour une entreprise individuelle (le cas le plus simple à 20 ans), comptez **environ 40 $ par an** de frais d'immatriculation, plus une déclaration annuelle obligatoire (même montant, même simplicité).

Le formulaire en ligne prend 30 minutes si vous avez vos papiers sous la main : pièce d'identité, adresse, nom de l'entreprise (vérifié disponible), description de l'activité. Vous obtenez un **Numéro d'entreprise du Québec (NEQ)** immédiatement.

Piège : choisissez bien votre nom. Une fois le NEQ émis, changer de nom coûte des frais et demande une nouvelle déclaration.

# Étape 2 : clicSÉQUR et le numéro fiscal

Avec votre NEQ, vous devez maintenant vous enregistrer auprès de **Revenu Québec** et de l'**ARC (Agence du revenu du Canada)** pour obtenir vos numéros fiscaux. C'est gratuit.

- **Revenu Québec** : numéro d'identification TVQ et TPS/TVH
- **ARC** : numéro de compte d'entreprise (BN)

Le portail clicSÉQUR Entreprises permet de tout faire en une session si vos identifiants personnels clicSÉQUR sont déjà créés. Sinon, prévoir 2-3 jours d'allers-retours postaux pour recevoir les codes d'activation.

À 20 ans, vous n'êtes obligé de vous inscrire aux taxes (TPS/TVQ) **qu'à partir de 30 000 $ de revenus annuels**. En dessous, vous pouvez choisir de ne pas facturer de taxes — mais ça vous empêche aussi d'en récupérer sur vos achats. À évaluer selon vos dépenses.

# Étape 3 : la Charte de la langue française

Depuis la Loi 96 (2022), toutes les entreprises québécoises ont des obligations linguistiques plus strictes, même les plus petites.

Pour une entreprise individuelle de moins de 25 employés, l'essentiel à respecter :

- **Nom d'entreprise** en français (ou bilingue avec le français aussi visible)
- **Site web** disponible en français (au minimum la page d'accueil et les CGU)
- **Factures et contrats** en français par défaut (la version anglaise reste possible si le client le demande explicitement)

Ce n'est pas optionnel. L'Office québécois de la langue française (OQLF) peut infliger des amendes, même aux petites structures. En pratique, tant que vous êtes de bonne foi, l'OQLF vous contactera avant pour demander des correctifs.

# Étape 4 : le compte bancaire d'entreprise

Séparez dès le jour 1 vos finances personnelles et celles de l'entreprise. Même pour une entreprise individuelle (où juridiquement, les fonds vous appartiennent), le comptable et le fisc vont vous remercier.

Les options en 2026 au Québec :

- **Desjardins** : compte d'entreprise gratuit les 6 premiers mois, puis 10-15 $/mois. Service en succursale disponible partout en région.
- **Banque Nationale** : offre similaire, légèrement plus avantageuse sur le change USD/CAD.
- **Wise Business** : compte multi-devises, pas de frais mensuels. Top si vous facturez en USD ou en EUR. Mais pas de succursale physique.
- **Stripe Atlas / Mercury** : si vous prévoyez de vendre à l'international et que vous êtes à l'aise avec le tout-en-ligne.

À 20 ans, la plupart des banques vont exiger un rendez-vous en personne avec votre **NEQ, votre pièce d'identité et une preuve d'adresse**. Prévoyez 45 minutes.

# Étape 5 : ce que personne ne vous dit

## Le comptable vaut son pesant d'or

Dès la première année, trouvez un comptable qui prend les entreprises individuelles (pas toutes les grandes firmes le font). Budget typique : 500 à 1 500 $/an pour une entreprise simple. Il vous évitera des erreurs de TPS/TVQ qui coûtent cher en intérêts.

## L'assurance responsabilité civile

Pas obligatoire pour une entreprise individuelle de services, mais à 20 ans, une poursuite peut liquider votre épargne à vie. Une police "erreurs et omissions" démarre autour de 40 $/mois chez Desjardins ou Intact.

## Les contrats écrits, même avec les proches

Votre premier client sera peut-être un ami ou un membre de la famille. Faites quand même un contrat écrit. Un désaccord oral détruit les relations ; un contrat écrit les protège.

## La trésorerie avant tout

À 20 ans, vous n'avez pas de réserves. Facturez des acomptes de 30 à 50 % avant de commencer. Refusez les paiements à 60 jours. Un client qui refuse un acompte est un client qui risque de ne pas payer.

# FAQ

**Puis-je fonder une entreprise avant 18 ans ?**
Oui, mais vous aurez besoin d'un tuteur légal pour signer les documents commerciaux. À partir de 18 ans, vous êtes pleinement autonome.

**Incorporation ou entreprise individuelle ?**
À 20 ans, en solo, sans risque juridique majeur, **l'entreprise individuelle suffit**. L'incorporation coûte 300-500 $ de plus par an en frais fiscaux et comptables, pour des avantages qui ne kickent réellement qu'à partir de 80 000-100 000 $ de revenus.

**Quels avantages à être jeune entrepreneur au Québec ?**
Plusieurs programmes : Futurpreneur (prêt jusqu'à 60 000 $ à taux réduit), Emploi-Québec (subventions embauche), BDC (accompagnement). Le Cégep et l'université offrent aussi souvent des bourses étudiants-entrepreneurs méconnues — demandez au service de vie étudiante.

---

J'ai créé Arivex avec zéro financement, juste en appliquant ce guide. Si vous êtes en train de franchir le pas, j'écris d'autres articles sur les premiers mois d'une entreprise — abonnez-vous à la newsletter pour les recevoir.
""",
        },
        "en": {
            "title": "Founding a company at 20 in Québec: what no one tells you",
            "excerpt": "The REQ, clicSÉQUR, the French Language Charter — the honest guide to registering your first business without getting lost in paperwork.",
            "content": """I registered Arivex at 20, in April 2026, from Saguenay. Between paperwork, hidden fees and small details no one mentions, I lost three days checking boxes I could have avoided. Here's the guide I wish I'd read before starting.

# Step 1: the Registraire des entreprises du Québec (REQ)

This is the unavoidable step. For a sole proprietorship (the simplest case at 20), expect **around $40 per year** in registration fees, plus a mandatory annual declaration (same amount, same simplicity).

The online form takes 30 minutes if you have your papers ready: ID, address, business name (verified available), activity description. You get a **Québec Business Number (NEQ)** immediately.

Trap: pick your name carefully. Once the NEQ is issued, changing names costs fees and requires a new declaration.

# Step 2: clicSÉQUR and tax numbers

With your NEQ, you now need to register with **Revenu Québec** and the **CRA (Canada Revenue Agency)** to get your tax numbers. It's free.

- **Revenu Québec**: GST/QST identification number
- **CRA**: Business Number (BN)

The clicSÉQUR Entreprises portal lets you do it all in one session if your personal clicSÉQUR credentials are already created. Otherwise, expect 2-3 days of mail back-and-forth for activation codes.

At 20, you're only required to register for taxes (GST/QST) **starting at $30,000 in annual revenue**. Below that, you can choose not to charge taxes — but it also prevents you from reclaiming them on your expenses. Evaluate based on your spending.

# Step 3: the French Language Charter

Since Bill 96 (2022), all Québec businesses have stricter language obligations, even the smallest.

For a sole proprietorship under 25 employees, the essentials:

- **Business name** in French (or bilingual with French equally visible)
- **Website** available in French (at minimum the home page and terms)
- **Invoices and contracts** in French by default (English version remains possible if the client explicitly requests it)

It's not optional. The Office québécois de la langue française (OQLF) can fine even small outfits. In practice, as long as you're in good faith, OQLF will contact you first to request fixes.

# Step 4: the business bank account

Separate personal and business finances from day one. Even for a sole proprietorship (where legally the funds are yours), your accountant and the tax office will thank you.

Options in 2026 in Québec:

- **Desjardins**: free business account for 6 months, then $10-15/month. Branch service available everywhere in the regions.
- **National Bank**: similar offer, slightly better on USD/CAD conversion.
- **Wise Business**: multi-currency account, no monthly fees. Top pick if you invoice in USD or EUR. But no physical branches.
- **Stripe Atlas / Mercury**: if you plan to sell internationally and are comfortable with fully online banking.

At 20, most banks will require an in-person appointment with your **NEQ, ID, and proof of address**. Allow 45 minutes.

# Step 5: what no one tells you

## The accountant is worth their weight in gold

From year one, find an accountant who handles sole proprietorships (not all big firms do). Typical budget: $500 to $1,500/year for a simple business. They'll save you GST/QST mistakes that cost a lot in interest.

## Civil liability insurance

Not mandatory for a service-based sole proprietorship, but at 20, one lawsuit can wipe out your lifetime savings. An "errors and omissions" policy starts around $40/month at Desjardins or Intact.

## Written contracts, even with close relations

Your first client might be a friend or family member. Still write a contract. A verbal disagreement destroys relationships; a written contract protects them.

## Cash flow above all

At 20, you have no reserves. Invoice 30-50% deposits before starting. Refuse 60-day payment terms. A client who refuses a deposit is a client who might not pay.

# FAQ

**Can I found a business before 18?**
Yes, but you'll need a legal guardian to sign business documents. From 18, you're fully autonomous.

**Incorporation or sole proprietorship?**
At 20, solo, without major legal risk, **sole proprietorship is enough**. Incorporation costs $300-500 more per year in tax and accounting fees, for benefits that only kick in starting at $80,000-100,000 in revenue.

**What advantages for young entrepreneurs in Québec?**
Several programs: Futurpreneur (loan up to $60,000 at reduced rate), Emploi-Québec (hiring grants), BDC (coaching). Cegep and university often offer lesser-known student-entrepreneur grants — ask the student life office.

---

I built Arivex with zero funding, just applying this guide. If you're about to take the leap, I'm writing more articles on the first months of a business — subscribe to the newsletter to get them.
""",
        },
    },
    {
        "slug": "pme-saguenay-automatisation",
        "category_slug": "pme-quebec",
        "cover_image": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=1600&q=80",
        "reading_time": 6,
        "featured": False,
        "published_at": date(2026, 4, 10),
        "tags": ["Saguenay", "PME", "Automatisation"],
        "fr": {
            "title": "Pourquoi les PME du Saguenay tardent à adopter l'automatisation (et comment changer ça)",
            "excerpt": "L'automatisation est perçue comme complexe et coûteuse dans la région. Voici pourquoi c'est faux, avec des exemples concrets.",
            "content": """J'ai grandi au Saguenay. J'ai étudié au Cégep de Jonquière. J'ai fondé Arivex ici, en avril 2026, parce que les PME de la région ont les mêmes besoins que celles de Montréal — mais beaucoup moins de prestataires qui leur parlent vraiment.

Et pourtant, sur l'automatisation, il y a un vrai retard. Voici pourquoi, et comment y remédier sans se ruiner.

# Les trois freins qu'on entend sur le terrain

## 1. "C'est pour les grandes entreprises"

Faux. **85 % des automatisations qu'on déploie chez Arivex le sont pour des structures de 2 à 15 employés**. Les grandes entreprises ont des équipes IT, elles font ça en interne. Les PME, elles, ont besoin d'un prestataire qui comprend leur échelle.

Un plombier avec deux employés à Chicoutimi a exactement les mêmes 5 problèmes qu'un cabinet de services à Montréal : facturation, rappels clients, calendrier. Seuls les montants changent.

## 2. "Ça coûte trop cher"

Autre faux. Un projet d'automatisation typique pour une PME régionale coûte **entre 1 500 $ et 4 500 $** en one-shot, avec des abonnements de 30 à 100 $/mois.

Le ROI se mesure en semaines :

> *"Avant, je passais mon lundi matin à faire des factures. Maintenant ça part tout seul, je consacre ce temps à prospecter. J'ai gagné deux nouveaux clients le premier mois."*
> — Gérant d'une entreprise de 6 personnes à Alma

## 3. "On n'a personne pour s'en occuper après"

Vrai souci, faux obstacle. Les outils modernes (Make, n8n, Zapier) sont conçus pour être maintenus par quelqu'un qui n'est pas développeur. Chez Arivex, chaque livraison inclut une doc et une session de formation pour qu'un employé actuel (souvent l'adjointe administrative) puisse faire les ajustements mineurs.

Si le système plante, il plante — ça se réactive en 15 minutes. Ce n'est pas la fin du monde.

# Les exemples concrets du Saguenay

## Un cabinet comptable à Chicoutimi

Problème : les courriels clients partaient pour demander les documents fiscaux, avec des relances manuelles jusqu'à 4 fois par dossier.

Solution : séquence automatique via Make + HelloSign. Le client reçoit un email le 1er février, une relance le 15 si rien n'est signé, une autre le 28. L'adjointe n'intervient plus que sur les cas bloqués.

Gain : **8 heures par semaine en février-mars**, et la saison des impôts s'est terminée sans burnout.

## Un restaurant à Jonquière

Problème : les réservations passaient par Facebook Messenger, un SMS parfois, un appel aussi. Impossible de consolider. Des doubles bookings chaque semaine.

Solution : un SimplyBook intégré au site, un chatbot Facebook qui redirige vers la page de réservation, une synchronisation avec Google Calendar. Budget : 1 200 $ one-shot, 35 $/mois.

Gain : zéro double booking depuis 4 mois, et **15 % de réservations en plus** — parce que les clients peuvent maintenant réserver à 23h sans parler à personne.

## Un fournisseur industriel à La Baie

Problème : les devis partaient sur papier, avec calcul manuel. 30 minutes par devis, et 5 à 10 par jour.

Solution : un configurateur web simple (Tally + Airtable + générateur PDF) qui permet au commercial de cliquer les options et sort un devis prêt à envoyer. Prototype en 3 semaines.

Gain : **3 heures par jour** récupérées, et des devis qui ne contiennent plus d'erreurs de calcul.

# Comment démarrer sans prendre de risque

## Choisir un seul processus au début

Pas tout automatiser en même temps. Un seul truc, celui qui vous fait perdre le plus de temps. Vous le livrez, vous le stabilisez sur 4-6 semaines, puis vous passez au suivant.

## Prévoir un audit gratuit avant

La plupart des prestataires sérieux (Arivex y compris) offrent un audit initial gratuit de 30 minutes. Utilisez-le. Vous saurez en sortant si le projet vaut le coup et combien il va coûter **avant** de signer.

## Vérifier que le prestataire livre une doc

Un projet d'automatisation sans documentation, c'est une dette technique qui explose dans 6 mois quand le prestataire n'est plus joignable. Exigez un document qui explique comment chaque flux fonctionne. Si on vous dit "pas besoin", fuyez.

# FAQ

**Y a-t-il des subventions pour l'automatisation au Québec ?**
Oui, plusieurs. Le programme **ESSOR** (MEI) finance jusqu'à 50 % des projets de numérisation pour les PME. **Audit Industrie 4.0** offre un audit financé à 100 %. Investissement Québec a aussi des volets dédiés. Un bon prestataire connaît ces programmes et peut vous aider à monter le dossier.

**Est-ce qu'un prestataire hors Saguenay comprend notre réalité régionale ?**
Ça dépend du prestataire. Un prestataire montréalais qui facture 200 $/h et ne vient jamais sur place est rarement le bon choix pour une PME régionale. Ceux qui fonctionnent en remote sans poser de problème existent (Arivex en est un), mais assurez-vous qu'ils comprennent vos réalités opérationnelles avant de signer.

**Combien de temps pour un premier projet ?**
Entre 2 et 6 semaines selon la complexité. Un processus simple (rappels clients, prise de RDV) se livre en 10 jours. Un flux plus complexe (devis automatisés, onboarding) prend 4-6 semaines.

---

Arivex est basée à Saguenay. On travaille avec des PME régionales qui veulent arrêter de perdre du temps sur l'administratif. L'audit initial est gratuit, ça part d'un courriel.
""",
        },
        "en": {
            "title": "Why Saguenay SMBs are slow to adopt automation (and how to change that)",
            "excerpt": "Automation is perceived as complex and costly in the region. Here's why that's false, with concrete examples.",
            "content": """I grew up in Saguenay. I studied at Cégep de Jonquière. I founded Arivex here in April 2026 because SMBs in the region have the same needs as those in Montréal — but far fewer providers who actually speak their language.

And yet, on automation, there's a real lag. Here's why, and how to fix it without going broke.

# The three objections we hear on the ground

## 1. "It's for big companies"

False. **85% of automations we deploy at Arivex are for outfits of 2 to 15 employees**. Big companies have IT teams, they do this in-house. SMBs need a provider who understands their scale.

A plumber with two employees in Chicoutimi has the exact same 5 problems as a service firm in Montréal: invoicing, client reminders, calendar. Only the amounts differ.

## 2. "It costs too much"

Also false. A typical automation project for a regional SMB costs **between $1,500 and $4,500** one-shot, with subscriptions of $30 to $100/month.

ROI is measured in weeks:

> *"Before, I spent Monday mornings doing invoices. Now it runs itself, I use that time to prospect. I won two new clients the first month."*
> — Manager of a 6-person business in Alma

## 3. "We have no one to maintain it"

Valid concern, false obstacle. Modern tools (Make, n8n, Zapier) are designed to be maintained by someone who isn't a developer. At Arivex, every delivery includes documentation and a training session so a current employee (often the administrative assistant) can handle minor tweaks.

If the system goes down, it goes down — it's reactivated in 15 minutes. It's not the end of the world.

# Concrete examples from Saguenay

## A Chicoutimi accounting firm

Problem: client emails went out requesting tax documents, with manual follow-ups up to 4 times per file.

Fix: automated sequence via Make + HelloSign. The client gets an email on February 1st, a reminder on the 15th if nothing's signed, another on the 28th. The assistant only steps in on blocked cases.

Gain: **8 hours per week in Feb-March**, and tax season ended without burnout.

## A Jonquière restaurant

Problem: reservations came through Facebook Messenger, occasionally SMS, sometimes a call. Impossible to consolidate. Double-bookings every week.

Fix: a SimplyBook widget on the site, a Facebook chatbot redirecting to the booking page, a sync with Google Calendar. Budget: $1,200 one-shot, $35/month.

Gain: zero double-booking in 4 months, and **15% more reservations** — because clients can now book at 11pm without talking to anyone.

## An industrial supplier in La Baie

Problem: quotes went out on paper, with manual calculation. 30 minutes per quote, and 5 to 10 per day.

Fix: a simple web configurator (Tally + Airtable + PDF generator) that lets the sales rep click options and spits out a ready-to-send quote. Prototype in 3 weeks.

Gain: **3 hours per day** reclaimed, and quotes that no longer contain math errors.

# How to get started without taking on risk

## Pick one process to start

Don't automate everything at once. One thing, the one that costs you the most time. Deliver it, stabilize it over 4-6 weeks, then move to the next.

## Do a free audit first

Most serious providers (Arivex included) offer a free 30-minute initial audit. Use it. You'll know on the way out whether the project is worth it and how much it will cost **before** signing.

## Make sure the provider delivers docs

An automation project without documentation is technical debt that explodes in 6 months when the provider is unreachable. Demand a document explaining how each flow works. If they say "no need", run.

# FAQ

**Are there grants for automation in Québec?**
Yes, several. The **ESSOR** program (MEI) funds up to 50% of digitization projects for SMBs. **Industry 4.0 Audit** covers 100% of an audit. Investissement Québec also has dedicated streams. A good provider knows these programs and can help you build the file.

**Will a non-Saguenay provider understand our regional reality?**
Depends on the provider. A Montréal firm billing $200/hr who never visits is rarely the right pick for a regional SMB. Providers who work remote without problems exist (Arivex is one), but make sure they understand your operational realities before signing.

**How long for a first project?**
Between 2 and 6 weeks depending on complexity. A simple process (client reminders, booking) ships in 10 days. A more complex flow (automated quotes, onboarding) takes 4-6 weeks.

---

Arivex is based in Saguenay. We work with regional SMBs tired of losing time on admin. Initial audit is free, starts with an email.
""",
        },
    },
    {
        "slug": "make-vs-zapier-vs-code",
        "category_slug": "automatisation",
        "cover_image": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1600&q=80",
        "reading_time": 9,
        "featured": False,
        "published_at": date(2026, 4, 3),
        "tags": ["Automatisation", "Outils", "Make", "Zapier"],
        "fr": {
            "title": "Make vs Zapier vs code custom : quel outil d'automatisation choisir ?",
            "excerpt": "Chaque outil a ses forces. Voici un guide comparatif honnête basé sur des projets réels livrés au Québec en 2026.",
            "content": """Make, Zapier et le code custom ne sont pas des concurrents directs — ils servent des cas d'usage différents. Le piège, c'est d'essayer de tout faire avec un seul outil.

Voici comment on tranche chez Arivex, basé sur une trentaine de projets livrés en 2025-2026.

# Zapier : le plus accessible, le moins puissant

**Pour qui** : une PME qui automatise 2-5 flux simples avec des services populaires (Gmail, Slack, HubSpot, Stripe).

**Forces**
- Interface la plus simple du marché. Un néophyte crée un flux en 15 minutes.
- 7 000+ intégrations prêtes, plus que tout concurrent.
- Documentation excellente, communauté massive.
- Parfait pour les déclencheurs événementiels ponctuels ("quand un email arrive, envoyer un Slack").

**Faiblesses**
- Prix qui grimpe vite. Un flux complexe avec 3-4 étapes consomme beaucoup de "tasks". Une PME active peut facilement dépasser 300 $/mois.
- Pas de logique conditionnelle avancée. Les "Paths" existent mais restent limités.
- Mauvais choix pour tout ce qui nécessite une boucle ou un traitement de volume.

**Prix typique** : 20 à 400 $/mois selon le plan et le volume.

# Make (ex-Integromat) : le sweet spot

**Pour qui** : une PME ou une agence qui automatise 5-20 flux avec des logiques conditionnelles, des boucles, des transformations de données.

**Forces**
- Visualisation des flux largement supérieure à Zapier. On voit le chemin des données.
- Logique avancée native : routeurs, agrégateurs, itérateurs, gestion d'erreurs.
- Prix beaucoup plus avantageux que Zapier à volume équivalent.
- Marchés européens et francophones bien desservis (support en français disponible).

**Faiblesses**
- Courbe d'apprentissage plus raide que Zapier. Un débutant se décourage parfois.
- Moins d'intégrations que Zapier (environ 2 000 vs 7 000), mais toutes les principales y sont.
- Quand un scénario plante, le debug est parfois cryptique.

**Prix typique** : 10 à 200 $/mois. **C'est le meilleur rapport qualité-prix pour la plupart des PME québécoises**.

# Code custom (Python, Node.js) : le plus flexible, le plus cher à démarrer

**Pour qui** : un cas d'usage très spécifique, une logique métier complexe, un volume élevé, ou une intégration à un système interne.

**Forces**
- Aucune limite technique. Tout ce qui peut être codé peut être automatisé.
- Pas d'abonnement à une plateforme tierce. Vous hébergez où vous voulez.
- Performance optimale : traitement par lots, parallélisation, caches.
- Vous possédez le code. Aucun risque de lock-in.

**Faiblesses**
- Développement initial plus cher (3 000 à 15 000 $ selon la complexité, vs 1 500-3 000 $ pour une solution Make équivalente).
- Nécessite un prestataire compétent et surtout une documentation solide.
- Maintenance sur le long terme : mises à jour de dépendances, sécurité, hébergement.

**Prix typique** : développement one-shot + 20 à 100 $/mois d'hébergement.

# La matrice de décision

| Votre situation | Outil recommandé |
|-----------------|-------------------|
| 1-3 flux simples, budget serré | **Zapier** (plan starter) |
| 5-20 flux avec logique | **Make** |
| Logique métier spécifique | **Code custom** |
| Volume > 100 k opérations/mois | **Code custom** (Zapier/Make deviennent chers) |
| Intégration système interne legacy | **Code custom** |
| Automatisation multi-équipes | **Make** (meilleur côté gouvernance) |
| On veut pouvoir maintenir en interne sans dev | **Zapier** ou **Make** |

# Le vrai critère qu'on oublie souvent

Au-delà de l'outil, c'est **la capacité à maintenir** qui compte. Un flux Make génial construit par un prestataire qui disparaît est pire qu'une solution Zapier moyenne maintenue en interne.

Avant de choisir, répondez à :

1. Qui va ajuster le flux dans 6 mois si un besoin change ?
2. Qui a accès au compte et aux secrets API ?
3. Si le prestataire n'est plus disponible, combien de temps pour reprendre ?

Si vous ne savez pas répondre, l'outil n'est pas votre problème — c'est le process.

# Combo hybrides qui marchent en 2026

Les meilleurs projets qu'on livre ne sont pas "100 % Make" ou "100 % code". Ce sont des combos :

- **Make pour l'orchestration**, **code custom pour la logique métier** (appelée via webhook)
- **Zapier pour les déclencheurs marketing**, **Make pour les flux opérationnels**
- **Code custom pour le cœur**, **Make pour les intégrations externes**

Chaque outil fait ce qu'il fait le mieux, et personne ne lutte contre ses limites.

# FAQ

**n8n est-il une alternative à Make ?**
Oui, sérieuse. n8n est open-source, auto-hébergeable, et souvent moins cher à volume. Mais la maintenance d'une instance auto-hébergée demande des compétences tech, et la communauté est plus petite. Pour une PME sans IT, Make reste plus accessible.

**Peut-on vraiment remplacer un CRM complet avec Make ?**
Pas complètement. Make orchestre, mais un CRM (HubSpot, Pipedrive) reste nécessaire pour stocker les données clients de manière structurée. La bonne archi : le CRM stocke, Make orchestre, le code custom (optionnel) fait la logique complexe.

**Comment on compte les "tasks" ou les "operations" ?**
Chaque outil a sa propre métrique. Zapier compte chaque étape d'un Zap comme une task. Make compte chaque opération (module activé) dans un scénario. Un flux à 4 étapes dans Zapier = 4 tasks, le même flux dans Make = 4 opérations. Mais Make facture au volume, Zapier aussi au volume + par "Zap unique".

---

Sur une trentaine de projets, environ **60 % finissent en Make**, 20 % en Zapier (flux simples), 20 % en code custom (cas spécifiques). Si vous hésitez sur votre cas, l'audit gratuit de 30 minutes permet de trancher en une session.
""",
        },
        "en": {
            "title": "Make vs Zapier vs custom code: which automation tool to choose?",
            "excerpt": "Each tool has its strengths. Here's an honest comparative guide based on real projects delivered in Québec in 2026.",
            "content": """Make, Zapier and custom code aren't direct competitors — they serve different use cases. The trap is trying to do everything with a single tool.

Here's how we decide at Arivex, based on about thirty projects delivered in 2025-2026.

# Zapier: the most accessible, the least powerful

**For whom**: an SMB automating 2-5 simple flows with popular services (Gmail, Slack, HubSpot, Stripe).

**Strengths**
- The simplest interface on the market. A beginner creates a flow in 15 minutes.
- 7,000+ ready integrations, more than any competitor.
- Excellent documentation, massive community.
- Perfect for one-off event triggers ("when an email arrives, send a Slack").

**Weaknesses**
- Pricing climbs fast. A complex flow with 3-4 steps consumes many "tasks". An active SMB can easily exceed $300/month.
- No advanced conditional logic. "Paths" exist but stay limited.
- Bad choice for anything requiring loops or volume processing.

**Typical price**: $20 to $400/month depending on plan and volume.

# Make (formerly Integromat): the sweet spot

**For whom**: an SMB or agency automating 5-20 flows with conditional logic, loops, and data transformations.

**Strengths**
- Flow visualization far superior to Zapier. You see how data flows.
- Native advanced logic: routers, aggregators, iterators, error handling.
- Much better price than Zapier at equivalent volume.
- European and francophone markets well served (French support available).

**Weaknesses**
- Steeper learning curve than Zapier. A beginner sometimes gets discouraged.
- Fewer integrations than Zapier (about 2,000 vs 7,000), but all the main ones are there.
- When a scenario crashes, debugging can be cryptic.

**Typical price**: $10 to $200/month. **It's the best value for most Québec SMBs**.

# Custom code (Python, Node.js): the most flexible, the most expensive to start

**For whom**: a very specific use case, complex business logic, high volume, or integration with an internal system.

**Strengths**
- No technical limits. Anything that can be coded can be automated.
- No third-party platform subscription. You host wherever you want.
- Optimal performance: batch processing, parallelization, caching.
- You own the code. No lock-in risk.

**Weaknesses**
- Higher initial development cost ($3,000 to $15,000 depending on complexity, vs $1,500-$3,000 for an equivalent Make solution).
- Requires a competent provider and solid documentation.
- Long-term maintenance: dependency updates, security, hosting.

**Typical price**: one-shot dev + $20 to $100/month hosting.

# The decision matrix

| Your situation | Recommended tool |
|----------------|-------------------|
| 1-3 simple flows, tight budget | **Zapier** (starter plan) |
| 5-20 flows with logic | **Make** |
| Specific business logic | **Custom code** |
| Volume > 100k operations/month | **Custom code** (Zapier/Make get expensive) |
| Legacy internal system integration | **Custom code** |
| Multi-team automation | **Make** (better governance) |
| Want to maintain in-house without a dev | **Zapier** or **Make** |

# The real criterion we often forget

Beyond the tool, what matters is **the ability to maintain**. A great Make flow built by a provider who disappears is worse than an average Zapier solution maintained in-house.

Before choosing, answer:

1. Who's going to adjust the flow in 6 months if a need changes?
2. Who has access to the account and API secrets?
3. If the provider becomes unavailable, how long to take over?

If you can't answer, the tool isn't your problem — the process is.

# Hybrid combos that work in 2026

The best projects we ship aren't "100% Make" or "100% code". They're combos:

- **Make for orchestration**, **custom code for business logic** (called via webhook)
- **Zapier for marketing triggers**, **Make for operational flows**
- **Custom code for the core**, **Make for external integrations**

Each tool does what it does best, and no one fights its limits.

# FAQ

**Is n8n an alternative to Make?**
Yes, a serious one. n8n is open-source, self-hostable, often cheaper at volume. But maintaining a self-hosted instance requires tech skills, and the community is smaller. For an SMB without IT, Make remains more accessible.

**Can Make really replace a full CRM?**
Not entirely. Make orchestrates, but a CRM (HubSpot, Pipedrive) is still needed to store client data in a structured way. The right architecture: CRM stores, Make orchestrates, custom code (optional) handles complex logic.

**How are "tasks" or "operations" counted?**
Each tool has its own metric. Zapier counts each step of a Zap as a task. Make counts each operation (activated module) in a scenario. A 4-step flow in Zapier = 4 tasks, the same flow in Make = 4 operations. But Make bills by volume, Zapier by volume + per "unique Zap".

---

Across about thirty projects, around **60% end up in Make**, 20% in Zapier (simple flows), 20% in custom code (specific cases). If you're unsure about your case, the free 30-minute audit lets us decide in one session.
""",
        },
    },
]


# ─── Seed ─────────────────────────────────────────────────────────────────

created = 0
updated = 0

for art in ARTICLES:
    group = uuid.uuid4()
    tag_objs = [_tag(t) for t in art["tags"]]

    for lang in ("fr", "en"):
        data = art[lang]
        post, was_created = BlogPost.objects.update_or_create(
            slug=art["slug"],
            language=lang,
            defaults={
                "title": data["title"],
                "excerpt": data["excerpt"],
                "content": data["content"],
                "category": cat_objs[art["category_slug"]],
                "cover_image": art["cover_image"],
                "reading_time": art["reading_time"],
                "featured": art["featured"],
                "status": "published",
                "published_at": art["published_at"],
                "translation_group": group,
                "author": "Darius Tokam",
            },
        )
        post.tags.set(tag_objs)
        if was_created:
            created += 1
        else:
            updated += 1
        print(f"  {'✔ created' if was_created else '↻ updated'}: {art['slug']} [{lang}]")

print(f"\nDone. {created} created, {updated} updated.")
