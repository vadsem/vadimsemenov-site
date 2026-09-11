"""Real site content for vadimsemenov.com.

Bio/tagline are DRAFT copy previewing the agreed framing (Harvard front and centre,
Anthropic added). Publication counts are copied from the current live site and still
need checking against ADS before publishing.
"""

NAME = "Vadim Semenov"
TAGLINE = "Computational astrophysicist"
AFFIL = "Center for Astrophysics | Harvard &amp; Smithsonian"
EMAIL = "vadim.semenov@cfa.harvard.edu"

# Served from the site itself. The previous Dropbox share link broke the moment the
# file was replaced -- Dropbox returns HTTP 200 with a "this item was deleted" page,
# so the breakage is invisible to a status-code check.
CV_URL = "VadimSemenov-CV.pdf"

# Main page scrolls between About and Research only; the other two are real pages.
NAV = [
    ("About", "index.html#about"),
    ("Research", "index.html#research"),
    ("Publications", "publications.html"),
    ("Visualizations", "visualizations.html"),
    ("CV", CV_URL),
]

PORTRAIT = "portrait.jpg"

BIO = [
    """I am a computational astrophysicist at the <a href="https://www.cfa.harvard.edu/" target="_blank" rel="noopener">Center for
    Astrophysics | Harvard &amp; Smithsonian</a>, where I have been a
    <a href="https://hubblesite.org/contents/news-releases/2019/news-2019-24.html" target="_blank" rel="noopener">NASA Hubble</a> and
    <a href="https://itc.cfa.harvard.edu/" target="_blank" rel="noopener">ITC</a> Postdoctoral Fellow since 2019. I am spending the
    summer of 2026 at Anthropic as a STEM Fellow. I received my PhD from the
    <a href="https://astro.uchicago.edu/index.php" target="_blank" rel="noopener">University of Chicago</a> in 2019.""",
    """I work at the interface between the physics of the interstellar medium and galaxy formation.
    Together with my collaborators, I design, run, and analyze supercomputer simulations that span
    scales from individual star-forming regions to cosmological volumes. In my current work, I am also
    exploring how next-generation numerical simulations can take advantage of AI and machine learning
    methods.""",
]

INTERESTS = [
    "AI for Science",
    "High Performance Computing",
    "Numerical Methods",
    "Computational Fluid Dynamics",
    "Large-Scale Cosmological Simulations",
]

# Abbreviated CV, grouped by institution. Source: VadimSemenov-CV.pdf.
POSITIONS = [
    ("Anthropic", [
        ("STEM Fellow", "Summer 2026"),
    ]),
    ("Harvard University", [
        ("ITC Fellow", "since 2022"),
        ("NASA Hubble Fellow", "2019&ndash;2022"),
    ]),
]

EDUCATION = [
    ("University of Chicago", [
        ("Ph.D. in Astronomy and Astrophysics", "2019"),
    ]),
    ("Moscow Institute of Physics and Technology", [
        ("B.Sc. &amp; M.Sc. in Applied Math and Physics", "2013"),
    ]),
]

STATS = [
    ("35", "papers"),
    ("14", "first-author"),
    ("9", "led by students"),
    ("20", "h-index"),
    ("1200+", "citations"),
]

RENDERS = [
    ("frame.0396.density.jpg", "cool"),
    ("frame.0425.vmag.jpg", "warm"),
    ("frame.0373.density.jpg", "cool"),
    ("frame.0396.vmag.jpg", "warm"),
    ("frame.0425.density.jpg", "cool"),
]

HERO = "frame.0396.density.jpg"

# Research sections. `papers` renders a faint reference line under each block;
# `video` embeds a figure between the text and the references.
RESEARCH = [
    {
        "id": "current-work",
        "icon": "turbulence.png",
        "kicker": "Current work",
        "title": "Learning what simulations cannot resolve",
        "text": """Modeling turbulent flows on unresolved scales is a general problem in fluid dynamics
        simulations across domains, from aerospace engineering and climate models to astrophysics. In
        each case the grid is far too coarse to follow the motions that still shape the large-scale
        solution, so their effect has to be modeled rather than computed. Such subgrid models are a
        natural place for next-generation simulations to take advantage of AI and machine learning
        methods, and to leverage the rise of GPU computing. In my current work I explore how such
        AI/ML-powered methods can be built into large-scale simulations to incorporate the missing
        physics, learned from expensive but sparse high-fidelity simulation data.""",
        "video": "semenov26-turb",
        "papers": [],
    },
    {
        "id": "first-galaxies",
        "icon": "zoom-logo.png",
        "title": "Modeling the Turbulent Formation of the First Galaxies",
        "text": """Why did galaxies in the early Universe form stars so quickly, and how did they settle
        into disks so soon? The James Webb Space Telescope (JWST) has found far more bright young
        galaxies in the first billion years than expected, and many already show disk morphologies and
        kinematics, which fits earlier evidence from the Atacama Large Millimeter/submillimeter Array
        (ALMA) for cold, rotating gas disks in the young Universe. We find that detailed modeling of
        turbulence in early galaxies is crucial for explaining both of these at once: the early vigorous
        evolution, and the transition to settled disks.""",
        "video": "semenov24-art",
        "papers": [
            ("Semenov", "2026", "How Do Disk Galaxies Form?", "2602.04950"),
            ("Semenov et al.", "2025", "How Early Could the Milky Way&rsquo;s Disk Form?", "2409.18173"),
            ("Semenov et al.", "2025", "From UV-bright Galaxies to Early Disks", "2410.09205"),
        ],
    },
    {
        "id": "milky-way-disk",
        "icon": "mw-logo.png",
        "title": "How Unusual is the Milky Way&rsquo;s Disk?",
        "text": """Did our Galaxy build its disk unusually early? Modern surveys such as Gaia and H3 let us
        reconstruct our Galaxy&rsquo;s history by digging into the kinematics and chemistry of its
        stars, an approach known as Galactic archaeology. We studied the same archaeological signatures
        in simulated Milky Way analogs and found that such galaxies form their disks later on average,
        indicating that the Milky Way is unusual but not rare. Comparisons of this kind let us learn
        about both the physics of galaxy formation in general and the possible history of our own
        Galaxy.""",
        "video": None,
        "papers": [
            ("Semenov et al.", "2024", "Formation of Galactic Disks I", "2306.09398"),
            ("Semenov et al.", "2024", "Formation of Galactic Disks II", "2306.13125"),
            ("Chandra et al.", "2024", "The Three-Phase Evolution of the Milky Way", "2310.13050"),
            ("Beane et al.", "2025", "Rising from the Ashes II: Abundance Bimodality", "2410.21580"),
        ],
    },
    {
        "id": "star-formation",
        "icon": "ngc300-icon.png",
        "title": "Why do galaxies form stars inefficiently?",
        "text": """Galaxies turn their gas into stars remarkably slowly, much slower than any relevant
        dynamical timescale would suggest. This has been one of the biggest puzzles in the physics of
        galaxies for many decades. We developed a framework that ties a galaxy&rsquo;s overall star
        formation rate to how long gas spends in each stage of its life cycle on the scales of
        individual star-forming regions, from assembly into dense star-forming clouds to dispersal by
        the stars they form. The framework explains many puzzles about star formation in galaxies,
        including why it is globally inefficient, the emergent scaling relations, and how it is
        self-regulated in galaxy simulations. The same feedback loop also shapes the structure of the
        gas between stars, so that structure records how the loop operates and enables us to constrain
        the physics of this cycle from observations.""",
        "video": "semenov21-ngc300",
        "papers": [
            ("Semenov et al.", "2017", "The Physical Origin of Long Gas Depletion Times", "1704.04239"),
            ("Semenov et al.", "2018", "How Galaxies Form Stars", "1803.00007"),
            ("Semenov et al.", "2019", "What Sets the Slope of the Molecular KS Relation?", "1809.07328"),
            ("Semenov et al.", "2021", "Spatial Decorrelation of Young Stars and Dense Gas", "2103.13406"),
            ("Kocjan &amp; Semenov", "2026", "The Rhythm of the ISM: Timescales of Gas Evolution", "2602.02657"),
        ],
    },
    {
        "id": "cosmic-rays",
        "icon": "cr-icon.png",
        "title": "Cosmic ray feedback",
        "text": """Cosmic rays are high-energy particles produced mainly by supernovae. Closer to home,
        the particle showers they set off in the atmosphere are a known nuisance for electronics,
        occasionally flipping a bit in computer memory, which is why aviation and spacecraft systems
        are hardened against them. On the scales of galaxies their effect is far more consequential:
        they can shape the distribution of gas inside and outside galaxies, and so help control how
        galaxies evolve. How far and how fast they travel is the critical unknown that limits our
        understanding of these effects. Observations indicate that cosmic rays move much more slowly
        near star-forming regions than through typical interstellar gas, likely because they scatter
        off the turbulent magnetic fields there. We showed that this slower transport changes galactic
        structure dramatically: in gas-rich, gravitationally unstable galaxies, the cosmic ray pressure
        that builds up locally prevents gas from collapsing, stabilizing the galaxy as a whole.""",
        "video": "semenov21cr3-fg0.4-suppk",
        "papers": [
            ("Semenov et al.", "2021", "CR Diffusion Suppression Inhibits Clump Formation", "2012.01427"),
        ],
    },
    {
        "id": "unresolved-turbulence",
        "icon": "sgst-icon.png",
        "title": "Modeling unresolved turbulence and star formation",
        "text": """Why does one clump of dense gas turn much of its mass into stars while another turns
        almost none? A large part of the answer lies in how turbulent gas motions shape the internal
        structure of such regions. These motions and structures exist on scales far smaller than
        state-of-the-art galaxy simulations can resolve, so they have to be modeled. I develop models
        for such unresolved turbulence, following the methods outlined above, and test how they shape
        galaxy evolution on large scales. This approach, also known as Large Eddy Simulation, helps
        make simulations predictive in extreme regimes where the usual approaches based on calibration
        against observations break down &mdash; for example, the early Universe described above.""",
        "video": "semenov17-maps",
        "papers": [
            ("Semenov et al.", "2016", "Nonuniversal Star Formation Efficiency", "1512.03101"),
            ("Semenov", "2025", "Capturing Turbulence with Numerical Dissipation", "2410.23339"),
            ("Semenov et al.", "2025", "From UV-bright Galaxies to Early Disks", "2410.09205"),
        ],
    },
    {
        "id": "numerical-methods",
        "icon": "numerical-grid.png",
        "title": "Numerical Methods for Astrophysics",
        "text": """Galaxy formation is an inherently multiscale and multiphysics problem. The range of
        scales involved is enormous, comparable to the range between the size of the Earth and an
        orange, and those scales are tightly coupled through the feedback loops described above.
        Together these make the problem hard to tackle numerically. Much of my work develops and
        improves the numerical methods needed to treat the relevant processes, including many of those
        described above: turbulence, cosmic rays, star formation, stellar feedback, and the broader
        algorithms behind adaptive mesh refinement hydrodynamics.""",
        "video": None,
        "papers": [
            ("Semenov et al.", "2022", "Entropy-Conserving Scheme for Nonthermal Energies", "2107.14240"),
            ("Semenov", "2025", "Capturing Turbulence with Numerical Dissipation", "2410.23339"),
            ("Gnedin et al.", "2018", "Enforcing the CFL Condition in Local Time Stepping", "1801.03108"),
        ],
    },
]

MOVIES = [
    ("semenov26-turb", "Driven supersonic turbulence: gas density and velocity magnitude", "dark"),
    ("semenov24-art", "Cosmological simulation of a Milky Way analog: gas density and small-scale turbulence", "dark"),
    ("semenov24-art-tng", "Cosmological simulation of a Milky Way-like galaxy with ART and TNG", "paper"),
    ("semenov24-art-disk", "Disk formation in a cosmological simulation of a MW analog", "paper"),
    ("semenov17-maps", "Simulation of a galaxy with a subgrid turbulence model: young stars, gas density, temperature, and turbulent velocities on unresolved scales", "dark"),
    ("semenov17-gas-cycling", "Cycling of interstellar gas between star-forming and non-star-forming states", "paper"),
    ("semenov21-ngc300", "NGC300-like galaxy simulation with subgrid turbulence and radiative transfer", "dark"),
    ("semenov21-ngc300-paper", "NGC300-like galaxy simulation &mdash; article version", "dark"),
    ("semenov21cr1-fg0.4-nocr", "Cosmic ray feedback in a gas-rich galaxy &mdash; no CRs", "dark"),
    ("semenov21cr2-fg0.4-constk", "Cosmic ray feedback &mdash; CRs with constant diffusivity", "dark"),
    ("semenov21cr3-fg0.4-suppk", "Cosmic ray feedback with local diffusivity suppression: gas density, star formation rate, turbulent pressure, cosmic ray pressure", "dark"),
]

# Intrinsic pixel dimensions -- emitted as width/height attributes so figures reserve
# correct space with preload="none" (otherwise <video> falls back to 300x150).
DIMS = {
    "semenov26-turb": (2048, 1024),
    "semenov17-gas-cycling": (1232, 720),
    "semenov17-maps": (2000, 1000),
    "semenov21-ngc300-paper": (2406, 814),
    "semenov21-ngc300": (2000, 1000),
    "semenov21cr1-fg0.4-nocr": (2000, 1000),
    "semenov21cr2-fg0.4-constk": (2000, 1000),
    "semenov21cr3-fg0.4-suppk": (2000, 1000),
    "semenov24-art-disk": (1950, 870),
    "semenov24-art-tng": (2670, 1500),
    "semenov24-art": (1200, 600),
}

LINKS = [
    ("ADS Library", "https://ui.adsabs.harvard.edu/public-libraries/_KemY1lYQ0-gJC90XI2MxA"),
    ("Google Scholar", "https://scholar.google.com/citations?user=xT6Np1wAAAAJ&amp;hl=en"),
    ("ORCID 0000-0002-6648-7136", "https://orcid.org/0000-0002-6648-7136"),
]

# Per-count ADS libraries, also from the live site.
STAT_LINKS = {
    "papers": "https://ui.adsabs.harvard.edu/public-libraries/_KemY1lYQ0-gJC90XI2MxA",
    "first-author": "https://ui.adsabs.harvard.edu/public-libraries/SDoyEcX6RqmDMdxtu-EnGw",
    "led by students": "https://ui.adsabs.harvard.edu/public-libraries/6yTr6gjZSdWlioEK2XSA4A",
}

STATS_NOTE = "based on <a href=\"%s\" target=\"_blank\" rel=\"noopener\">ADS metrics</a>, April 2026"
ADS_LIBRARY = "https://ui.adsabs.harvard.edu/public-libraries/_KemY1lYQ0-gJC90XI2MxA"

# (authors, journal, arxiv_id, title). arxiv_id "" where the live site lists none.
PUBS = [
    ("First author", [
        ("Semenov 2026", "ApJ accepted", "2602.04950",
         "How Do Disk Galaxies Form?"),
        ("Semenov, Conroy, Hernquist 2025", "ApJ 989, 219", "2410.09205",
         "From UV-bright Galaxies to Early Disks: the Importance of Turbulent Star Formation in the Early Universe"),
        ("Semenov, Conroy, Smith, Puchwein, Hernquist 2025", "ApJ 990, 7", "2409.18173",
         "How Early Could the Milky Way&rsquo;s Disk Form?"),
        ("Semenov 2025", "ApJS 281, 37", "2410.23339",
         "Capturing Turbulence with Numerical Dissipation: a Simple Dynamical Model for Unresolved Turbulence in Hydrodynamic Simulations"),
        ("Semenov, Conroy, Chandra, Hernquist, Nelson 2024", "ApJ 962, 84", "2306.09398",
         "Formation of Galactic Disks I: Why did the Milky Way&rsquo;s Disk Form Unusually Early?"),
        ("Semenov, Conroy, Chandra, Hernquist, Nelson 2024", "ApJ 972, 73", "2306.13125",
         "Formation of Galactic Disks II: the Physical Drivers of Disk Spin-up"),
        ("Semenov, Kravtsov, Diemer 2022", "ApJS 261, 16", "2107.14240",
         "Entropy-Conserving Scheme for Modeling Nonthermal Energies in Fluid Dynamics Simulations"),
        ("Semenov, Kravtsov, Gnedin 2021", "ApJ 918, 13", "2103.13406",
         "Spatial Decorrelation of Young Stars and Dense Gas as a Probe of the Star Formation&ndash;Feedback Cycle in Galaxies"),
        ("Semenov, Kravtsov, Caprioli 2021", "ApJ 910, 126", "2012.01427",
         "Cosmic Ray Diffusion Suppression in Star-Forming Regions Inhibits Clump Formation in Gas-Rich Galaxies"),
        ("Semenov, Kravtsov, Gnedin 2019", "ApJ 870, 79", "1809.07328",
         "What Sets the Slope of the Molecular Kennicutt&ndash;Schmidt Relation?"),
        ("Semenov, Kravtsov, Gnedin 2018", "ApJ 861, 4", "1803.00007",
         "How Galaxies Form Stars: the Connection between Local and Global Star Formation in Galaxy Simulations"),
        ("Semenov, Kravtsov, Gnedin 2017", "ApJ 845, 133", "1704.04239",
         "The Physical Origin of Long Gas Depletion Times in Galaxies"),
        ("Semenov, Kravtsov, Gnedin 2016", "ApJ 826, 200", "1512.03101",
         "Nonuniversal Star Formation Efficiency in Turbulent ISM"),
        ("Semenov 2013", "Astronomy Reports 57, 485", "2013ARep",
         "Statistical Analysis of the Large-Scale Structure of the Universe Using Observational Data and Numerical Modeling"),
    ]),
    ("Led by co-advised students", [
        ("Kocjan, Diemer, Semenov, Bialy, Malamud 2026", "submitted", "2608.28747",
         "Shock-heated Away: The Impact of Radiative Cooling on Gas-Phase Transitions in Supernova Remnants"),
        ("Kocjan, Semenov 2026", "ApJ 1007, 46", "2602.02657",
         "The Rhythm of the ISM: Tracing the Timescales of Gas Evolution and Star Formation across Galactic Environments"),
        ("Konietzka, Connor, Semenov, Beane, Springel, Hernquist 2025", "ApJ accepted", "2507.07090",
         "Ray-tracing Fast Radio Bursts Through IllustrisTNG: Cosmological Dispersion Measures from Redshift 0 to 5.5"),
        ("Polzin, Kravtsov, Semenov, Gnedin 2024", "OJAp 7, 114", "2407.11125",
         "On the Universality of Star Formation Efficiency in Galaxies"),
        ("Polzin, Kravtsov, Semenov, Gnedin 2024", "ApJ 966, 172", "2310.10712",
         "Modeling Molecular Hydrogen in Low Metallicity Galaxies"),
        ("Chandra, Semenov, Rix, Conroy, Bonaca, Naidu, Andrae, Li, Hernquist 2024", "ApJ 972, 112", "2310.13050",
         "The Three-Phase Evolution of the Milky Way"),
        ("Han, Semenov, Conroy, Hernquist 2023", "ApJL 954, L24", "2309.07208",
         "Tilted Dark Halos are Common, Long-Lived, and Can Warp Galactic Disks"),
        ("Appel, Burkhart, Semenov, Federrath, Rosen, Tan 2023", "ApJ 954, 93", "2301.07723",
         "What Sets the Star Formation Rate of Molecular Clouds? The Density Distribution as a Fingerprint of Compression and Expansion Rates"),
        ("Appel, Burkhart, Semenov, Federrath, Rosen 2022", "ApJ 927, 75", "2109.13271",
         "The Effects of Magnetic Fields and Outflow Feedback on the Shape and Evolution of the Density PDF in Turbulent Star-Forming Clouds"),
    ]),
    ("In collaboration", [
        ("Wheeler, Kravtsov, Chiti, Katz, Semenov 2025", "OJAp 8, 151", "2507.03182",
         "What Sets the Metallicity of Ultra-Faint Dwarfs?"),
        ("Segovia Otero, Agertz, Renaud, Kraljic, Romeo, Semenov 2025", "MNRAS 538, 2646", "2410.08266",
         "Cosmic evolution of the star formation efficiency in Milky Way-like galaxies"),
        ("Robinson, Avestruz, Gnedin, Semenov 2024", "OJAp subm.", "2412.15324",
         "The effects of different cooling and heating function models on a simulated analog of NGC300"),
        # The live site repeats Segovia Otero's title here; real title via the arXiv API.
        ("Beane, Johnson, Semenov, Hernquist, Chandra, Conroy 2025", "ApJ 985, 221", "2410.21580",
         "Rising from the Ashes II: The Bar-driven Abundance Bimodality of the Milky Way"),
        ("Aung, Mandelker, Dekel, Semenov, van den Bosch 2024", "MNRAS 532, 2965", "2403.00912",
         "Entrainment of Hot Gas into Cold Streams: The Origin of Excessive Star-formation Rates at Cosmic Noon"),
        ("Kiihne, Appel, Burkhart, Semenov, Federrath 2025", "ApJ 979, 89", "2305.11218",
         "Fitting Probability Distribution Functions in Turbulent Star-Forming Molecular Clouds"),
        ("Jeffreson, Semenov, Krumholz 2023", "MNRAS 527, 7093", "2301.10251",
         "Clouds of Theseus: Long-lived Molecular Clouds are Composed of Short-lived H2 Molecules"),
        ("Shin, Tacchella, Kim, Iyer, Semenov 2023", "ApJ 947, 61", "2211.01922",
         "Star Formation Variability as a Probe for the Baryon Cycle within Galaxies"),
        ("Bialy, Zucker, Goodman, Foley, Alves, Semenov, Benjamin, Leike, En&szlig;lin 2021", "ApJL 919, L5", "2109.09763",
         "The Per-Tau Shell: A Giant Star-forming Spherical Shell Revealed by 3D Dust Observations"),
        ("Gnedin, Semenov, Kravtsov 2018", "JCoPh 359, 93", "1801.03108",
         "Enforcing the Courant&ndash;Friedrichs&ndash;Lewy Condition in Explicitly Conservative Local Time Stepping Schemes"),
        ("Li, Gnedin, Gnedin, Meng, Semenov, Kravtsov 2017", "ApJ 834, 69", "1608.03244",
         "Star Cluster Formation in Cosmological Simulations. I. Properties of Young Clusters"),
        ("Kim et al. (AGORA Collaboration) 2016", "ApJ 833, 202", "1610.03066",
         "The AGORA High-resolution Galaxy Simulations Comparison Project. II. Isolated Disk Test"),
    ]),
]


# arXiv id -> {ADS bibcode, publisher URL}. Parsed per <li> from the live
# publications page so each link belongs to its own entry; missing publisher
# links fall back to a DOI resolved from the arXiv API or Crossref.
REFS = {
    "2608.28747": {"ads": '2026arXiv260828747K', "url": None},
    "2013ARep": {"ads": '2013ARep...57..485S', "url": None},
    "1512.03101": {"ads": None, "url": 'https://doi.org/10.3847/0004-637X/826/2/200'},
    "1608.03244": {"ads": None, "url": 'https://doi.org/10.3847/1538-4357/834/1/69'},
    "1610.03066": {"ads": None, "url": 'https://doi.org/10.3847/1538-4357/833/2/202'},
    "1704.04239": {"ads": None, "url": 'https://doi.org/10.3847/1538-4357/aa8096'},
    "1801.03108": {"ads": None, "url": 'https://doi.org/10.1016/j.jcp.2018.01.008'},
    "1803.00007": {"ads": None, "url": 'https://doi.org/10.3847/1538-4357/aac6eb'},
    "1809.07328": {"ads": None, "url": 'https://doi.org/10.3847/1538-4357/aaf163'},
    "2012.01427": {"ads": '2021ApJ...910..126S', "url": 'https://doi.org/10.3847/1538-4357/abe2a6'},
    "2103.13406": {"ads": '2021arXiv210313406S', "url": 'https://doi.org/10.3847/1538-4357/ac0a77'},
    "2107.14240": {"ads": '2022ApJS..261...16S', "url": 'https://doi.org/10.3847/1538-4365/ac69e1'},
    "2109.09763": {"ads": None, "url": 'https://doi.org/10.3847/2041-8213/ac1f95'},
    "2109.13271": {"ads": '2022ApJ...927...75A', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ac4be3'},
    "2211.01922": {"ads": '2022arXiv221101922S', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/acc251'},
    "2301.07723": {"ads": '2023arXiv230107723A', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ace897'},
    "2301.10251": {"ads": '2023arXiv230110251J', "url": 'https://academic.oup.com/mnras/article/527/3/7093/7424987'},
    "2305.11218": {"ads": '2023arXiv230511218K', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ad99d5'},
    "2306.09398": {"ads": '2024ApJ...962...84S', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ad150a'},
    "2306.13125": {"ads": '2023arXiv230613125S', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ad57ba'},
    "2309.07208": {"ads": '2023arXiv230907208H', "url": 'https://iopscience.iop.org/article/10.3847/2041-8213/ad0641'},
    "2310.10712": {"ads": '2023arXiv231010712P', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ad32cb'},
    "2310.13050": {"ads": '2023arXiv231013050C', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ad5b60'},
    "2403.00912": {"ads": '2024arXiv240300912A', "url": 'https://academic.oup.com/mnras/article/532/3/2965/7710759'},
    "2407.11125": {"ads": '2024arXiv240711125P', "url": 'https://astro.theoj.org/article/127042-on-the-universality-of-star-formation-efficiency-in-galaxies'},
    "2409.18173": {"ads": '2024arXiv240918173S', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/addf48'},
    "2410.08266": {"ads": '2024arXiv241008266S', "url": 'https://academic.oup.com/mnras/article/538/4/2646/8082127'},
    "2410.09205": {"ads": '2024arXiv241009205S', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ade22d'},
    "2410.21580": {"ads": '2024arXiv241021580B', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/adceab'},
    "2410.23339": {"ads": '2024arXiv241023339S', "url": 'https://iopscience.iop.org/article/10.3847/1538-4365/ae0cc6'},
    "2412.15324": {"ads": '2024arXiv241215324R', "url": None},
    "2507.03182": {"ads": '2025arXiv250703182W', "url": 'https://astro.theoj.org/article/145734-what-sets-the-metallicity-of-ultra-faint-dwarfs'},
    "2507.07090": {"ads": '2025arXiv250707090K', "url": None},
    "2602.02657": {"ads": '2026ApJ..1007...46K', "url": 'https://iopscience.iop.org/article/10.3847/1538-4357/ae8539'},
    "2602.04950": {"ads": '2026arXiv260204950S', "url": None},
}

# Per-video download and reference links, taken from the live visualizations page.
#  are (short title, arXiv id);  anchors the Read-more link.
MOVIE_LINKS = {
    "semenov26-turb": {
        "section": "current-work",
        "papers": [],
    },
    "semenov24-art": {
        "section": "first-galaxies",
        "papers": [('How Early Could the Milky Way&rsquo;s Disk Form?', '2409.18173'), ('From UV-bright Galaxies to Early Disks', '2410.09205')],
    },
    "semenov24-art-tng": {
        "section": "first-galaxies",
        "papers": [('How Early Could the Milky Way&rsquo;s Disk Form?', '2409.18173'), ('From UV-bright Galaxies to Early Disks', '2410.09205')],
    },
    "semenov24-art-disk": {
        "section": "first-galaxies",
        "papers": [('How Early Could the Milky Way&rsquo;s Disk Form?', '2409.18173'), ('From UV-bright Galaxies to Early Disks', '2410.09205')],
    },
    "semenov17-maps": {
        "section": "unresolved-turbulence",
        "papers": [('The Physical Origin of Long Gas Depletion Times', '1704.04239'), ('How Galaxies Form Stars', '1803.00007')],
    },
    "semenov17-gas-cycling": {
        "section": "star-formation",
        "papers": [('The Physical Origin of Long Gas Depletion Times', '1704.04239'), ('How Galaxies Form Stars', '1803.00007')],
    },
    "semenov21-ngc300": {
        "section": "star-formation",
        "papers": [('Spatial Decorrelation of Young Stars and Dense Gas', '2103.13406')],
    },
    "semenov21-ngc300-paper": {
        "section": "star-formation",
        "papers": [('Spatial Decorrelation of Young Stars and Dense Gas', '2103.13406')],
    },
    "semenov21cr1-fg0.4-nocr": {
        "section": "cosmic-rays",
        "papers": [('CR Diffusion Suppression Inhibits Clump Formation', '2012.01427')],
    },
    "semenov21cr2-fg0.4-constk": {
        "section": "cosmic-rays",
        "papers": [('CR Diffusion Suppression Inhibits Clump Formation', '2012.01427')],
    },
    "semenov21cr3-fg0.4-suppk": {
        "section": "cosmic-rays",
        "papers": [('CR Diffusion Suppression Inhibits Clump Formation', '2012.01427')],
    },
}

# YouTube ids, taken from the live visualizations page and verified via oEmbed.
# The WordPress build embeds these because VideoPress (self-hosted video) needs a
# Business plan. semenov26-turb is not on YouTube yet.
YOUTUBE = {
    "semenov24-art": "JEFr88X-qSk",
    "semenov24-art-tng": "yEkjuvtAsXc",
    "semenov24-art-disk": "p0VtSuCOHGA",
    "semenov17-maps": "UZV-NV2uwq4",
    "semenov17-gas-cycling": "946op8XGQ9w",
    "semenov21-ngc300": "D-zkMzfts18",
    "semenov21-ngc300-paper": "qjzhhAwzqUc",
    "semenov21cr1-fg0.4-nocr": "e5TVFC8EWDk",
    "semenov21cr2-fg0.4-constk": "oQvf3VC-bUw",
    "semenov21cr3-fg0.4-suppk": "qeOWSJpp3nM",
}
