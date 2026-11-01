// ดอยพร้าวฮิลล์ โรสเตอร์ส: สคริปต์หน้าเว็บ (เมนูบนจอเล็ก และฟอร์มติดต่อ)
'use strict';

// 1. เมนูนำทาง: ยุบไว้หลังปุ่มเมื่อจอแคบกว่า 768px
(function setupNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById(toggle ? toggle.getAttribute('aria-controls') : '');
  if (!toggle || !nav) return;

  const label = toggle.querySelector('.nav-toggle-label');
  const desktop = window.matchMedia('(min-width: 768px)');

  function isOpen() {
    return toggle.getAttribute('aria-expanded') === 'true';
  }

  function setOpen(open) {
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    if (label) label.textContent = open ? 'ปิด' : 'เมนู';
  }

  // ปุ่ม <button> จะยิง click ให้เองเมื่อกด Enter หรือ Space
  toggle.addEventListener('click', function () {
    setOpen(!isOpen());
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && isOpen()) {
      setOpen(false);
      toggle.focus();
    }
  });

  // ปิดเมนูเมื่อเลือกลิงก์ หรือคลิกนอกเมนู
  nav.addEventListener('click', function (event) {
    if (event.target.closest('a') && !desktop.matches) setOpen(false);
  });

  document.addEventListener('click', function (event) {
    if (isOpen() && !nav.contains(event.target) && !toggle.contains(event.target)) {
      setOpen(false);
    }
  });

  desktop.addEventListener('change', function (event) {
    if (event.matches) setOpen(false);
  });
})();

// 2. ฟอร์มติดต่อ: ตรวจข้อมูลแล้วเปิดโปรแกรมอีเมลผ่าน mailto
(function setupContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  // ปิด validation ของ browser เพื่อแสดงข้อความภาษาไทยของเราเอง
  form.noValidate = true;

  const EMAIL_TO = 'hello@doiphraohill.example';
  const SUBJECT = 'ติดต่อจากเว็บไซต์';
  const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const status = document.getElementById('cf-status');

  const fields = [
    {
      input: form.elements.namedItem('name'),
      check: function (value) {
        return value ? '' : 'กรุณากรอกชื่อของคุณ';
      }
    },
    {
      input: form.elements.namedItem('email'),
      check: function (value) {
        if (!value) return 'กรุณากรอกอีเมล';
        return EMAIL_PATTERN.test(value) ? '' : 'รูปแบบอีเมลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง';
      }
    },
    {
      input: form.elements.namedItem('message'),
      check: function (value) {
        return value ? '' : 'กรุณากรอกข้อความ';
      }
    }
  ];

  function errorElement(input) {
    return document.getElementById(input.id + '-error');
  }

  function showError(input, message) {
    const error = errorElement(input);
    if (message) {
      error.textContent = message;
      error.hidden = false;
      input.setAttribute('aria-invalid', 'true');
      input.setAttribute('aria-describedby', error.id);
    } else {
      error.textContent = '';
      error.hidden = true;
      input.removeAttribute('aria-invalid');
      input.removeAttribute('aria-describedby');
    }
  }

  function validate(field) {
    const message = field.check(field.input.value.trim());
    showError(field.input, message);
    return message === '';
  }

  // แก้ข้อความ error ทันทีที่ผู้ใช้แก้ช่องที่ผิดอยู่
  fields.forEach(function (field) {
    field.input.addEventListener('input', function () {
      if (field.input.getAttribute('aria-invalid') === 'true') validate(field);
    });
  });

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    let firstInvalid = null;
    fields.forEach(function (field) {
      if (!validate(field) && !firstInvalid) firstInvalid = field.input;
    });

    if (firstInvalid) {
      status.textContent = 'กรุณาตรวจสอบช่องที่มีข้อความแจ้งเตือน';
      firstInvalid.focus();
      return;
    }

    const name = fields[0].input.value.trim();
    const email = fields[1].input.value.trim();
    const message = fields[2].input.value.trim();
    const body = 'ชื่อ: ' + name + '\r\nอีเมล: ' + email + '\r\n\r\n' + message;

    status.textContent = 'กำลังเปิดโปรแกรมอีเมลของคุณ';
    window.location.href =
      'mailto:' + EMAIL_TO +
      '?subject=' + encodeURIComponent(SUBJECT) +
      '&body=' + encodeURIComponent(body);
  });
})();
