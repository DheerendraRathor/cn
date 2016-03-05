
var citation_value;

var rejection_reason_value;


$("#id_verification_status").on('change', function(){
    var val = this.value;
    var $citation_form_div = $("#citation_form_div");
    var $rejection_reason_form_div = $("#rejection_reason_form_div");

    $citation_form_div.addClass('hide');
    $rejection_reason_form_div.addClass('hide');

    if (val == citation_value){
        $citation_form_div.removeClass('hide');
    }

    if (val == rejection_reason_value){
        $rejection_reason_form_div.removeClass('hide');
    }
});