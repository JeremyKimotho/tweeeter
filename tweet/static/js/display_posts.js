const comment_form_lite_homepage_button = document.getElementById("modal-comment-lite-reply-button");
const comment_form_lite_homepage = document.getElementById("new-comment-form-lite-id");

comment_form_lite_homepage.addEventListener('input', function() {
  if(comment_form_lite_homepage.value.trim() === "") {
    comment_form_lite_homepage_button.style.opacity="0.5";
  } else {
    comment_form_lite_homepage_button.style.opacity="1";
  }
});