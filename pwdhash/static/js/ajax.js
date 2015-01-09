/**
 * Deletes the selected entry from the vault.-
 */
function deleteKey ( )
{
    var delete_field = document.getElementById("delete");
    //
    // we use the delete field to know which entry should be deleted
    //
    delete_field.value = document.getElementById("name").value;
    //
    // send the form
    //
    document.getElementById("hash_form").submit ( );
    return false;
}


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


/**
 * Displays a modal dialog with a semi-transparent overlay.-
 */
function displayDialog ( )
{
    var modal= document.getElementById('modal');
    var shade= document.getElementById('shade');
    
    //
    // if these elements do not exist, there is nothing to display
    //
    if (modal != null && shade != null)
    {
        modal.style.display = 'block';
        shade.style.display = 'block';
        document.getElementById('close_dialog').onclick= function() {
            modal.style.display=shade.style.display= 'none';
        };
    }
}
 
window.onload = displayDialog;
