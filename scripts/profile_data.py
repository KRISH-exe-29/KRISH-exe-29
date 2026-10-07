"""Facts about me, shared by every design. Edit here, then rerun the generator in scripts/."""

NAME = "Krishna Raju S"
EMAIL = "krishnarajus2004@gmail.com"
LINKEDIN = "https://linkedin.com/in/krishnarajus2004"
CITY = "Chennai, India"
COLLEGE = "St. Joseph's College of Engineering"
DEGREE = "B.E. Electrical & Electronics"
CGPA = "8.38"
GRAD = "2026"
LANGUAGES = ["Tamil", "English", "Kannada", "Hindi"]
QUOTE = "Engineering isn't just circuits and code. It's building things that make a real difference."

# org, role, when, where, what, win
EXPERIENCE = [
    ("Indo Tech Transformers", "Engineer, Testing & Projects → Digitalisation", "2026 – now", "Kanchipuram",
     "Started in IEC 60076 testing (SFRA, PD, OLTC). Now writes the plant's software.",
     "Fastener standard pitched to the CEO, approved"),
    ("Bühler India", "Automation Hardware Engineering Intern", "Jun 2025", "Bengaluru",
     "MCC panels for 8–10 TPH plants: DOL · VFD · soft-starter feeders, I/O cards.",
     "Built a Python tool: 30 min of paperwork → 30 s"),
    ("Inovate Technologies", "Full Stack Developer Intern", "Mar – Jun 2024", "Chennai",
     "Shipped Project Phantom end to end in HTML, CSS and JavaScript.", "First production deploy"),
    ("Mettur Thermal Power Plant", "Electrical Intern", "Jun – Jul 2024", "Tamil Nadu",
     "Inspected generation-side electrical systems and wrote the reports.", "Saw megawatts up close"),
    ("Southern Railway", "Electrical Intern", "Jan 2023", "Chennai",
     "Electrical documentation and quality inspection on the railway side.", "Where it started"),
]

# slug, name, status, url (None = private), hook, impact, stack
PROJECTS = [
    ("dispatch", "Dispatch Management", "PRODUCTION", "https://github.com/KRISH-exe-29/Dispatch-ITTL",
     "Work order → packing → loading → gate pass.", "5 roles · 128 tests · auto escalations", "React 19 · Supabase · PL/pgSQL"),
    ("job-lens", "Job Lens", "LIVE", "https://krishna-ittl.github.io/Candidate-Screener/",
     "100 resumes in. A ranked shortlist out.", "Offline AI · OCR · Excel reports", "TypeScript · Transformers.js"),
    ("kiosk-sentinel", "KioskSentinel", "NEW", None,
     "Attendance that survives power cuts.", "Offline-first · 3 shifts · locked down", "Java 21 · SQLite · Postgres"),
    ("test-planner", "Test Planner", "LIVE", "https://transformer-test-planner.vercel.app",
     "Every IEC 60076 test, scheduled.", "40 tests · multi-unit · Excel export", "TypeScript · Next.js"),
    ("hardware", "Hardware Platform v1.3", "IN USE", "https://github.com/KRISH-exe-29/Fasteners-Project",
     "Hardware PDF in, weighted BOM out.", "20–30 min → under 60 s", "Python · PyQt5 · Pandas"),
    ("street-light", "Intelligent Street Lighting", "PATENT FILED", None,
     "A light bubble that follows the car.", "60% less energy · GPS fault alerts", "C · ESP8266 · MERN"),
    ("rtcc", "RTCC & M.Box Tracker", "IN USE", "https://github.com/KRISH-exe-29/Pannel-Box-Transformers-",
     "Chases pending points so nobody has to.", "48-hour auto follow-ups", "React · Express · node-cron"),
    ("industrial-data", "Industrial Data System", "LIVE", "https://github.com/KRISH-exe-29/indotech-transformers",
     "QR-tagged test data + a 3D transformer.", "4 role modules · OTP admin", "React · Three.js"),
    ("hwe-tool", "HWE Automation Tool", "SHIPPED", None,
     "Feeder classes, loads and I/O in one click.", "30 min → 30 s at Bühler", "Python · Streamlit"),
    ("flood", "Flood Alerting System", "BUILT", None,
     "Rising water, instant alerts.", "90% lower outage risk", "IoT · Embedded C"),
]

# when, title, where
WINS = [
    ("Feb 2025", "Rank #7 / 1500+", "National Entrepreneurship Challenge, IIT Bombay"),
    ("Feb 2025", "Runner-up", "Fish Tank pitch, IIT Bombay E-Summit"),
    ("Aug 2025", "Patent filed", "Street lighting with automated fault detection"),
    ("Jun 2024", "National finalist", "Technical Symposium, Loyola College"),
]

CERTS = ["Arduino & C · UC Irvine", "Raspberry Pi & Python · UC Irvine", "Intro to IoT · NPTEL",
         "Digital Circuits · NPTEL", "Supply Chain Mgmt · CII"]

SKILLS = {
    "Power": ["IEC 60076 testing", "SFRA", "MCC panels", "VFD · DOL · soft starter", "Relays 87T · 63 · 64REF", "OLTC", "AutoCAD", "MATLAB"],
    "Code": ["TypeScript", "React", "Python", "Java", "C", "Node", "Supabase", "PostgreSQL", "Three.js"],
    "Things": ["ESP8266", "Arduino", "Raspberry Pi", "Proteus", "IoT"],
    "AI": ["Claude", "OpenAI", "LangChain", "LangGraph", "Transformers.js"],
}
