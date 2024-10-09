const modal = new bootstrap.Modal(document.getElementById("modal"))
const form_textareas = document.querySelectorAll('.auto-expand');
const logout_popup = document.getElementById("logout-popover")

const post_form_lite_homepage_button = document.getElementById("modal-post-lite-button");
const post_form_lite_homepage = document.getElementById("new-post-form-lite-id");

const nav_home = document.getElementById("home-button-navbar-id");
const nav_explore = document.getElementById("explore-button-navbar-id");
const nav_notifications = document.getElementById("notifications-button-navbar-id");
const nav_bookmarks = document.getElementById("bookmark-button-navbar-id");
const nav_profile = document.getElementById("profile-button-navbar-id");
const nav_settings = document.getElementById("settings-button-navbar-id");

const nav_home_text = document.getElementById("home-button-text-navbar-id");
const nav_explore_text = document.getElementById("explore-button-text-navbar-id");
const nav_notifications_text = document.getElementById("notifications-button-text-navbar-id");
const nav_bookmarks_text = document.getElementById("bookmark-button-text-navbar-id");
const nav_profile_text = document.getElementById("profile-button-text-navbar-id");
const nav_settings_text = document.getElementById("settings-button-text-navbar-id");

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

try {
  post_form_lite_homepage.addEventListener('input', function() {
    if(post_form_lite_homepage.value.trim() === "") {
      post_form_lite_homepage_button.style.opacity="0.5";
    } else {
      post_form_lite_homepage_button.style.opacity="1";
    }
  });
} catch (error) {
  if(error instanceof TypeError) {
    // This is okay, happens when not in home
  } else {
    console.log(error.message);
  }
  
}

function removeActiveClass() {
  if(nav_home_text.classList.contains('active-text')) {
    return nav_home_text.classList.remove('active-text');
  } else if(nav_explore_text.classList.contains('active-text')) {
    return nav_explore_text.classList.remove('active-text');
  } else if(nav_notifications_text.classList.contains('active-text')) {
    return nav_notifications_text.classList.remove('active-text');
  } else if(nav_bookmarks_text.classList.contains('active-text')) {
    return nav_bookmarks_text.classList.remove('active-text');
  } else if(nav_profile_text.classList.contains('active-text')) {
    return nav_profile_text.classList.remove('active-text');
  } else if(nav_settings_text.classList.contains('active-text')) {
    return nav_settings_text.classList.remove('active-text');
  }
}

nav_home.addEventListener("click", () => {
  removeActiveClass();
  url = nav_home.getAttribute('data-url');
  window.location.href=url;
  nav_home_text.classList.add('active-text');
});

nav_explore.addEventListener("click", () => {
  removeActiveClass();
  url = nav_explore.getAttribute('data-url');
  window.location.href=url;
  nav_explore_text.classList.add('active-text');
});

nav_notifications.addEventListener("click", () => {
  removeActiveClass();
  nav_notifications_text.classList.add('active-text');
});

nav_bookmarks.addEventListener("click", () => {
  removeActiveClass();
  nav_bookmarks_text.classList.add('active-text');
});

nav_profile.addEventListener("click", () => {
  removeActiveClass();
  nav_profile_text.classList.add('active-text');
});

nav_settings.addEventListener("click", () => {
  removeActiveClass();
  nav_settings_text.classList.add('active-text');
});

