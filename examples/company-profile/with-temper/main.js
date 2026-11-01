(function () {
  "use strict";

  /* Mobile navigation */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  var desktop = window.matchMedia("(min-width: 768px)");

  function setOpen(open, returnFocus) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    nav.classList.toggle("is-open", open);
    if (!open && returnFocus) toggle.focus();
  }

  function isOpen() {
    return toggle && toggle.getAttribute("aria-expanded") === "true";
  }

  if (toggle && nav) {
    // A native <button> fires "click" for mouse, touch, Enter and Space.
    toggle.addEventListener("click", function () {
      setOpen(!isOpen(), false);
    });

    document.addEventListener("keydown", function (event) {
      if ((event.key === "Escape" || event.key === "Esc") && isOpen()) {
        event.preventDefault();
        setOpen(false, true);
      }
    });

    // Close after choosing a section.
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a") && isOpen()) setOpen(false, false);
    });

    // Close when clicking outside the header.
    document.addEventListener("click", function (event) {
      if (isOpen() && !event.target.closest(".site-header")) setOpen(false, false);
    });

    var onChange = function () {
      if (desktop.matches) setOpen(false, false);
    };
    if (desktop.addEventListener) desktop.addEventListener("change", onChange);
    else if (desktop.addListener) desktop.addListener(onChange);
  }

  /* Contact form */
  var form = document.getElementById("contact-form");
  if (!form) return;

  var TO = "hello@doiphraohill.example";
  var SUBJECT = "ติดต่อจากเว็บไซต์";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var status = document.getElementById("form-status");

  var rules = {
    name: function (v) {
      return v ? "" : "กรุณากรอกชื่อของคุณหรือชื่อร้าน";
    },
    email: function (v) {
      if (!v) return "กรุณากรอกอีเมล";
      return EMAIL_RE.test(v) ? "" : "รูปแบบอีเมลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง";
    },
    message: function (v) {
      return v ? "" : "กรุณากรอกข้อความที่ต้องการส่งถึงเรา";
    }
  };

  function showError(field, message) {
    var error = document.getElementById(field.id + "-error");
    if (message) {
      error.textContent = message;
      error.hidden = false;
      field.setAttribute("aria-invalid", "true");
      field.setAttribute("aria-describedby", error.id);
    } else {
      error.textContent = "";
      error.hidden = true;
      field.removeAttribute("aria-invalid");
      field.removeAttribute("aria-describedby");
    }
  }

  // Focus the first bad field and make sure its label is not left under the
  // sticky header (focus() alone only scrolls the input itself into view).
  function revealField(field) {
    var wrap = field.closest(".field") || field;
    var header = document.querySelector(".site-header");
    var top = header ? header.getBoundingClientRect().bottom : 0;
    var box = wrap.getBoundingClientRect();
    field.focus({ preventScroll: true });
    if (box.top < top + 8 || box.bottom > window.innerHeight) {
      wrap.scrollIntoView({ block: "start" });
    }
  }

  function validate(field) {
    var message = rules[field.name](field.value.trim());
    showError(field, message);
    return !message;
  }

  Object.keys(rules).forEach(function (name) {
    var field = form.elements[name];
    // Re-check a field once it has been marked invalid, so the message clears as the user fixes it.
    field.addEventListener("input", function () {
      if (field.getAttribute("aria-invalid") === "true") validate(field);
    });
    field.addEventListener("blur", function () {
      if (field.getAttribute("aria-invalid") === "true") validate(field);
    });
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    status.textContent = "";

    var firstInvalid = null;
    Object.keys(rules).forEach(function (name) {
      var field = form.elements[name];
      if (!validate(field) && !firstInvalid) firstInvalid = field;
    });

    if (firstInvalid) {
      revealField(firstInvalid);
      return;
    }

    var name = form.elements.name.value.trim();
    var email = form.elements.email.value.trim();
    var message = form.elements.message.value.trim();
    var body = message + "\n\n" + "ชื่อ: " + name + "\n" + "อีเมลติดต่อกลับ: " + email;
    var href = "mailto:" + TO + "?subject=" + encodeURIComponent(SUBJECT) + "&body=" + encodeURIComponent(body);

    status.textContent = "กำลังเปิดโปรแกรมอีเมลของคุณ หากไม่เปิดขึ้น ";
    var link = document.createElement("a");
    link.href = href;
    link.textContent = "คลิกที่นี่เพื่อส่งอีเมล";
    status.appendChild(link);

    window.location.href = href;
  });
})();
