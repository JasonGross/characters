
function setUpForm( form_name, button_name ) {
  if (isTurk())
    turkSetAssignmentID(form_name, button_name);
  else {
    if (form_name == null) {
      form_name = 'mturk_form';
    }
      
    form = document.getElementById(form_name); 
    if (form) {
       form.action = unescape(getURLParameter('submitTo')); 
    }
  }
}