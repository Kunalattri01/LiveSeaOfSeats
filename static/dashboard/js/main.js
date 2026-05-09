// open & close modal

document.addEventListener("DOMContentLoaded", () => {
  const openBtns = document.querySelectorAll("[data-modal]");
  const closeBtns = document.querySelectorAll(".close, [data-close]");

  if (!openBtns || !closeBtns) return;

  // OPEN MODAL
  openBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const modalSelector = btn.dataset.modal;
      const modal = document.querySelector(modalSelector);
      if (!modal) return;

      modal.classList.remove("hidden");
      modal.classList.add("flex");
      document.body.style.overflow = "hidden";
    });
  });

  // CLOSE MODAL BUTTON
  closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const modal = btn.closest(".modal");
      if (!modal) return;

      modal.classList.add("hidden");
      modal.classList.remove("flex");
      document.body.style.overflow = "auto";
    });
  });

  // CLOSE ON BACKDROP CLICK
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.style.overflow = "auto";
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const drawerBtns = document.querySelectorAll(".drawerBtn");
  const drawerOverlay = document.getElementById("overlay2");
  const closeDrawers = document.querySelectorAll(
    "#close-drawer, #close-customer-drawer",
  );

  if (!drawerBtns.length || !drawerOverlay || !closeDrawers.length) return;

  drawerBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetDrawerId = btn.dataset.drawerTarget;
      const targetDrawer = document.querySelector(targetDrawerId);

      if (!targetDrawer) return;

      drawerOverlay.classList.remove("hidden");
      targetDrawer.classList.remove("hidden");
      targetDrawer.classList.add("open");
      document.body.style.overflow = "hidden";
    });
  });

  function closeDrawer() {
    drawerOverlay.classList.add("hidden");
    document.querySelectorAll(".drawer").forEach((d) => {
      d.classList.add("hidden");
      d.classList.remove("open");
    });
    document.body.style.overflow = "auto";
  }

  closeDrawers.forEach((btn) => btn.addEventListener("click", closeDrawer));
  drawerOverlay.addEventListener("click", closeDrawer);
});

document.addEventListener("DOMContentLoaded", () => {
  const wrappers = document.querySelectorAll(".dropdown-wrapper");

  wrappers.forEach((wrapper) => {
    const moreBtn = wrapper.querySelector(".more");
    const dropdown = wrapper.querySelector(".dropdown");

    moreBtn.addEventListener("click", (e) => {
      e.stopPropagation();

      // Close all dropdowns first
      document.querySelectorAll(".dropdown").forEach((d) => {
        d.classList.add("hidden");
        d.classList.remove("flex");
      });

      // Open current dropdown
      dropdown.classList.remove("hidden");
      dropdown.classList.add("flex");
    });
  });

  // Close when clicking outside
  document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown").forEach((dropdown) => {
      dropdown.classList.add("hidden");
      dropdown.classList.remove("flex");
    });
  });
});

// for event page
document.addEventListener("DOMContentLoaded", () => {
  const cardView = document.getElementById("view-grid");
  const listView = document.getElementById("view-list");
  const gridCard = document.getElementById("grid-card");
  const listTable = document.getElementById("list-table");

  if (!cardView || !listView || !gridCard || !listTable) return;

  cardView.addEventListener("click", () => {
    cardView.classList.add("active");
    listView.classList.remove("active");
    gridCard.classList.remove("hidden");
    listTable.classList.add("hidden");
  });
  listView.addEventListener("click", () => {
    listView.classList.add("active");
    cardView.classList.remove("active");
    listTable.classList.remove("hidden");
    gridCard.classList.add("hidden");
  });
});

// Accordion functionality
document.addEventListener("DOMContentLoaded", () => {
  const accordionTriggers = document.querySelectorAll(".accordion-trigger");
  accordionTriggers.forEach((button) => {
    button.addEventListener("click", () => toggleAccordion(button));
  });
});

// Accordion functionality
function toggleAccordion(button) {
  const content = button.nextElementSibling;
  const icon = button.querySelector("i");
  const isOpen = content.classList.contains("open");

  // Close all other accordions
  document.querySelectorAll(".accordion-content.open").forEach((item) => {
    if (item !== content) {
      item.classList.remove("open");
      const otherIcon = item.previousElementSibling.querySelector("i");
      otherIcon.classList.remove("rotate-180");
    }
  });
  if (isOpen) {
    content.classList.remove("open");
    icon.classList.remove("rotate-180");
  } else {
    content.classList.add("open");
    icon.classList.add("rotate-180");
  }
}

const uploadBtn = document.getElementById("upload-btn");
const removeBtn = document.getElementById("remove-btn");
const fileInput = document.getElementById("file-input");
const profileImg = document.getElementById("profile-img");

// Trigger file input when upload button is clicked
if (uploadBtn) {
  uploadBtn.addEventListener("click", () => {
    fileInput.click();
  });
}

// Handle file selection
if (fileInput) {
  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        profileImg.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
}
// Remove image
if (removeBtn) {
  removeBtn.addEventListener("click", () => {
    profileImg.src = "./assets/images/Untitled.png";
    fileInput.value = "";
  });
}

// for marketing page

// for help tab active functions
document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".help-tab-btn");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        const id = entry.target.getAttribute("id");

        navLinks.forEach((link) => {
          link.classList.toggle(
            "active",
            link.getAttribute("href") === `#${id}`,
          );
        });
      });
    },
    {
      rootMargin: "-40% 0px -50% 0px",
      threshold: 0,
    },
  );

  sections.forEach((section) => observer.observe(section));
});

// for support page
const listViewBtn = document.getElementById("list-view-btn");
const gridViewBtn = document.getElementById("grid-view-btn");
const listViewCard = document.getElementById("tickets-list-view");
const gridViewCard = document.getElementById("tickets-grid-view");

if (listViewBtn) {
  listViewBtn.addEventListener("click", () => {
    listViewBtn.classList.add("active");
    gridViewBtn.classList.remove("active");
    listViewCard.classList.remove("hidden");
    gridViewCard.classList.add("hidden");
    gridViewCard.classList.remove("grid");
  });
}

if (gridViewBtn) {
  gridViewBtn.addEventListener("click", () => {
    gridViewBtn.classList.add("active");
    gridViewBtn.classList.add("grid");
    listViewBtn.classList.remove("active");
    listViewCard.classList.add("hidden");
    gridViewCard.classList.remove("hidden");
    gridViewCard.classList.add("grid");
  });
}

// message page
document.addEventListener("DOMContentLoaded", () => {
  const chatArea = document.getElementById("chat-area");
  const messageForm = document.getElementById("message-form");
  const messageInput = document.getElementById("message-input");

  if (!messageForm || !messageInput || !chatArea) return;

  messageForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (text === "") return;

    // Create sent message bubble
    const messageDiv = document.createElement("div");
    messageDiv.className = "flex items-start gap-3 justify-end";

    messageDiv.innerHTML = `
                <div class="text-right">
                    <div class="bg-border text-text p-3 rounded-lg rounded-tr-none max-w-xs md:max-w-md shadow">
                        <p>${text}</p>
                    </div>
                    <span class="text-xs text-gray-500 mt-1 block">${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
                </div>
                <img src="./assets/images/profile/emma.jpg" alt="Me" class="w-8 h-8 rounded-full shrink-0">
            `;

    chatArea.appendChild(messageDiv);
    messageInput.value = "";
    chatArea.scrollTop = chatArea.scrollHeight; // Auto-scroll to bottom
  });
});

// color option
document.querySelectorAll(".color-option").forEach((option) => {
  option.addEventListener("click", function () {
    document
      .querySelectorAll(".color-option")
      .forEach((opt) => opt.classList.remove("selected"));
    this.classList.add("selected");
    const selectedColor = this.getAttribute("data-color");
    console.log("Selected color:", selectedColor);
  });
});

// reviews view
document.addEventListener("DOMContentLoaded", () => {
  const listBtn = document.getElementById("list-reviews");
  const gridBtn = document.getElementById("grid-reviews");
  const listViewContainer = document.getElementById("list-view-container");
  const gridViewContainer = document.getElementById("grid-view-container");

  if (!listBtn || !gridBtn) return;

  listBtn.addEventListener("click", () => {
    listBtn.classList.add("active");
    gridBtn.classList.remove("active");
    listViewContainer.classList.remove("hidden");
    gridViewContainer.classList.add("hidden");
  });

  gridBtn.addEventListener("click", () => {
    gridBtn.classList.add("active");
    listBtn.classList.remove("active");
    listViewContainer.classList.add("hidden");
    gridViewContainer.classList.remove("hidden");
    gridViewContainer.classList.add("grid");
  });
});

// // select dropdown
// // Select all dropdown containers
// document.querySelectorAll(".select-dropdown").forEach((dropdown) => {
//   const button = dropdown.querySelector(".select-dropdown-button");
//   const icon = dropdown.querySelector(".select-toggle-icon");
//   const items = dropdown.querySelectorAll(".select-dropdown-item");

//   // Toggle dropdown open/close
//   button.addEventListener("click", (e) => {
//     e.stopPropagation();
//     dropdown.classList.toggle("open");
//     icon.className = dropdown.classList.contains("open")
//       ? "ph ph-caret-up"
//       : "ph ph-caret-down";
//   });

//   // Update selected text and close dropdown
//   items.forEach((item) => {
//     item.addEventListener("click", () => {
//       button.querySelector("span").textContent = item.textContent;
//       const hiddenInput = dropdown.querySelector('input[type="hidden"]');
//       if (hiddenInput) {
//         hiddenInput.value =
//           item.getAttribute("data-value") || item.textContent.trim();
//         hiddenInput.dispatchEvent(new Event("change", { bubbles: true }));
//       }
//       dropdown.classList.remove("open");
//       icon.className = "ph ph-caret-down";
//     });
//   });
// });

// // Close all dropdowns when clicking outside
// document.addEventListener("click", () => {
//   document.querySelectorAll(".select-dropdown").forEach((dropdown) => {
//     dropdown.classList.remove("open");
//     const icon = dropdown.querySelector("#select-toggle-icon");
//     if (icon) icon.className = "ph ph-caret-down";
//   });
// });
document.querySelectorAll(".select-dropdown").forEach((dropdown) => {
  const button = dropdown.querySelector(".select-dropdown-button");
  const icon = dropdown.querySelector(".select-toggle-icon");
  const menu = dropdown.querySelector(".select-dropdown-menu");
  const items = dropdown.querySelectorAll(".select-dropdown-item");

  // Close all dropdowns except current
  function closeOtherDropdowns() {
    document
      .querySelectorAll(".select-dropdown.open")
      .forEach((openDropdown) => {
        if (openDropdown !== dropdown) {
          openDropdown.classList.remove("open");

          const openIcon = openDropdown.querySelector(".select-toggle-icon");
          const openMenu = openDropdown.querySelector(".select-dropdown-menu");

          if (openIcon) openIcon.className = "ph ph-caret-down";

          if (openMenu) {
            openMenu.style.top = "100%";
            openMenu.style.bottom = "auto";
            openMenu.style.left = "0";
            openMenu.style.right = "auto";
          }
        }
      });
  }

  button.addEventListener("click", (e) => {
    e.stopPropagation();

    const isOpen = dropdown.classList.contains("open");

    // Always close other dropdowns first
    closeOtherDropdowns();

    // Toggle current dropdown
    dropdown.classList.toggle("open", !isOpen);
    icon.className = !isOpen ? "ph ph-caret-up" : "ph ph-caret-down";

    if (!isOpen) {
      // Measure menu height safely
      menu.style.visibility = "hidden";
      menu.style.display = "block";

      const menuHeight = menu.offsetHeight;
      const btnRect = button.getBoundingClientRect();
      const viewportHeight = window.innerHeight;

      // Vertical positioning
      const spaceBelow = viewportHeight - btnRect.bottom;
      const spaceAbove = btnRect.top;

      if (spaceBelow < menuHeight && spaceAbove > menuHeight) {
        menu.style.top = "auto";
        menu.style.bottom = "100%";
      } else {
        menu.style.top = "100%";
        menu.style.bottom = "auto";
      }

      // Horizontal positioning
      const viewportWidth = window.innerWidth;
      const menuWidth = menu.offsetWidth;
      const spaceRight = viewportWidth - btnRect.left;

      if (spaceRight < menuWidth) {
        menu.style.left = "auto";
        menu.style.right = "0";
      } else {
        menu.style.left = "0";
        menu.style.right = "auto";
      }

      // Restore visibility
      menu.style.visibility = "";
      menu.style.display = "";
    } else {
      // Reset position when closed
      menu.style.top = "100%";
      menu.style.bottom = "auto";
      menu.style.left = "0";
      menu.style.right = "auto";
    }
  });

  // Item selection
  items.forEach((item) => {
    item.addEventListener("click", () => {
      button.querySelector("span").textContent = item.textContent;

      const hiddenInput = dropdown.querySelector('input[type="hidden"]');
      if (hiddenInput) {
        hiddenInput.value =
          item.getAttribute("data-value") || item.textContent.trim();
        hiddenInput.dispatchEvent(new Event("change", { bubbles: true }));
      }

      dropdown.classList.remove("open");
      icon.className = "ph ph-caret-down";

      menu.style.top = "100%";
      menu.style.bottom = "auto";
      menu.style.left = "0";
      menu.style.right = "auto";
    });
  });
});

// Close all dropdowns on outside click
document.addEventListener("click", () => {
  document.querySelectorAll(".select-dropdown.open").forEach((dropdown) => {
    dropdown.classList.remove("open");

    const icon = dropdown.querySelector(".select-toggle-icon");
    const menu = dropdown.querySelector(".select-dropdown-menu");

    if (icon) icon.className = "ph ph-caret-down";

    if (menu) {
      menu.style.top = "100%";
      menu.style.bottom = "auto";
      menu.style.left = "0";
      menu.style.right = "auto";
    }
  });
});

// capacity bar
window.addEventListener("load", () => {
  document.querySelectorAll(".capacity-fill").forEach((bar) => {
    const value = bar.dataset.capacity;

    // small delay ensures transition runs
    setTimeout(() => {
      bar.style.width = value;
    }, 100);
  });
});

// for analytics page progress
document.addEventListener("DOMContentLoaded", () => {
  const progressElements = document.querySelectorAll("[data-target]");

  progressElements.forEach((el) => {
    const circle = el.querySelector(".progress-circle");
    const text = el.querySelector(".progress-text");
    const target = parseInt(el.dataset.target);
    const duration = 1200;

    let start = null;

    function animate(timestamp) {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const value = Math.floor(progress * target);

      // Animate stroke
      circle.setAttribute("stroke-dasharray", `${value}, 100`);

      // Animate number
      text.textContent = `${value}%`;

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }

    requestAnimationFrame(animate);
  });
});

// for setting page color preset
document.addEventListener("DOMContentLoaded", () => {
  let defaultColor = "#1e2939";

  const btnPrimary = document.getElementById("btnPrimary");
  const btnSecondary = document.getElementById("btnSecondary");
  if (!btnPrimary || !btnSecondary) return;

  // Initialize buttons
  function setButtonColors(color) {
    // Primary button filled
    btnPrimary.style.backgroundColor = color;
    btnPrimary.style.color = "#fff";
    btnPrimary.style.border = "none";

    // Secondary button outlined
    btnSecondary.style.backgroundColor = "transparent";
    btnSecondary.style.color = color;
    btnSecondary.style.borderColor = color;
  }

  // Set default color
  setButtonColors(defaultColor);

  // Handle preset clicks
  const presets = document.querySelectorAll(".color-preset");
  presets.forEach((preset) => {
    preset.addEventListener("click", () => {
      const color = preset.dataset.color;
      setButtonColors(color);
    });
  });
});
