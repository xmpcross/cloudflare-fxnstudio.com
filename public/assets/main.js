/* ==========================================================================
   FXN Studio - Ultra Luxury Interactive System
   - Theme Switcher (Dark Velvet Obsidian / Light Cashmere Pearl)
   - Interactive Spotlight Aura Mouse Follower
   - Smooth Scroll & Top Progress Indicator
   - Bento Category Filter
   - Interactive Project Estimator Calculator
   - Modal Brief Handler
   - IntersectionObserver Reveal Animations
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // Lucide SVG Icons Initialization
  const initIcons = () => {
    if (typeof lucide !== "undefined" && typeof lucide.createIcons === "function") {
      lucide.createIcons();
    }
  };
  initIcons();

  // 0. Lenis Smooth Scrolling Engine (https://tunabytes.com/blog/smooth-scrolling)
  let lenis = null;
  if (typeof Lenis !== "undefined") {
    lenis = new Lenis({
      autoRaf: true,
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      touchMultiplier: 2,
    });
  }

  // 1. Permanent Light Theme Initialization
  document.documentElement.setAttribute("data-theme", "light");
  localStorage.setItem("fxnstudio_theme", "light");


  // 2. Interactive Spotlight Aura Mouse Follower
  const aura = document.createElement("div");
  aura.className = "spotlight-aura";
  aura.setAttribute("aria-hidden", "true");
  document.body.appendChild(aura);

  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let auraX = mouseX;
  let auraY = mouseY;

  window.addEventListener("pointermove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  }, { passive: true });

  const animateAura = () => {
    auraX += (mouseX - auraX) * 0.12;
    auraY += (mouseY - auraY) * 0.12;
    aura.style.transform = `translate3d(${auraX}px, ${auraY}px, 0) translate(-50%, -50%)`;
    requestAnimationFrame(animateAura);
  };
  requestAnimationFrame(animateAura);

  // 3. Top Scroll Progress Indicator & Header Blur State
  const progressBar = document.createElement("div");
  progressBar.id = "scroll-progress";
  progressBar.className = "scroll-progress-bar";
  progressBar.setAttribute("aria-hidden", "true");
  document.body.appendChild(progressBar);

  const header = document.querySelector("[data-header]");

  const handleScroll = () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

    progressBar.style.width = `${Math.min(100, Math.max(0, scrollPercent))}%`;

    if (header) {
      header.classList.toggle("is-scrolled", scrollTop > 20);
    }
  };

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll();

  // 4. Smooth Anchor Scroll with Header Offset & Lenis Integration
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#" || targetId === "#project-brief-modal") return;

      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        const headerOffset = header ? header.offsetHeight + 20 : 80;

        if (lenis) {
          lenis.scrollTo(targetEl, { offset: -headerOffset, duration: 1.2 });
        } else {
          const elementPosition = targetEl.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          window.scrollTo({
            top: offsetPosition,
            behavior: "smooth"
          });
        }

        // Close mobile menu if open
        const mobileMenu = document.querySelector("[data-mobile-menu]");
        const navToggle = document.querySelector("[data-nav-toggle]");
        if (mobileMenu && mobileMenu.classList.contains("is-open")) {
          mobileMenu.classList.remove("is-open");
          if (navToggle) navToggle.setAttribute("aria-expanded", "false");
          document.body.style.overflow = "";
        }
      }
    });
  });

  // 5. Services Mega Menu Toggle
  const megaToggle = document.querySelector("[data-mega-toggle]");
  const megaMenu = document.querySelector("[data-mega-menu]");

  if (megaToggle && megaMenu) {
    megaToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = megaMenu.classList.toggle("is-open");
      megaToggle.setAttribute("aria-expanded", String(isOpen));
      megaMenu.setAttribute("aria-hidden", String(!isOpen));
    });

    document.addEventListener("click", (e) => {
      if (!megaMenu.contains(e.target) && !megaToggle.contains(e.target)) {
        megaMenu.classList.remove("is-open");
        megaToggle.setAttribute("aria-expanded", "false");
        megaMenu.setAttribute("aria-hidden", "true");
      }
    });
  }

  // 6. Mobile Navigation Toggle
  const navToggle = document.querySelector("[data-nav-toggle]");
  const mobileMenu = document.querySelector("[data-mobile-menu]");

  if (navToggle && mobileMenu) {
    navToggle.addEventListener("click", () => {
      const isOpen = mobileMenu.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      mobileMenu.setAttribute("aria-hidden", String(!isOpen));
      document.body.style.overflow = isOpen ? "hidden" : "";
    });
  }

  // 7. Interactive Need Selector Tabs
  const needTabs = document.querySelectorAll("[data-need-tabs] .need-tabs button");
  const panelTitle = document.getElementById("panel-title");
  const panelDesc = document.getElementById("panel-desc");
  const panelLink = document.getElementById("panel-link");
  const panelSteps = document.getElementById("panel-steps");

  const tabData = {
    "1": {
      title: "Website Design & Custom Development",
      desc: "Bespoke digital platforms engineered for brand authority, fluid responsive design, rapid load speeds and high conversion rate optimization.",
      link: "/services/#web-design",
      steps: [
        "Brand Strategy & Digital Architecture",
        "High-Fidelity Visual & Interactive UX",
        "Clean Modern Frontend & CMS Engine",
        "Technical SEO, Speed Optimization & QA"
      ]
    },
    "2": {
      title: "eCommerce & High-Converting Storefronts",
      desc: "Architected for maximum sales throughput: seamless product browsing, custom Shopify/headless code, and checkout friction removal.",
      link: "/services/#ecommerce",
      steps: [
        "E-commerce Strategy & Catalog Hierarchy",
        "Conversion-Engineered Product & Cart UX",
        "Custom Shopify / Headless API Integration",
        "Checkout Optimization & Analytics Tuning"
      ]
    },
    "3": {
      title: "AI Integrations & Custom Web Automation",
      desc: "Empower your business operations with intelligent AI chat agents, custom workflow tools, and automated customer acquisition pipelines.",
      link: "/services/#ai-integrations",
      steps: [
        "AI Opportunity Audit & System Mapping",
        "LLM & Model API Integration Architecture",
        "Custom AI Web & Conversational Interfaces",
        "Automated Lead Capture & CRM Sync"
      ]
    },
    "4": {
      title: "Technical SEO & Search Dominance",
      desc: "Data-driven SEO programs engineered around high-intent keywords, core web vitals, and scalable authority building for Perth & global search.",
      link: "/services/#seo-growth",
      steps: [
        "Commercial Intent & Keyword Intelligence",
        "Technical Audit & Core Web Vitals Optimization",
        "Information Architecture & Landing Systems",
        "Search Authority & Conversion Analytics"
      ]
    }
  };

  if (needTabs.length && panelTitle && panelDesc && panelSteps) {
    needTabs.forEach((button) => {
      button.addEventListener("click", () => {
        const tabId = button.getAttribute("data-tab");
        const data = tabData[tabId];
        if (!data) return;

        needTabs.forEach((btn) => btn.setAttribute("aria-selected", "false"));
        button.setAttribute("aria-selected", "true");

        panelTitle.textContent = data.title;
        panelDesc.textContent = data.desc;
        if (panelLink) panelLink.setAttribute("href", data.link);

        panelSteps.innerHTML = data.steps
          .map((step, idx) => `<li><span>0${idx + 1}</span> <strong>${step}</strong></li>`)
          .join("");
      });
    });
  }

  // 8. Selected Work Bento Grid Interactive Category Filter
  const filterBtns = document.querySelectorAll("[data-bento-filter]");
  const bentoItems = document.querySelectorAll(".bento-card[data-category]");

  if (filterBtns.length && bentoItems.length) {
    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const filter = btn.getAttribute("data-bento-filter");
        filterBtns.forEach((b) => b.classList.remove("is-active"));
        btn.classList.add("is-active");

        bentoItems.forEach((item) => {
          const category = item.getAttribute("data-category");
          if (filter === "all" || category === filter) {
            item.style.display = "";
            setTimeout(() => {
              item.style.opacity = "1";
              item.style.transform = "translateY(0) scale(1)";
            }, 20);
          } else {
            item.style.opacity = "0";
            item.style.transform = "translateY(15px) scale(0.96)";
            setTimeout(() => {
              item.style.display = "none";
            }, 300);
          }
        });
      });
    });
  }

  // 9. Interactive Project Budget & Timeline Estimator Widget
  const estimatorForm = document.querySelector("[data-estimator]");
  if (estimatorForm) {
    const scopeCheckboxes = estimatorForm.querySelectorAll("input[type='checkbox']");
    const timelineSelect = estimatorForm.querySelector("select[name='timeline']");
    const estimatePriceEl = document.getElementById("est-price");
    const estimateTimeEl = document.getElementById("est-time");

    const calculateEstimate = () => {
      let basePrice = 0;
      let totalWeeks = 0;

      scopeCheckboxes.forEach((cb) => {
        if (cb.checked) {
          basePrice += parseInt(cb.dataset.price || "0", 10);
          totalWeeks += parseInt(cb.dataset.weeks || "0", 10);
        }
      });

      if (basePrice === 0) {
        if (estimatePriceEl) estimatePriceEl.textContent = "Select services";
        if (estimateTimeEl) estimateTimeEl.textContent = "--";
        return;
      }

      const timelineVal = timelineSelect ? timelineSelect.value : "standard";
      if (timelineVal === "express") {
        basePrice = Math.round(basePrice * 1.25);
        totalWeeks = Math.max(2, Math.round(totalWeeks * 0.7));
      }

      if (estimatePriceEl) estimatePriceEl.textContent = `$${basePrice.toLocaleString()} AUD`;
      if (estimateTimeEl) estimateTimeEl.textContent = `${totalWeeks} - ${totalWeeks + 2} Weeks`;
    };

    scopeCheckboxes.forEach((cb) => cb.addEventListener("change", calculateEstimate));
    if (timelineSelect) timelineSelect.addEventListener("change", calculateEstimate);
    calculateEstimate();
  }

  // 10. Project Brief Modal Handlers
  const briefModal = document.querySelector("[data-brief-modal]");
  const briefOpeners = document.querySelectorAll("[data-open-brief]");
  const briefClosers = document.querySelectorAll("[data-close-brief]");

  const openModal = (e) => {
    if (e) e.preventDefault();
    if (briefModal) {
      briefModal.classList.add("is-open");
      briefModal.setAttribute("aria-hidden", "false");
      if (typeof briefModal.showModal === "function") {
        try { briefModal.showModal(); } catch (err) {}
      }
      document.body.style.overflow = "hidden";
    }
  };

  const closeModal = () => {
    if (briefModal) {
      briefModal.classList.remove("is-open");
      briefModal.setAttribute("aria-hidden", "true");
      if (typeof briefModal.close === "function") {
        try { briefModal.close(); } catch (err) {}
      }
      document.body.style.overflow = "";
    }
  };

  briefOpeners.forEach((btn) => btn.addEventListener("click", openModal));
  briefClosers.forEach((btn) => btn.addEventListener("click", closeModal));

  if (briefModal) {
    briefModal.addEventListener("click", (e) => {
      if (e.target === briefModal) closeModal();
    });
  }

  // 11. IntersectionObserver Scroll Reveal Animations
  const revealElements = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });

    revealElements.forEach((el) => observer.observe(el));
  } else {
    revealElements.forEach((el) => el.classList.add("is-visible"));
  }

  // 12. Preview Build Version System (preview.fxnstudio.com)
  // 12. Preview Build Version & Live Auto-Reload System (preview.fxnstudio.com)
  const initBuildVersion = () => {
    const isPreviewHost = window.location.hostname.includes("preview") ||
                          window.location.hostname.includes("fxnstudio.com") ||
                          window.location.search.includes("preview=1") ||
                          window.location.hostname === "localhost" ||
                          window.location.hostname === "127.0.0.1";

    let initialBuildNumber = null;
    let isReloading = false;

    const fetchVersion = async (isPolling = false) => {
      try {
        const res = await fetch(`/assets/version.json?_t=${Date.now()}`, { cache: "no-store" });
        if (res.ok) {
          const info = await res.json();
          const currentBuildId = info.buildNumber || info.version;

          if (initialBuildNumber === null) {
            initialBuildNumber = currentBuildId;
          } else if (isPolling && currentBuildId !== initialBuildNumber) {
            if (!isReloading) {
              isReloading = true;
              console.log("[FXN Preview Live Reload] New build detected:", info.version, "Reloading preview automatically...");
              const badge = document.getElementById("preview-build-badge");
              if (badge) {
                badge.style.background = "#4f46e5";
                badge.innerHTML = `<span class="pv-dot"></span> <span class="pv-version">AUTO-UPDATING TO ${info.version}...</span>`;
              }
              setTimeout(() => {
                window.location.reload(true);
              }, 400);
            }
            return;
          }

          renderBuildVersion(info, isPreviewHost);
        } else if (window.FXN_BUILD_INFO) {
          renderBuildVersion(window.FXN_BUILD_INFO, isPreviewHost);
        }
      } catch (e) {
        if (window.FXN_BUILD_INFO) {
          renderBuildVersion(window.FXN_BUILD_INFO, isPreviewHost);
        }
      }
    };

    const renderBuildVersion = (data, showBadge) => {
      // Update any DOM elements tagged with data attributes
      document.querySelectorAll("[data-build-version]").forEach((el) => (el.textContent = data.version));
      document.querySelectorAll("[data-build-commit]").forEach((el) => (el.textContent = data.commit));
      document.querySelectorAll("[data-build-time]").forEach((el) => (el.textContent = data.buildFormatted));

      if (!showBadge) return;

      let badge = document.getElementById("preview-build-badge");
      let popover = document.getElementById("preview-build-popover");

      if (!badge) {
        badge = document.createElement("div");
        badge.id = "preview-build-badge";
        badge.className = "preview-build-badge";
        badge.setAttribute("role", "button");
        badge.setAttribute("aria-expanded", "false");
        badge.setAttribute("title", "Click to view preview build details. Auto-reload is ACTIVE.");

        popover = document.createElement("div");
        popover.id = "preview-build-popover";
        popover.className = "preview-build-popover";

        document.body.appendChild(badge);
        document.body.appendChild(popover);

        badge.addEventListener("click", (e) => {
          e.stopPropagation();
          const isOpen = popover.classList.toggle("is-open");
          badge.setAttribute("aria-expanded", String(isOpen));
        });

        document.addEventListener("click", (e) => {
          if (popover && !popover.contains(e.target) && !badge.contains(e.target)) {
            popover.classList.remove("is-open");
            badge.setAttribute("aria-expanded", "false");
          }
        });
      }

      badge.innerHTML = `
        <span class="pv-dot"></span>
        <span class="pv-tag">LIVE SYNC</span>
        <span class="pv-version">${data.version}</span>
        <span class="pv-commit">(${data.commit})</span>
      `;

      popover.innerHTML = `
        <div class="pv-pop-header">
          <div class="pv-pop-title">⚡ Live Preview Build Engine</div>
          <button type="button" class="pv-pop-close" id="pv-pop-close-btn">&times;</button>
        </div>
        <div class="pv-pop-row">
          <span class="pv-pop-label">Host:</span>
          <span class="pv-pop-value">${window.location.hostname}</span>
        </div>
        <div class="pv-pop-row">
          <span class="pv-pop-label">Live Sync:</span>
          <span class="pv-pop-value" style="color: #10b981;">● Active (1.5s auto-refresh)</span>
        </div>
        <div class="pv-pop-row">
          <span class="pv-pop-label">Version:</span>
          <span class="pv-pop-value">${data.version}</span>
        </div>
        <div class="pv-pop-row">
          <span class="pv-pop-label">Git Commit:</span>
          <span class="pv-pop-value">${data.commit}</span>
        </div>
        <div class="pv-pop-row">
          <span class="pv-pop-label">Build Time:</span>
          <span class="pv-pop-value">${data.buildFormatted}</span>
        </div>
        <div class="pv-pop-actions">
          <button type="button" class="pv-pop-btn" id="pv-refresh-btn">↻ Force Refresh</button>
          <button type="button" class="pv-pop-btn" id="pv-copy-btn">📋 Copy Info</button>
        </div>
      `;

      const closeBtn = document.getElementById("pv-pop-close-btn");
      if (closeBtn) {
        closeBtn.addEventListener("click", () => {
          popover.classList.remove("is-open");
          badge.setAttribute("aria-expanded", "false");
        });
      }

      const refreshBtn = document.getElementById("pv-refresh-btn");
      if (refreshBtn) {
        refreshBtn.addEventListener("click", () => {
          window.location.reload(true);
        });
      }

      const copyBtn = document.getElementById("pv-copy-btn");
      if (copyBtn) {
        copyBtn.addEventListener("click", () => {
          const textToCopy = `Preview Build: ${data.version} (${data.commit}) - ${data.buildFormatted}`;
          navigator.clipboard.writeText(textToCopy).then(() => {
            copyBtn.textContent = "✓ Copied";
            setTimeout(() => { copyBtn.textContent = "📋 Copy Info"; }, 1500);
          });
        });
      }
    };

    fetchVersion();

    // Auto-Reload engine on preview domain: polls every 1.5s for changes
    if (isPreviewHost) {
      setInterval(() => {
        if (!isReloading && document.visibilityState !== "hidden") {
          fetchVersion(true);
        }
      }, 1500);

      document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "visible" && !isReloading) {
          fetchVersion(true);
        }
      });
    }
  };

  initBuildVersion();

  // 13. Hero Terminal Tab Switcher
  const termTabs = document.querySelectorAll("[data-term-tab]");
  termTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const targetKey = tab.getAttribute("data-term-tab");
      termTabs.forEach((t) => t.classList.remove("is-active"));
      tab.classList.add("is-active");

      document.querySelectorAll(".term-panel").forEach((panel) => {
        panel.classList.remove("is-active");
      });

      const activePanel = document.getElementById(`term-panel-${targetKey}`);
      if (activePanel) {
        activePanel.classList.add("is-active");
      }
    });
  });

  // 14. Modern Form Submission Handler (Zero Netlify Dependency)
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    if (form.hasAttribute("data-estimator")) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector("button[type='submit']");
      const originalText = submitBtn ? submitBtn.innerHTML : "Submit";

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i data-lucide="loader-2" class="icon-sm spin"></i> Sending Brief...`;
        if (typeof lucide !== "undefined" && typeof lucide.createIcons === "function") lucide.createIcons();
      }

      setTimeout(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<i data-lucide="check-circle" class="icon-sm"></i> Brief Submitted Successfully!`;
          if (typeof lucide !== "undefined" && typeof lucide.createIcons === "function") lucide.createIcons();
        }

        form.reset();

        const briefModal = document.querySelector("[data-brief-modal]");
        setTimeout(() => {
          if (briefModal && briefModal.classList.contains("is-open")) {
            briefModal.classList.remove("is-open");
            briefModal.setAttribute("aria-hidden", "true");
            if (typeof briefModal.close === "function") {
              try { briefModal.close(); } catch (err) {}
            }
            document.body.style.overflow = "";
          }
          if (submitBtn) submitBtn.innerHTML = originalText;
        }, 2000);
      }, 1000);
    });
  });
});


