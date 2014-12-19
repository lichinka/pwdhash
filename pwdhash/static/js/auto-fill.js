/**
 * Fills the input fields with the received information after clicking
 * on one of the site-specific icons.-
 */
function autoFill (element)
{
    var input_field = document.getElementById("domain");
    //
    // the 'id' of the field should contain the domain name
    //
    input_field.value = "http://www." + element.id;
    //
    // send the form
    //
    document.getElementById("hashform").submit ( );
}
