"""Facts shared by every design. Edit here, then rerun the generator in scripts/."""

NAME = "Krishna Raju S"
EMAIL = "krishnarajus2004@gmail.com"
LINKEDIN = "linkedin.com/in/krishnarajus2004"

STATS = [  # (value, label)
    ("9", "apps in production"),
    ("128", "tests guarding dispatch"),
    ("30m→30s", "one chore, automated"),
    ("#7", "of 1500+ colleges"),
]

# slug, icon, name, status, url (None = private), hook, detail, stack
PROJECTS = [
    ("dispatch", "🚚", "Dispatch Management", "PRODUCTION", "https://github.com/KRISH-exe-29/Dispatch-ITTL",
     "Work order to gate pass, zero phone calls.", "5 roles · 128 tests · auto escalations", "React 19 · Supabase · PL/pgSQL"),
    ("job-lens", "🔍", "Job Lens", "LIVE DEMO", "https://krishna-ittl.github.io/Candidate-Screener/",
     "100 resumes in. A ranked shortlist out.", "Rubric scoring · ATS checks · offline AI", "TypeScript · Transformers.js · OCR"),
    ("kiosk-sentinel", "🔐", "KioskSentinel", "NEW", None,
     "Attendance that survives power cuts.", "Lock-screen kiosks · offline-first · 3 shifts", "Java 21 · SQLite · PostgreSQL"),
    ("test-planner", "🧪", "Transformer Test Planner", "LIVE DEMO", "https://transformer-test-planner.vercel.app",
     "Every IEC 60076 test, planned per unit.", "Live status board · one-click Excel", "TypeScript · Next.js · Vercel"),
    ("rtcc", "🧰", "RTCC & M.Box Tracker", "IN USE", "https://github.com/KRISH-exe-29/Pannel-Box-Transformers-",
     "Chases pending points so nobody has to.", "48-hour follow-ups · role-based", "React · Express · node-cron"),
    ("fasteners", "🔩", "Fasteners Automation", "IN USE", "https://github.com/KRISH-exe-29/Fasteners-Project",
     "A 30-minute job, now 30 seconds.", "Hardware PDF in · weighted BOM out", "Python · Pandas · PyQt5"),
    ("epms", "📅", "EPMS", "BUILT", "https://github.com/KRISH-exe-29/PMS",
     "Project HQ with an interactive Gantt.", "Milestones · budgets · daily reports", "TypeScript · React · Supabase"),
    ("industrial-data", "📡", "Industrial Data System", "BUILT", "https://github.com/KRISH-exe-29/indotech-transformers",
     "QR-tagged test data with a 3D model.", "QR codes · OTP login · Three.js", "React · Express · Three.js"),
    ("dmat", "🧠", "dMAT Practice", "LIVE APP", "https://krishna-ittl.github.io/dmat-practice/",
     "A full exam simulator in one HTML file.", "Timed mocks · 990 checks · offline", "HTML · CSS · JavaScript"),
    ("shop-floor", "🏭", "Shop Floor Job Status", "IN DESIGN", None,
     "Live job status for every bay.", "Cycle-time norms · worker efficiency", "Requirements · flowcharts"),
]

MILESTONES = [  # year, title, detail
    ("2024", "National finalist", "Technical symposium"),
    ("2025", "Patent holder", "Street-light fault detection"),
    ("2025", "Rank #7 of 1500+", "IIT Bombay NEC"),
    ("2025", "Runner-up", "Fish Tank, IIT B E-Summit"),
    ("2026", "9 apps shipped", "Indo Tech Transformers"),
]

TOOLS = {
    "Factory floor": ["IEC 60076 testing", "MCC panels", "Protection relays", "OLTC", "ESP8266", "Proteus"],
    "Code": ["TypeScript", "React", "Next.js", "Python", "Java", "Node", "Supabase", "PostgreSQL", "Three.js"],
    "AI": ["Claude", "OpenAI", "LangChain", "LangGraph", "Transformers.js", "Tesseract"],
}
