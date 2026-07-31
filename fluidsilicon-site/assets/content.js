// ============================================================
// FLUID SILICON SITE CONTENT
// Edit this file to change the site. No HTML knowledge needed.
// ============================================================

window.SITE = {

  // Home page video. Set to "assets/video/home.mp4" when the video is ready.
  // While null, the animated chip fabric shows instead.
  video: null,

  // ---- Solution pillars (home page). One sentence each. ----
  solutions: [
    { title: "Silicon Health Monitoring",
      text: "On-chip sensors measure the health of logic at speed of operation, on unmodified commercial devices." },
    { title: "Adaptive Compensation",
      text: "Voltage and frequency tuned to the measured characteristics of each individual chip." },
    { title: "Self-Healing",
      text: "Degrading resources detected, isolated, and repaired on the fly, before they fail." }
  ],

  // ---- How it works (home page). A real sequence. ----
  steps: [
    { n: "01", title: "Sense",
      text: "Distributed sensors, built from the chip's own spare logic, measure timing health across the device." },
    { n: "02", title: "Track",
      text: "The platform follows each device over its lifetime and anticipates failures before they happen." },
    { n: "03", title: "Act",
      text: "Tuning and repair run through reconfiguration, scheduled in safe or idle periods, while the system operates." }
  ],

  // ---- Industries (home band + industries page). One sentence each. ----
  industries: [
    { name: "Aerospace & Defense",
      tag: "Reliability · Lifetime",
      text: "Health monitoring and in-field repair for missions where replacement is impossible." },
    { name: "Hyperscale & Cloud",
      tag: "Energy · Reliability",
      text: "Health monitoring and adaptive voltage and frequency to cut energy across the fleet." },
    { name: "Telecom & High-Reliability",
      tag: "Reliability · Performance",
      text: "Continuous monitoring, compensation, and repair for systems that cannot fail quietly." },
    { name: "Finance & HFT",
      tag: "Latency",
      text: "Frequency tuned to the measured limits of each chip for lower, verified latency." }
  ],

  // ---- Careers listings. href points to the job page. ----
  jobs: {
    fulltime: [
      { title: "FPGA Engineer",
        meta: "Full-Time · Philadelphia",
        href: "jobs/fpga-engineer.html" },
      { title: "Systems Software Engineer, HW/SW Co-Design",
        meta: "Full-Time · Philadelphia",
        href: "jobs/systems-software-engineer.html" }
    ],
    intern: [
      { title: "Software Engineering Intern",
        meta: "Internship · Philadelphia",
        href: "jobs/internships.html#swe" },
      { title: "Hardware Design / FPGA Intern",
        meta: "Internship · Philadelphia",
        href: "jobs/internships.html#hde" },
      { title: "Business Development Intern",
        meta: "Internship · Philadelphia",
        href: "jobs/internships.html#bd" }
    ]
  },

  // ---- Recognition (home page). Add items to add logos. ----
  recognition: [
    { img: "assets/img/presidents_sustainability_prize.png",
      caption: "President's Sustainability Prize · University of Pennsylvania" }
  ]
};
