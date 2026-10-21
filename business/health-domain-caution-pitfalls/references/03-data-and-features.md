# health-domain-caution-pitfalls §3 — Data and features

## 3.1 What counts as health data
1. **Treat as health data anything that reveals or lets someone infer a condition**: a diagnosis, a medication, a
   symptom, a clinic visit, a search or a purchase that points to one. Symptom: a free-text field that fills with
   conditions. Check: ask whether a stranger reading the record could infer a health state.
2. **A label on the data does not change what it reveals.** Pseudonymised data can still be health data about a
   person; ask the qualified owner before assuming otherwise.
2b. **Inference and cross-referencing make data health data.** The French data-protection regulator's page on health
   data (read 2026-10-20) defines it as data on a person's past, present or future physical or mental health that
   reveals health status; it distinguishes data that is health data by nature (history, diseases, care, results,
   disability), by cross-referencing (for example weight with step count or calorie intake, blood pressure with
   exertion), and by medical use; a step count alone with no cross-referencing is not. It says wellbeing and sport app
   data may or may not qualify depending on nature and cross-referencing, and that the law does not apply to an app whose
   data is used only by the person, stored locally with no outside connection and kept for personal purposes. This
   supports the inference test above; once the app sends data to a server, assume the qualified owner must decide.
3. **Health data is a special category in many places**, with stricter grounds and duties. The rule that applies
   depends on place and role; the qualified owner decides it (`business/data-protection`).

## 3.2 Collect, keep, share
1. **Collect only what the feature needs to work.** Symptom: a sign-up form asking for conditions the product never
   uses. Fix: remove the field or make the use explicit and optional.
2. **State a retention period and delete at its end**; check that backups and analytics copies follow.
3. **Limit access to named roles and log it.** A support agent does not need a medical history to reset a password.
4. **Do not send health data to a third party or a tool without the qualified owner's approval**, including
   analytics, session recorders, error logs and generated-text services. Check what leaves the system on each page.
5. **Keep health data out of examples, test data and prompts**; use invented values.

## 3.3 Assistants and symptom tools
1. **Say what the tool is and is not at the start**, in plain words: general information, no diagnosis.
2. **Define what it must refuse and hand over**: urgent symptoms, medication changes, diagnoses, minors, crisis
   topics. Test with real-looking messages for each, and keep the tests.
3. **Never present a generated answer as clinical advice**; where a person may act on it with their body, a
   qualified human reviews or answers (`business/ai-content-disclosure-and-provenance-pitfalls`).
4. **Log failures and wrong answers and review them** with a qualified person on a schedule.
5. **Do not make a clinical performance claim** (accuracy, sensitivity, outcomes) without evidence the qualified
   owner has reviewed.

## 3.4 Status of the product
1. **Software that diagnoses, monitors or treats may be regulated as a medical product** in some places. Ask the
   regulatory owner before building or marketing such a function. The FDA page read says software functions that meet the
   device definition are regulated whatever the platform, that oversight focuses on software whose failure poses greater
   risk, and that for minimal-risk functions such as helping a user self-manage a condition without specific treatment
   suggestions it generally does not expect premarket review; the page does not cover intended use or claims, and no
   European rule was read. Regulatory status is the qualified owner's call. Re-read 2026-10-20: the FDA page still says software meeting the
   device definition is covered whatever the platform, and that for minimal-risk software helping a patient
   self-manage without specific treatment suggestions, or automating simple tasks for providers, it intends to use
   enforcement discretion and does not expect premarket submissions; the European guidance on qualifying software
   as a medical device could not be opened (not found), so no European rule was read.
2. **Describe the function honestly in the product copy**; do not name an intended medical purpose in marketing
   that the product team has not scoped.
3. **Keep a record of the decisions and who took them.**
