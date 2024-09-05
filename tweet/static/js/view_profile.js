const edit_profile_modal = new bootstrap.Modal(document.getElementById("edit-profile-modal"));

console.log("I view_profile.js was loaded in and is getting active !")

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #edit-profile => show the modal
  if (e.detail.target.id == "edit-profile") {
    edit_profile_modal.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #comment => hide the modal
  if (e.detail.target.id == "edit-profile" && !e.detail.xhr.response) {
    edit_profile_modal.hide()
    e.detail.shouldSwap = false
  }
})

htmx.on("hidden.bs.modal", () => {
  document.getElementById("edit-profile").innerHTML = ""
})

