const comment_modal = new bootstrap.Modal(document.getElementById("comment-modal"));
const quote_modal = new bootstrap.Modal(document.getElementById("quote-modal"));
const post_form_homepage = document.getElementById("new-post-form-textarea");
const delete_post_modal = new bootstrap.Modal(document.getElementById("delete-post-modal"));
const block_user_modal = new bootstrap.Modal(document.getElementById("block-user-modal"))

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
    
  } else if (e.detail.target.id == "quote") {
    quote_modal.show()
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

htmx.on("htmx:afterRequest", (e) => {
  if (e.target.id == "new-post-form-textarea") {
    post_form_homepage.reset()
  }
})

document.body.addEventListener('htmx:afterRequest', function(event) {
    // Check if the form that triggered the request is the one we want to clear
    if (event.target.id === "new-post-form-textarea") {
      // Reset the form after submission
      post_form_homepage.reset();
    }
  }, true);       

document.addEventListener('click', function (event) {
  var dropdowns = document.querySelectorAll('.dropdown-menu');
  dropdowns.forEach(function (dropdown) {
    // Check if click is outside the dropdown and its button
    if (!dropdown.contains(event.target) && !dropdown.previousElementSibling.contains(event.target)) {
      dropdown.classList.remove('show');
    }
  });
}, true);



