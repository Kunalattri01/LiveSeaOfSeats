

  // Password Toggle Logic
  const passwordToggleIcons = document.querySelectorAll(
    ".password-toggle-icon",
  );

  passwordToggleIcons.forEach((icon) => {
    icon.addEventListener("click", () => {
      // Find the input within the same container
      const input = icon.previousElementSibling;
      if (!input) return;

      if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("ph-eye-slash");
        icon.classList.add("ph-eye");
      } else {
        input.type = "password";
        icon.classList.remove("ph-eye");
        icon.classList.add("ph-eye-slash");
      }
    });
  });
