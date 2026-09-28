# Secure User Registration & Semantic Input Validation Engine

A hardened user onboarding and identity validation service built with Python and Flask. The system implements defense-in-depth sanitization, NIST-aligned password policy enforcement, domain-restricted semantic verification, cryptographic CSRF mitigation, and contextual security auditing to prevent client-side injection attacks.

---

## Security Architecture & Core Capabilities

```text
[ Incoming HTTP POST ]
         │
         ▼
[ Flask-WTF CSRF Validation ]
         │
         ▼
[ Custom WTForms Semantic Validators ]
   ├── Reserved Identity Filter (admin, root, superuser)
   ├── Domain Whitelist Verifier (.edu, .ac.uk, .org)
   └── NIST SP 800-63B Password Complexity & Dictionary Engine
         │
         ├─► [ Validation Failure ] ──► [ Security Audit Logger (WARNING + IP + UTC) ]
         │
         ▼
[ Dynamic Content Sanitization Pipeline (Bleach) ]
   └── Strict Tag & Attribute Whitelist Stripping
         │
         ▼
[ Safe Jinja2 Auto-Escaped Rendering & Simulated State Persistence ]
         │
         ▼
[ Security Audit Logger (INFO + Client IP + Event Context) ]