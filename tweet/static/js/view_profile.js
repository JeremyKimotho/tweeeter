const edit_profile_modal = new bootstrap.Modal(document.getElementById("edit-profile-modal"));
console.log("I view_profile.js was loaded in and is getting active !");

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #edit-profile => show the modal
  if (e.detail.target.id == "edit-profile") {
    edit_profile_modal.show();

    let name_label = document.getElementById("name-label");
    let location_label = document.getElementById("location-label");

    let name_input = document.getElementById("p-change-form-name");
    let location_input = document.getElementById("p-change-form-location");

    let edit_birthday_button = document.getElementById("confirm-edit-birthday-button")
    let birthday_info_div = document.getElementById("birthday-field")
    let edit_birthday_info_div = document.getElementById("edit-birthday")

    name_input.addEventListener('input', function () {
      if(name_input.value.trim() === "") {
        name_label.style.display='none';
      } else {
        name_label.style.display='block';
      }
    });

    location_input.addEventListener('input', function () {
      if(location_input.value.trim() === "") {
        location_label.style.display='none';
      } else {
        location_label.style.display='block';
      }
    });

    edit_birthday_button.addEventListener('click', function () {
      birthday_info_div.style.display='none';
      edit_birthday_info_div.style.display='block';
    });
  }
});

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #comment => hide the modal
  if (e.detail.target.id == "edit-profile" && !e.detail.xhr.response) {
    edit_profile_modal.hide();
    e.detail.shouldSwap = false;
  }
});

htmx.on("hidden.bs.modal", () => {
  document.getElementById("edit-profile").innerHTML = "";
});

