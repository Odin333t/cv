from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

IMG_FOLDER = 'images'
os.makedirs(IMG_FOLDER, exist_ok=True)

# Optional: warn if images are missing
required_images = [
    'hero_photo.jpg', 'suit_pants.jpg', 'grilling_prototype.jpg',
    'taskflow_dashboard.jpg', 'tech_background.jpg'
]
for img in required_images:
    if not os.path.exists(os.path.join(IMG_FOLDER, img)):
        print(f"Warning: Missing 'images/{img}' – add for full visual experience")

if not os.path.exists('cv.pdf'):
    print("Note: Place 'cv.pdf' in the root folder for CV download functionality")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Odin Osayande | Fullstack Developer</title>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent: #60a5fa;
            --accent-yellow: #facc15;
            --border: #334155;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { 
            font-family: 'Inter', system-ui, sans-serif; 
            background: var(--bg-primary); 
            color: var(--text-primary); 
            line-height: 1.6;
        }
        .container { max-width: 1280px; margin: 0 auto; padding: 0 1.5rem; }
        header { 
            position: fixed; top: 0; left: 0; right: 0;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            z-index: 1000;
        }
        nav { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 0; }
        .logo { font-size: 1.9rem; font-weight: 800; color: var(--accent-yellow); }
        .nav-links { display: flex; gap: 2.5rem; }
        .nav-links a { color: var(--text-secondary); text-decoration: none; font-weight: 500; transition: color 0.3s; }
        .nav-links a:hover { color: var(--accent-yellow); }
        .menu-toggle { display: none; font-size: 2.2rem; cursor: pointer; color: var(--accent-yellow); }
        .theme-toggle { background: none; border: none; font-size: 1.7rem; cursor: pointer; color: var(--accent-yellow); }
        .mobile-menu { 
            position: fixed; top: 0; left: -100%;
            width: 85%; max-width: 380px; height: 100vh;
            background: var(--bg-secondary);
            padding: 3rem 2rem;
            transition: left 0.4s ease;
            z-index: 2000;
        }
        .mobile-menu.open { left: 0; }
        .overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 1500; }
        .overlay.active { display: block; }
        .hero {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
            background: url('/images/tech_background.jpg') no-repeat center/cover fixed;
            position: relative;
        }
        .hero::before { content: ''; position: absolute; inset: 0; background: rgba(15,23,42,0.78); }
        .hero-content { position: relative; z-index: 1; padding: 2rem 0; }
        .suit-banner { width: 100%; max-width: 960px; margin: 0 auto 3rem; border-radius: 1.5rem; border: 5px solid var(--accent-yellow); box-shadow: 0 12px 40px rgba(0,0,0,0.7); }
        .hero-photo { width: 260px; height: 260px; border-radius: 50%; object-fit: cover; border: 8px solid var(--accent-yellow); margin: 2.5rem auto; display: block; }
        .hero h1 { font-size: 4.5rem; color: var(--accent-yellow); margin-bottom: 0.8rem; }
        .hero p { font-size: 1.5rem; max-width: 800px; margin: 1.5rem auto; color: var(--text-secondary); }
        .btn {
            display: inline-block;
            padding: 1.1rem 2.5rem;
            background: var(--accent-yellow);
            color: #0f172a;
            font-weight: 700;
            border-radius: 999px;
            margin: 1rem 0.8rem;
            transition: all 0.3s;
            text-decoration: none;
        }
        .btn:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(250,204,21,0.4); }
        section { padding: 10rem 0 8rem; }
        h2 { font-size: 3.5rem; text-align: center; margin-bottom: 4rem; color: var(--accent-yellow); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 3rem; }
        .card { background: var(--bg-secondary); padding: 2.5rem; border-radius: 1.5rem; border: 1px solid var(--border); }
        .project-img { width: 100%; height: 220px; object-fit: cover; border-radius: 1rem; margin-bottom: 1.5rem; }
        footer { text-align: center; padding: 5rem 0; background: var(--bg-secondary); color: var(--text-secondary); }
        @media (max-width: 768px) {
            .nav-links, .theme-toggle { display: none; }
            .menu-toggle { display: block; }
            .hero h1 { font-size: 3.2rem; }
            .hero-photo { width: 220px; height: 220px; }
        }
    </style>
</head>
<body data-theme="dark">
    <header>
        <div class="container">
            <nav>
                <div class="logo">Odin.dev</div>
                <div class="nav-links">
                    <a href="#about">About</a>
                    <a href="#skills">Skills</a>
                    <a href="#experience">Experience</a>
                    <a href="#projects">Projects</a>
                    <a href="#contact">Contact</a>
                </div>
                <div style="display: flex; align-items: center; gap: 1.8rem;">
                    <button class="theme-toggle" onclick="toggleTheme()">☀️</button>
                    <div class="menu-toggle" onclick="toggleMenu()">☰</div>
                </div>
            </nav>
        </div>
    </header>

    <div class="overlay" onclick="toggleMenu()"></div>
    <div class="mobile-menu" id="mobileMenu">
        <div class="mobile-menu-header">
            <div class="logo">Odin.dev</div>
            <button onclick="toggleMenu()" style="font-size: 2.8rem; cursor: pointer; background: none; border: none; color: var(--accent-yellow); padding: 0;">✕</button>
        </div>
        <div class="mobile-menu-links" style="display: flex; flex-direction: column; gap: 1.2rem; margin: 2rem 0;">
            <a href="#about" class="btn" style="text-align: center; margin: 0;">About</a>
            <a href="#skills" class="btn" style="text-align: center; margin: 0;">Skills</a>
            <a href="#experience" class="btn" style="text-align: center; margin: 0;">Experience</a>
            <a href="#projects" class="btn" style="text-align: center; margin: 0;">Projects</a>
            <a href="#contact" class="btn" style="text-align: center; margin: 0;">Contact</a>
        </div>
        <div class="mobile-cta" style="display: flex; flex-direction: column; gap: 1rem; margin-top: 2rem;">
            <a href="/download_cv" class="btn-yellow" style="text-align: center; margin: 0;">↓ Download CV</a>
            <a href="#projects" class="btn-yellow" style="text-align: center; margin: 0;">View Projects</a>
            <a href="#contact" class="btn-dark" style="text-align: center; margin: 0;">Get In Touch</a>
        </div>
    </div>

    <section class="hero" id="home">
        <div class="hero-content">
            <img src="/images/suit_pants.jpg" alt="Professional" class="suit-banner">
            <img src="/images/hero_photo.jpg" alt="Odin Osayande" class="hero-photo">
            <h1>Odin Osayande</h1>
            <p>Junior Fullstack Developer & UI/UX Enthusiast</p>
            <p>Building modern web solutions • Benin City, Nigeria</p>
            <div>
                <a href="#projects" class="btn">View Projects</a>
                <a href="/download_cv" class="btn">Download CV</a>
            </div>
        </div>
    </section>

    <!-- About Me -->
    <section id="about">
        <div class="container">
            <h2>About Me</h2>
            <div class="card" style="max-width: 900px; margin: 0 auto; text-align: center;">
                <img src="/images/hero_photo.jpg" alt="Odin Osayande" class="hero-photo" style="margin-bottom: 2rem;">
                <p style="font-size: 1.2rem; line-height: 1.8;">
                    Mechanical Engineering graduate (July 2024) transitioning into fullstack development.<br>
                    Proficient in C#, Python (Flask/Django), Node.js, React, and UI/UX design.<br><br>
                    Delivered responsive web applications, RESTful APIs, and a hardware-integrated automation prototype.<br>
                    Passionate about building intuitive, user-centered digital solutions.<br><br>
                    Seeking junior fullstack, frontend, or UI/UX developer roles.
                </p>
                <p style="margin-top: 2rem; font-weight: 500;">
                    38 Ehioghea, Off Sapere Road, Benin City, Edo State, Nigeria<br>
                    (+234) 807-315-6249 | odinosayande@gmail.com
                </p>
            </div>
        </div>
    </section>

    <!-- Skills -->
    <section id="skills" style="background: var(--bg-secondary);">
        <div class="container">
            <h2>Skills</h2>
            <div class="grid">
                <div class="card">
                    <h3>Languages & Frameworks</h3>
                    <p>C#, Python (Flask, Django), Node.js, JavaScript, React, Angular, HTML5, CSS3 (Tailwind/Bootstrap)</p>
                </div>
                <div class="card">
                    <h3>Databases</h3>
                    <p>SQLite, MySQL, MongoDB</p>
                </div>
                <div class="card">
                    <h3>Tools & Platforms</h3>
                    <p>Git, GitHub, Figma, Adobe XD, Postman, VS Code, Arduino, MS Office, Vercel/Netlify</p>
                </div>
                <div class="card">
                    <h3>Specialties</h3>
                    <p>Fullstack Web Apps • RESTful APIs • Responsive Design • UI/UX Prototyping • Hardware-Software Integration • Data Visualization</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience -->
    <section id="experience">
        <div class="container">
            <h2>Experience</h2>
            <div class="grid">
                <div class="card">
                    <h3>Freelance Web Developer</h3>
                    <p><strong>Self-Employed • Benin City, Nigeria • Jul 2024 – Present</strong></p>
                    <ul style="margin-top: 1rem; padding-left: 1.5rem; line-height: 1.7;">
                        <li>Developed 10+ responsive websites and dashboards (100% cross-browser/mobile compatibility)</li>
                        <li>Designed UI/UX prototypes in Figma → +45% user satisfaction</li>
                        <li>Integrated contact forms with Nodemailer → 60% faster inquiry response</li>
                        <li>Added dark mode to 5 sites using CSS variables + localStorage</li>
                        <li>Optimized performance (lazy loading, image compression) → -35% load time</li>
                        <li>Created reusable React components → 30% faster subsequent development</li>
                    </ul>
                </div>

                <div class="card">
                    <h3>Capstone Project: Smart Meat Grilling Automation System</h3>
                    <p><strong>University of Benin Final Year Project • Mar – Jul 2024</strong></p>
                    <img src="/images/grilling_prototype.jpg" alt="Grilling Prototype" class="project-img">
                    <ul style="margin-top: 1rem; padding-left: 1.5rem; line-height: 1.7;">
                        <li>Built unsupervised electric grilling system with temperature sensors & relays</li>
                        <li>Developed C# WinForms GUI with real-time charting & auto-shutoff</li>
                        <li>Achieved ±1.5°C sensor accuracy</li>
                        <li>Implemented overheat detection & automatic power cutoff</li>
                        <li>Optimized algorithm → 25% reduction in grilling time variability</li>
                        <li>Ranked among top 5 most innovative projects in cohort</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects -->
    <section id="projects" style="background: var(--bg-secondary);">
        <div class="container">
            <h2>Projects</h2>
            <div class="grid">
                <div class="card">
                    <h3>Personal Portfolio Website</h3>
                    <p>Modern single-page portfolio with dark mode, smooth animations, Google Analytics, and backend contact API</p>
                    <p><strong>Tech:</strong> React, Tailwind CSS, Figma, Vercel</p>
                    <p><strong>Live:</strong> <a href="https://odin-osayande.vercel.app" target="_blank">odin-osayande.vercel.app</a></p>
                </div>

                <div class="card">
                    <h3>TaskFlow – Task Management App</h3>
                    <img src="/images/taskflow_dashboard.jpg" alt="TaskFlow Dashboard" class="project-img">
                    <p>Fullstack CRUD application with authentication, drag-and-drop, search/filtering, offline support</p>
                    <p><strong>Tech:</strong> React, Node.js/Express, MongoDB, JWT</p>
                    <p><strong>GitHub:</strong> <a href="https://github.com/odin-osayande/taskflow" target="_blank">github.com/odin-osayande/taskflow</a></p>
                </div>

                <div class="card">
                    <h3>GrillMaster Control Desktop App</h3>
                    <p>Desktop interface for capstone grilling system with real-time sensor visualization and safety controls</p>
                    <p><strong>Tech:</strong> C#, WinForms, Arduino Serial, LiveCharts</p>
                    <p><strong>GitHub:</strong> <a href="https://github.com/odin-osayande/grillmaster" target="_blank">github.com/odin-osayande/grillmaster</a></p>
                </div>
            </div>
        </div>
    </section>

    <!-- Education -->
    <section id="education">
        <div class="container">
            <h2>Education</h2>
            <div class="card" style="max-width: 800px; margin: 0 auto;">
                <h3>University of Benin</h3>
                <p><strong>Bachelor of Science in Mechanical Engineering</strong><br>Jul 2020 – Jul 2024 • Benin City, Nigeria</p>
                <p>Second Class Honours</p>
                <p style="margin-top: 1rem;"><strong>Relevant Coursework:</strong> Programming for Engineers, Data Structures & Algorithms, Control Systems, Engineering Data Analysis</p>
            </div>
        </div>
    </section>

    <!-- Contact -->
    <section id="contact" style="background: var(--bg-secondary);">
        <div class="container">
            <h2>Contact</h2>
            <div class="card" style="max-width: 700px; margin: 0 auto; text-align: center;">
                <p style="font-size: 1.3rem; margin-bottom: 1.5rem;">
                    Open to junior fullstack, frontend, or UI/UX developer opportunities.<br>
                    Let's build something great together!
                </p>
                <p style="margin: 1.5rem 0; font-weight: 600;">
                    odinosayande@gmail.com<br>
                    (+234) 807-315-6249<br>
                    Benin City, Edo State, Nigeria
                </p>
                <div style="margin-top: 2rem;">
                    <a href="https://odin-osayande.vercel.app" target="_blank" class="btn">View Live Portfolio</a>
                    <a href="https://github.com/odin-osayande" target="_blank" class="btn" style="margin-left: 1rem;">GitHub</a>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <p>Personal Portfolio • All local • Updated January 2026</p>
    </footer>

    <script>
        function toggleTheme() {
            const body = document.body;
            const current = body.getAttribute('data-theme') || 'dark';
            const next = current === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            document.querySelectorAll('.theme-toggle').forEach(el => 
                el.textContent = next === 'dark' ? '☀️' : '🌙'
            );
        }
        function toggleMenu() {
            document.getElementById('mobileMenu').classList.toggle('open');
            document.querySelector('.overlay').classList.toggle('active');
        }
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);
                if (target) {
                    const headerHeight = document.querySelector('header')?.offsetHeight || 80;
                    const offset = -headerHeight - 30;
                    const y = target.getBoundingClientRect().top + window.pageYOffset + offset;
                    window.scrollTo({ top: y, behavior: 'smooth' });
                    if (document.getElementById('mobileMenu').classList.contains('open')) {
                        toggleMenu();
                    }
                }
            });
        });
        window.addEventListener('load', () => {
            const saved = localStorage.getItem('theme') || 'dark';
            document.body.setAttribute('data-theme', saved);
            document.querySelectorAll('.theme-toggle').forEach(el => 
                el.textContent = saved === 'dark' ? '☀️' : '🌙'
            );
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/download_cv')
def download_cv():
    try:
        return send_from_directory('.', 'cv.pdf', as_attachment=True, download_name='Odin_Osayande_CV.pdf')
    except FileNotFoundError:
        return "CV file not found.", 404

if __name__ == '__main__':
    print("Portfolio server starting...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    app.run(debug=False, port=5000, host='0.0.0.0')
