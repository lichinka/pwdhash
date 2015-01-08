/**
 * Forwards the selected entry to the corresponding form target.-
 */
function sendEntry (element)
{
    var domain_field = document.getElementById("domain");
    //
    // the 'id' of the field should contain the domain name
    //
    domain_field.value = element.id;
    //
    // send the form
    //
    document.getElementById("entries_form").submit ( );
    return false;
}
