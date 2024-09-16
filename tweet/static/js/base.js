const modal = new bootstrap.Modal(document.getElementById("modal"))
const form_textareas = document.querySelectorAll('.auto-expand');
const logout_popup = document.getElementById("logout-popover")

const post_form_lite_homepage_button = document.getElementById("modal-post-lite-button");
const post_form_lite_homepage = document.getElementById("new-post-form-lite-id");

console.log("I navbar.js was loaded in and is getting active ! ");

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show();

    const textareas = document.querySelectorAll('.auto-expand');

    textareas.forEach(textarea => {
      textarea.addEventListener('input', function () {
        this.style.height = 'auto'; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set to scrollHeight
      });
    });

    const post_form_homepage = document.getElementById("new-post-form-id");
    const post_form_homepage_button = document.getElementById("modal-post-button");

    post_form_homepage.addEventListener('input', function() {
      if(post_form_homepage.value.trim() === "") {
        post_form_homepage_button.style.opacity="0.5";
      } else {
        post_form_homepage_button.style.opacity="1";
      }
    });
  }
});

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
    modal.hide();
    e.detail.shouldSwap = false;
  }
});

htmx.on("hidden.bs.modal", () => {
  document.getElementById("dialog").innerHTML = "";
});

form_textareas.forEach(textarea => {
  textarea.addEventListener('input', function () {
        this.style.height = 'auto'; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set to scrollHeight
      }, true);
}, true);

post_form_lite_homepage.addEventListener('input', function() {
  if(post_form_lite_homepage.value.trim() === "") {
    post_form_lite_homepage_button.style.opacity="0.5";
    console.log("No input")
  } else {
    post_form_lite_homepage_button.style.opacity="1";
    console.log("Input")
  }
});

var popover = new bootstrap.Popover(logout_popup, {
  container: 'body'
});

