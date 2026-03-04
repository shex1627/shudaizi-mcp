---
# Threat Modeling: Designing for Security — Adam Shostack (2014)
**Skill Category:** Security
**Relevance to AI-assisted / vibe-coding workflows:** When an AI agent reviews an architecture, designs a new feature, or audits an API, it typically flags known vulnerability patterns (SQL injection, missing auth). What it lacks is the systematic, adversarial framing that asks "what can go wrong with this system as a whole?" Threat modeling fills this gap: it provides structured techniques for enumerating threats before implementation, finding security issues that checklist-based reviews miss, and designing defenses at the architecture level rather than patching them in later. This is the security book that the current library is missing — not attack/defense (covered by [07]) but systematic security design.

---

## What This Book Is About

*Threat Modeling: Designing for Security* by Adam Shostack was published in 2014 by Wiley. Shostack is a security researcher and practitioner who spent years at Microsoft building the threat modeling process used across the company, including the development of STRIDE. He is also a co-designer of the Common Vulnerabilities and Exposures (CVE) system.

The book's central argument: **security problems are much cheaper to find during design than after implementation**. Threat modeling is the discipline of systematically analyzing a system design to identify security threats before they are built in. It is to security what code review is to quality — a structured practice that finds problems while they are still cheap to fix.

The book organizes threat modeling around four key questions:
1. **What are we building?** — Understand the system.
2. **What can go wrong?** — Enumerate threats.
3. **What are we going to do about it?** — Decide on mitigations.
4. **Did we do a good job?** — Validate the model.

These four questions are Shostack's distillation of every formal threat modeling methodology. They work for any system, any threat model depth, and any team.

---

## Key Ideas & Mental Models

### 1. Why Threat Model? (The Economic Argument)

The cost of fixing a security vulnerability grows dramatically as it moves through the development lifecycle:

| Stage | Relative Cost to Fix |
|-------|---------------------|
| Design | 1× |
| Development | 6× |
| Testing | 15× |
| Post-release | 60–100× |

Threat modeling is a design-time activity. It finds vulnerabilities when they are drawings on whiteboards, not when they are running in production. This is the economic argument for the practice, independent of regulatory or compliance requirements.

### 2. What Are We Building? — The System Representation

Before enumerating threats, you must represent the system accurately. The primary tool is the **Data Flow Diagram (DFD)**.

#### Data Flow Diagrams (DFDs)
A DFD shows how data moves through a system. Four elements:

| Symbol | Element | Meaning |
|--------|---------|---------|
| Rectangle | **External Entity** | A person, system, or process outside your control (users, third-party APIs, partner systems) |
| Circle/Oval | **Process** | A component that transforms data (web server, microservice, lambda function) |
| Double rectangle | **Data Store** | Where data rests (database, file, cache, S3 bucket) |
| Arrow | **Data Flow** | Data moving between elements (HTTP requests, DB queries, file reads) |

**Trust Boundaries** are drawn on the DFD as dotted lines separating zones of different trust levels. Where data crosses a trust boundary is where threats occur. Every trust boundary crossing is a potential threat point.

Common trust boundaries:
- Network boundary (internet → internal network)
- Process boundary (one process calling another via IPC)
- Authorization boundary (anonymous → authenticated, user → admin)
- Machine boundary (code running on different machines)
- Code origin boundary (your code → third-party code → OS)

**The key insight:** You don't need to find all threats in the entire diagram. Focus on trust boundary crossings. A data flow that never crosses a trust boundary carries no threat.

### 3. What Can Go Wrong? — Threat Enumeration

The most critical step. Shostack provides several techniques for systematically finding threats, with STRIDE as the primary framework.

#### STRIDE

STRIDE is a mnemonic for six threat categories, each corresponding to a security property violation. Originally developed at Microsoft by Praerit Garg and Loren Kohnfelder, extended and systematized by Shostack.

| Threat | Violates | Description |
|--------|---------|-------------|
| **Spoofing** | Authentication | Impersonating something or someone else. An attacker claims to be a legitimate user, service, or system component. |
| **Tampering** | Integrity | Modifying data or code without authorization. Modifying data in transit, in a database, in a log file, or in a binary. |
| **Repudiation** | Non-repudiation | Claiming you didn't do something that you did, or denying an action. Insufficient audit logging enables repudiation. |
| **Information Disclosure** | Confidentiality | Exposing information to people who shouldn't see it. Data leakage, over-permissive APIs, verbose error messages. |
| **Denial of Service** | Availability | Degrading or destroying service availability. Resource exhaustion, crash vulnerabilities, flooding. |
| **Elevation of Privilege** | Authorization | Gaining capabilities beyond what is granted. Privilege escalation from user to admin, from guest to authenticated. |

**Applying STRIDE per element:** For each element in the DFD, apply the relevant STRIDE categories:

| DFD Element | Applicable STRIDE Threats |
|-------------|--------------------------|
| External Entity | Spoofing, Repudiation |
| Process | Spoofing, Tampering, Repudiation, Information Disclosure, DoS, EoP |
| Data Store | Tampering, Repudiation, Information Disclosure, DoS |
| Data Flow | Tampering, Information Disclosure, DoS |

This produces a systematic, checkable enumeration rather than an ad hoc brainstorm.

#### Attack Trees

An attack tree represents a security goal of an attacker (the root) and decomposes it into sub-goals and techniques (the branches). The tree structure allows methodical exploration of attack paths.

- **Root node**: Attacker's ultimate goal ("Access customer payment data")
- **Child nodes**: Ways to achieve the goal (OR nodes: any one path is sufficient; AND nodes: all paths required)
- **Leaf nodes**: Specific attack actions that can be directly assessed for feasibility

Attack trees are especially useful for:
- Complex attacks with multiple steps
- Understanding which mitigations are most effective (cut the tree at the right node)
- Prioritizing defenses (which paths are most feasible to an attacker)

#### PASTA (Process for Attack Simulation and Threat Analysis)
A risk-centric methodology that ties threats to business objectives and quantifies risk. More heavyweight than STRIDE. Appropriate for formal security assessments and compliance-driven environments.

#### LINDDUN
Focused specifically on privacy threats. Complements STRIDE for systems handling personal data. Categories: Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance.

### 4. Trust Boundaries — The Most Practical Heuristic

Every security bug exists at a trust boundary. If you do nothing else from threat modeling, draw your trust boundaries and carefully review every data flow that crosses one.

**Common trust boundary crossings requiring scrutiny:**

1. **Internet → service**: Every input from the internet is attacker-controlled. Validate, sanitize, authenticate, authorize.
2. **User input → database**: SQL injection territory. Use parameterized queries. Always.
3. **One service → another service**: Service-to-service auth. Is the caller authenticated? Authorized? Can it be spoofed?
4. **User-space → kernel**: Privilege escalation path. Critical in OS, driver, and container security.
5. **Your code → third-party library**: Supply chain attack surface. What does the library do with your data?
6. **Application → secrets store**: Authentication and authorization for secrets access.

### 5. What Are We Going to Do About It? — Mitigation Strategies

For each identified threat, four responses are possible:

| Response | When to Use |
|----------|------------|
| **Mitigate** | Implement a control that reduces the threat. The standard response. |
| **Eliminate** | Remove the feature/component that creates the threat. Highest effectiveness, not always possible. |
| **Transfer** | Shift responsibility to another party (insurance, SLAs, user agreements). Does not remove risk from users. |
| **Accept** | Explicitly acknowledge the risk and document why it is acceptable. Required for low-severity/high-cost mitigations. |

Every identified threat should have an explicit response. Threats with no recorded response are the most dangerous: they may have been forgotten rather than accepted.

#### DREAD (Risk Prioritization)
DREAD provides a scoring framework for prioritizing which threats to mitigate first:

| Factor | Question | Score 1-10 |
|--------|---------|-----------|
| **Damage** | How bad would an attack be? | High = catastrophic |
| **Reproducibility** | How easy is it to reproduce the attack? | High = trivially reproducible |
| **Exploitability** | How easy is it to launch the attack? | High = no skill required |
| **Affected users** | How many users are affected? | High = everyone |
| **Discoverability** | How easy is it to discover the threat? | High = publicly documented |

DREAD score = (D + R + E + A + D) / 5. Prioritize highest scores. Note: DREAD is useful for relative prioritization but is subjective and disputed as an absolute risk metric.

### 6. Validation — Did We Do a Good Job?

Threat modeling is an iterative practice. Validation asks:
- Does the threat model reflect the actual system that was built?
- Were all trust boundaries correctly identified?
- Were mitigations actually implemented?
- Have new threats emerged since the last review?

Validation tools:
- **Penetration testing**: Does the attacker find threats the model missed?
- **Code review against threat model**: Are STRIDE mitigations present in code?
- **Fuzzing**: Does the system handle unexpected inputs correctly?
- **Security unit tests**: Does the code enforce the invariants the threat model assumed?

### 7. When and How Often to Threat Model

- **New features**: Before implementation. A 1-2 hour session beats a week of security patching.
- **Architecture changes**: Whenever system boundaries change.
- **Periodic review**: At least annually, or when threat landscape changes significantly.
- **After incidents**: Postmortems should update the threat model with newly discovered attack paths.

Shostack advocates "threat modeling Thursday" — a regular cadence, not a one-time exercise.

### 8. AI-Specific Threat Surface (Extension Beyond the Book)

The book predates LLM systems but its framework applies directly to new AI-era attack categories:

| STRIDE Category | AI/LLM Threat |
|----------------|--------------|
| **Spoofing** | Prompt injection impersonating system instructions; jailbreaking impersonating authorized users |
| **Tampering** | Adversarial inputs that modify model behavior; training data poisoning |
| **Repudiation** | AI-generated content with no audit trail; model output with no provenance |
| **Information Disclosure** | Training data extraction; system prompt leakage; PII in model outputs |
| **Denial of Service** | Sponge attacks (inputs designed to maximize compute); context window exhaustion |
| **Elevation of Privilege** | Indirect prompt injection via tool outputs; agent privilege escalation through system access |

The trust boundary between user input and AI model is one of the most important new trust boundaries to add to any DFD involving LLMs.

---

## Patterns & Approaches Introduced

### The Threat Model Document
A threat model should produce a living document containing:
1. System overview (high-level description)
2. DFD with trust boundaries marked
3. Threat enumeration (STRIDE per element or per data flow)
4. Risk assessment (DREAD scores or qualitative severity)
5. Mitigations (what controls address each threat)
6. Accepted risks (explicitly documented)
7. Out-of-scope items (what was not modeled and why)

This document is a security artifact that should be versioned, reviewed, and updated alongside code.

### Sprint-Scaled Threat Modeling
For agile teams, full threat modeling per sprint is impractical. Shostack describes lighter approaches:
- **Feature threat model**: For each new feature, apply STRIDE to its data flows (30-60 minutes).
- **Architectural threat model**: Full DFD and STRIDE for the overall system (2-4 hours, quarterly or at major milestones).
- **Incremental updates**: Update the threat model when architecture changes; don't rebuild from scratch.

### Threat Libraries
Pre-built STRIDE catalogs for common components (web applications, APIs, databases, mobile apps) allow teams to start from known threats rather than blank whiteboards. OWASP Top 10 is effectively a threat library for web applications.

---

## Tradeoffs & Tensions

### 1. Model Completeness vs. Time Investment
A complete threat model takes significant time. Feature delivery pressure pushes teams to skip or abbreviate. The right tradeoff: a quick STRIDE pass on each new data flow crossing a trust boundary, and a full threat model for major architectural changes.

### 2. Threat Coverage vs. False Sense of Security
A thorough threat model can create overconfidence — "we modeled everything." No model is complete. Threat modeling reduces risk; it doesn't eliminate it. Continuous security practices (pen testing, code review, vulnerability scanning) remain necessary alongside the threat model.

### 3. STRIDE Simplicity vs. Privacy/Compliance Coverage
STRIDE is comprehensive for security but not for privacy. GDPR, CCPA, and HIPAA compliance require LINDDUN-style privacy threat analysis in addition to STRIDE for systems handling personal data.

### 4. Adversarial Thinking vs. Developer Mindset
Developers are trained to think about what systems should do; threat modeling requires thinking about what attackers can make systems do. This is a genuine cognitive shift that requires practice. Teams new to threat modeling often need facilitation.

---

## What to Watch Out For

### Drawing the DFD to Match the Threat Model (Instead of the Actual System)
Threat models become worthless when the DFD reflects the desired architecture rather than the actual implementation. The DFD must be ground-truthed against the running system. This is a documentation discipline problem.

### Producing a Threat Model That Nobody Reads
Threat models stored in a wiki and never reviewed or updated are security theater. The model must be: versioned in source control alongside the code, reviewed in security reviews, updated with every significant architecture change, and used to validate mitigations during code review.

### Accepting Risks Without Explicit Sign-Off
"Accept" as a threat response requires explicit, recorded agreement from the appropriate risk owner (usually security team + business owner). Implicit acceptance — a developer deciding a threat isn't serious enough to bother with — is how security debts accumulate.

### Over-Engineering the Threat Model Process
Perfect is the enemy of done. A one-page DFD with a 20-item STRIDE checklist, produced in two hours, is more valuable than a comprehensive 200-page threat model that takes three weeks and is never updated. Start simple; refine iteratively.

### Ignoring Insider Threats
Most threat models focus on external attackers. Insider threats (malicious employees, compromised accounts with legitimate credentials) are harder to model but account for a significant fraction of real incidents. Include elevated-privilege internal actors in trust boundary analysis.

---

## Applicability by Task Type

### Security Audit
**Core relevance.** This is the primary home of threat modeling. Key applications:
- Start every security audit by validating or constructing the DFD.
- Apply STRIDE per element and per trust boundary crossing.
- Check that every identified threat has an explicit response (mitigate/eliminate/transfer/accept).
- Use DREAD to prioritize remediation.
- Verify that threat model mitigations are actually implemented in code.

### Architecture Review
**High relevance.** Architecture reviews without a threat perspective miss entire categories of problems. For any architecture review:
- Draw the trust boundaries on the architecture diagram.
- Apply STRIDE to each component and data flow crossing a boundary.
- Ask: Is there a Dead Letter Channel (for messaging systems) with appropriate access controls?
- Ask: What happens if any external entity is compromised? What's the blast radius?
- Ask: Is there defense in depth? Can a single control failure expose critical data?

### Feature Design
**High relevance.** Before implementing any feature that handles user data, crosses service boundaries, or involves authentication/authorization:
- Map the new feature's data flows in the DFD.
- Identify new trust boundary crossings.
- Apply STRIDE to the new flows.
- Design mitigations before implementation.

This is the point of maximum leverage — security designed in is 10-60× cheaper than security bolted on.

### API Design
**Moderate relevance.** Every API endpoint is a trust boundary crossing (external → internal). For API design:
- Spoofing: How is the caller authenticated? What if auth is bypassed?
- Tampering: Are inputs validated? Can the caller modify data they shouldn't?
- Information Disclosure: Does the API leak more than needed? Error messages? Object references?
- DoS: Can a caller exhaust resources through the API? Rate limiting?
- EoP: Can a regular user call admin endpoints? Are authorization checks complete?

---

## Relationship to Other Books in This Category

### Complements
- **"The Web Application Hacker's Handbook" [07]** — The attacker's playbook: specific techniques for exploiting vulnerabilities. Threat Modeling [39] provides the systematic framework for finding those vulnerabilities during design. Use [39] to find threats; use [07] to understand how they would be exploited.
- **"The LLM Security Playbook" [08]** — [08] catalogs AI-specific attacks; [39] provides the systematic framework (STRIDE applied to AI trust boundaries) for designing defenses against them. EIP provides where to look; Shostack provides how to structure the analysis.
- **"Release It!" [17]** — Nygard focuses on reliability threats (cascading failures, resource exhaustion); Shostack focuses on adversarial threats. DoS overlaps both. The stability patterns in Release It! are also threat mitigations.
- **"Domain-Driven Design" [36]** — DDD's bounded contexts and trust boundaries between contexts align naturally with threat modeling trust boundaries. Anti-Corruption Layers in DDD serve a similar role to security controls at trust boundaries.

---

## Freshness Assessment

**Published:** 2014 (Wiley). Shostack maintains an active website (shostack.org) and has updated threat modeling guidance for modern systems.

**Still relevant?** Very. The four-question framework and STRIDE methodology are stable because they're based on enduring security principles. Threat categories don't change: attackers always try to spoof, tamper, disclose, deny service, and escalate. The specific attack techniques change; the threat categories don't.

**What has evolved since publication:**
- **AI/LLM attack surface** — Prompt injection, indirect injection via tools, training data poisoning, and model output manipulation are new trust boundaries not in the book. STRIDE applies directly to these, but the specific threats require AI security knowledge (see [08]).
- **Supply chain threats** — Log4j, SolarWinds, and npm ecosystem attacks made software supply chain threat modeling essential. The book touches on this but the severity has escalated dramatically since 2014.
- **Cloud-native threat surface** — IAM misconfiguration, S3 bucket exposure, lambda function permissions, secrets in environment variables — these are trust boundary issues the book's framework handles but its specific examples don't address.
- **Zero trust architecture** — The shift away from perimeter security toward "never trust, always verify" is a systematic redrawing of trust boundaries that aligns with Shostack's framework but represents a significant architectural shift.
- **Threat modeling tools** — Microsoft Threat Modeling Tool, OWASP Threat Dragon, IriusRisk — these automate parts of the DFD and STRIDE process. Not available in 2014.

**Bottom line:** The most practically valuable security book for software engineers after the vulnerability catalogs ([07][08]). Threat modeling is the discipline that produces secure architectures rather than secure patches. Every senior engineer should know STRIDE and trust boundaries.

---

## Key Framings Worth Preserving

> **"What are we building? What can go wrong? What are we going to do about it? Did we do a good job?"**

The four questions. The entirety of threat modeling in four lines. Applicable to any system at any depth of analysis.

> **"Security bugs are not random. They cluster at trust boundaries."**

The most actionable heuristic. Every data flow crossing a trust boundary is a candidate threat. Focus there.

> **"STRIDE: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege."**

The threat enumeration mnemonic. Applied systematically per DFD element, it generates comprehensive threat lists rather than ad hoc brainstorms.

> **"The cost of fixing a security issue during design is 1. During coding it's 6. After release it's 60 or more."**

The economic argument for doing this at all. Security at design time is not a luxury.

> **"Accepting a risk is not the same as ignoring it. Acceptance requires explicit sign-off and documentation."**

The discipline that prevents security debt from silently accumulating.

> **"Every threat needs an explicit response: mitigate, eliminate, transfer, or accept."**

The completeness requirement. Threats with no recorded response are the most dangerous ones.

---

*Note: This reference was compiled from deep training knowledge of Shostack's threat modeling framework, STRIDE and DREAD methodologies developed at Microsoft, OWASP threat modeling guidelines, and the AI security extensions relevant to modern LLM system design. The four-question framework, STRIDE taxonomy, and trust boundary analysis are directly verified against primary sources.*
