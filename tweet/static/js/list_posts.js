const comment_modal = new bootstrap.Modal(document.getElementById("comment-modal"));
const quote_modal = new bootstrap.Modal(document.getElementById("quote-modal"));
const delete_post_modal = new bootstrap.Modal(document.getElementById("delete-post-modal"));
const block_user_modal = new bootstrap.Modal(document.getElementById("block-user-modal"));

const pin_text_links = document.querySelectorAll('.pin-text');
const like_button = document.querySelectorAll('.like-button-icon-base');
const repost_button = document.querySelectorAll('.repost-button-icon-base');
const bookmark_button = document.querySelectorAll('.bookmark-button-icon-base');

console.log("I homepage.js was loaded in and is getting active ! ")

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #comment => show the modal
  if (e.detail.target.id == "comment") {
    comment_modal.show()

    const textareas = document.querySelectorAll('.auto-expand');

    textareas.forEach(textarea => {
      textarea.addEventListener('input', function () {
        this.style.height = 'auto'; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set to scrollHeight
      });
    });

    const comment_form_homepage_button = document.getElementById("modal-comment-reply-button");
    const comment_form_homepage = document.getElementById("new-comment-form-id");

    comment_form_homepage.addEventListener('input', function() {
      if(comment_form_homepage.value.trim() === "") {
        comment_form_homepage_button.style.opacity="0.5";
      } else {
        comment_form_homepage_button.style.opacity="1";
      }
    });
    
  } else if (e.detail.target.id == "quote") {
    quote_modal.show()

    const textareas = document.querySelectorAll('.auto-expand');

    textareas.forEach(textarea => {
      textarea.addEventListener('input', function () {
        this.style.height = 'auto'; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set to scrollHeight
      });
    });

    const quote_form_homepage_button = document.getElementById("modal-quote-reply-button");
    const quote_form_homepage = document.getElementById("new-comment-form-id");

    quote_form_homepage.addEventListener('input', function() {
      if(quote_form_homepage.value.trim() === "") {
        quote_form_homepage_button.style.opacity="0.5";
      } else {
        quote_form_homepage_button.style.opacity="1";
      }
    });
    
  } 
  else if (e.detail.target.id == "block-user") {
    block_user_modal.show();
  } else if (e.detail.target.id == "delete-post") {
    delete_post_modal.show();
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #comment => hide the modal
  if (e.detail.target.id == "comment" && !e.detail.xhr.response) {
    comment_modal.hide();
    e.detail.shouldSwap = false;
  } else if (e.detail.target.id == "quote" && !e.detail.xhr.response) {
    quote_modal.hide();
    e.detail.shouldSwap = false;
  } 
  else if (e.detail.target.id == "block-user" && !e.detail.xhr.response) {
    block_user_modal.hide();
    e.detail.shouldSwap = false;
  } else if (e.detail.target.id == "delete-post" && !e.detail.xhr.response) {
    delete_post_modal.hide();
    e.detail.shouldSwap = false;
  }
})

htmx.on("hidden.bs.modal", () => {
  document.getElementById("comment").innerHTML = ""
  document.getElementById("quote").innerHTML = ""
})    

document.addEventListener('click', function (event) {
  var dropdowns = document.querySelectorAll('.dropdown-menu');
  dropdowns.forEach(function (dropdown) {
    // Check if click is outside the dropdown and its button
    if (!dropdown.contains(event.target) && !dropdown.previousElementSibling.contains(event.target)) {
      dropdown.classList.remove('show');
    } else if (dropdown.contains(event.target)) {
      dropdown.classList.remove('show');
    }
  });
}, true);

pin_text_links.forEach(function (pinText) {
  pinText.addEventListener('click', function () {
    var toastEl = document.getElementById('myToast');
    var toast = new bootstrap.Toast(toastEl);
    toast.show();
  }, true);

}, true);

like_button.forEach(function (button) {
  button.addEventListener('click', function() {
    url = button.getAttribute('data-url');
    icon = document.getElementById('like-button-icon-actual-' + url);
    if (icon.classList.contains('fa-regular')) {
      icon.classList.remove('fa-regular');
      icon.classList.remove('default-icon');

      icon.classList.add('fa-solid');
      icon.classList.add('liked-icon-change');
    } else {
      icon.classList.remove('fa-solid');
      icon.classList.remove('liked-icon-change');

      icon.classList.add('fa-regular');
      icon.classList.add('default-icon');
    }
  });
});

repost_button.forEach(function (button) {
  button.addEventListener('click', function() {
    url = button.getAttribute('data-url');
    icon = document.getElementById('repost-button-icon-actual-' + url);
    if (icon.classList.contains('default-icon')) {
      icon.classList.remove('default-icon');
      icon.classList.add('reposted-icon-change');
    } else {
      icon.classList.remove('reposted-icon-change');
      icon.classList.add('default-icon');
    }
  });
});

bookmark_button.forEach(function (button) {
  button.addEventListener('click', function() {
    url = button.getAttribute('data-url');
    icon = document.getElementById('bookmark-button-icon-actual-' + url);
    if (icon.classList.contains('fa-regular')) {
      icon.classList.remove('fa-regular');
      icon.classList.remove('default-icon');

      icon.classList.add('fa-solid');
      icon.classList.add('bookmarked-icon-change');
    } else {
      icon.classList.remove('fa-solid');
      icon.classList.remove('bookmarked-icon-change');

      icon.classList.add('fa-regular');
      icon.classList.add('default-icon');
    }
  });
});
