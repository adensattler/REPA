// Functions for providing street address autocompletion on Property Search page

let autocomplete;
let zipcode = "";

function initAutocomplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("autocomplete"),
    {
      types: ["address"],
      componentRestrictions: { country: ["us"] },
    }
  );
  autocomplete.addListener("place_changed", getzip);
}

function getzip() {
  const place = autocomplete.getPlace();
  for (const component of place.address_components) {
    if (component.types[0] == "postal_code") {
      zipcode = component.long_name;
    }
  }
  let inputF = document.getElementById("autocomplete");
  inputF.value =
    inputF.value.substring(0, inputF.value.length - 5) + " " + zipcode;
}
