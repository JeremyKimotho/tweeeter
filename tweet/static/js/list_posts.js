const comment_modal = new bootstrap.Modal(document.getElementById("comment-modal"));
const quote_modal = new bootstrap.Modal(document.getElementById("quote-modal"));
const comment_reply_text_info = document.getElementById("comment-modal-reply-info-div")
const post_form_homepage = document.getElementById("new-post-form-textarea")

console.log("I homepage.js was loaded in and is getting active ! ")

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #comment => show the modal
  if (e.detail.target.id == "comment") {
    comment_reply_text_info.style.display = "none"; // show the text relating to post info when commenting
    comment_modal.show()

    const textareas = document.querySelectorAll('.auto-expand');

    console.log("Loading in listeners " + textareas.length)

    textareas.forEach(textarea => {
      textarea.addEventListener('input', function () {
        this.style.height = 'auto'; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set to scrollHeight
      });
    });
    
  } else if (e.detail.target.id == "quote") {
    quote_modal.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #comment => hide the modal
  if (e.detail.target.id == "comment" && !e.detail.xhr.response) {
    comment_reply_text_info.style.display = "block"; // show the text relating to post info when commenting
    comment_modal.hide()
    e.detail.shouldSwap = false
  } else if (e.detail.target.id == "quote" && !e.detail.xhr.response) {
    quote_modal.hide()
    e.detail.shouldSwap = false
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
  console.log("Something happened");
})

document.body.addEventListener('htmx:afterRequest', function(event) {
    // Check if the form that triggered the request is the one we want to clear
    if (event.target.id === "new-post-form-textarea") {
      // Reset the form after submission
      post_form_homepage.reset();
    }
  });


let like_toggle = true;
let bookmark_toggle = true;
let repost_toggle = false;
var isDropdownVisible = false;

$('#comment_button').click(function() {
    var commentUrl = $(this).data('url');
    var postID = $(this).data('id');
    $.ajax({
        url: commentUrl,
        method: 'GET',
        success: function(response) {
            $('#post-comments-{{ postID }}').text(response.content);
        },
        error: function(xhr, status, error) {
            console.log("An error occurred: " + error);
        }
    });
});

$('#repost_button').click(function() {
    if (repost_toggle) {
        var repostUrl = $(this).data('t-url');
        var repostText = "Unrepost";
    } else {
        var repostUrl = $(this).data('f-url');
        var repostText = "Repost";
    }
    repost_toggle = !repost_toggle;  // Switch the toggle flag

    $.ajax({
        url: repostUrl,
        method: 'GET',
        success: function(response) {
            $("#post-repost-dd").text(repostText)
            $('#post-reposts').text(response.total);
        },
        error: function(xhr, status, error) {
            console.log("An error occurred: " + error);
        }
    });

    hideDropdown();
    isDropdownVisible = false;
}); 


